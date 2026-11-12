"""Make the two Shoot Back sounds. Run with:

    python scripts/make_shoot-back_sounds.py

Writes shoot.wav and hit.wav into public/downloads/shoot-back/.
Standard library only. 22050 Hz, mono, 16-bit.
"""
import math
import pathlib
import struct
import wave

RATE = 22050
OUT = pathlib.Path(__file__).resolve().parent.parent
OUT = OUT / "public" / "downloads" / "shoot-back"


def sweep(seconds, start_hz, end_hz, volume, square):
    """A tone that slides from start_hz to end_hz and fades out."""
    samples = []
    phase = 0.0
    total = int(RATE * seconds)
    for i in range(total):
        t = i / total
        hz = start_hz + (end_hz - start_hz) * t
        phase += 2 * math.pi * hz / RATE
        value = math.sin(phase)
        if square:
            # Mix in a softened square wave for a rougher sound.
            value = 0.5 * value + 0.5 * math.copysign(1.0, value)
        fade = (1 - t) ** 2
        attack = min(1.0, i / 40)
        samples.append(int(32767 * volume * value * fade * attack))
    return samples


def save(name, samples):
    with wave.open(str(OUT / name), "wb") as file:
        file.setnchannels(1)
        file.setsampwidth(2)
        file.setframerate(RATE)
        file.writeframes(struct.pack(f"<{len(samples)}h", *samples))


OUT.mkdir(parents=True, exist_ok=True)
save("shoot.wav", sweep(0.12, 1200, 300, 0.35, False))
save("hit.wav", sweep(0.18, 320, 60, 0.5, True))
print("wrote shoot.wav and hit.wav to", OUT)
