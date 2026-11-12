"""Check the tutorial code. Run with:  python scripts/test_code.py

Two checks:

1. Every step file in code/ runs without a screen. Each game folder can have a
   play.py that says how to play it during the test (see below), so the parts
   of the game that need input or bad luck get run too.
2. Every code block in the tutorials that names a step file (file=... in the
   block's first line) matches that file exactly, so the pages can't drift
   away from the tested code.

Screenshots from every run are saved to scripts/shots/.

play.py (optional, one per folder in code/)
-------------------------------------------
    ASSETS = "rain-dodge"      # folder in public/downloads/ whose files the game
                               # loads. Defaults to the code folder's own name.

    def plays(step):           # step is the pathlib.Path of the step file
        return [
            {
                "name": "plain",      # used in output and screenshot names
                "seconds": 1.2,       # how long to let it run before closing it
                "events": [(0.5, pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r))],
                                      # (seconds from start, event to post)
                "patch": some_function,   # optional. Called before the run to
                                          # replace things (random, held keys,
                                          # mouse position). Must return a
                                          # function that undoes it.
                "check": some_function,   # optional. Called after the run with
                                          # (workdir, frames). Raise to fail.
                "shots": [0.25, 0.9],     # optional. Extra screenshots, as
                                          # fractions of the way through the run.
            },
        ]

Without a play.py, each step gets one plain 1.2 second run.
"""
import _thread
import importlib.util
import os
import pathlib
import re
import runpy
import shutil
import sys
import tempfile
import threading

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOWNLOADS = ROOT / "public" / "downloads"
SHOTS = ROOT / "scripts" / "shots"
DOCS = ROOT / "src" / "content" / "docs"
STEPS = sorted((ROOT / "code").glob("*/step*.py"))
ONLY = sys.argv[1] if len(sys.argv) > 1 else None  # e.g. "pop" to test one folder
MAX_FRAMES = 1500


def load_play(folder):
    path = folder / "play.py"
    if not path.exists():
        return None
    spec = importlib.util.spec_from_file_location(f"play_{folder.name}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(step, play, assets):
    """Run one step file in a temp folder. Returns the frames it drew."""
    workdir = pathlib.Path(tempfile.mkdtemp())
    if assets.is_dir():
        for file in assets.iterdir():
            shutil.copy(file, workdir)
    os.chdir(workdir)

    undo = play["patch"]() if play.get("patch") else None

    frames = []
    real_update, real_flip = pygame.display.update, pygame.display.flip

    def capture(real):
        def wrapped(*args):
            real(*args)
            frames.append(pygame.display.get_surface().copy())
            del frames[:-MAX_FRAMES]
        return wrapped

    pygame.display.update = capture(real_update)
    pygame.display.flip = capture(real_flip)
    real_delay, real_wait = pygame.time.delay, pygame.time.wait
    pygame.time.delay = lambda ms: real_delay(min(ms, 50))
    pygame.time.wait = lambda ms: real_wait(min(ms, 50))

    done = threading.Event()
    seconds = play.get("seconds", 1.2)

    def driver():
        elapsed = 0.0
        for when, event in sorted(play.get("events", []), key=lambda pair: pair[0]):
            # done.wait returns True as soon as the step has finished on its own.
            if done.wait(max(0.0, when - elapsed)):
                return
            elapsed = max(elapsed, when)
            try:
                pygame.event.post(event)
            except pygame.error:
                return
        if done.wait(max(0.0, seconds - elapsed)):
            return
        for _ in range(16):
            try:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            except pygame.error:
                return
            if done.wait(0.5):
                return
        _thread.interrupt_main()  # the game ignored 8 seconds of QUIT events

    thread = threading.Thread(target=driver, daemon=True)
    thread.start()
    try:
        runpy.run_path(str(step), run_name="__main__")
    except KeyboardInterrupt:
        raise RuntimeError("did not close when the window's X was clicked")
    finally:
        done.set()
        thread.join()
        pygame.display.update, pygame.display.flip = real_update, real_flip
        pygame.time.delay, pygame.time.wait = real_delay, real_wait
        if undo:
            undo()
        os.chdir(ROOT)
    return frames, workdir


def check_steps():
    SHOTS.mkdir(exist_ok=True)
    failed = False
    plays_for = {}
    for step in STEPS:
        folder = step.parent
        if ONLY and folder.name != ONLY:
            continue
        if folder not in plays_for:
            plays_for[folder] = load_play(folder)
        module = plays_for[folder]
        assets = DOWNLOADS / getattr(module, "ASSETS", folder.name)
        plays = module.plays(step) if module else [{"name": "plain"}]
        for play in plays:
            label = f"{folder.name}/{step.name}  ({play['name']})"
            try:
                frames, workdir = run(step, play, assets)
                if not frames:
                    raise RuntimeError("nothing was drawn")
                name = f"{folder.name}-{step.stem}-{play['name'].replace(' ', '-')}"
                pygame.image.save(frames[-1], SHOTS / f"{name}-end.png")
                pygame.image.save(frames[len(frames) // 3], SHOTS / f"{name}-mid.png")
                for fraction in play.get("shots", []):
                    index = min(len(frames) - 1, int(fraction * len(frames)))
                    pygame.image.save(frames[index], SHOTS / f"{name}-{int(fraction * 100):02d}.png")
                if play.get("check"):
                    play["check"](workdir, frames)
                print(f"ok    {label}")
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
            if ONLY and not source[1].startswith(ONLY + "/"):
                continue
            start = int((re.search(r"startLineNumber=(\d+)", meta) or [0, 1])[1])
            lines = (ROOT / "code" / source[1]).read_text(encoding="utf-8").splitlines()
            shown = body.rstrip("\n").split("\n")
            if lines[start - 1 : start - 1 + len(shown)] != shown:
                failed = True
                print(f"FAIL  {page.name}: block from {source[1]} line {start} doesn't match the file")
            else:
                print(f"ok    {page.name}: {source[1]} lines {start} to {start + len(shown) - 1}")
    return failed


sys.exit(1 if check_steps() | check_pages() else 0)
