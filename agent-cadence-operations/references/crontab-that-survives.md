# The crontab that survives

A checklist for an agent job that must fire daily for months, plus the proof
protocol for changing it. Every item here paid for itself once.

## The line itself

```cron
CRON_TZ=Asia/Kolkata
0 10 * * * /bin/bash -c 'cd /abs/path/to/job && PATH=/usr/local/bin:/usr/bin:/bin ./daily.sh'
```

- **CRON_TZ matches the app.** If the app computes "due today" in a timezone,
  the cron must fire in that same timezone, or items slip across the boundary.
- **`/bin/bash` explicitly.** Do not rely on the login shell.
- **Absolute everything.** Script path, working directory, every binary the
  script needs (via PATH inside the command). Cron's default environment is
  not yours.
- **One line per schedule.** A second slot (for example an afternoon catch-up)
  is its own complete line, not an edit of the first.

## Diagnosing "it did not run"

In order:

1. **The cron journal** (`journalctl` or syslog around the fire time): did the
   scheduler even dispatch? Other jobs firing at the same minute proves the
   daemon is alive and the dispatch failed for this entry alone.
2. **The job's own log**: did it start and die, or never start?
3. **The lock**: an empty lock file with an old timestamp and no live holder
   is a leftover from the last finished run. It is evidence, not a cause.
4. **The environment**: a bare relative command with a missing PATH is the
   classic silent non-starter.

## The dry-run proof protocol

Never claim a schedule is fixed without cron firing the proof:

1. Save the current crontab and its SHA-256.
2. Add a temporary line that runs the job in dry-run mode every minute
   (the job must have a dry-run mode that changes nothing).
3. Wait for the journal to show the dispatch and the job's log to show the
   dry run.
4. Remove the temporary line.
5. Re-hash the crontab and compare byte-for-byte with the saved hash.

## Batching and catch-up

- Catch-up runs process the oldest slipped items first, under a hard cap.
- Each item is an independent child run: own work order, own gates, own
  completion marker. A failed item is retried tomorrow; it does not block or
  taint the others.
- An item that is already built and waiting for its publisher is left alone:
  it is done from the build side, and rebuilding it fakes activity.
- The cap is a ceiling. When the queue is empty, the run logs an empty day and
  exits zero. Nothing is manufactured.
