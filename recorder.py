import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write


def list_input_devices():
    devices = sd.query_devices()
    input_devices = []

    print("Available input devices:")
    for i, dev in enumerate(devices):
        if dev["max_input_channels"] > 0:
            print(f"{i}: {dev['name']}")
            input_devices.append(i)

    return input_devices


def record_audio(filename="input.wav", duration=5, fs=16000, device=None):
    print(f"Recording for {duration} seconds... Speak now.")

    audio = sd.rec(
        int(duration * fs),
        samplerate=fs,
        channels=1,
        dtype="int16",
        device=device
    )
    sd.wait()

    peak = np.abs(audio).max()
    print(f"Audio peak level: {peak}")

    if peak == 0:
        print("Warning: recorded audio is completely silent.")

    write(filename, fs, audio)
    print(f"Saved audio to {filename}")