# The release bar, line by line

The checklist as a fill-in list. Print it, walk it, and where a line cannot be
checked, the release moves - it does not ship with the line unchecked.

## Content

- [ ] One real change (or one new repo), not several split changes dressed up
      as activity.
- [ ] Tests exist and pass on the machine that built this (`pytest -q` output
      seen, not assumed).
- [ ] A playbook or template has a worked example that actually ran, in place
      of tests.
- [ ] No client names, no private paths, no prices, no real contacts anywhere
      in the tree. Self-contained and generic.

## README

- [ ] Starts with the repo name as a heading.
- [ ] Badges near the top (CI, Python versions, licence).
- [ ] A bold one-line hook that says what problem this kills.
- [ ] Problem - one paragraph, no marketing.
- [ ] Install - the exact commands.
- [ ] Quickstart - exact commands, then output pasted from a real run with the
      date it was run. Re-run it before publishing; if the output has drifted,
      re-paste it.
- [ ] How it works - honest mechanism, including what the tool does NOT do.
- [ ] "Use it with AI agents" - the real exit codes and how an agent should
      branch on them.
- [ ] Limits - where the tool stops being true.
- [ ] About - who built it and why.

## Metadata

- [ ] SKILL.md: frontmatter `name` = repo name; `description` is 1-3 sentences
      and says when to use it.
- [ ] LICENSE: MIT (CC-BY-4.0 for prose-only work).
- [ ] CHANGELOG.md: this release as a dated line; every previous version kept.
- [ ] CI: `.github/workflows/tests.yml` on the oldest and newest claimed
      Python (this house: 3.10 and 3.12).
- [ ] pyproject.toml: `description` sharp and under 350 characters; 8-20
      `keywords` that are valid GitHub topics (lowercase, digits, hyphens,
      max 50 chars); classifiers; `[project.urls]` with Homepage and Issues;
      `readme`, `license`, `authors`, `version`.
- [ ] Version bumped exactly one step from the last release, matching the
      changelog.

## Privacy grading (before writing, not after)

- **GREEN** - no private data anywhere near the source: normal gates only.
- **AMBER** - the source touches private material: write the release fresh as
  a generic version (never copy the private source), then write a privacy
  proof file listing every red flag found in the inventory and exactly how
  each was removed. No proof file, no publish, regardless of quality.
- Even GREEN gets a final grep of the packaged tree for banned strings - the
  build greps its own output before anyone else does.

## Cadence

- [ ] Two to three releases a week; never two big ones in one week.
- [ ] Not ready on its day? It moves to the next free slot. The date bends;
      the bar does not.
