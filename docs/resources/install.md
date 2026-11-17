# Install

- Required: Bash, `jq`, `find`, and `uuidgen`.
- Linked services: authenticated `asana-cli`, `glab`, and `wt`.
- Inspect existing entries before replacing them; avoid duplicate skill registrations.

Clone the source, register it for Codex, and connect Claude Code:

```sh
git clone https://github.com/ggkguelensan/work-unit-skill.git \
  "$HOME/Projects/work-unit-skill"
mkdir -p "$HOME/.agents/skills" "$HOME/.claude/skills"
ln -s "$HOME/Projects/work-unit-skill/skills/work-unit" \
  "$HOME/.agents/skills/work-unit"
ln -s "$HOME/.agents/skills/work-unit" \
  "$HOME/.claude/skills/work-unit"
```

Start a new session and invoke `work-unit`, or let the harness select it. For discovery and instruction adapters, see [Agents](../agents.md).
