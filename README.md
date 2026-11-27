# agentic-skills

[![tests](https://github.com/Ravishankerchaturvedi/agentic-skills/actions/workflows/tests.yml/badge.svg)](https://github.com/Ravishankerchaturvedi/agentic-skills/actions/workflows/tests.yml)
![python](https://img.shields.io/badge/python-3.10%2B-blue)
![license](https://img.shields.io/badge/license-MIT-green)
![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

**Ten field-tested skills for building and shipping real agentic apps - and a checker that keeps every SKILL.md honest.** The skills are plain Markdown that works with Claude Code, Cursor, Codex or any LLM; the checker is a standard-library-only CLI that validates a skill library's structure and scans it for private-data markers.

These are written from hard-won production scars, not tutorials. The recurring theme: most failures are not in features; they are in wiring, state, verification, cost, and trust.

## Problem

Two problems, one repo.

Agent skills rot quietly: a renamed folder leaves a stale frontmatter `name`, a description drifts to four sentences, a `references/` deep dive is deleted while the SKILL.md still points at it, and a private path slips into a file that is about to be made public. Nothing fails until an agent loads the broken skill or the repo goes out.

And agent work itself fails in known ways - a scheduled job silently misses four days, an approval is given for bytes that later changed, a "done" report turns out to have changed nothing. The second half of this library is the operating discipline that catches those: cadence operations, the release bar, evidence markers, and the audit for fake work.

## Install

```bash
pip install -e .[test]
```

Python 3.10 or newer; no dependencies beyond `pytest` for the tests.

## Quickstart

Check this repo's own library (eleven SKILL.md files: the root plus ten skills), then check the deliberately broken fixture:

```bash
agentic-skills check .
agentic-skills check examples/bad-library
```

Real output of those commands (run on 2026-11-26):

```
$ agentic-skills check .
11 skills checked, 0 problems
$ agentic-skills check examples/bad-library
no-description/SKILL.md: SKILL_NO_DESCRIPTION: frontmatter has no description
wrong-name/SKILL.md: SKILL_NAME_MISMATCH: frontmatter name 'right-name' does not match folder 'wrong-name'
notes.md:4: PRIVATE_MARKER: line 4: absolute Unix home path (match redacted)
3 problems in 3 file(s)
```

The fixture failure is the tool working: a name that does not match its folder, a missing description, and a private home path that must never reach a public repo - each reported with its file, and the private match itself redacted. Point it at any library:

```bash
agentic-skills check path/to/your/skills --banned-file extra-patterns.txt
```

Run the tests with `python -m pytest -q`.

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

Each skill folder holds a `SKILL.md` (the loadable summary) and an optional `references/` directory (load-on-demand deep dives).

## How it works

**The skills** are plain Markdown with YAML frontmatter (`name`, `description`). `SKILL.md` is the always-load summary; `references/*.md` are deep dives. Drop a folder into your agent's skills directory, paste `SKILL.md` into your rules, or reference it from `AGENTS.md`.

**The checker** (`agentic-skills check [path]`) walks the library and enforces the house rules:

- every `SKILL.md` starts with frontmatter carrying `name` and `description`;
- `name` equals the folder the skill lives in - for the root `SKILL.md`, the project name from `pyproject.toml` (or the root folder name without one);
- `description` is non-empty, at least 40 characters, and at most 3 sentences;
- the body under the frontmatter is not empty;
- every `` `references/...` `` file a SKILL.md mentions exists (wildcard mentions like `references/*.md` document the convention and are exempt);
- every Markdown file is scanned for private-data markers: absolute home paths, private IP ranges, and common token shapes (AWS, GitHub, Slack, PEM keys). The matched text is never printed, only the label and line.

Findings are one line each (`file: CODE: message`), then a count and `PASS` or `FAIL`. `--banned-file` adds patterns (one regex per line, `#` comments); `--no-private` skips the scan; `--json` prints one JSON object. Directories named `examples` are skipped in a library-wide walk - they hold intentional fixtures - but the checker walks them when you point it at one directly, which is what the failing quickstart command does.

## Use it with AI agents

- The repo is itself a skill library: a coding agent that reads skills (for example Claude Code) discovers the root `SKILL.md`, then loads individual skill folders as needed.
- Give the checker to an agent that writes or edits skills and let it gate its own work before committing: `agentic-skills check . || fix the reported files`.
- Exit code `0` = pass, `1` = problems found (each printed as `file: CODE: message`), `2` = bad input (for example a missing path).
- In CI, `agentic-skills check .` fails the build on any violation; the private-marker scan keeps private strings out of published Markdown.

## Format (intentionally tool-agnostic)

Every skill is plain Markdown with YAML frontmatter. Nothing depends on a specific runtime. Load it into whatever you use:

- **Claude Code / Claude skills** - drop the folder in `~/.claude/skills/` or project `.claude/skills/`.
- **Cursor / Windsurf** - paste `SKILL.md` into `.cursor/rules/` (or project rules).
- **OpenAI Codex / Antigravity** - reference `SKILL.md` from your `AGENTS.md`.
- **Any MCP agent or LLM chat** - paste the body as system context; pull a `references/*.md` file when depth is needed.

## Versioning

The library is versioned in this repo: see CHANGELOG.md. v0.1.0 was the June 2026 six-skill snapshot; from v0.2.0 the skills live at the repo root and new revisions are version bumps, not new dated folders, so a clone plus a tag is always reproducible.

## Limits

- The checker reads simple `key: value` frontmatter only - no nested YAML, no multi-line values.
- The private-marker scan covers Markdown files only; scanning code and secrets is the job of your secret scanner in CI.
- Name checks are exact string matches, not fuzzy - `my-skill` and `my_skill` are different names.
- The default marker patterns are a floor, not a ceiling; add site-specific patterns with `--banned-file`.
- The skills encode one operator's field practice; treat them as strong defaults, not standards.

## About

Built by Ravi Shanker Chaturvedi at RAD Media, Mumbai. The skills are distilled from running a real agent build-and-publish operation every day; we build AI systems for growing businesses. Questions, bugs or a custom build: open an issue.
