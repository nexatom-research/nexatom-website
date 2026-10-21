# Website development entry point

## Start-up and configuration boundary

Read the complete `AGENTS.md` and [SHARED-DEVELOPMENT.md](../SHARED-DEVELOPMENT.md),
then the project-specific authorities linked below. Check the current branch,
HEAD and working-tree state before taking an owned task branch/worktree.
Use `workstation` or `laptop-2023` for machine/task attribution, not separate
source histories. Integrate reviewed changes through merge-commit PRs; preserve
old commits and branches.

This is shared documentation, not permission to install tools, run a build,
launch an app, access hardware, synchronize another checkout or publish.
Existing project pauses and approval requirements still apply. A dated result
applies only to its named source and inputs; it is not a pass for later commits.

Keep actual credentials, local `.env`/operator settings, license files, SSH keys,
SDKs, virtual environments, caches and generated build metadata outside Git.
Use the repository's existing sanitized configuration examples where present.
Record required variable names and purpose, never actual secret values.
Local SDK paths are machine mappings, not application source dependencies.

## Repository and local setup

This is the static website only. Read [AGENTS.md](../AGENTS.md) in full for
current content, DNS, form and hosting decisions. The application/native API
and `nexatom-downloads` repositories are separate ownership boundaries.
Do not move updater manifests or installer artifacts into this repository.

Use a local Python 3 interpreter with the existing
[static checker](../tools/verify_site.py). It is not a web server or deployment
step. When a check is in scope, the repository-root command is:

```powershell
python tools/verify_site.py
```

Select the intended installed interpreter explicitly if PATH differs between
machines. Keep temporary output outside tracked website content. No private
developer credentials or production environment file needs to be committed to
make the static source understandable.

## Validation record, 2026-09-07

Source: `a3b118c0c461aa5deb14b9424b7610b8dde21a5a`, target `main`.
The existing exact-source static-check **PASS** from the earlier migration
validation is retained; it was not rerun during the later parity goal or this
documentation task.

This is not a browser rendering, form delivery, DNS, GitHub Pages publication,
download/update or production acceptance result. Those actions remain separate
from local static checks and require their own scope and evidence.
