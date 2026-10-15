# Skills — June 2026

A library of portable, field-tested skills for building and shipping real agentic apps.
Each skill is a folder with a `SKILL.md` (the loadable instruction file) and an optional
`references/` directory for deep dives.

These are written from hard-won, production scars — not tutorials. The recurring theme:
**most failures are not in features; they are in wiring, state, verification, cost, and trust.**

## Skills in this set
| Skill | What it's for |
|---|---|
| `building-real-agentic-apps` | The bible. How to architect/build/ship a real agentic app from all angles. |
| `agentic-app-reality-audit` | Read-only "verify, don't trust" audit of any agent/app — claimed-vs-actually-done. |
| `live-gated-handoff` | Writing cold-start work orders that prove completion by live behavior, not tests. |
| `voice-agent-architecture-and-cost` | Stack choice (rent vs own) + per-minute cost & margin model for voice/LLM apps. |
| `find-what-to-build` | Choosing what to build: pay-willingness ∩ real pain ∩ reliably-automatable. |
| `productize-to-recurring` | Turning a one-time build into setup + MRR + usage; the white-label ladder. |

## Format (intentionally tool-agnostic)
Every skill is **plain Markdown with YAML frontmatter** (`name`, `description`). Nothing
depends on a specific runtime. Load it into whatever you use:

- **Claude Code / Claude skills** — drop the folder in your skills directory (`~/.claude/skills/` or project `.claude/skills/`).
- **Cursor / Windsurf** — paste `SKILL.md` into `.cursor/rules/` (or project rules).
- **OpenAI Codex / Antigravity** — reference `SKILL.md` from your `AGENTS.md` (or paste as a system/context file).
- **Hermes / OpenClaw / any MCP agent** — point the agent at the `SKILL.md` path as a context/instruction file, or expose the folder as a resource.
- **Any LLM chat** — paste the `SKILL.md` body as system context; pull a `references/*.md` file when depth is needed.

Convention: `SKILL.md` is the always-load summary; `references/*.md` are load-on-demand
deep dives (keeps the context window lean — see `building-real-agentic-apps`, Part 2).

## Versioning
Folder is dated (`Skills - June 2026`). Future revisions live in new dated folders so a
shared snapshot is always reproducible.
