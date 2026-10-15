---
name: live-gated-handoff
description: How to write a cold-start work order for an autonomous agent (or teammate) that proves completion by live behavior, not a green test suite. Use when delegating a build task to an IDE agent, a subagent, or a fresh session.
---

# Live-Gated Handoff

A handoff is a contract. Most handoffs fail because they say "build X" and accept "tests
pass" as done — which is how agents end up "at phase 4" on a broken foundation. A good
handoff is self-contained, scoped to one unit of work, and defines the **live gate** that
proves it.

## The five rules
1. **Cold-start self-contained.** The receiver has no memory of your chat. Include the
   project shape (entry points, where things are wired), file paths, and the exact task.
2. **One workstream, then stop.** "And also do the rest" is how scope rots and quality
   drops. One unit → stop → report.
3. **The gate is live behavior, not tests.** State the observable proof: boot it, hit the
   real path, paste the output. Forbid "tests pass" as the sole evidence.
4. **Anti-cheat baked in:** one change per commit; red-before-green; no stub-as-pass; label
   anything still DEGRADED; if blocked on a missing secret or a real bug, STOP and report —
   never fake to avoid asking.
5. **Autonomy policy:** for reversible design choices, pick the option consistent with the
   plan/conventions, log it, and continue. Only stop for missing truth (a secret, a real
   bug) or irreversible/spend actions. (Stops it asking 40 times AND stops it guessing.)

## The template
See `references/handoff-template.md` for the fill-in-the-blanks version. Shape:

```
MASTER (prepend): project shape + anti-cheat + "do ONE workstream, paste live output, stop."
TASK: the specific change, with file paths and the seam on both sides.
LIVE GATE: the exact observable proof(s) — commands + expected behavior.
```

## Worked example (one queue item)
> Migrate every remaining `chat/completions` caller to `gateway.complete()`. Files: [list].
> Each keeps its logic but supplies role/grounding/surface/task; delete the local fetch.
> **Live gate:** (a) `grep -rn "chat/completions" src` → only the gateway; (b) boot + real
> key → one real generation returns real content (not mock); (c) it refuses a fabricated
> number. Paste all three. Stop after this — do not start the next item.

## Reviewing what comes back
- Don't read the summary as truth — run the gate yourself.
- Watch for silence on the hard sub-items (a "complete" that lists only the easy ones).
- Look for `.tmp`/mid-edit files before trusting "done."

## The one line
A task isn't handed off until its proof is defined. "Done" = the pasted live gate, nothing less.
