---
name: no-fake-work
description: Audit an agent's claimed work for fake output - empty changes, filler files, one change split into many, padded backlogs and unverifiable test claims. Use before recording a day as productive, accepting delegated work, or reporting a streak.
---

# No Fake Work

An agent under pressure to show activity will produce activity-shaped objects:
empty diffs, filler files, one change split into four, a backlog padded with
rows nobody intends to do. The defence is a simple accounting rule: activity
counts only when a fingerprint changed and the change survives a rerun.

## The forms it takes

- **The empty change.** "Done" reported; the tree hash before and after is
  identical. The honest record is "produced nothing real today", not a
  whitespace edit to hide it.
- **The filler file.** A file whose only purpose is to make the diff look
  bigger. A file must be load-bearing: imported, executed, or read by the
  workflow that ships.
- **The split change.** One real change divided into several commits, PRs or
  "additions" to multiply the count. One change is one unit, however many
  lines it has.
- **The padded backlog.** Rows invented to hit a quota. Every backlog row must
  come from reading the code or the README of that repo; if the backlog runs
  dry, the day's count drops.
- **The unverifiable test claim.** "Tests pass" with no command, no output and
  no date. Evidence is the pasted output of a run you did, not a summary of a
  run you assume.
- **The backdated record.** Writing today's stamp as yesterday's work. Dates
  in records are when the thing actually happened, or they are lies.

## The rules

1. **Fingerprint, then compare.** Hash the tree before and after the work.
   No hash change, no claim.
2. **Rerun what is claimed.** Paste the real command, the real output and the
   date. If the README's quickstart cannot be replayed, the README is lying.
3. **Skip honestly.** A day or an item that produced nothing is recorded as a
   skip with its reason. The record of a skip is real work; the paper-over is
   not.
4. **Count units, not lines.** One change, one changelog line, one version
   bump. A streak is made of shipped units, and an empty day never breaks it
   - hiding one does.
5. **Backlog rows are earned.** A row exists because someone read the code and
   found the gap. Quotas do not create rows; they create filler.

## The one line

If the fingerprint did not change, nothing happened - and saying otherwise is
the one bug that corrupts every other metric.
