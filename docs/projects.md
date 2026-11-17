# Projects

Keep each project's repositories, worktrees, instructions, settings, and work-unit records under its own `~/Projects/<project-name>/` root.

## Layout

Illustrative layout; create directories only when needed:

```text
~/Projects/
├── example/
│   ├── AGENTS.md
│   ├── CLAUDE.md
│   ├── .agents/
│   │   ├── docs/
│   │   ├── skills/
│   │   ├── scripts/
│   │   └── work-units/<uuid>.json
│   ├── .config/worktrunk.toml
│   ├── project-settings/
│   ├── repos/<owner>/<repository>/
│   └── worktrees/<owner>/<repository>/<branch>/
└── another-project/
    ├── .agents/work-units/
    └── repos/
```

| Location | Owns |
| --- | --- |
| `AGENTS.md` | Project entry point: repository selection, baseline branches, links to scoped instructions |
| `CLAUDE.md` | Native import of the same project instructions when required |
| `.agents/docs/` | Project architecture and procedures |
| `.agents/skills/` | Project-specific skills |
| `.agents/scripts/` | Shared project helpers |
| `.agents/work-units/` | Local records spanning the project's repositories and sessions |
| `.config/` | Tool-native configuration, including workspace Worktrunk settings |
| `project-settings/` | Optional project-owned settings that have no existing native owner |
| `repos/` | Primary checkouts, preserving forge namespaces |
| `worktrees/` | Isolated checkouts managed by Worktrunk |

Use existing native config files as their source of truth. `project-settings/` is an optional directory convention, not a manifest parsed by this skill. Keep credentials in the relevant tool's supported credential store.

A project root may contain independent repositories without being a repository itself. A single-repository project may use the root as its checkout. Preserve existing layouts: for example, Ticketon keeps primary checkouts under `ticketon-fho/` rather than `repos/`.

## Instructions and settings

- Put personal defaults and reusable skills in the user's agent configuration; keep project facts in the project's instructions.
- Route from `AGENTS.md` to detailed documents by reading condition. Connect native agent entry points to that source instead of maintaining copies.
- Load workspace instructions explicitly when entering a nested repository or worktree. Keep repository/subtree instructions and native tool configuration scoped to their checkout.
- Derive setup, build, test, and hooks from each repository. Run them in that repository or its selected worktree.
- Keep source and deployment-config repositories distinct. Track their branches, checks, and MRs separately.

## Start or resume work

1. Select the owning project root; locate its work unit using a task, title, MR, session, branch, or path.
2. Read its goal, description, DoD, references, and participants. Confirm relevant links with the services and local checkouts.
3. Identify each target repository. Check its physical path, Git status, branch, worktrees, and instructions before changes.
4. Reuse a suitable worktree or create one with `wt` from the project's selected baseline. Use Worktrunk's reported path.
5. Work and validate per repository. Update implementation links, scope, and participant observations in the project record as they change.

Use the required baseline from project instructions or the task; the forge's default branch alone does not establish the development baseline. For workspace-wide Ticketon analysis, `dev` is preferred where available; other projects define their own baseline.

## Worktrunk

Use the effective path configuration rather than constructing worktree paths manually. Preserve owner/subgroup namespaces so similarly named repositories stay separate.

When a project provides an explicit workspace config:

```sh
wt --config "$project_root/.config/worktrunk.toml" -C "$repo_root" list
wt --config "$project_root/.config/worktrunk.toml" -C "$repo_root" \
  switch --create "$branch"
```

Ticketon uses this explicit config pattern. Its repository lifecycle hooks live in each repository's `.config/wt.toml`. These are different scopes; a workspace path convention does not define every repository's setup commands.

Before removing a worktree, check dirty/untracked files, unpreserved commits, and the associated MR. A finished session does not establish that its worktree is disposable.

## Work-unit records

Use the [work-unit skill](../skills/work-unit/SKILL.md) for the record schema and read/write procedures. Units belong to their project root even when work spans several nested repositories or checkouts.

The visual title is four emoji followed by the working name. Use it where title conventions permit; use the UUID for durable identity. Store supplied agent/session IDs with their tool name, and treat last-seen timestamps as observations.

Delivery status remains in Asana/GitLab. Local records retain the unit's purpose, DoD, resources, participants, and verified implementation links. Project membership alone does not link unrelated tasks.

Keep live records out of source commits. In a repository-backed project root, add `/.agents/work-units/` to that repository's local Git exclude file; in a linked worktree, locate it with `git rev-parse --git-path info/exclude`. Synthetic examples may be versioned separately.

See the [example record](resources/work-unit.example.json); its tasks, paths, MRs, and session IDs are fictional.
