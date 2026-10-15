# Deep reference — Verification & "done means done"

This is the most violated discipline in agentic work, including by the agents building the
app. Load this whenever you're about to accept a "done"/"complete"/"tests pass" claim.

## Why this exists (the scar)
An autonomous build reported "1,481 tests passed, all workstreams complete." The code
showed: a gateway with a temporal-dead-zone bug that threw on **every real LLM call**
(tests passed because they only hit the mock path); 8 services still bypassing the
gateway; and an entitlement cap wired as `countToday: () => 0` (passes tests, never
fires). "Green + complete" while three foundational things were broken. This is the
default failure mode, not an edge case.

## The rule
**A claim is true only when a live behavior proves it.** Tests, type-checks, and an
agent's self-report are necessary, never sufficient.

## Define a LIVE done-gate per feature
For each feature, write the gate *before* building, as observable behavior:
- Boot the real thing (not a test harness).
- Exercise the real path (real key, real request, real restart).
- Watch the output. Paste it.

Examples of good live gates:
- "Set a real API key → one real generation returns actual content (not the mock), and
  it refuses a fabricated number." (proves the LLM path + the constitution)
- "Create a record → restart the process → the record is still there." (proves durability)
- "Exceed the free daily cap → the next call returns 402." (proves enforcement, not a stub)
- `grep -rn "chat/completions" src` → only the gateway. (proves the single-seam claim)

## The forbidden patterns (auto-fail)
1. **Tests-as-proof** for anything that has a mock path. If the mock returns early, the
   real code never ran in the suite.
2. **Stub-as-pass:** a constant returned to satisfy a signature. Grep for `() => 0`,
   `return []`, `return true`, hardcoded values on a path that claims to be live.
3. **Advancing on red:** reporting "at phase N" while phases < N fail their gates. Always
   re-verify claimed-done before building on top.
4. **Status-only assertions:** `expect(res.status).toBe(200)` without asserting the body.
5. **Vacuous/conditional assertions:** an `expect` guarded by an `if` that may not run.
6. **Fallback-as-PASS:** a deterministic stub/template under test is DEGRADED, not PASS.

## Honest tags (use exactly one per capability)
- **PASS** — real output verified, evidence pasted.
- **DEGRADED** — works via stub/fallback; real path unverified. (Beats a fake PASS.)
- **SKIP-needs-X** — needs a key/credential/network; say which.
- **FAIL** — broken.

## The audit trace (when verifying "it works")
Follow the chain end to end and flag every broken link:
`UI element → client function → HTTP route → service method → data store`.
The **UI↔backend seam** is where bugs hide because in-process tests skip it. (Scar: a UI
that called `/api/v1/voice/*` while the route was `/api/v1/writing/voice/*` — every test
green, the page 404.)

## Reviewing an agent's "complete" report — checklist
- [ ] Did it list the workstreams it *didn't* mention? (Silence on the hard ones = red flag.)
- [ ] Run the grep/boot/restart gates yourself; don't read the summary.
- [ ] Look for `.tmp` files / mid-edit state before trusting "done."
- [ ] Check each claimed enforcement actually fires (trip the cap, hit the gate).
- [ ] Confirm the real (non-mock) path executed at least once with pasted output.

## The one line
Evidence before assertions, always. If you can't paste the live output, it isn't done.
