"""Check the tutorial code. Run with:  python scripts/test_code.py

Two checks:

1. Every step file in code/ runs without a screen, once as a plain run and once
   with rain forced onto the player so the game-over code runs too.
2. Every code block in the tutorials that names a step file (file=... in the
   block's first line) matches that file exactly, so the pages can't drift
   away from the tested code.

Screenshots of the game-over runs are saved to scripts/shots/.
"""
import os
import pathlib
import random
import re
import runpy
import shutil
import sys
import tempfile
import threading
import time

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "public" / "downloads" / "rain-dodge"
SHOTS = ROOT / "scripts" / "shots"
DOCS = ROOT / "src" / "content" / "docs"
STEPS = sorted((ROOT / "code").glob("*/step*.py"))


def run(step, force_hits, keys):
    """Run one step file in a temp folder. Returns the frames it drew."""
    workdir = tempfile.mkdtemp()
    for name in ("bg.png", "ship.png"):
        shutil.copy(ASSETS / name, workdir)
    os.chdir(workdir)

    real_randint = random.randint
    if force_hits:
        # Spawn a drop every frame, straight above the player's start position.
        random.randint = lambda a, b: 0 if b == 100 else 420

    frames = []
    real_update = pygame.display.update

    def update(*args):
        real_update(*args)
        frames.append(pygame.display.get_surface().copy())
        del frames[:-600]

    pygame.display.update = update
    real_delay = pygame.time.delay
    pygame.time.delay = lambda ms: real_delay(min(ms, 50))

    done = threading.Event()

    def driver():
        # done.wait returns True as soon as the step has finished on its own.
        if done.wait(4.0 if force_hits else 1.2):
            return
        for key in keys:
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=key))
            if done.wait(0.5):
                return
        while not done.wait(0.5):
            try:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            except pygame.error:
                return

    thread = threading.Thread(target=driver, daemon=True)
    thread.start()
    try:
        runpy.run_path(str(step), run_name="__main__")
    finally:
        done.set()
        thread.join()
        random.randint = real_randint
        pygame.display.update = real_update
        pygame.time.delay = real_delay
        os.chdir(ROOT)
    return frames, pathlib.Path(workdir)


def check_steps():
    SHOTS.mkdir(exist_ok=True)
    failed = False
    for step in STEPS:
        label = f"{step.parent.name}/{step.name}"
        restartable = "while main()" in step.read_text()
        for force_hits in (False, True):
            keys = [pygame.K_r] if restartable and force_hits else []
            try:
                frames, workdir = run(step, force_hits, keys)
                if not frames:
                    raise RuntimeError("nothing was drawn")
                if force_hits:
                    name = f"{step.parent.name}-{step.stem}"
                    pygame.image.save(frames[-1], SHOTS / f"{name}-end.png")
                    pygame.image.save(frames[len(frames) // 3], SHOTS / f"{name}-mid.png")
                    if "save_best" in step.read_text() and not (workdir / "best.txt").exists():
                        raise RuntimeError("best.txt was not written")
                print(f"ok    {label}  ({'forced hits' if force_hits else 'plain run'})")
            except Exception as error:  # report and keep going
                failed = True
                print(f"FAIL  {label}: {type(error).__name__}: {error}")
    return failed


def check_pages():
    """Each ```python file=<folder>/<step>.py startLineNumber=N block must match the file."""
    failed = False
    fence = re.compile(r"^```python([^\n]*)\n(.*?)^```", re.S | re.M)
    for page in sorted(DOCS.rglob("*.md*")):
        for meta, body in fence.findall(page.read_text(encoding="utf-8")):
            source = re.search(r"file=(\S+)", meta)
            if not source:
                continue
            start = int((re.search(r"startLineNumber=(\d+)", meta) or [0, 1])[1])
            lines = (ROOT / "code" / source[1]).read_text().splitlines()
            shown = body.rstrip("\n").split("\n")
            if lines[start - 1 : start - 1 + len(shown)] != shown:
                failed = True
                print(f"FAIL  {page.name}: block from {source[1]} line {start} doesn't match the file")
            else:
                print(f"ok    {page.name}: {source[1]} lines {start} to {start + len(shown) - 1}")
    return failed


sys.exit(1 if check_steps() | check_pages() else 0)
