---
name: agent-cadence-operations
description: Run an autonomous build-and-publish agent on a daily schedule for months - locks, catch-up runs, timezone-stable dates and no filler. Use when a scheduled agent job has missed days, or before you trust a streak of daily runs.
---

# Agent Cadence Operations

A daily agent that "has run every day" is a claim until you read the scheduler's
own records. The recurring failure is not the agent's work; it is the wiring
between cron, the timezone and the agent's idea of "today". Every rule below
comes from a real incident.

## The scars

- Four days of missed runs looked like a hung lock. The lock file was an empty
  `flock` target with no live holder; its old timestamp was a red herring. The
  real cause: the scheduler never dispatched the job at all. The cron journal
  proved other jobs fired at the same minute while this one did not.
- The app computed due dates in one timezone while cron fired in another, so
  every item silently slipped a day across the boundary. Fix the app to use the
  cron's timezone, not the other way round.
- A "fixed" schedule is a claim until a cron-fired run proves it.

## The rules

1. **A lock file is not a lock holder.** Diagnose dispatch (journal/syslog
   around the fire time) before touching locks. An old lock with no live
   process is a leftover, not a cause.
2. **One explicit cron line.** Fixed timezone, `/bin/bash`, explicit `PATH`,
   absolute working directory, absolute script path. No bare relative entries.
3. **Prove scheduling fixes with cron itself.** Install a temporary
   every-minute line that runs the job in dry-run mode, watch it fire, remove
   the line, then diff the restored crontab byte-for-byte against its saved
   hash.
4. **Catch up from the oldest slipped item**, under a hard batch cap. The cap
   is a ceiling, never a target - an empty day is a logged empty day.
5. **One item, one child run.** Each item in a batch gets its own order, its
   own gates and its own completion marker, so one failure cannot poison the
   rest. A repo with an unpublished marker waits; it is not built again.
6. **No filler.** If nothing is due and no release is scheduled, the run logs
   its emptiness and exits. Streaks are made of real work or they are lies.

The crontab checklist and the dry-run proof protocol: `references/crontab-that-survives.md`.

## The one line

Schedule the proof, not the promise: the cron journal is the truth about
cadence, and the marker files are the truth about the work.
