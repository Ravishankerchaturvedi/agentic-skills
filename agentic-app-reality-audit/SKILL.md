---
name: agentic-app-reality-audit
description: A read-only, evidence-first method to audit any agentic app or codebase for what's ACTUALLY built vs what's claimed — surfacing broken wiring, stubs, dead state, and "tests-green-but-broken" gaps. Use before trusting a status report, before shipping, or when inheriting an unfamiliar agent app.
---

# Agentic App Reality Audit

Purpose: produce a truthful "claimed vs actually-done" map of an app, grounded in code and
live behavior — never in docs or self-reports (both lie). Read-only: change nothing.

## When to use
- An agent/teammate reports "done" / "complete" / "tests pass."
- You inherit a codebase and need the real state.
- Before a release, a demo, or building on top of someone's work.

## Operating rules
- **Read-only.** Never edit during an audit; you'll corrupt the thing you're measuring.
- **Don't trust docs.** Verify every doc claim against code (docs were caught claiming
  "all pages 200" while a page 404'd).
- **Label honestly:** REAL · DEGRADED (stub/fallback) · BROKEN · HOLLOW (exists,
  disconnected) · NOT-OPENED (wired, not yet read). Never imply more verification than done.

## The method (in order)
1. **Map the inventory from the source of truth**, not the docs. For a DI app, that's the
   container/wiring file — it lists every service that actually exists and is constructed.
2. **Trace the seams end-to-end.** For each user action: UI element → client fn → HTTP
   route → service → data store. Flag every broken link. The UI↔backend seam hides the
   most bugs.
3. **Sweep for fakes & stubs** across the whole tree (cheap, high-signal):
   - `Math.random` on a data path (fake numbers).
   - `TODO|FIXME|placeholder|not implemented|mock|stub`.
   - constants returned to satisfy a signature (`() => 0`, `return []`, `return true`).
   - key-gated degradation (`if (!process.env.X) return <fallback>`).
4. **Check state durability.** Which stores persist vs in-memory? Find services with
   `getSnapshot` the persistence layer never calls (capable ≠ wired).
5. **Probe the LLM seam.** How many places call the model directly? Is there one gateway
   or N? Does the real (non-mock) path actually run?
6. **Run the live gates** for the riskiest claims (boot, real call, restart, trip a cap).
   Tests passing is not a gate.
7. **Produce the verdict table:** per subsystem → status + one-line evidence (file:line).

Full step-by-step with the exact greps and a worked example: `references/audit-playbook.md`.

## Output shape
A single table the owner can act on:

| Subsystem | Status | Evidence | Verdict |
|---|---|---|---|
| … | REAL/DEGRADED/BROKEN/HOLLOW | file:line or pasted gate output | WORKING / NEEDS-FIX |

Plus: the systemic findings (the few root causes behind many symptoms) and the smallest
set of fixes that flip the most red to green.

## The one line
Trust the diff and the live behavior, never the summary. Evidence before assertions.
