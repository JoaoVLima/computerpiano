import math
import itertools
import numpy as np
import pyaudio
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window

# Constants
BUFFER_SIZE = 256
SAMPLE_RATE = 44100
NOTE_AMP = 0.1

# Key to frequency mapping for a basic C-major scale
KEY_FREQUENCY_MAP = {
    97: 261.63,  # 'a' key -> C4
    115: 293.66, # 's' key -> D4
    100: 329.63, # 'd' key -> E4
    102: 349.23, # 'f' key -> F4
    103: 392.00, # 'g' key -> G4
    104: 440.00, # 'h' key -> A4
    106: 493.88, # 'j' key -> B4
    107: 523.25, # 'k' key -> C5
}

# Helper functions
def get_sin_oscillator(freq=55, amp=1, sample_rate=SAMPLE_RATE):
    increment = (2 * math.pi * freq) / sample_rate
    return (
        math.sin(v) * amp * NOTE_AMP for v in itertools.count(start=0, step=increment)
    )

def get_samples(notes_dict, num_samples=BUFFER_SIZE):
    samples = [0] * num_samples
    for note, osc in notes_dict.items():
        for i in range(num_samples):
            samples[i] += next(osc)
    return [int(sample * 32767) for sample in samples]

# Initialize PyAudio
p = pyaudio.PyAudio()

notes_dict = {}

class SynthWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_key_up=self.on_key_up)

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        if key in KEY_FREQUENCY_MAP and key not in notes_dict:
            freq = KEY_FREQUENCY_MAP[key]
            notes_dict[key] = get_sin_oscillator(freq=freq, amp=1)

    def on_key_up(self, window, key, scancode):
        if key in KEY_FREQUENCY_MAP and key in notes_dict:
            del notes_dict[key]

class SynthApp(App):
    def build(self):
        return SynthWidget()

if __name__ == "__main__":
    SynthApp().run()
