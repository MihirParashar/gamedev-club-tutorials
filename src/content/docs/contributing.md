---
title: Fix or add a tutorial
description: How club members correct a mistake, add a missing error to a checkpoint, or write a new tutorial.
---

This site is a folder of text files on GitHub. Anyone in the club can suggest a change. You need a free GitHub account. You don't need Git or any other software installed.

## Fix something on a page

1. Scroll to the bottom of the page and click **Edit page**. The first time, GitHub asks you to fork the repository, which means making your own copy to edit. Click the green button. The file then opens in an editor in your browser.
2. Make your change. The text is Markdown, which is plain text with a few symbols: `##` starts a heading and backticks go around `code`.
3. Click **Commit changes**, write one line saying what you changed, and click **Propose changes**.
4. On the next page, click **Create pull request**. A pull request is how GitHub sends your change to the club for review.
5. A board member reads it. If it's right, they merge it and the site updates a couple of minutes later.

The most useful fix is a missing error. If you hit an error that a checkpoint didn't list, and you worked out how to solve it, add a row to that checkpoint's table:

```md
| `NameOfTheError` | What caused it and what to do. |
```

## Write a new tutorial

Talk to a board member first, so two people don't write the same one.

Every tutorial follows the same shape. Open an existing one, such as Rain Dodge, with **Edit page** to see how each part is written.

1. **The top of the file** sets the title, a one-sentence description, its number in the list, roughly how long it takes, which tutorial comes first, and what the reader needs to know.
2. **A screenshot** of what the reader will have at the end.
3. **Numbered steps.** Each one explains an idea, shows the code, and says where the code goes.
4. **A checkpoint after every step.** Say exactly what the reader should see when they run it, then list the errors people hit and the fix for each.
5. **The finished code**, so a stuck reader can compare.

A checkpoint is written like this:

```md
:::tip[Checkpoint 1]
Run it. You should see a window that stays open until you click the X.

| If you see | Do this |
| --- | --- |
| `FileNotFoundError` | The image isn't next to main.py. |
:::
```

Before you ask for a review:

- Run every piece of code you show, at every step and not only at the end. Put the code for each step in the `code` folder so it can be tested.
- Watch someone else follow the tutorial. The errors they hit go into the checkpoints.
- Take the screenshots from your own run.

## For whoever maintains the site

The repository's README explains how to preview the site on your own computer, how the code tests work, and how to add a page to the menu.
