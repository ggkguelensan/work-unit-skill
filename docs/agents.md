# Claude Code and Codex

For shared project context and work-unit handoff:

- Instructions: one `AGENTS.md`; a sibling `CLAUDE.md` containing `@AGENTS.md` imports it for Claude.
- Skills: one source in `.agents/skills/`; link Claude's `.claude/skills/<name>` to it.
- User installation: follow [setup](resources/install.md); reusable skills remain available from nested checkouts.
- Settings: keep permissions, MCP, and hooks in each harness's native format.
- Nested repositories: explicitly supply the owning project's `AGENTS.md`; keep checkout-specific instructions local.
- Handoff: read the same project record and add the receiving participant using the [skill](../skills/work-unit/SKILL.md). Live conversations and runtime permissions remain harness-specific.

Discovery depends on harness version and configuration. Codex scans repository `.agents/skills` up to the Git root and user `~/.agents/skills`. Claude scans project `.claude/skills` and user `~/.claude/skills`; both support symlinked skill directories.

Official behavior: [Codex skills](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills), [Claude skills](https://code.claude.com/docs/en/skills#choose-where-skills-load), [Claude instruction imports](https://code.claude.com/docs/en/memory#share-one-file-with-other-coding-tools).
