---
name: release-bar-shipping
description: A per-item checklist that turns real work into small, publishable repos - passing tests, a README whose quickstart output is real and dated, packaged metadata and privacy grading. Use when shipping a new repo, a version bump, or deciding a release must move instead of ship.
---

# Release Bar Shipping

A release is a bar, not a mood. Either the item meets every line of the bar
today, or it moves to the next free slot - it is never rushed to hold a date.
The bar exists because a stranger decides in one minute whether a repo is
worth their trust, and every line of the bar is aimed at that minute.

## The bar (every item, every time)

- **Real code with tests that pass.** A playbook or template ships a worked
  example instead of tests. "Real" means it ran on your machine, today.
- **README with:** a bold one-line hook; badges; Problem; Install; Quickstart
  whose output is pasted from a real run with the date it ran; How it works;
  a "Use it with AI agents" section with the tool's real exit codes; Limits;
  About. If the quickstart cannot be replayed, it is decoration.
- **SKILL.md** with frontmatter `name` (the repo name) and a 1-3 sentence
  `description` that says when to use it.
- **Licence** (MIT for code, CC-BY-4.0 for prose), **CHANGELOG.md**, and CI on
  the oldest and newest Python you claim to support.
- **Packaging:** a sharp one-line `description`, 8-20 keywords that are valid
  GitHub topics, classifiers, project URLs (Homepage and Issues), readme,
  license, authors, version.

## The cadence rules

- Two to three releases a week; never two big ones in one week.
- A release that is not ready on its day **moves**; the calendar serves the
  work, not the reverse.
- An update to an existing repo is a version bump: one real change, one
  changelog line, one patch or minor number - not a re-announcement.
- Grade privacy before writing: GREEN goes through the normal gates; AMBER is
  rewritten fresh as a generic version plus a written privacy proof, or it
  does not ship at all.

The full per-item checklist with the privacy grading: `references/release-bar.md`.

## The one line

Ship the bar, or move the date - a rushed release costs more than a moved one.
