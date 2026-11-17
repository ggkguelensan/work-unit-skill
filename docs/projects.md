# Projects

For organizing independent projects under `~/Projects/<project-name>/`.

## Layout

Illustrative tree; create only needed directories and preserve existing layouts:

```text
~/Projects/<project-name>/
├── AGENTS.md
├── CLAUDE.md
├── .agents/
│   ├── docs/
│   ├── skills/
│   ├── scripts/
│   └── work-units/<uuid>.json
├── .config/worktrunk.toml
├── project-settings/
├── repos/<owner>/<repository>/
└── worktrees/<owner>/<repository>/<branch>/
```

- `AGENTS.md`: project entry point, repository selection, baselines, and scoped document routes.
- `.agents/`: project guidance, skills, helpers, and local work records.
- `.config/`: native tool settings. Use optional `project-settings/` only for settings without an existing owner; the skill does not parse it.
- `repos/` and `worktrees/`: preserve forge namespaces. A project may contain independent repositories or be a single checkout itself.
- Credentials: use each tool's supported credential store.

Ticketon keeps primary checkouts in `ticketon-fho/`; this convention does not require moving them.

## Repository work

- Keep personal defaults in user configuration and project facts in project instructions.
- Load owning workspace instructions explicitly from nested repositories/worktrees; apply repository/subtree guidance within its checkout.
- Before edits, check physical path, Git status, branch, worktrees, and applicable instructions.
- Select the task/project baseline; the forge default branch may differ. Ticketon workspace analysis prefers `dev` where available.
- Derive setup, tests, and hooks per repository; run them in its selected checkout.
- Track source and deployment-config repositories separately, including branches, MRs, and checks.

For native instruction and skill connections, read [Agents](agents.md).

## Worktrees

- Reuse a suitable worktree; otherwise create it with `wt`.
- Use effective Worktrunk configuration and its reported path.
- When a workspace provides `.config/worktrunk.toml`, pass it explicitly:

```sh
wt --config "$project_root/.config/worktrunk.toml" -C "$repo_root" list
wt --config "$project_root/.config/worktrunk.toml" -C "$repo_root" \
  switch --create "$branch"
```

- Keep lifecycle hooks in each repository's `.config/wt.toml`; workspace path settings have a different scope.
- Before removal, check dirty/untracked files, unpreserved commits, and MR state. Session completion alone does not make a worktree disposable.

## Work units

Use the [skill](../skills/work-unit/SKILL.md) for recovery and persistence across all project checkouts. Its [example](resources/work-unit.example.json) is fictional; live records stay local.
