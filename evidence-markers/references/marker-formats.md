# Marker formats

A marker is one small file per finished unit of work. It is written only when
every gate passed, and it is the single thing a reviewer needs to trust - or
disprove - the claim.

## The publish marker (one per built item)

```
repo=<name>
mode=new|update
date=<YYYY-MM-DD>
built_by=<tool and models that ran, no secrets>
source=calendar|cadence
additions=<ids touched, if any>
release_build=yes|no
privacy=GREEN|AMBER
privacy_proof=yes|no|n/a
lint=PASS|FAIL
verify=PASS|FAIL
package=PASS|FAIL
scan=CLEAN|HITS
tree_hash=<sha256 of the exact tree>
approval_id=<id, bound to the tree hash>
release=vX.Y.Z
public_url=<url, once known>
note=<one line: what this item was>
```

Rules of use:

- Written **only** after every gate passed. A failed gate removes the pending
  marker instead.
- `tree_hash` is a full-tree fingerprint: sorted walk, every file's relative
  path plus its bytes, hashed together. One changed byte, new hash, invalid
  approval.
- `privacy_proof=no` with `privacy=AMBER` means "do not publish this" - the
  marker itself carries the refusal.
- The publisher collects every marker it finds and publishes each one; the
  marker is the work order for the publish step.

## The tree fingerprint

```python
import hashlib, os
EXCL = {".git", "__pycache__", ".pytest_cache", ".venv", "node_modules"}
h = hashlib.sha256()
for dirpath, dirnames, filenames in os.walk(root):
    dirnames[:] = sorted(d for d in dirnames if d not in EXCL)
    for fn in sorted(filenames):
        rel = os.path.relpath(os.path.join(dirpath, fn), root)
        h.update(rel.encode()); h.update(b"\0")
        h.update(open(os.path.join(dirpath, fn), "rb").read())
print(h.hexdigest())
```

Take the fingerprint before the agent starts and after it stops. Equal hashes
with a "built nothing" note is an honest empty day; equal hashes with a "done"
claim is a fake.

## The run log line

Between markers, the append-only log carries the narrative - one line per
event, timestamped, never rewritten:

```
2026-11-26 10:04:11 === daily run 2026-11-26 (mode=real) ===
2026-11-26 10:04:12 -- 1. plan: nothing real to do today
2026-11-26 10:04:12 === daily run 2026-11-26 end: no work items ===
```

An empty day logs its emptiness. The log is how a missed Tuesday is proved to
have been missed - and how the fix is proved to work.
