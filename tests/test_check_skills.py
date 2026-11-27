"""Tests for the agentic-skills checker."""

import json

import pytest

from agentic_skills import cli, core

GOOD_DESC = ("Check skill files before they ship: frontmatter, names, "
             "descriptions and private-data markers. Use before publishing "
             "a skill library.")


def write_skill(folder, name=None, description=GOOD_DESC, body=None, skill_dirname=None):
    """Create a skill folder with a SKILL.md; returns the SKILL.md path."""
    d = folder / (skill_dirname or name)
    d.mkdir(parents=True)
    fm = ["---"]
    if name is not None:
        fm.append("name: %s" % name)
    if description is not None:
        fm.append("description: %s" % description)
    fm.append("---")
    (d / "SKILL.md").write_text("\n".join(fm) + "\n\n" + (body or "# Title\n\nWords.\n"),
                                encoding="utf-8")
    return d / "SKILL.md"


def make_library(root, project_name="test-lib"):
    """A minimal library that must pass: root skill, one skill, one reference."""
    (root / "pyproject.toml").write_text(
        '[project]\nname = "%s"\n' % project_name, encoding="utf-8")
    (root / "SKILL.md").write_text(
        "---\nname: %s\ndescription: %s\n---\n\n# test-lib\n\nBody.\n"
        % (project_name, GOOD_DESC), encoding="utf-8")
    write_skill(root, name="alpha", body="# Alpha\n\nSee `references/deep.md`.\n")
    (root / "alpha" / "references").mkdir()
    (root / "alpha" / "references" / "deep.md").write_text("Deep dive.\n", encoding="utf-8")


def codes(problems):
    return sorted(p["code"] for p in problems)


# ------------------------------------------------------------------ happy path

def test_good_library_passes(tmp_path):
    make_library(tmp_path)
    report = core.check_library(tmp_path)
    assert report["ok"], core.report_text(report)
    assert report["skills_checked"] == 2  # root skill + alpha


def test_root_name_may_come_from_pyproject(tmp_path):
    make_library(tmp_path, project_name="other-name")
    (tmp_path / "SKILL.md").write_text(
        "---\nname: other-name\ndescription: %s\n---\n\n# x\n\nBody.\n"
        % GOOD_DESC, encoding="utf-8")
    assert core.check_library(tmp_path)["ok"]


# ------------------------------------------------------------------ frontmatter

def test_name_mismatch_flagged(tmp_path):
    make_library(tmp_path)
    write_skill(tmp_path, name="beta", skill_dirname="gamma")
    report = core.check_library(tmp_path)
    assert not report["ok"]
    assert "SKILL_NAME_MISMATCH" in codes(report["problems"])


def test_root_skill_name_mismatch_flagged(tmp_path):
    make_library(tmp_path)
    (tmp_path / "SKILL.md").write_text(
        "---\nname: wrong\ndescription: %s\n---\n\n# x\n\nBody.\n"
        % GOOD_DESC, encoding="utf-8")
    report = core.check_library(tmp_path)
    assert "SKILL_NAME_MISMATCH" in codes(report["problems"])


def test_missing_name_flagged(tmp_path):
    make_library(tmp_path)
    write_skill(tmp_path, name=None, skill_dirname="beta")
    report = core.check_library(tmp_path)
    assert "SKILL_NO_NAME" in codes(report["problems"])


def test_missing_description_flagged(tmp_path):
    make_library(tmp_path)
    write_skill(tmp_path, name="beta", description=None)
    report = core.check_library(tmp_path)
    assert "SKILL_NO_DESCRIPTION" in codes(report["problems"])


def test_short_description_flagged(tmp_path):
    make_library(tmp_path)
    write_skill(tmp_path, name="beta", description="Just a skill.")
    report = core.check_library(tmp_path)
    assert "SKILL_DESC_TOO_SHORT" in codes(report["problems"])


def test_four_sentence_description_flagged(tmp_path):
    make_library(tmp_path)
    long_desc = ("One. Two. Three. Four.")
    write_skill(tmp_path, name="beta", description=long_desc)
    report = core.check_library(tmp_path)
    assert "SKILL_DESC_TOO_LONG" in codes(report["problems"])


def test_empty_body_flagged(tmp_path):
    make_library(tmp_path)
    write_skill(tmp_path, name="beta", body="\n")
    report = core.check_library(tmp_path)
    assert "SKILL_EMPTY_BODY" in codes(report["problems"])


