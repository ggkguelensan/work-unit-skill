# Work unit

An agent skill for keeping a piece of work connected across tasks, repositories, merge requests, worktrees, and sessions.

A work unit has a stable UUID, a working name, four random emoji, a short description, a goal, and a definition of done. It can link multiple Asana tasks, GitLab MRs, worktrees, resources, and participating agents or sessions.

## Install

Requires Bash, `jq`, and `find`; `uuidgen` creates new IDs. Linked-service operations use authenticated `asana-cli`, `glab`, and `wt` installations.

Clone into its own project directory:

```sh
git clone https://github.com/ggkguelensan/work-unit-skill.git \
  "$HOME/Projects/work-unit-skill"
```

Register one shared skill source. Codex discovers user skills here:

```sh
mkdir -p "$HOME/.agents/skills"
ln -s "$HOME/Projects/work-unit-skill/skills/work-unit" \
  "$HOME/.agents/skills/work-unit"
```

Connect Claude Code to that source:

```sh
mkdir -p "$HOME/.claude/skills"
ln -s "$HOME/.agents/skills/work-unit" \
  "$HOME/.claude/skills/work-unit"
```

If an entry already exists, inspect it before replacing it. Avoid duplicate registrations in directories scanned by the same harness. Start a new agent session and invoke `work-unit`, or let the harness select it for relevant work. See [Claude Code and Codex](docs/agents.md) for discovery paths and instruction adapters.

## Use

Store records in the project being worked on, such as `~/Projects/example/.agents/work-units/`. The skill installation and project records have separate owners.

```sh
"$HOME/Projects/work-unit-skill/skills/work-unit/scripts/find.sh" \
  "$HOME/Projects/example" DEMO-42
```

The search returns one JSON array containing matching file paths and records. An empty registry returns `[]`; missing registries and read/parse failures return an error.

Agents recover context before choosing a checkout, verify links through the relevant CLI, and save changes locally. The skill does not run a background sync service.

- [Skill instructions](skills/work-unit/SKILL.md)
- [Projects: layout and workflow](docs/projects.md)
- [Claude Code and Codex: shared sources and native adapters](docs/agents.md)
- [JSON Schema](skills/work-unit/references/work-unit.schema.json)
- [Synthetic work-unit example](docs/resources/work-unit.example.json)

## Validate

Run the search tests with Python 3, Bash, and `jq`:

```sh
python3 -m unittest discover -s tests -v
```

Also validate the schema and example when `uv` is available:

```sh
uv run --with 'jsonschema[format]' python tests/check_schema.py
```
