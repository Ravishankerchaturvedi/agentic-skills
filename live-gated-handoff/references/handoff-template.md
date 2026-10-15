# Handoff template (copy, fill the [brackets])

## MASTER PROMPT (prepend to every handoff)
> Continue [PROJECT] ([stack]; entry `[entry file]`; wiring/DI in `[config file]`;
> [other key locations]). Read [PLAN DOC] + [CONVENTIONS DOC] first.
> One change per commit, red-before-green, paste real output. "Tests pass" is never the
> gate — only the live checks are. For reversible decisions, choose per the plan/conventions,
> log it, and continue; stop ONLY for a missing secret, a real bug, or an irreversible/spend
> action; never stub-as-pass or fake to avoid stopping. Do ONE workstream, then STOP and
> paste its live-gate output. Label anything still DEGRADED.

## TASK BLOCK (one per handoff)
> **Workstream:** [name + one-line goal]
> **Why / context:** [the seam: what calls this, what it should call, the data flow]
> **Do:** [numbered, concrete steps with file paths]
> **Do NOT:** [scope fence — what's out of bounds for this unit]
> **Live gate (paste all):**
> - [observable proof 1 — command + expected behavior]
> - [observable proof 2 — boot/real-call/restart/trip-a-cap]
> - [observable proof 3]
> Stop after the gate. Do not start the next item.

## SECRETS & DECISIONS (so it doesn't ask 40 times)
> Pre-answered (use these, don't ask): [list reversible decisions already made]
> You must STOP and ask only for: [the real secrets/inputs only the human can provide]

## REVIEW CHECKLIST (for the person receiving the report)
- [ ] Ran the live gate myself; output matches.
- [ ] No `.tmp`/mid-edit files; commit is focused.
- [ ] Hard sub-items addressed (not just the easy ones).
- [ ] Each claimed enforcement actually fires.
- [ ] Real (non-mock) path executed with pasted evidence.
