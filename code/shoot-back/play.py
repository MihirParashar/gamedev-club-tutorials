"""How scripts/test_code.py plays Shoot Back. Not part of the tutorial.

Three plays:

- "pilot": an autopilot holds the arrow keys and presses Space. Held keys do
  not respond to posted events, so pygame.key.get_pressed is replaced. The
  autopilot finds the enemies by watching pygame.draw.polygon (each enemy is
  one polygon) and keeps its own copy of the ship's x position, which stays
  exact because it applies the same speed and edge checks as move_player.
  In the finished game it stops playing after a while, so the enemies get
  through, the game ends with a real score, and R restarts it.
- "overrun": nobody plays and enemies spawn often, so the code that removes
  enemies at the bottom (and later takes lives) runs.
- "plain": no input at all.

Sounds are counted, so the test can check that shots were fired and enemies
were hit.
"""
import pathlib
import random
import time

import pygame

SHIP_W = 66
SHIP_VEL = 7
SPACE = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
PRESS_R = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r)

played = {}
marks = {}  # "game over": index of the frame that shows the game-over text


class Held:
    """Stands in for the result of pygame.key.get_pressed()."""

    def __init__(self, keys):
        self.keys = keys

    def __getitem__(self, key):
        return key in self.keys


class CountingSound(pygame.mixer.Sound):
    def __init__(self, name):
        super().__init__(name)
        self.name = name

    def play(self):
        played[self.name] = played.get(self.name, 0) + 1
        return super().play()


def count_sounds():
    real_sound = pygame.mixer.Sound
    pygame.mixer.Sound = CountingSound
    played.clear()

    def undo():
        pygame.mixer.Sound = real_sound

    return undo


def pilot(stop_after):
    """Returns a patch function. The autopilot gives up after stop_after s."""

    def patch():
        undo_sounds = count_sounds()
        random.seed(7)
        real_pressed = pygame.key.get_pressed
        real_polygon = pygame.draw.polygon
        state = {"x": 400, "seen": [], "start": time.time()}
        state["calls"] = 0
        state["last"] = time.time()
        marks.clear()

        def polygon(surface, color, points, *args):
            top, bottom = points[0], points[2]
            state["seen"].append((top[0], bottom[1]))
            return real_polygon(surface, color, points, *args)

        def pressed():
            seen, state["seen"] = state["seen"], []
            now = time.time()
            if now - state["last"] > 1 and "game over" not in marks:
                # The game stopped asking for keys for a while: that was the
                # game-over screen, drawn straight after the last game frame.
                marks["game over"] = state["calls"]
            state["last"] = now
            state["calls"] += 1
            elapsed = now - state["start"]
            if elapsed > stop_after:
                return Held(set())
            if seen:
                # Chase the enemy closest to the bottom.
                target = max(seen, key=lambda enemy: enemy[1])[0]
            else:
                # Nothing to chase (early steps): sweep left, then right.
                target = 150 if int(elapsed) % 2 == 0 else 650
            keys = set()
            centre = state["x"] + SHIP_W // 2
            if target - centre <= -SHIP_VEL and state["x"] - SHIP_VEL >= 0:
                keys.add(pygame.K_LEFT)
                state["x"] -= SHIP_VEL
            elif (target - centre >= SHIP_VEL
                    and state["x"] + SHIP_W + SHIP_VEL <= 800):
                keys.add(pygame.K_RIGHT)
                state["x"] += SHIP_VEL
            if not seen or abs(target - centre) < 20:
                pygame.event.post(SPACE)
            return Held(keys)

        pygame.key.get_pressed = pressed
        pygame.draw.polygon = polygon

        def undo():
            pygame.key.get_pressed = real_pressed
            pygame.draw.polygon = real_polygon
            undo_sounds()

        return undo

    return patch


def overrun():
    """Spawn an enemy every 10th frame and never shoot."""
    undo_sounds = count_sounds()
    real_randint = random.randint
    calls = {"n": 0}

    def randint(a, b):
        if b == 100:
            calls["n"] += 1
            return 0 if calls["n"] % 10 == 0 else 100
        return real_randint(a, b)

    random.randint = randint

    def undo():
        random.randint = real_randint
        undo_sounds()

    return undo


def need_sound(name):
    def check(workdir, frames):
        if not played.get(name):
            raise RuntimeError(f"{name} was never played")

    return check


def save_game_over(workdir, frames):
    need_sound("hit.wav")(workdir, frames)
    if "game over" not in marks:
        raise RuntimeError("the game-over screen never appeared")
    shots = pathlib.Path(__file__).resolve().parent.parent.parent
    shots = shots / "scripts" / "shots"
    pygame.image.save(frames[marks["game over"]],
                      shots / "shoot-back-step5-pilot-gameover.png")


def plays(step):
    source = step.read_text()
    result = [{"name": "plain"}]
    piloted = {
        "name": "pilot",
        "seconds": 4.0,
        "patch": pilot(100),
        "shots": [0.5, 0.7, 0.9],
    }
    if "SHOOT.play()" in source:
        piloted["check"] = need_sound("shoot.wav")
    if "class Enemy" in source:
        piloted["seconds"] = 8.0
        result.append({
            "name": "overrun",
            "seconds": 6.0,
            "patch": overrun,
            "shots": [0.5, 0.8],
        })
    if "HIT.play()" in source:
        piloted["seconds"] = 12.0
        piloted["check"] = need_sound("hit.wav")
    if "while main()" in source:
        # Play well for 14 seconds, stop, lose, then press R and play on.
        piloted["patch"] = pilot(14)
        piloted["seconds"] = 30.0
        piloted["events"] = [(28.5, PRESS_R)]
        piloted["shots"] = [0.4, 0.55, 0.7, 0.8]
        piloted["check"] = save_game_over
        # Lose without firing, press R to restart, then lose again.
        result[-1]["seconds"] = 14.0
        result[-1]["events"] = [(9.0, PRESS_R)]
        result[-1]["shots"] = [0.3, 0.6, 0.75]
    result.append(piloted)
    return result
