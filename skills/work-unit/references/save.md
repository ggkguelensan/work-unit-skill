# Save a work unit

Read the [schema](work-unit.schema.json) before editing.

- Identity: reuse `id` and `emojis`; for new units, generate a lowercase UUID with `uuidgen` and choose four random emoji. Exclude the registry through Git's local exclude file when inside a checkout.
- Titles: use `<emojis joined without spaces> <name>` for suitable unit-related session, tab, terminal, document, or MR titles. Preserve required title formats and scope; use the UUID for exact linkage. Derive the label rather than storing a duplicate field.
- Scope: derive a short name, outcome, and testable DoD from confirmed sources. Keep `description` to one short sentence; link detailed context through `references`.
- Links: group confirmed tasks and implementations by shared outcome. Use task GIDs, full MR URLs, and absolute worktree paths; identify implementations by origin URL + branch. Allow multiple entries; deduplicate by identity.
- Resources: label other URLs, URIs, or absolute paths in `references`. Link requirements/evidence; keep delivery status in Asana/GitLab.
- Participants: deduplicate by `(tool, kind, id)` using supplied agent IDs, falling back to session IDs. Update `last_seen_at` on participation; optionally set `role`. Last seen does not establish liveness.
- Changes: save selected/created/found MRs and worktrees, revised scope, and changed links. Remove confirmed deleted worktree paths; preserve branch/MR links and unrelated entries.

Write under a per-unit lock: reread → update with `jq --arg`/`--argjson` → validate against the schema → atomically replace via a same-directory temporary file. Release the lock on success or failure. `jq -e` is not schema validation.
