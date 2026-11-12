"""How scripts/test_code.py plays Brick Buster. Not part of the tutorial.

The game reads held keys, so the test replaces pygame.key.get_pressed with a
robot: either "left" (hold the left arrow, which misses every ball) or "track"
(follow the ball, hitting it with a different part of the paddle each time).

Clearing the wall takes a few thousand frames. To keep the test short and its
memory use small, a run can be fast-forwarded: for the first `skip` frames the
clock does not wait and the test is handed one shared blank picture instead of
a copy of the screen. Fast-forward also ends as soon as an end message is
drawn, so the end screen itself is always a real frame.
"""
import math

import pygame

WIN_TEXT = "You cleared the wall!"
LOSE_TEXT = "Out of lives!"


def robot(mode, skip, state):
    """Returns a patch function for one run. `state` collects what happened."""

    def patch():
        real_rect = pygame.Rect
        real_clock = pygame.time.Clock
        real_font = pygame.font.Font
        real_get_pressed = pygame.key.get_pressed
        real_get_surface = pygame.display.get_surface
        state.update(frames=0, skip=skip, hits=0, texts=[])
        rects = []
        blank = pygame.Surface((800, 600))

        class SpyRect(real_rect):
            def __init__(self, *args):
                super().__init__(*args)
                rects.append(self)

            def collidelist(self, others):
                result = super().collidelist(others)
                if result != -1:
                    state["hits"] += 1
                return result

        class FastClock:
            def __init__(self):
                self.real = real_clock()

            def tick(self, fps=0):
                state["frames"] += 1
                if state["frames"] > state["skip"]:
                    return self.real.tick(fps)
                return 0

        class SpyFont(real_font):
            def render(self, text, *args):
                state["texts"].append(text)
                if text in (WIN_TEXT, LOSE_TEXT):
                    state["skip"] = 0  # stop fast-forwarding
                return super().render(text, *args)

        class Blank:
            def copy(self):
                return blank

        def get_surface():
            if state["frames"] <= state["skip"]:
                return Blank()
            return real_get_surface()

        class Keys:
            def __init__(self, left, right):
                self.held = {pygame.K_LEFT: left, pygame.K_RIGHT: right}

            def __getitem__(self, key):
                return self.held.get(key, False)

        def newest(size):
            for rect in reversed(rects):
                if rect.size == size:
                    return rect
            return None

        def get_pressed():
            if mode == "left":
                return Keys(True, False)
            paddle = newest((120, 14))
            ball = newest((16, 16))
            if ball is None:
                return Keys(False, False)
            wobble = 45 * math.sin(state["frames"] / 50)
            target = ball.centerx + wobble
            return Keys(paddle.centerx > target + 10,
                        paddle.centerx < target - 10)

        pygame.Rect = SpyRect
        pygame.time.Clock = FastClock
        pygame.font.Font = SpyFont
        pygame.key.get_pressed = get_pressed
        pygame.display.get_surface = get_surface

        def undo():
            pygame.Rect = real_rect
            pygame.time.Clock = real_clock
            pygame.font.Font = real_font
            pygame.key.get_pressed = real_get_pressed
            pygame.display.get_surface = real_get_surface

        return undo

    return patch


def press_r(when):
    return (when, pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r))


def plays(step):
    source = step.read_text()
    runs = [{"name": "plain"}]

    left = {}
    runs.append({"name": "hold left", "seconds": 1.0,
                 "patch": robot("left", 0, left)})

    if "colliderect" in source:
        track = {}

        def check_track(workdir, frames):
            if "collidelist" in source and track["hits"] == 0:
                raise RuntimeError("the ball never hit a brick")

        runs.append({"name": "autoplay", "seconds": 2.0,
                     "patch": robot("track", 2600, track),
                     "check": check_track})

    if "end_screen" in source:
        win = {}

        def check_win(workdir, frames):
            if WIN_TEXT not in win["texts"]:
                raise RuntimeError("the robot never cleared the wall")

        runs.append({"name": "win", "seconds": 5.0,
                     "patch": robot("track", 10**9, win),
                     "check": check_win})

        lose = {}

        def check_lose(workdir, frames):
            texts = lose["texts"]
            if LOSE_TEXT not in texts:
                raise RuntimeError("three misses did not end the game")
            if "Lives: 3" not in texts[texts.index(LOSE_TEXT):]:
                raise RuntimeError("R did not start a new game")

        runs.append({"name": "lose and restart", "seconds": 3.5,
                     "patch": robot("left", 10**9, lose),
                     "events": [press_r(3.0)],
                     "check": check_lose})
    return runs
