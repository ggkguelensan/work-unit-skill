# Recover a work unit

1. Identify the owning project root; its repositories and worktrees share one registry.
2. Search by unit ID/name/title, task, participant, resource, repository, branch, or checkout reference:

```sh
"$skill_root/scripts/find.sh" "$project_root" "$reference"
```

[find.sh](../scripts/find.sh) uses [find.jq](../scripts/find.jq). It returns one array, including `[]` for no matches; missing registries and read/parse failures are errors.

3. Resolve ambiguous matches using repository and task/MR evidence. Check services and worktrees before creating unrecorded resources.
4. Read goal, description, DoD, and participants. Verify relevant links against current service/local state; timestamps alone do not prove validity.
5. Resolve stale paths or conflicting identities before updating. Saved links alone do not justify recreating resources.
