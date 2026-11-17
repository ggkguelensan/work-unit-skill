# Work unit

An agent skill linking a goal and DoD to tasks, MRs, worktrees, resources, and sessions.

- One local record per unit, inside its project.
- Multiple tasks, repositories, MRs, worktrees, and participants.
- A stable UUID and a visual title: four emoji + working name.

## Start

- To install for Codex or Claude Code, follow [setup](docs/resources/install.md).
- To create or resume work, use the [skill](skills/work-unit/SKILL.md).
- To arrange projects, read [Projects](docs/projects.md).
- To connect both agents, read [Agents](docs/agents.md).

Data contract: [schema](skills/work-unit/references/work-unit.schema.json). Illustrative data: [synthetic example](docs/resources/work-unit.example.json).

## Checks

Requires Python 3, Bash, `jq`, and `find`; the schema check uses `uv`:

```sh
python3 -m unittest discover -s tests -v
uv run --with 'jsonschema[format]' python tests/check_schema.py
```
