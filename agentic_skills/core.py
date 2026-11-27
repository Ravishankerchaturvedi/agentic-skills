"""Check a library of agent skills.

A skill library is a tree of folders; each skill is a folder with a SKILL.md
(plain Markdown with YAML frontmatter) and an optional references/ directory.
The rules this checker enforces are the ones this library itself lives by:

- every SKILL.md starts with frontmatter carrying `name` and `description`;
- `name` equals the folder the skill lives in (for the library's root SKILL.md,
  it equals the project name in pyproject.toml, or the root folder name when
  there is no pyproject);
- `description` is non-empty, at least 40 characters, and at most 3 sentences;
- the body under the frontmatter is not empty;
- every `references/...` file the SKILL.md mentions exists on disk;
- no private-data marker (home paths, private IP ranges, token shapes) appears
  in any Markdown file of the library.

Directories named `examples` are skipped during a library-wide walk: they hold
intentionally broken fixtures. Point the checker at such a directory directly
to check it (that is the failing quickstart command).

Exit codes: 0 = pass, 1 = problems found, 2 = bad input.
"""

import json
import os
import re
from pathlib import Path

# Dirs never walked: VCS internals, caches, and intentionally broken fixtures.
SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", ".pytest_cache",
             "node_modules", ".mypy_cache", ".ruff_cache", "build", "dist"}
FIXTURE_DIR = "examples"

# Private-marker patterns: (compiled regex, human label). These are defaults;
# a library can add more with --banned-file. The matched text is never printed.
DEFAULT_BANNED = [
    (r"/home/", "absolute Unix home path"),
    (r"C:\\Users", "absolute Windows home path"),
    (r"192\.168\.", "private IPv4 address"),
    (r"10\.0\.", "private IPv4 address"),
    (r"172\.1[6-9]\.", "private IPv4 address"),
    (r"172\.2[0-9]\.", "private IPv4 address"),
    (r"172\.3[01]\.", "private IPv4 address"),
    (r"100\.(6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.", "CGNAT IPv4 address"),
    (r"AKIA[A-Z0-9]{16}", "AWS access key id"),
    (r"ghp_[A-Za-z0-9]{30,}", "GitHub token"),
    (r"github_pat_[A-Za-z0-9_]{20,}", "GitHub fine-grained token"),
    (r"sk-[A-Za-z0-9_-]{40,}", "API key"),
    (r"xox[baprs]-[A-Za-z0-9-]{10,}", "Slack token"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "private key block"),
]

REFERENCE_RE = re.compile(r"`(references/[^`\s]+)`")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
NAME_LINE_RE = re.compile(r'^\s*name\s*=\s*["\']([^"\']+)["\']\s*', re.M)
MIN_DESC_CHARS = 40
MAX_DESC_SENTENCES = 3


def parse_frontmatter(text):
    """Return (fields, body, error). Fields come from simple `key: value` lines."""
    if not text.lstrip().startswith("---"):
        return {}, "", "SKILL.md does not start with YAML frontmatter"
    rest = text.lstrip()[3:]
    end = rest.find("\n---")
    if end == -1:
        return {}, "", "SKILL.md frontmatter is not closed"
    fm = rest[:end]
    body = rest[end + 4:].lstrip("\n")
    fields = {}
    for line in fm.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields, body, None


def _md_files(root):
    """All .md files under root, pruning SKIP_DIRS and fixture dirs."""
    root = root.resolve()
    for dirpath, dirnames, filenames in os.walk(root):
        here = Path(dirpath)
        keep = []
        for d in sorted(dirnames):
            p = here / d
            if d in SKIP_DIRS:
                continue
            # Prune fixture dirs that sit below the walk root; when the root
            # itself lives inside one, the checker was pointed at the
            # fixtures directly and must walk them.
            if d == FIXTURE_DIR and root in p.parents:
                continue
            keep.append(d)
        dirnames[:] = keep
        for fn in sorted(filenames):
            if fn.endswith(".md"):
                yield here / fn


def _pyproject_name(root):
    """Best-effort project.name from pyproject.toml (no TOML writer needed)."""
    p = root / "pyproject.toml"
    if not p.is_file():
        return None
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    in_project = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("["):
            in_project = stripped == "[project]"
            continue
        if in_project:
            m = NAME_LINE_RE.match(line)
            if m:
                return m.group(1)
    return None


def _load_banned(banned_file):
    """Extra private-marker patterns, one regex per line (# starts a comment)."""
    patterns = []
    for raw in Path(banned_file).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            patterns.append((line, "banned pattern from %s" % Path(banned_file).name))
    return patterns