def test_missing_reference_file_flagged(tmp_path):
    make_library(tmp_path)
    write_skill(tmp_path, name="beta", body="# Beta\n\nSee `references/nope.md`.\n")
    report = core.check_library(tmp_path)
    assert "SKILL_MISSING_REFERENCE" in codes(report["problems"])


def test_wildcard_reference_mention_allowed(tmp_path):
    make_library(tmp_path)
    write_skill(tmp_path, name="beta", body="# Beta\n\nPull `references/*.md` when needed.\n")
    assert core.check_library(tmp_path)["ok"]


def test_missing_frontmatter_flagged(tmp_path):
    make_library(tmp_path)
    d = tmp_path / "beta"
    d.mkdir()
    (d / "SKILL.md").write_text("# no frontmatter\n", encoding="utf-8")
    report = core.check_library(tmp_path)
    assert "SKILL_BAD_FRONTMATTER" in codes(report["problems"])


# ------------------------------------------------------------------ private scan

def test_private_marker_in_markdown_flagged(tmp_path):
    make_library(tmp_path)
    (tmp_path / "notes.md").write_text(
        "call me at /home/devuser/notes.md\n", encoding="utf-8")
    report = core.check_library(tmp_path)
    assert "PRIVATE_MARKER" in codes(report["problems"])
    # the match itself is never echoed
    assert "/home/devuser" not in core.report_text(report)


def test_no_private_flag_skips_scan(tmp_path):
    make_library(tmp_path)
    (tmp_path / "notes.md").write_text(
        "call me at /home/devuser/notes.md\n", encoding="utf-8")
    report = core.check_library(tmp_path, no_private=True)
    assert report["ok"], core.report_text(report)


def test_banned_file_extends_patterns(tmp_path):
    make_library(tmp_path)
    (tmp_path / "notes.md").write_text("project alpha-internal-42\n", encoding="utf-8")
    banned = tmp_path / "banned.txt"
    banned.write_text("# one regex per line\nalpha-internal-\\d+\n", encoding="utf-8")
    report = core.check_library(tmp_path, banned_file=str(banned))
    assert "PRIVATE_MARKER" in codes(report["problems"])


def test_examples_dir_skipped_in_library_check(tmp_path):
    make_library(tmp_path)
    bad = tmp_path / "examples" / "broken"
    write_skill(bad, name="right", skill_dirname="wrong")
    report = core.check_library(tmp_path)
    assert report["ok"], core.report_text(report)
    # ...but pointing the checker at the fixtures directly checks them
    direct = core.check_library(bad)
    assert not direct["ok"]


# ------------------------------------------------------------------ cli

def run_cli(argv):
    return cli.main(["check"] + [str(a) for a in argv])


def test_cli_exit_codes(tmp_path):
    make_library(tmp_path)
    assert run_cli([tmp_path]) == 0

    write_skill(tmp_path, name="beta", skill_dirname="gamma")
    assert run_cli([tmp_path]) == 1

    assert run_cli([tmp_path / "no-such-dir"]) == 2


def test_cli_json_output(tmp_path, capsys):
    make_library(tmp_path)
    write_skill(tmp_path, name="beta", skill_dirname="gamma")
    assert run_cli([tmp_path, "--json"]) == 1
    payload = json.loads(capsys.readouterr().out)["result"]
    assert payload["ok"] is False
    assert payload["problem_count"] >= 1
    assert "SKILL_NAME_MISMATCH" in codes(payload["problems"])


def test_cli_json_output_pass(tmp_path, capsys):
    make_library(tmp_path)
    assert run_cli([tmp_path, "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)["result"]
    assert payload["ok"] is True
    assert payload["skills_checked"] == 2


def test_missing_path_is_bad_input(tmp_path):
    assert run_cli([tmp_path / "missing"]) == 2


def test_default_path_is_cwd(tmp_path, monkeypatch):
    make_library(tmp_path)
    monkeypatch.chdir(tmp_path)
    assert cli.main(["check"]) == 0


@pytest.mark.parametrize("text,label", [
    ("token AKIAIOSFODNN7EXAMPLE here", "AWS access key id"),
    ("paste ghp_" + "a" * 36, "GitHub token"),
    ("key sk-" + "x" * 45, "API key"),
])
def test_token_shapes_flagged(tmp_path, text, label):
    make_library(tmp_path)
    (tmp_path / "leak.md").write_text(text + "\n", encoding="utf-8")
    report = core.check_library(tmp_path)
    assert any(p["code"] == "PRIVATE_MARKER" and label in p["message"]
               for p in report["problems"]), core.report_text(report)
