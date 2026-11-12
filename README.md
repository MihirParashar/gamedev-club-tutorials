# IMSA Game Dev Club tutorials

The club's tutorial site: eight lessons that take a new member from installing Python, through five small games, to a game of their own. Each game teaches a few new skills (the game loop, mouse and sound, bouncing, gravity and levels, classes), and the last lesson is a starter template and a way to plan a game small enough to finish. Members read it to catch up on their own, and members write it, so what the club knows stays after each class graduates.

This file is for whoever maintains the site. If you only want to fix a typo or add an error to a checkpoint, you don't need any of this: use the **Edit page** link at the bottom of the page on the site.

- `SPEC.md` says what v1 of the site is and who it's for.

## How the site is put together

It's built with [Astro Starlight](https://starlight.astro.build/), a documentation site generator. Pages are Markdown files. There is very little custom code on purpose.

| Path | What it is |
| --- | --- |
| `src/content/docs/` | The pages. One file per tutorial. `index.mdx` is the homepage. |
| `src/assets/` | Screenshots and diagrams used in the pages. |
| `public/downloads/` | Files readers download, such as the Rain Dodge images. |
| `code/` | The tutorial code, saved as it should look after each step. These files are tested. |
| `scripts/test_code.py` | Runs every step file and checks the pages match them. |
| `src/styles/custom.css` | Colors, fonts and the checkpoint style. |
| `src/components/` | Three small components: the page title block, the homepage top section and the homepage tutorial list. |
| `astro.config.mjs` | Site name, the menu, and the GitHub address. |
| `.github/workflows/deploy.yml` | Tests the code and publishes the site whenever `main` changes. |

## Preview the site on your computer

You need [Node.js](https://nodejs.org/) 22 or newer.

```sh
npm install
npm run dev
```

Open http://localhost:4321. The page reloads when you save a file.

If code blocks ever show up as plain unstyled text after you change `astro.config.mjs`, stop the server, delete the `.astro` folder and start again.

## Test the tutorial code

You need Python 3.10 or newer and pygame-ce (`python -m pip install pygame-ce`).

```sh
python scripts/test_code.py
```

Add a folder name to test one game: `python scripts/test_code.py pop`.

It does two things:

1. Runs every file in `code/` without opening a window. Each game folder has a `play.py` that tells the test how to play that game (which keys to press, where to click, how to force a win or a loss), so the code that only runs when something happens gets run too. The comment at the top of `scripts/test_code.py` explains the format.
2. Checks that every code block in a tutorial that names a step file (`file=rain-dodge/step2.py` on the block's first line) is an exact copy of those lines in that file.

The second check is what stops a page and its tested code from drifting apart. If you change code in a tutorial, change the step file to match, and the other way round.

## Add a tutorial

1. Write the code first, one file per step, in a new folder under `code/`. Add a `play.py` next to them (copy one from another game) so the test can play it. Run the tests.
2. Copy an existing tutorial in `src/content/docs/` and replace its content. The block at the top sets:
   - `title` and `description` (the description appears under the title and on the homepage)
   - `number` (its place in the homepage list)
   - `time` (for example `About 45 minutes`)
   - `first` (the file name, without `.md`, of the tutorial to do before this one)
   - `needs` (what the reader should already know)
   - `teaches` (the new skills, as a short list; shown on the page and on the homepage)
3. Add it to the menu: one line in the `sidebar` list in `astro.config.mjs`.
4. Numbered tutorials appear on the homepage automatically. If the new one teaches something a member might want in their own game, add a row to the table in `src/content/docs/your-own-game.md`.
5. Have someone who hasn't seen it follow it on a real club laptop. Add every error they hit to the checkpoints.

### Conventions the tutorials follow

- **Checkpoints** are written as `:::tip[Checkpoint 1]` ... `:::`. Say what the reader should see, then give a table of errors and fixes.
- **Code blocks that add to earlier code** use `showLineNumbers startLineNumber=14` so the numbers match the reader's file, `ins={...}` for new lines (green, marked +) and `mark={...}` for changed lines (gold, marked ~). The numbers inside the braces count from the top of the block, not the file.
- **Links between pages are relative**: `../setup/`, not `/setup/`. That keeps them working wherever the site is hosted.
- **Commands** are given for both Windows (`py`) and Mac (`python3`).
- Install instructions say `pygame-ce`, never `pygame`. As of November 2026, `pygame` has no ready-made build for Python 3.14 or 3.15 and fails to install on them.

## Publishing

Every change merged into `main` is tested, built and published by GitHub Actions. One-time setup: in the repository's **Settings > Pages**, set **Source** to **GitHub Actions**.

If the repository moves (for example into a club organization), change the `repo` line at the top of `astro.config.mjs`. Nothing else needs to change.

## Credits

Rain Dodge is inspired by Tech With Tim's Python game development tutorial. The Rain Dodge background and ship images come from the club's first lesson. The sound effects are generated by the `scripts/make_*_sounds.py` scripts.
