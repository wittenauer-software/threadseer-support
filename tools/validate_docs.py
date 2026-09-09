#!/usr/bin/env python3
"""Validate the static Threadseer support site without third-party packages."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BASE_URL = "https://wittenauer-software.github.io/threadseer-support"
PUBLIC_CONTACT_EMAIL = "jasonwittenauer@wittenauersoftware.com"
REQUIRED_PAGES = (
    "",
    "getting-started",
    "licensing",
    "support",
    "known-issues",
    "release-notes",
    "privacy",
    "terms",
    "accessibility",
)
REQUIRED_VIEWS = (
    "Process Map",
    "Variants",
    "Compare",
    "Conformance",
    "Drivers",
    "Bottlenecks",
    "Rework",
    "Improve",
    "Cases",
    "Data Quality",
)
failures: list[str] = []
release_status = json.loads((DOCS / "release-status.json").read_text(encoding="utf-8"))
current_version = release_status.get("version")
last_reviewed = release_status.get("lastReviewed")
try:
    reviewed_date = date.fromisoformat(last_reviewed)
    reviewed_label = f"{reviewed_date.strftime('%B')} {reviewed_date.day}, {reviewed_date.year}"
except (TypeError, ValueError):
    reviewed_label = None


def require(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def page_path(slug: str) -> Path:
    return DOCS / "index.html" if not slug else DOCS / slug / "index.html"


html_files = sorted(DOCS.rglob("*.html"))
for slug in REQUIRED_PAGES:
    require(page_path(slug).is_file(), f"Missing required page: {slug or '/'}")

for slug in REQUIRED_PAGES:
    content = page_path(slug).read_text(encoding="utf-8")
    for navigation_label in ("Pricing", "Get help", "Release notes"):
        require(
            navigation_label in content,
            f"{slug or '/'} is missing the customer navigation label: {navigation_label}",
        )

for html_file in html_files:
    content = html_file.read_text(encoding="utf-8")
    relative = html_file.relative_to(ROOT)
    require('<html lang="en">' in content, f"{relative} must declare lang=en")
    require('name="viewport"' in content, f"{relative} is missing viewport metadata")
    require('name="description"' in content, f"{relative} is missing a meta description")
    require("<title>" in content, f"{relative} is missing a title")
    require("<h1" in content, f"{relative} is missing an h1")
    require('class="skip-link"' in content, f"{relative} is missing a skip link")
    require('class="site-footer"' in content, f"{relative} is missing the site footer")

    for href in re.findall(r'href="([^"]+)"', content):
        parsed = urlsplit(href)
        if parsed.scheme:
            if parsed.scheme == "mailto":
                require(
                    href == f"mailto:{PUBLIC_CONTACT_EMAIL}",
                    f"{relative} contains an unapproved email link: {href}",
                )
                continue
            require(parsed.scheme == "https", f"{relative} contains a non-HTTPS link: {href}")
            continue
        if href.startswith("#"):
            continue
        clean = parsed.path
        if not clean:
            continue
        if clean.startswith("/threadseer-support/"):
            clean = clean.removeprefix("/threadseer-support/")
            candidate = DOCS / clean
        else:
            candidate = (html_file.parent / clean).resolve()
        if href.endswith("/") or clean.endswith("/"):
            candidate = candidate / "index.html"
        require(candidate.exists(), f"{relative} contains a broken local link: {href}")

sitemap_path = DOCS / "sitemap.xml"
try:
    sitemap = ElementTree.parse(sitemap_path)
    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locations = {node.text for node in sitemap.findall("s:url/s:loc", namespace)}
except (ElementTree.ParseError, OSError) as exc:
    failures.append(f"Invalid sitemap.xml: {exc}")
    locations = set()

expected_locations = {
    f"{BASE_URL}/" if not slug else f"{BASE_URL}/{slug}/"
    for slug in REQUIRED_PAGES
}
require(locations == expected_locations, "sitemap.xml must contain exactly the required public pages")

getting_started = page_path("getting-started").read_text(encoding="utf-8")
require(
    'id="automatic-restoration"' in getting_started
    and "unchanged" in getting_started
    and "current license" in getting_started,
    "Getting Started must explain automatic restoration of unchanged, previously authorized analysis within current license limits",
)
require(
    isinstance(current_version, str) and re.fullmatch(r"\d+\.\d+\.\d+\.\d+", current_version) is not None,
    "release-status.json must identify a four-part numeric version",
)
require(
    release_status.get("documentationScope") == "product-guide" and "status" not in release_status,
    "release-status.json must describe product documentation without asserting Marketplace state",
)
require(reviewed_label is not None, "release-status.json must identify a valid lastReviewed date")
for view in REQUIRED_VIEWS:
    require(view in getting_started, f"Getting Started is missing the {view} view")
require("Event / Row ID" in getting_started, "Getting Started is missing Event / Row ID guidance")
require(
    "source report" in getting_started and "dashboard tiles" in getting_started,
    "Getting Started is missing the incomplete-dashboard guidance",
)
require(
    "Get more visuals" in getting_started and "AppSource" in getting_started,
    "Getting Started must explain how to add the visual in Power BI",
)

release_notes = page_path("release-notes").read_text(encoding="utf-8")
for view in REQUIRED_VIEWS:
    require(view in release_notes, f"Release Notes is missing the {view} view")
require("Release notes</h1>" in release_notes, "Release Notes must provide version notes")
require("Public release date" not in release_notes, "Do not invent a Marketplace release date")
require(
    "US$20 per assigned user per month" not in release_notes
    and "US$200 per assigned user per year" not in release_notes,
    "Release Notes must link to Pricing instead of duplicating plan prices",
)

licensing = page_path("licensing").read_text(encoding="utf-8")
for required_term in (
    "Community is free for personal, educational, evaluation, and internal commercial use",
    "same proprietary Threadseer visual",
    "Microsoft Standard Contract",
    "US$20 per assigned user per month",
    "US$200 per assigned user per year",
    "no time-limited Professional trial",
    "United States",
):
    require(required_term in licensing, f"Licensing is missing approved term: {required_term}")

require(
    "Where can I purchase Professional?" in licensing
    and licensing.count("United States") == 1
    and "allow up to an hour" in licensing,
    "Pricing must explain purchasing scope and license activation without repeated launch notices",
)

known_issues = page_path("known-issues").read_text(encoding="utf-8")
require(
    "Supported Power BI environments" in known_issues,
    "Known Issues must state the supported-environment boundary",
)
require(
    "first 10,000 events" in known_issues
    and "loading indefinitely" in known_issues
    and "Power BI Service" in known_issues,
    "Known Issues is missing the current dashboard and Service boundary",
)
require(
    "loading indefinitely" in release_notes
    and "all ten analytical views" in release_notes,
    "Release Notes is missing the current dashboard-loading fix and validation scope",
)
for name, content in (
    ("Getting Started", getting_started),
    ("Known Issues", known_issues),
    ("Release Notes", release_notes),
):
    require(
        f"Threadseer {current_version}" in content,
        f"{name} must identify release-status.json version {current_version}",
    )
    require(
        reviewed_label is not None and reviewed_label in content,
        f"{name} must identify release-status.json review date {reviewed_label}",
    )

support = page_path("support").read_text(encoding="utf-8")
require(
    "GitHub account" in support and "sign in" in support,
    "Support must disclose the GitHub account and sign-in requirement",
)

privacy = page_path("privacy").read_text(encoding="utf-8")
require(
    'id="support-email"' in privacy
    and "email address" in privacy
    and "attachments" in privacy
    and "stored through the email services" in privacy,
    "Privacy must explain what support email receives and stores separately from Power BI report data",
)
terms = page_path("terms").read_text(encoding="utf-8")
accessibility = page_path("accessibility").read_text(encoding="utf-8")
for name, content in (
    ("Support", support),
    ("Privacy", privacy),
    ("Terms", terms),
    ("Accessibility", accessibility),
):
    require("Wittenauer Software LLC" in content, f"{name} must identify the publisher")
    require(
        f'mailto:{PUBLIC_CONTACT_EMAIL}' in content,
        f"{name} must publish the approved private-contact mailbox",
    )
require(
    "Microsoft Standard Contract for Microsoft Marketplace" in terms,
    "Terms must identify the selected Microsoft Standard Contract",
)

bug_form = (ROOT / ".github" / "ISSUE_TEMPLATE" / "bug_report.yml").read_text(encoding="utf-8")
require("About information" not in bug_form, "Bug form must not claim an in-visual About page exists")
require("PBIVIZ filename" in bug_form, "Bug form must explain how to identify the version")
require(
    isinstance(current_version, str) and current_version in bug_form,
    "Bug form version example must match release-status.json",
)
require(
    "this issue and any attachments" in bug_form,
    "Bug form privacy confirmation must describe the public issue rather than a report",
)

all_public_text = "\n".join(path.read_text(encoding="utf-8") for path in html_files)
public_copy_paths = [
    *html_files,
    *(ROOT / name for name in ("README.md", "SUPPORT.md", "SECURITY.md", "CONTRIBUTING.md")),
    *sorted((ROOT / ".github" / "ISSUE_TEMPLATE").glob("*.yml")),
]
public_copy = "\n".join(path.read_text(encoding="utf-8") for path in public_copy_paths)
for path in public_copy_paths:
    require(
        re.search(
            r"https://(?:github\.com/jasonwi1202|jasonwi1202\.github\.io)/threadseer-support(?=[/#?\s]|$)",
            path.read_text(encoding="utf-8"),
            re.IGNORECASE,
        ) is None,
        f"{path.relative_to(ROOT)} links to the personal support repository instead of the company repository",
    )

issue_picker = (ROOT / ".github" / "ISSUE_TEMPLATE" / "config.yml").read_text(encoding="utf-8")
contact_urls = re.findall(r"^\s*url:\s*(https://\S+)\s*$", issue_picker, re.MULTILINE)
require(
    len(contact_urls) == 2 and set(contact_urls) == {
        f"{BASE_URL}/support/",
        "https://github.com/wittenauer-software/threadseer-support/security/advisories/new",
    },
    "Issue picker must link to the company support guide and private security reporting",
)
require("blank_issues_enabled: false" in issue_picker, "Issue picker must keep blank public issues disabled")

for obsolete in (
    "undergoing final validation",
    "Marketplace availability is not yet confirmed",
    "Current Threadseer 0.1.x validation builds",
    "verified private",
    "before public sale",
    "pre-submission",
    "pre-release",
    "has not been submitted",
    "No Marketplace submission has been made",
    "Not submitted",
    "coming soon",
    "pending",
    "Professional (planned)",
    "after the offer becomes available",
    "When a live offer is verified",
    "What remains before a public release",
    "Current validation focus",
    "after public release",
    "Before Marketplace availability",
    "intended for distribution",
    "pilot invitation",
    "Private Professional Preview evaluators",
    "Before public Marketplace release",
    "After launch",
    "Threadseer analyzes only when",
    "does not receive or retain the underlying Microsoft plan identifier",
):
    require(re.search(r"\b" + re.escape(obsolete) + r"(?=\W|$)", public_copy, re.IGNORECASE) is None, f"Public content contains obsolete status copy: {obsolete}")

support_markdown = (ROOT / "SUPPORT.md").read_text(encoding="utf-8")
require(PUBLIC_CONTACT_EMAIL in support_markdown, "SUPPORT.md must publish the approved private-contact mailbox")
require("before public sale" not in support_markdown, "SUPPORT.md contains the obsolete pre-sale contact promise")

for internal_term in (
    "publisher-controlled services",
    "explicit analysis scale",
    "admitted capacity",
    "service-plan state",
    "transactability",
    "incomplete loaded prefix",
    "contributing-case cohort",
    "Power BI property replays",
    "serialized and coalesced",
):
    require(
        internal_term not in all_public_text,
        f"Public pages contain implementation-first language: {internal_term}",
    )

homepage = page_path("").read_text(encoding="utf-8")
for customer_message in (
    "See how work really flows",
    "Your data stays in Power BI",
    "common paths, delays, rework, and individual cases",
):
    require(customer_message in homepage, f"Homepage is missing customer message: {customer_message}")

require((ROOT / "CONTRIBUTING.md").is_file(), "CONTRIBUTING.md is missing")
require((ROOT / "SECURITY.md").is_file(), "SECURITY.md is missing")
require((ROOT / ".github" / "CODEOWNERS").is_file(), "CODEOWNERS is missing")

if "--require-github" in sys.argv:
    try:
        result = subprocess.run(
            ["gh", "label", "list", "--repo", "wittenauer-software/threadseer-support", "--limit", "1000", "--json", "name"],
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )
        labels = json.loads(result.stdout)
        require(
            any(label.get("name") == "known issue" for label in labels),
            "GitHub must contain the known issue label used by the public Known Issues filter",
        )
    except (OSError, subprocess.SubprocessError, ValueError, TypeError, AttributeError) as exc:
        failures.append(f"Could not verify live GitHub labels: {type(exc).__name__}")

agent_instructions_path = ROOT / "AGENTS.md"
require(agent_instructions_path.is_file(), "AGENTS.md is missing")
if agent_instructions_path.is_file():
    agent_instructions = agent_instructions_path.read_text(encoding="utf-8")
    for required_instruction in (
        "docs/release-status.json",
        "threadseer-support/",
        "python tools/validate_docs.py",
        "docs:verify:release",
        "live company Pages site",
        "successful, failed, skipped, and not-run checks",
    ):
        require(
            required_instruction in agent_instructions,
            f"AGENTS.md is missing the release instruction: {required_instruction}",
        )

if failures:
    print("Documentation validation failed:", file=sys.stderr)
    for failure in failures:
        print(f"- {failure}", file=sys.stderr)
    raise SystemExit(1)

print(f"Documentation validation passed for {len(html_files)} HTML files and {len(locations)} sitemap entries.")
print("Live GitHub label check passed." if "--require-github" in sys.argv else "Live GitHub label check not run (use --require-github).")
