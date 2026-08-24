# Public Support Engineering Instructions

## Source of truth and boundaries

The private `wittenauer-software/pbi-process-mining` repository is the source of
truth for Threadseer behavior, supported roles and limits, privacy architecture,
edition policy, exact package/report version, Marketplace state, and release
evidence. Verify those facts against its current reviewed commit before changing
this public repository. Do not infer approval, availability, pricing, licensing,
or certification state from public copy alone.

Keep this repository free of product source, private release evidence, customer
names, PBIX/PBIP files, event logs, tenant information, credentials, proprietary
field names, and other confidential or operational data. Public issue guidance
must continue to request synthetic reproductions and prohibit sensitive uploads.

## Version and documentation reconciliation

Treat every product-version or candidate update as a repository-wide public
documentation change. Before handoff, inventory every current- and prior-version
reference and reconcile all applicable living surfaces:

- `docs/release-status.json` version, state, and review date;
- Getting Started, Known Issues, Release Status, Support, licensing, privacy,
  terms, accessibility, and homepage copy affected by the release;
- `.github/ISSUE_TEMPLATE/bug_report.yml` version guidance;
- customer-facing behavior, limits, environment validation, and recovery steps;
- navigation, relative links, sitemap entries, and the Pages deployment path;
- Marketplace submission, approval, purchase, availability, and certification
  claims; and
- the exact public-support commit recorded by the private product repository.

Review every version hit in context. Update living status pages, but do not
rewrite historical records to imply that an older gate or release passed.

For every version reconciliation, run all of the following against the same
support worktree:

```powershell
python tools/validate_docs.py
$env:THREADSEER_SUPPORT_REPO='<absolute path to this support worktree>'
npm --prefix '<absolute path to pbi-process-mining>' run docs:verify
npm --prefix '<absolute path to pbi-process-mining>' run docs:verify:release
```

Render and inspect the changed pages locally at the same `/threadseer-support/`
base path used by GitHub Pages. After merge, verify the live company Pages site,
its release-status JSON, changed pages, navigation, and public repository commit.
Preserve the separate personal pilot Pages site unless the owner explicitly
authorizes changing or removing it.

Any stale, failed, skipped, unavailable, or cross-repository check remains an
explicit release blocker. Report successful, failed, skipped, and not-run checks
separately, and never describe Threadseer as submitted, approved, available,
purchasable, or certified without current external evidence.
