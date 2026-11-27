---
name: agentic-skills
description: Ten portable, field-tested skills for building and shipping real agentic apps, plus a checker that validates every SKILL.md in a skill library. Drop the folders into your agent's skills directory; each skill is plain Markdown that works with Claude Code, Cursor, Codex or any LLM.
---

# agentic-skills

A library of portable, field-tested skills for building and shipping real
agentic apps, written from hard-won production scars - not tutorials. Each
skill is a folder with a `SKILL.md` (the loadable instruction file) and an
optional `references/` directory for deep dives.

The recurring theme: **most failures are not in features; they are in wiring,
state, verification, cost, and trust.**

## Skills in this set

| Skill | What it's for |
|---|---|
| `building-real-agentic-apps` | The bible. How to architect/build/ship a real agentic app from all angles. |
| `agentic-app-reality-audit` | Read-only "verify, don't trust" audit of any agent/app - claimed-vs-actually-done. |
| `live-gated-handoff` | Writing cold-start work orders that prove completion by live behavior, not tests. |
| `voice-agent-architecture-and-cost` | Stack choice (rent vs own) + per-minute cost and margin model for voice/LLM apps. |
| `find-what-to-build` | Choosing what to build: pay-willingness, real pain, reliably-automatable. |
| `productize-to-recurring` | Turning a one-time build into setup + MRR + usage; the white-label ladder. |
| `agent-cadence-operations` | Running an agent job on a daily schedule for months: locks, catch-up, timezones, no filler. |
| `release-bar-shipping` | The per-item bar that turns real work into small publishable repos - or moves the date. |
| `evidence-markers` | Markers that bind every claimed run to a content hash, gate results and a date. |
| `no-fake-work` | Auditing claimed work for empty changes, filler files, split changes and padded backlogs. |

## Format (intentionally tool-agnostic)

Every skill is **plain Markdown with YAML frontmatter** (`name`, `description`).
Nothing depends on a specific runtime. Load it into whatever you use:

- **Claude Code / Claude skills** - drop the folder in your skills directory
  (`~/.claude/skills/` or project `.claude/skills/`).
- **Cursor / Windsurf** - paste `SKILL.md` into `.cursor/rules/` (or project rules).
- **OpenAI Codex / Antigravity** - reference `SKILL.md` from your `AGENTS.md`
  (or paste as a system/context file).
- **Any MCP agent or LLM chat** - point the agent at the `SKILL.md` path, or
  paste the body as system context; pull a `references/*.md` file when depth
  is needed.

Convention: `SKILL.md` is the always-load summary; `references/*.md` are
load-on-demand deep dives (keeps the context window lean).

## Checking a skill library

This repo ships `agentic-skills`, a stdlib-only checker that enforces the
library's own rules on any skill tree: frontmatter with `name` and
`description` (1-3 sentences), name matching the folder, non-empty body,
resolvable `references/` mentions, and a private-data marker scan over every
Markdown file. See the README quickstart; directories named `examples` are
treated as intentional fixtures and skipped in a library-wide check.
