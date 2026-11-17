# Recover a work unit

1. Identify the owning project root from task context. Its nested repositories and worktrees share that project's registry; keep other projects separate.
2. Search by unit ID/name/title, participant ID, resource target, task ID/key/URL, MR URL, repository, branch, or worktree path with [find.sh](../scripts/find.sh):

```sh
"$skill_root/scripts/find.sh" "$project_root" "$reference"
```

The command returns one array, including `[]` for an empty registry; a missing registry or read/parse failure is an error. It uses [find.jq](../scripts/find.jq) for matching.

3. Resolve multiple matches by repository and task/MR evidence. If none match, check services and local worktrees before creating resources.
4. Read the unit's goal, description, DoD, and participants. Verify relevant links against current service/local state before acting; timestamps alone do not establish validity.
5. Report stale paths or conflicting identities; recover the actual relationship before updating it. A saved link alone does not justify recreating a missing resource.
