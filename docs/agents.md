# Claude Code and Codex

Share instructions, skills, and work-unit data. Keep runtime configuration in each harness's native format.

## Project convention

```text
~/Projects/example/
├── AGENTS.md                     # Shared project instructions
├── CLAUDE.md                     # Imports @AGENTS.md
├── .agents/
│   ├── docs/                     # Scoped project guidance
│   ├── skills/<skill>/           # Shared project-specific skills
│   └── work-units/<uuid>.json    # Shared local work records
├── .claude/
│   ├── skills/<skill> -> ../../.agents/skills/<skill>
│   └── settings.json            # Claude-specific settings
├── .codex/config.toml           # Codex-specific settings
├── repos/
└── worktrees/
```

This is a convention, not a bootstrap script. Create only the adapters and settings actually needed.

| Concern | Shared owner | Native connection |
| --- | --- | --- |
| Project instructions | `AGENTS.md` | Codex reads it; Claude uses the import below |
| Detailed guidance | `.agents/docs/` | Reading conditions in `AGENTS.md` |
| Skill instructions/scripts | `.agents/skills/<skill>/` | Codex discovery; Claude skill-directory symlink |
| Work state | Project `.agents/work-units/` | Same schema and lookup script in either harness |
| Permissions, MCP, hooks | Each harness's settings | Configure separately using its supported schema |

Use this entire `CLAUDE.md` when no Claude-specific guidance is needed:

```text
@AGENTS.md
```

Claude's direct `AGENTS.md` support depends on version and configuration. The import provides an explicit connection and can coexist with direct support. See [Claude instruction loading](https://code.claude.com/docs/en/memory#agentsmd).

Codex discovers repository skills under `.agents/skills` from the working directory up to the repository root, and user skills under `~/.agents/skills`; symlinked skill folders are supported. See [Codex skill discovery](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills). Claude discovers project skills under `.claude/skills` and user skills under `~/.claude/skills`, including symlinked directories. See [Claude skill discovery](https://code.claude.com/docs/en/skills#choose-where-skills-load).

For reusable user skills such as `work-unit`, follow the [installation instructions](../README.md#install). For project-specific skills, keep their source under the project's `.agents/skills/` and link only the adapters needed by the installed harness.

## Nested repositories and worktrees

A project container is not necessarily a Git root. Do not assume a harness discovers project instructions or skills across nested repository boundaries.

- Start from the owning project, or explicitly provide its `AGENTS.md` when launching inside a repository/worktree.
- Keep repository-specific instructions in that checkout; give them an explicit reference to the owning workspace where needed.
- Keep reusable `work-unit` installed at user scope so both harnesses can find it from any checkout.
- Pass the owning project root to `find.sh`; every checkout uses the same project registry.

## Participants and handoff

Record each harness's actual supplied identity as `(tool, kind, id)`, for example tool names `codex` or `claude-code`. Use an agent ID when exposed, otherwise a session ID. IDs are opaque and need not have matching formats.

At handoff, the receiving agent reads the same unit and checks its scope, DoD, resources, and current implementation links. It records its own participation without replacing previous participants. A last-seen timestamp does not establish liveness.

This standard shares project context and work state. It does not translate live conversations, resume another harness's session, or unify permission and hook semantics.
