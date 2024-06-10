import math
import itertools
import numpy as np
import pyaudio
import pygame
import librosa

# Constants
BUFFER_SIZE = 256
SAMPLE_RATE = 44100
NOTE_AMP = 0.1

LETTERS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NUMBERS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

for letter in LETTERS:
    for number in NUMBERS:
        print(librosa.note_to_hz(letter + str(number)))


def pythagorean_tempered_scale(a=A):
    ...


# Key to frequency mapping for a basic C-major scale
KEY_FREQUENCY_MAP = {
    pygame.K_a: 261.63,  # C4
    pygame.K_s: 293.66,  # D4
    pygame.K_d: 329.63,  # E4
    pygame.K_f: 349.23,  # F4
    pygame.K_g: 392.00,  # G4
    pygame.K_h: 440.00,  # A4
    pygame.K_j: 493.88,  # B4
    pygame.K_k: 523.25,  # C5
}


# Helper functions
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


# Initialize PyAudio and Pygame
p = pyaudio.PyAudio()
stream = p.open(
        rate=SAMPLE_RATE,
        channels=1,
        format=pyaudio.paInt16,
        output=True,
        frames_per_buffer=BUFFER_SIZE,
)

pygame.init()
screen = pygame.display.set_mode((200, 200))

# Run the synth
try:
    print("Starting...")
    notes_dict = {}
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key in KEY_FREQUENCY_MAP:
                freq = KEY_FREQUENCY_MAP[event.key]
                if event.key not in notes_dict:
                    notes_dict[event.key] = get_sin_oscillator(freq=freq, amp=1)
            elif event.type == pygame.KEYUP and event.key in KEY_FREQUENCY_MAP:
                if event.key in notes_dict:
                    del notes_dict[event.key]

        if notes_dict:
            # Play the notes
            samples = get_samples(notes_dict)
            samples = np.int16(samples).tobytes()
            stream.write(samples)

except KeyboardInterrupt as err:
    print("Stopping...")

finally:
    pygame.quit()
    stream.close()
    p.terminate()
