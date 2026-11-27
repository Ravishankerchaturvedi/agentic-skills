# Changelog

## v0.2.0 - 2026-11-26

- Added four skills distilled from running an agent build-and-publish cadence
  daily: `agent-cadence-operations` (scheduled runs that survive missed days),
  `release-bar-shipping` (the per-item publish bar), `evidence-markers`
  (claims bound to content hashes) and `no-fake-work` (auditing claimed work).
- Added the `agentic-skills` checker (standard library only): validates every
  SKILL.md in a library - frontmatter, name matching the folder, 1-3 sentence
  descriptions, non-empty bodies, resolvable `references/` mentions - and
  scans all Markdown for private-data markers. Exit codes: 0 pass, 1 problems
  found, 2 bad input.
- Added a pytest suite (24 tests), CI on Python 3.10 and 3.12, packaging
  (pyproject.toml, console script) and this changelog.
- Housekeeping: removed the rupee conversion in
  `voice-agent-architecture-and-cost/references/cost-model.md` so the whole
  library is currency-neutral (all examples in one currency).

## v0.1.0 - 2026-06

- The initial six skills: `building-real-agentic-apps`,
  `agentic-app-reality-audit`, `live-gated-handoff`,
  `voice-agent-architecture-and-cost`, `find-what-to-build`,
  `productize-to-recurring`.