def _check_one_skill(path, root, project_name):
    """All structural checks for one SKILL.md. Returns a list of problems."""
    problems = []
    rel = path.relative_to(root).as_posix()
    folder = path.parent.name
    is_root_skill = path.parent == root
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return [{"code": "UNREADABLE", "file": rel, "message": "cannot read: %s" % e}]

    fields, body, err = parse_frontmatter(text)
    if err:
        return [{"code": "SKILL_BAD_FRONTMATTER", "file": rel, "message": err}]

    name = fields.get("name", "")
    if not name:
        problems.append({"code": "SKILL_NO_NAME", "file": rel,
                         "message": "frontmatter has no name"})
    elif is_root_skill:
        expected = project_name or root.name
        if name != expected:
            problems.append({"code": "SKILL_NAME_MISMATCH", "file": rel,
                             "message": "frontmatter name %r does not match the "
                                        "library name %r" % (name, expected)})
    elif name != folder:
        problems.append({"code": "SKILL_NAME_MISMATCH", "file": rel,
                         "message": "frontmatter name %r does not match folder %r"
                                    % (name, folder)})

    desc = fields.get("description", "")
    if not desc:
        problems.append({"code": "SKILL_NO_DESCRIPTION", "file": rel,
                         "message": "frontmatter has no description"})
    else:
        if len(desc) < MIN_DESC_CHARS:
            problems.append({"code": "SKILL_DESC_TOO_SHORT", "file": rel,
                             "message": "description is %d characters (minimum %d); "
                                        "say when to use the skill"
                                        % (len(desc), MIN_DESC_CHARS)})
        sentences = [s for s in SENTENCE_SPLIT_RE.split(desc.strip()) if s]
        if len(sentences) > MAX_DESC_SENTENCES:
            problems.append({"code": "SKILL_DESC_TOO_LONG", "file": rel,
                             "message": "description is %d sentences (maximum %d)"
                                        % (len(sentences), MAX_DESC_SENTENCES)})

    if not body.strip():
        problems.append({"code": "SKILL_EMPTY_BODY", "file": rel,
                         "message": "no content under the frontmatter"})

    for ref in REFERENCE_RE.findall(text):
        # A wildcard mention (`references/*.md`) documents the convention; it
        # is not a pointer to a specific file.
        if "*" in ref:
            continue
        if not (path.parent / ref).is_file():
            problems.append({"code": "SKILL_MISSING_REFERENCE", "file": rel,
                             "message": "mentions %r but that file does not exist" % ref})
    return problems


def _private_markers(root, banned_extra):
    """Scan every Markdown file for private-data markers. Never echoes matches."""
    patterns = [(re.compile(p), label) for p, label in DEFAULT_BANNED + banned_extra]
    hits = []
    for path in _md_files(root):
        rel = path.relative_to(root).as_posix()
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines, 1):
            for rx, label in patterns:
                if rx.search(line):
                    hits.append({"code": "PRIVATE_MARKER", "file": rel, "line": i,
                                 "message": "line %d: %s (match redacted)" % (i, label)})
    return hits


def check_library(root, banned_file=None, no_private=False):
    """Check a whole library. Returns a report dict; problems empty means pass."""
    root = Path(root)
    if not root.is_dir():
        return {"ok": False, "code": "BAD_INPUT",
                "error": "not a directory: %s" % root}
    root = root.resolve()

    project_name = _pyproject_name(root)
    problems = []
    skills = 0
    for path in sorted(_md_files(root)):
        if path.name != "SKILL.md":
            continue
        skills += 1
        problems += _check_one_skill(path, root, project_name)

    if not no_private:
        extra = _load_banned(banned_file) if banned_file else []
        problems += _private_markers(root, extra)

    files = sorted({p["file"] for p in problems})
    return {"ok": not problems, "path": str(root), "skills_checked": skills,
            "problem_count": len(problems), "problems": problems, "files": files}


def report_text(report):
    """Human-readable report. Private matches are redacted by construction."""
    if report.get("code") == "BAD_INPUT":
        return "ERROR: %s" % report["error"]
    lines = []
    for p in report["problems"]:
        where = p["file"] + (":%d" % p["line"] if p.get("line") else "")
        lines.append("%s: %s: %s" % (where, p["code"], p["message"]))
    if report["ok"]:
        lines.append("%d skills checked, 0 problems" % report["skills_checked"])
    else:
        lines.append("%d problems in %d file(s)" % (report["problem_count"],
                                                    len(report["files"])))
    return "\n".join(lines)


def report_json(report):
    return json.dumps({"result": report}, indent=2)
