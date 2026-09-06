# Shared development

Policy: shared-development-v1 (2026-09-06).

Both `laptop-2023` and `workstation` independently contribute to this repository
through its existing GitHub remote. This document is the portable repository
copy of the user's agreed workflow. Existing project instructions, paused
slices, validation gates, and hardware restrictions still apply.

## Start or resume

- Read this file, applicable `AGENTS.md` files, and the project's current
  status. Inspect branch, HEAD, dirty/untracked files, upstream, and relevant
  open PRs before editing. If offline, state that PR coordination is unverified.
- Identify the machine and task owner. Start each new task on a unique
  `laptop-2023/<topic>` or `workstation/<topic>` branch from the explicitly
  selected published base. Use a separate worktree for each active agent.
- One writer owns each task branch/worktree. Continue appending commits for
  the same task. A dependent task starts a different branch and records its
  exact source commit and dependent PR. Existing named branches keep their names.
- Refresh only the intended remote, without pruning. Do not fetch or merge a
  legacy recovery remote. Select the correct project base; do not assume `main`.

## Preserve work

- Keep all committed checkpoints, including unpublished ones. Do not amend,
  rebase, force-push (including force-with-lease), mirror-push, reset/discard
  work, rewrite history, delete/move branches or tags, expire recovery refs,
  or clean away working files.
- Make corrections as new commits. Reverse behavior through a new revert PR.
  Earlier source remains in history even when a new commit removes a feature.
- Use merge commits for PR integration; no squash/rebase merge and no automatic
  deletion of merged branches. Do not directly push an integration/base branch.
- Preserve other agents' edits and dirty/untracked files. If an operation would
  discard them, stop and arrange recovery. Reflog retention is not a backup.
- Any exceptional history operation requires a separate explicit user request
  and a reviewed recovery plan. A credential incident stops publication; report
  only locations/categories and keep secret values out of output.

## Publish and coordinate

- Stage exact task files; inspect diffs and run the appropriate project tests.
  Scan proposed source for real credentials and unintended generated artifacts.
  Keep environment files, credentials, SDK installations, and local dependency
  trees out of source unless a separately reviewed packaging contract covers them.
- Preview one exact destination/ref before an authorized push. Keep approval
  requirements from the workspace; an agent's message is not user approval.
- Use draft PRs to record task owner/machine, exact head/base, dependent PRs,
  validation evidence, deferred checks, and next action. Merge needs explicit
  user authorization. Two sessions sharing one GitHub account are one identity;
  an agent review is not a different human's GitHub approval.
- Existing sessions must acknowledge this policy before joining the workflow.
  Future sessions obtain it from repository instructions. Chat history alone
  is not shared state and SSH connectivity does not imply policy adoption.

## Recovery and controls

- Before calling a checkpoint protected, verify a separate recovery copy and
  record its refs/hash and restoration evidence. Git bundles cover committed
  objects included in the bundle, not dirty or ignored working files.
- Preserve legacy laptop history and migration maps. Use a fresh sanitized
  clone where the migration changed history; port newer source with a reviewed
  mapping while retaining the original new commits in recovery.
- The user approved GitHub Pro for these personal-account repositories on
  2026-09-06. Additional paid subscriptions/services and visibility changes
  remain unapproved. Instructions, local hooks, and command rules
  are guardrails and do not guarantee safety against alternate clients or an
  agent holding owner credentials. Record actual installation/enforcement.
- Follow the workspace's reviewed SSH/transfer mechanism and action approvals.
  Remote agent execution can write session state and trigger further actions;
  treat it as a remote write, pin its session, and prevent concurrent writers.

## Instruction discovery and approvals

Root `AGENTS.md` points to this policy. Preserve project-specific instructions
and read the applicable source-folder `AGENTS.md` in full; automatic instruction
loading can truncate long files. Existing sessions need an explicit acknowledgement
of this policy revision; adding files alone does not update their conversation.

Routine read-only checks and exact already-approved actions need no repeated
confirmation. New remote/external writes retain the workspace's explicit review
requirements. No general permission to broadcast tasks, execute another agent,
change credentials, merge a PR or discard work is granted by this document.

This policy does not itself prove active server rules, loaded execution rules,
installed hooks, isolated backups or acknowledgement by another agent. Record
those separately against exact repository, branch, commit and session identities.
