"""How scripts/test_code.py plays Rain Dodge. Not part of the tutorial."""
import random

import pygame

ASSETS = "rain-dodge"


def force_hits():
    """Spawn a drop every frame, straight above the player's start position."""
    real_randint = random.randint
    random.randint = lambda a, b: 0 if b == 100 else 420

    def undo():
        random.randint = real_randint

    return undo


def plays(step):
    source = step.read_text()
    forced = {"name": "forced hits", "seconds": 4.0, "patch": force_hits}
    if "while main()" in source:
        # Lose, press R to restart, then lose again.
        forced["seconds"] = 4.5
        forced["events"] = [(4.0, pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r))]
    if "save_best" in source:

        def check(workdir, frames):
            if not (workdir / "best.txt").exists():
                raise RuntimeError("best.txt was not written")

        forced["check"] = check
    return [{"name": "plain"}, forced]
