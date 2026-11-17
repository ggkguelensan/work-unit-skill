# Save a work unit

Read the [schema](work-unit.schema.json) before editing.

- Identity: reuse UUID and emoji; for new units, use lowercase `uuidgen` output and four random emoji.
- Title: emoji joined without spaces + working name. Preserve required title conventions; derive the label, store no duplicate.
- Scope: confirmed short name, outcome, and testable DoD; `description` is one short sentence. Link detailed context and unresolved questions through `references`.
- Links: group confirmed work by shared outcome. Identify tasks by GID and implementations by origin URL + branch. Use full MR URLs and absolute worktree paths; allow multiple entries and deduplicate by identity.
- Resources: label URLs, URIs, or absolute paths. Link requirements/evidence; leave delivery status in Asana/GitLab.
- Participants: supplied `(tool, kind, id)`; prefer agent ID, otherwise session ID. Deduplicate; update `last_seen_at` on participation; `role` is optional. Last seen does not prove liveness.
- Updates: save selected/found/created resources and changed scope/links. Remove confirmed deleted worktree paths; retain branch/MR links and unrelated entries.
- Locality: inside a Git checkout, exclude live records through its local Git exclude file (`git rev-parse --git-path info/exclude`).

Write under a per-unit lock: reread → update with `jq --arg`/`--argjson` → schema validation → atomic replacement via a same-directory temporary file. Release the lock on success or failure. `jq -e` is not schema validation.
