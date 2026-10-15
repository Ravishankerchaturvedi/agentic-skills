# Deep reference — Reality audit playbook (commands + worked example)

## Phase 0 — Inventory (don't trust docs)
- Find the wiring/DI/container file (where services are constructed). It is the true list
  of what exists. Read its imports + the returned container object.
- List routes/endpoints from the router/server file, not from the API docs.

## Phase 1 — Seam tracing
For each major user action, follow the chain and record where it breaks:
`UI → client function → HTTP path → mounted route → service method → store`.
Common breaks:
- client calls a path that isn't mounted (404) — e.g. `/api/v1/voice/*` vs `/api/v1/writing/voice/*`.
- route exists but returns a shape the UI doesn't read (`{items}` vs `{ideas}`).
- two API clients / dead generated clients drifting apart.

## Phase 2 — Fake/stub sweep (run across the whole source tree)
```
# fake numbers
grep -rn "Math.random" src --include=*.ts | grep -v test
# stubs / placeholders
grep -rniE "TODO|FIXME|not implemented|placeholder|coming soon|\bstub\b|simulate" src --include=*.ts | grep -v test
# constants-as-implementation (entitlements, scores, confidence)
grep -rnE "\(\) => (0|\[\]|true|false)" src --include=*.ts
# key-gated degradation
grep -rn "process.env" src --include=*.ts | grep -iE "API_KEY|return.*fallback"
```
Triage each hit: legitimate (e.g. Thompson sampling uses random) vs fake-on-a-real-path.

## Phase 3 — Durability
```
grep -rln "getSnapshot" src --include=*.ts        # persistence-capable services
```
Open the persistence manager; list which of those it actually saves/restores. The delta =
data that dies on restart. Flag especially: learning/reinforcement, profiles, entities,
audit logs, billing/plan state.

## Phase 4 — LLM seam
```
grep -rln "chat/completions" src --include=*.ts    # how many mouths?
```
One file (the gateway) = good. N files = ungoverned drift; constitution/verification reach
only some paths. Check the gateway's real path actually executes (not just a mock branch).

## Phase 5 — Live gates (the only real proof)
- Boot the app; `curl /health` (DI collisions are silent at compile time, fail at boot).
- Real key set → one real generation returns real content + obeys the constitution.
- Create a record → restart → still present.
- Trip an enforcement cap → expect the block (proves it's not a stub).

## Worked example (condensed, from a real audit)
- Inventory: container had ~150 services; ~9 user-facing, rest plumbing/operator.
- Seam: voice page 404'd (prefix mismatch); 4 endpoints the UI called didn't exist.
- Sweep: clean of fake data EXCEPT a `confidence: 0.5 + Math.random()*0.3` and an image
  placeholder — both labeled DEGRADED.
- Durability: 6 of ~20 stores persisted; the entire learning moat was RAM-only.
- LLM seam: gateway existed but 8 callers bypassed it; a TDZ bug threw on every real call
  while 1,481 tests passed on the mock path.
- Verdict: "real software, not fake — but wiring + durability + verification are the
  fractures." Four small fixes flipped most of it.

## The discipline
One change-set you DON'T make during an audit. You only look, trace, grep, boot, and
report — with file:line or pasted output behind every claim.
