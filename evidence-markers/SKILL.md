---
name: evidence-markers
description: Leave a re-checkable marker for every claimed run - a small file binding the claim to a content hash, gate results and a date, so a reviewer can verify it without re-running the job. Use when an agent's output is checked by someone who was not in the session.
---

# Evidence Markers

A claim without a marker is a rumor. When an agent (or a teammate) says "all
gates passed", the next question is always "show me" - and "show me" should be
a file on disk, not a rerun. A marker binds a claim to the exact bytes it was
true for.

## The rules

1. **Every finished unit writes a marker.** One small file per unit of work:
   the repo, the mode (new/update), the date, the gate results, the content
   hash, the approval id, and the public URL once known.
2. **Bind approvals to exact bytes.** An approval is valid for the tree hash
   it approved; any later byte change invalidates it. Hash the whole tree
   (sorted walk, path + content), not a directory mtime.
3. **Gate what will ship.** Run the gates on the packaged copy that would
   actually be published, not on an older staged tree. Packaging first, then
   lint/verify/scan, is the honest order.
4. **Fingerprint before and after.** Hash the tree before an agent runs and
   after. "Changed nothing" is a legitimate result - record it as such, never
   as a failure to hide, and never paper over with a filler edit.
5. **Grep your own output first.** The private-marker scan runs over the
   packaged tree, before publishing, by whoever built it.
6. **Markers are append-only truth.** A failed gate deletes the pending
   marker, never the record of the failure.

## What a marker holds

See `references/marker-formats.md` for the template. Minimum fields:

```
repo=, mode=new|update, date=, built_by=, gates=lint/verify/scan results,
tree_hash=, approval_id=, release=vX.Y.Z, public_url=, note=
```

## The one line

If a claim cannot be checked from a file, it was not work - it was narration.
