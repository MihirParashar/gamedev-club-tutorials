"""How scripts/test_code.py plays Coin Climb. Not part of the tutorial.

The game reads held keys, which posted events can't reach, so the "route"
play replaces pygame.key.get_pressed with a fixed list of keys for each frame.
ROUTE collects every coin in the tutorial's level, which proves the level can
be finished with the tutorial's jump height. While the route is running the
clock doesn't wait, so 427 frames take a fraction of a second.
"""
import pathlib

import pygame

SHOTS = pathlib.Path(__file__).resolve().parents[2] / "scripts" / "shots"

# (keys held, number of frames). R and L are the arrow keys, J is space.
ROUTE = [
    ("", 10), ("R", 13), ("RJ", 1), ("R", 31), ("RJ", 1), ("R", 39),
    ("RJ", 1), ("R", 29), ("L", 16), ("LJ", 1), ("L", 39), ("LJ", 1),
    ("L", 39), ("R", 18), ("RJ", 1), ("R", 39), ("RJ", 1), ("R", 54),
    ("", 28), ("L", 65),
]
NAMES = {"L": pygame.K_LEFT, "R": pygame.K_RIGHT, "J": pygame.K_SPACE}
FRAMES = []
for held, count in ROUTE:
    FRAMES.extend([held] * count)

# Frames worth keeping as screenshots, by step file name.
KEEP = {
    "step3.py": [45],
    "step4.py": [3, 20],
    "step5.py": [30, 150],
    "step6.py": [30, 150, 230, 300],
}
texts = []  # everything the game has drawn as text, in order


def follow_route():
    state = {"frame": 0}
    real_clock = pygame.time.Clock
    real_ticks = pygame.time.get_ticks
    real_pressed = pygame.key.get_pressed
    real_font = pygame.font.Font
    del texts[:]

    class Clock:
        def __init__(self):
            self.real = real_clock()

        def tick(self, fps=0):
            state["frame"] += 1
            if state["frame"] <= len(FRAMES):
                return 0
            return self.real.tick(fps)

    class Keys:
        def __getitem__(self, key):
            index = state["frame"] - 1
            if index >= len(FRAMES):
                return False
            for letter in FRAMES[index]:
                if NAMES[letter] == key:
                    return True
            return False

    class Font:
        def __init__(self, *args):
            self.real = real_font(*args)

        def render(self, text, *args):
            texts.append(text)
            return self.real.render(text, *args)

    pygame.time.Clock = Clock
    pygame.time.get_ticks = lambda: state["frame"] * 1000 // 60
    pygame.key.get_pressed = lambda: Keys()
    pygame.font.Font = Font

    def undo():
        pygame.time.Clock = real_clock
        pygame.time.get_ticks = real_ticks
        pygame.key.get_pressed = real_pressed
        pygame.font.Font = real_font

    return undo


def plays(step):
    source = step.read_text()
    if "def move_x" not in source:
        return [{"name": "plain"}]

    def keep_frames(workdir, frames):
        for index in KEEP.get(step.name, []):
            name = f"coin-climb-{step.stem}-frame{index}.png"
            pygame.image.save(frames[index], SHOTS / name)

    route = {"name": "route", "seconds": 1.5, "patch": follow_route,
             "check": keep_frames}
    if "def win_screen" not in source:
        return [{"name": "plain"}, route]

    def check_win(workdir, frames):
        keep_frames(workdir, frames)
        if not any(text.startswith("Every coin in") for text in texts):
            raise RuntimeError("the route did not reach the win screen")
        if "Coins left: 1" not in " ".join(texts):
            raise RuntimeError("the coin counter never showed 1 left")

    def check_restart(workdir, frames):
        joined = " ".join(texts)
        after_win = joined[joined.index("Every coin in"):]
        if "Coins left: 8" not in after_win:
            raise RuntimeError("R on the win screen did not start a new game")

    route["check"] = check_win
    again = {
        "name": "play again", "seconds": 2.0, "patch": follow_route,
        "events": [(1.2, pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r))],
        "check": check_restart,
    }
    return [{"name": "plain"}, route, again]
