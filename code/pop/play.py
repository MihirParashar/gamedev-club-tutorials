"""How scripts/test_code.py plays Pop. Not part of the tutorial.

The game is played with the mouse, and the targets appear at random places,
so the test has to know where they are. It replaces random.randint with a
seeded copy that remembers the last place it handed out, and wraps
pygame.event.get so that every so often a click arrives on that place (a hit)
or in the top left corner (a miss).
"""
import random

import pygame


def player(hit_every, miss_every, speed=1):
    """Build a patch function.

    hit_every, miss_every: frames between clicks on the newest target and
    clicks on nothing. speed runs the game's clock faster: speed=5 makes a
    30 second round take 6 seconds.
    """

    def patch():
        rng = random.Random(7)
        real_randint = random.randint
        real_get = pygame.event.get
        real_ticks = pygame.time.get_ticks
        places = []
        calls = [0]

        def randint(a, b):
            value = rng.randint(a, b)
            if b != 100:  # a position, not the "spawn this frame?" roll
                places.append(value)
            return value

        def click(pos):
            return pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pos, button=1)

        def get(*args):
            events = real_get(*args)
            calls[0] += 1
            if calls[0] % hit_every == 0:
                if len(places) >= 2:
                    count = len(places) // 2 * 2
                    events.append(click((places[count - 2], places[count - 1])))
                else:
                    events.append(click((400, 300)))  # where step 2 starts
            if calls[0] % miss_every == 0:
                events.append(click((5, 5)))
                # The scroll wheel also sends MOUSEBUTTONDOWN. It must be ignored.
                wheel = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(5, 5), button=4)
                events.append(wheel)
            return events

        first = real_ticks()

        def ticks():
            return first + (real_ticks() - first) * speed

        random.randint = randint
        pygame.event.get = get
        pygame.time.get_ticks = ticks

        def undo():
            random.randint = real_randint
            pygame.event.get = real_get
            pygame.time.get_ticks = real_ticks

        return undo

    return patch


def plays(step):
    source = step.read_text()
    result = [
        {"name": "plain"},
        {
            "name": "clicks",
            "seconds": 6.0,
            "patch": player(hit_every=70, miss_every=200),
            "shots": [0.5, 0.7, 0.9],
        },
    ]
    if "game_over" in source:
        # Clock at double speed, to reach the busy second half of a round.
        result.append({
            "name": "late",
            "seconds": 9.0,
            "patch": player(hit_every=75, miss_every=170, speed=2),
            "shots": [0.5, 0.6, 0.7, 0.8, 0.9],
        })
        # A whole round in 6 seconds, then R, then a second whole round.
        result.append({
            "name": "fast round",
            "seconds": 14.0,
            "patch": player(hit_every=25, miss_every=110, speed=5),
            "events": [(7.0, pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r))],
        })
    return result
