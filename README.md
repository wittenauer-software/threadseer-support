# Threadseer support

This company-owned public repository hosts the support hub, legal notices, and issue tracker for **Threadseer for Power BI**, published and owned by **Wittenauer Software LLC**.

- [Threadseer product and documentation home](https://wittenauer-software.github.io/threadseer-support/)
- [Getting started](https://wittenauer-software.github.io/threadseer-support/getting-started/)
- [Plans and pricing](https://wittenauer-software.github.io/threadseer-support/licensing/)
- [Release status](https://wittenauer-software.github.io/threadseer-support/release-notes/)
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

Threadseer's initial Microsoft Marketplace launch is planned for the United
States under the Microsoft Standard Contract. Community is free. Professional
launch pricing is US$20 per assigned user per month or US$200 per assigned user
per year. There is no time-limited Professional trial at launch; Community is
the permanent free evaluation path. Marketplace approval and checkout are not
yet verified, and optional Power BI certification is deferred until after
launch.

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

The same validator runs in GitHub Actions. Public release notes must name every
released Marketplace version; pre-release pages must not claim approval,
availability, purchase, or certification before those states are verified.
