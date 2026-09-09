# Threadseer support

This company-owned public repository hosts the support hub, legal notices, and issue tracker for **Threadseer for Power BI**, published and owned by **Wittenauer Software LLC**.

- [Threadseer product and documentation home](https://wittenauer-software.github.io/threadseer-support/)
- [Getting started](https://wittenauer-software.github.io/threadseer-support/getting-started/)
- [Plans and pricing](https://wittenauer-software.github.io/threadseer-support/licensing/)
- [Release notes](https://wittenauer-software.github.io/threadseer-support/release-notes/)
- [Known issues and limits](https://wittenauer-software.github.io/threadseer-support/known-issues/)
- [Get help](https://wittenauer-software.github.io/threadseer-support/support/)
- [Open a bug report](https://github.com/wittenauer-software/threadseer-support/issues/new?template=bug_report.yml)
- [Request a feature](https://github.com/wittenauer-software/threadseer-support/issues/new?template=feature_request.yml)
- [Report a security vulnerability privately](https://github.com/wittenauer-software/threadseer-support/security/advisories/new)
- [Privacy notice](https://wittenauer-software.github.io/threadseer-support/privacy/)
- [Terms of use](https://wittenauer-software.github.io/threadseer-support/terms/)
- [Accessibility](https://wittenauer-software.github.io/threadseer-support/accessibility/)

Threadseer is distributed as a self-contained Power BI custom visual. Its product source code is maintained privately; this repository intentionally contains only public support and website content.

Before posting, remove employer data, event logs, report files, screenshots with case identifiers, tenant details, proprietary field names, credentials, and secrets. Use a synthetic reproduction whenever possible.

Support is provided on a reasonable-efforts basis. No response-time commitment is offered unless a separate written agreement says otherwise.

Community is free. Professional is US$20 per assigned user per month or
US$200 per assigned user per year. Microsoft manages Professional purchasing and
license assignment under the Microsoft Standard Contract. Community is the
permanent free evaluation path; there is no time-limited Professional trial.
See the pricing page for purchasing regions and environment limitations.

## Maintaining this repository

The private product repository is the source of truth for implementation,
supported roles, limits, privacy architecture, edition policy, exact candidate
identity, and Marketplace state. Update this public repository whenever those
customer-facing facts change. Product source and private release evidence do not
belong here.

Validate changes locally with:

```powershell
python tools/validate_docs.py
```

The same validator runs in GitHub Actions. Public pages are durable product
documentation, not a submission-status dashboard. `docs/release-status.json`
retains its existing URL for compatibility and identifies the documented
version, documentation scope, and review date; it does not assert Marketplace
approval or publication. Keep setup, pricing, limitations, and version notes
complete without launch countdowns or private validation checklists. Record
Marketplace review evidence in the private product repository. Add direct
listing links only when their exact destinations are verified. Do not invent
release dates, approval, certification, or successful host-test results.
