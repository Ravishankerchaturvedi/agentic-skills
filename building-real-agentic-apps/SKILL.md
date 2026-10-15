---
name: building-real-agentic-apps
description: A field-tested bible for building production agentic apps — not just features, but the wiring, state, verification, cost, and trust disciplines that decide whether it actually works. Use when architecting, building, auditing, or reviewing any LLM/agent app.
---

# Building Real Agentic Apps

Most guides teach you to wire an LLM to tools. That gets you a demo. This skill is the
80% nobody teaches: the disciplines that separate a demo from a system a customer pays
for and trusts. Fuses external canon (Anthropic *Building Effective Agents*, Karpathy
*context/agentic engineering*) with production scars.

## The two laws (everything else serves these)
1. **Verify, never trust.** "Tests pass" / "done" / "all complete" are claims, not facts.
   A claim is true only when a *live behavior* proves it.
2. **A feature that isn't wired, durable, and reachable is not done** — it's a lie
   waiting to be found.

## Part 1 — Decide if you even need an agent
- Start with the **simplest thing that works**: a single call or a fixed **workflow**
  (LLM on rails) often beats an autonomous agent.
- **Workflow vs agent:** workflow = predictable, well-defined, predefined paths. Agent =
  open-ended, unpredictable step count, must trust model decisions. Agents trade
  latency+cost for flexibility — only pay it when the problem demands it.
- **Build narrow and deep, not wide.** One painful, paid-for workflow done excellently >
  100 shallow agents. Ship one, get one paying user, then expand.

## Part 2 — Context engineering is the job
- LLM = CPU; **context window = RAM.** Your job is filling it with *just* the right info
  for the next step.
- **One mouth (a gateway):** route *every* LLM call through one seam, or a rule fixed in
  one place is ignored everywhere else.
- **Stable prefix, volatile suffix:** identity/rules/role in a cache-friendly prefix;
  fresh facts after it. Cost lever (cache hits) + correctness lever.
- **Read at decision time, never cache beliefs**, or the agent acts on stale info.
- `references/context-gateway-and-truthfulness.md` for the full pattern.

## Part 3 — Truthfulness is architecture, not a prompt
- A **Constitution** (immutable top rules) on every call: assert only what's in
  tools/grounding; never invent a number/price/status; mark inference vs fact.
- A **Verification Gate** on anything outbound: every claim/number must trace to a
  source, else block → human.
- **Ground in tools, not memory.** Few, stable, well-described tools. Audit for
  *phantom tools* (a tool returning a hardcoded string = the agent acts on fake data).
- Deep dive: `references/context-gateway-and-truthfulness.md`.

## Part 4 — Verification: "done means done"
- **Tests green ≠ done.** Suites pass on mock paths while the real path throws.
- Define a **LIVE done-gate per feature**; accept nothing else. Boot it, hit the real
  path, watch behavior, paste output.
- **Never advance on red.** Re-verify claimed-done before building on top.
- **Hunt stub-as-pass:** a constant returned to satisfy a type signature (e.g.
  `countToday: () => 0`) passes tests while the feature is dead.
- Honest tags: PASS / DEGRADED / SKIP-needs-X / FAIL. A labeled DEGRADED beats a fake PASS.
- Full playbook + our scars: `references/verification-and-done-gates.md`.

## Part 5 — State is the substrate
- **In-memory state dies on restart** → demo, not product. Wire persistence as you build
  each stateful service, not "later."
- Watch the **half-wire**: a service with `getSnapshot()` the persistence layer never calls.
- **Single source of truth + events:** each fact in one service; UI reads/writes it;
  changes emit events; the next agent action reads the change live.
- Deep dive: `references/state-durability-and-the-loop.md`.

## Part 6 — The compounding loop (the real moat)
- The moat is the loop: `action → outcome → learning → better next action`, and (multi-
  tenant) that learning **aggregated, anonymized, and redistributed** so every user
  improves every other.
- Inputs (scrapers, providers) sit **behind ports** so one dying ≠ moat dying.
- Deep dive: `references/state-durability-and-the-loop.md`.

## Part 7 — Safety, cost, the human edge
- **Human checkpoints before irreversible/spend actions** (publish, send, pay, delete).
- **Sandbox untrusted execution** (per-run isolation).
- **Model unit economics before scaling** — autonomous LLM/voice apps spend with no human
  in the loop; know cost-per-action and cap it.
- **Rent commodities** (telephony, voice, STT); **own the brain + data + loop**; keep every
  rented piece swappable behind a port.

## Part 8 — How to drive an AI building the app (agentic engineering)
- **Spec first** (requirement + done-gate before prompting).
- **Eval design** (verifiable signals; truth-traps).
- **Diff review** (read output for architectural correctness; don't merge on vibes).
- **Live-gated handoffs** (one workstream, cold-start context, the exact live gate,
  "stop and paste the output"). See the `live-gated-handoff` skill.

## One-paragraph version
Pick the smallest thing that solves a real, paid-for pain. Route every LLM call through one
gateway with a constitution + verification gate, grounded in real tools. Make state durable
from day one and let edits propagate live. Build the action→outcome→learning loop — that's
the moat. Gate irreversible actions with a human, model the cost, rent commodities, own the
brain. Never accept "done" without a live gate that proves it.

## Sources
- Anthropic — Building Effective Agents (anthropic.com/research/building-effective-agents)
- Karpathy — context engineering / agentic engineering (LLM = OS; spec, eval, diff review)
- Patterns from 2026 agent repos (MCP-native tools, pgvector memory, per-run sandboxes,
  stateful agents, teams-of-specialized-agents)
