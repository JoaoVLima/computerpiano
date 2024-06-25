import math
import itertools
import numpy as np
import pyaudio
import librosa
import threading
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window

BUFFER_SIZE = 64
SAMPLE_RATE = 44100
NOTE_AMP = 0.1

KEY_FREQUENCY_MAP = {
    9: librosa.note_to_hz('B3'),
    113: librosa.note_to_hz('C4'),
    50: librosa.note_to_hz('C#4'),
    119: librosa.note_to_hz('D4'),
    51: librosa.note_to_hz('D#4'),
    101: librosa.note_to_hz('E4'),
    114: librosa.note_to_hz('F4'),
    53: librosa.note_to_hz('F#4'),
    116: librosa.note_to_hz('G4'),
    54: librosa.note_to_hz('G#4'),
    121: librosa.note_to_hz('A4'),
    55: librosa.note_to_hz('A#4'),
    117: librosa.note_to_hz('B4'),
    105: librosa.note_to_hz('C5'),
    57: librosa.note_to_hz('C#5'),
    111: librosa.note_to_hz('D5'),
    48: librosa.note_to_hz('D#5'),
    112: librosa.note_to_hz('E5'),
    122: librosa.note_to_hz('F5'),
    115: librosa.note_to_hz('F#5'),
    120: librosa.note_to_hz('G5'),
    100: librosa.note_to_hz('G#5'),
    99: librosa.note_to_hz('A5'),
    102: librosa.note_to_hz('A#5'),
    118: librosa.note_to_hz('B5'),
    98: librosa.note_to_hz('C6'),
    104: librosa.note_to_hz('C#6'),
    110: librosa.note_to_hz('D6'),
    106: librosa.note_to_hz('D#6'),
    109: librosa.note_to_hz('E6'),
    44: librosa.note_to_hz('F6'),
    108: librosa.note_to_hz('F#6'),
    46: librosa.note_to_hz('G6'),
    303: librosa.note_to_hz('G#6'),
    59: librosa.note_to_hz('A6'),
    304: librosa.note_to_hz('B6'),
}


def get_sin_oscillator(freq=55, amp=1, sample_rate=SAMPLE_RATE):
    increment = (2 * math.pi * freq) / sample_rate
    return (
        math.sin(v) * amp * NOTE_AMP for v in itertools.count(start=0, step=increment)
    )


def get_samples(notes_dict, num_samples=BUFFER_SIZE):
    return [
        sum([int(next(osc) * 32767) for _, osc in notes_dict.items()])
        for _ in range(num_samples)
    ]

class ThreadFunc:
    def __init__(self, notes_dict):
        self.run = True
        self.t1 = None
        self.notes_dict = notes_dict
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
                rate=SAMPLE_RATE,
                channels=1,
                format=pyaudio.paInt16,
                output=True,
                frames_per_buffer=BUFFER_SIZE,
        )

    def func(self):
        while self.run:
            if self.notes_dict:
                samples = get_samples(self.notes_dict)
                samples = np.int16(samples).tobytes()
                self.stream.write(samples)

    def go(self):
        self.t1 = threading.Thread(target=self.func)
        self.t1.start()

    def stop(self):
        self.run = False
        self.t1.stop()
        self.stream.close()
        self.audio.terminate()


class SynthWidget(Widget):
    def __init__(self, **kwargs):
        super(SynthWidget, self).__init__(**kwargs)
        self.notes_dict = {}
        self.last_notes = {}
        Window.bind(on_key_down=self.key_down_action)
        Window.bind(on_key_up=self.key_up_action)
        self.tf = ThreadFunc(self.notes_dict)
        self.tf.go()

    def key_down_action(self, window, key, scancode, codepoint, modifier):
        if key in KEY_FREQUENCY_MAP:
            freq = KEY_FREQUENCY_MAP[key]
            if key not in self.notes_dict:
                self.notes_dict[key] = get_sin_oscillator(freq=freq, amp=1)
                print(len(self.notes_dict), self.notes_dict)

    def key_up_action(self, window, key, scancode):
        if key in self.notes_dict:
            del self.notes_dict[key]
            print(len(self.notes_dict), self.notes_dict)

    def on_stop(self):
        self.tf.stop()


class MyApp(App):
    def build(self):
        return SynthWidget()


if __name__ == '__main__':
    try:
        MyApp().run()
    except KeyboardInterrupt:
        print("Stopping...")
