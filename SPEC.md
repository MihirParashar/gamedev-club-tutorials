# Game Dev Club Tutorial Site: v1 Spec

Status: **approved 2026-11-11.** Tutorials 1 to 3 are built; see README.md for how the site works.

## Audience

IMSA game dev club members. Assume the Python taught in the mandatory intro CS class and nothing beyond it. Some members code in their free time, but no tutorial may depend on that.

Machines: roughly 70% Windows, 30% Mac. Some members use school loaner laptops (Windows, not locked down, slow).

Main blocker today: setup, not concepts. At the first session several people could not install pygame (wheel errors), and the rest waited while leads debugged.

*Unverified:* Mihir was not at that session. He will ask whoever ran it (1) where people got stuck and (2) what finishers did next. Update this section when he hears back.

## Tools

Python and pygame only. Unity and Godot help stays in-person mentoring. Git is not required of members.

Decided during build (2026-11-11): install `pygame-ce`, not `pygame`. python.org now offers Python 3.15, and `pygame` 2.6.1 has ready-made builds only up to 3.13, which is the likely cause of the failed installs at the first meeting (not yet confirmed on a member laptop). `pygame-ce` 2.5.8 has builds for 3.10 through 3.15 on Windows and Mac, so no Python version needs pinning.

## Tutorials (one ordered "Start here" list)

| # | Tutorial | Source | First used |
|---|---|---|---|
| 1 | Set up Python and pygame | New. Pinned version, table of install errors and fixes | Meeting before Thanksgiving (by Nov 20) |
| 2 | Rain Dodge | Existing slide deck, converted | Already taught; page is for catch-up |
| 3 | Extend Rain Dodge: lives, restart, high score | Deck's challenge slide, with worked solutions | Meeting before Thanksgiving |
| 4 | Shoot Back: bullets, enemies, sound | New. Sprites and sound taught as the game needs them | First December meeting |
| 5 | Start your own game | New. Starter template with title and game-over screens | Second December meeting, run as a mini jam |

Rain Dodge keeps its credit to Tech With Tim's tutorial.

## Tutorial page template

Goal (what you will have at the end), estimated time, prerequisites, steps, common errors and fixes, finished code, next tutorial. After each step: a checkpoint that says "run it, you should see…" plus the errors likely at that step. This is the format the Rain Dodge deck already uses. Screenshots come from Mihir's test runs.

## Who does what

- **Writing:** Claude drafts all five and runs every code sample.
- **Testing:** Mihir follows each tutorial on a real machine before it is taught. One member with a Mac runs tutorial 1.
- **Contributing:** each page has an "Edit this page" link that opens GitHub's web editor and creates a pull request. Mihir reviews and merges.
- **Ownership:** Mihir, a club board member, owns the repo for now. *Open:* a named junior successor by end of January 2027.

## Stack

Astro Starlight, content as Markdown files, GitHub repo, GitHub Pages at the default address with deploy on merge. No custom domain. Custom code kept to a minimum.

## Done for v1

1. Five tutorials live at a public URL.
2. Site used at both December meetings (finals start Dec 14).
3. Each tutorial test-run by Mihir on a real machine.

Target dates: tutorials 1 to 3 live before the pre-Thanksgiving meeting, 4 before the first December meeting, 5 before the second.

## Metrics (counted by hand at meetings)

- Members with a working install after tutorial 1
- Members who finished Rain Dodge
- Members with a playable game of their own at the jam
- Members who contributed an edit

## Out of scope

Accounts, comments, progress tracking, any backend, engine tutorials, tracks, custom domain.

The in-browser Python runner gets a half-day test during build. It ships in v1 only if tutorial code runs in it without confusing changes and it is usable on a slow loaner. Otherwise it is deferred.

## Next phase

Design: mock up the homepage and one tutorial page (references: Godot docs, the Rust Book), following the club's "must not look vibecoded" design rules. Build starts after Mihir approves the mockups.
