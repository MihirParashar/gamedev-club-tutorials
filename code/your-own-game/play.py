"""How scripts/test_code.py plays the starter template. Not part of the tutorial."""
import random

import pygame


def key(k):
    return pygame.event.Event(pygame.KEYDOWN, key=k)


class HeldRight:
    """Stands in for pygame.key.get_pressed(): only the right arrow is down."""

    def __getitem__(self, k):
        return k == pygame.K_RIGHT


class FastClock:
    """A clock that never waits, so a 20 second round takes a moment."""

    def tick(self, fps=0):
        return 0


def demo():
    """Hold the right arrow, with coins placed along the way and one behind."""
    real_pressed, real_randint = pygame.key.get_pressed, random.randint
    xs = [520, 640, 180]
    calls = []

    def randint(a, b):
        if a == 60:  # the y coordinate of a coin
            return 310
        calls.append(1)
        return xs[min(len(calls), len(xs)) - 1]

    pygame.key.get_pressed = HeldRight
    random.randint = randint

    def undo():
        pygame.key.get_pressed, random.randint = real_pressed, real_randint

    return undo


def fast():
    """Run the round at full speed. The first 7 coins land on the player."""
    real_clock, real_randint = pygame.time.Clock, random.randint
    calls = []

    def randint(a, b):
        calls.append(1)
        return (a + b) // 2 if len(calls) <= 14 else a

    pygame.time.Clock = FastClock
    random.randint = randint

    def undo():
        pygame.time.Clock, random.randint = real_clock, real_randint

    return undo


def plays(step):
    source = step.read_text()
    space = (0.4, key(pygame.K_SPACE))
    result = [
        {"name": "title", "seconds": 0.8},
        {"name": "demo", "seconds": 2.2, "events": [space], "patch": demo},
    ]
    if "game_over_screen" in source:
        result.append({"name": "round", "seconds": 2.0, "events": [space], "patch": fast})
        result.append(
            {
                "name": "again",
                "seconds": 3.0,
                "events": [space, (1.5, key(pygame.K_r)), (2.0, key(pygame.K_SPACE))],
                "patch": fast,
            }
        )
    if "paused" in source:
        pause = [space, (1.0, key(pygame.K_p)), (1.6, key(pygame.K_p))]
        result.append({"name": "pause", "seconds": 1.4, "events": pause[:2], "patch": demo})
        result.append({"name": "resume", "seconds": 2.2, "events": pause, "patch": demo})
    return result
