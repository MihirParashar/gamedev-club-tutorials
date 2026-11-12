"""Make the two sound effects for the Pop tutorial.

Run with:  python scripts/make_pop_sounds.py

Writes pop.wav and miss.wav into public/downloads/pop/. Both are 22050 Hz,
mono, 16-bit, and shorter than 0.2 seconds. Only the standard library is used,
so anyone can change the numbers below and make their own sounds.
"""
import math
import pathlib
import struct
import wave

RATE = 22050
OUT = pathlib.Path(__file__).resolve().parent.parent / "public" / "downloads" / "pop"


def make(seconds, start_hz, end_hz, decay, volume, harmonics):
    """A tone that slides from start_hz to end_hz and dies away.

    harmonics is a list of (multiple, strength) pairs. (1, 1.0) alone is a
    pure tone. Adding (2, 0.3) mixes in a quieter tone at twice the pitch,
    which helps low sounds come through on small laptop speakers.
    """
    count = int(RATE * seconds)
    fade_in = int(RATE * 0.004)
    fade_out = int(RATE * 0.025)
    total = sum(strength for _, strength in harmonics)
    samples = []
    phase = 0.0
    for i in range(count):
        t = i / RATE
        hz = start_hz + (end_hz - start_hz) * (i / count)
        phase += 2 * math.pi * hz / RATE
        value = 0.0
        for multiple, strength in harmonics:
            value += strength * math.sin(phase * multiple)
        value = value / total * math.exp(-decay * t)
        # Fades at both ends, so the speaker never jumps and makes a click.
        value *= min(1.0, i / fade_in, (count - 1 - i) / fade_out)
        samples.append(int(value * volume * 32767))
    return samples


def save(name, samples):
    OUT.mkdir(parents=True, exist_ok=True)
    with wave.open(str(OUT / name), "wb") as file:
        file.setnchannels(1)
        file.setsampwidth(2)
        file.setframerate(RATE)
        file.writeframes(struct.pack(f"<{len(samples)}h", *samples))
    print(f"{name}: {len(samples) / RATE:.3f} s")


# A quick rising blip.
save("pop.wav", make(0.11, 440, 990, 22, 0.6, [(1, 1.0), (2, 0.15)]))
# A lower, flatter thud that falls in pitch.
save("miss.wav", make(0.16, 220, 150, 14, 0.5, [(1, 1.0), (2, 0.35), (3, 0.15)]))
