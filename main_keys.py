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


# Key to frequency mapping for a basic C-major scale
KEY_FREQUENCY_MAP = {
    pygame.K_q: librosa.note_to_hz('C4'),
    pygame.K_2: librosa.note_to_hz('C#4'),
    pygame.K_w: librosa.note_to_hz('D4'),
    pygame.K_3: librosa.note_to_hz('D#4'),
    pygame.K_e: librosa.note_to_hz('E4'),
    pygame.K_r: librosa.note_to_hz('F4'),
    pygame.K_5: librosa.note_to_hz('F#4'),
    pygame.K_t: librosa.note_to_hz('G4'),
    pygame.K_6: librosa.note_to_hz('G#4'),
    pygame.K_y: librosa.note_to_hz('A4'),
    pygame.K_7: librosa.note_to_hz('A#4'),
    pygame.K_u: librosa.note_to_hz('B4'),
    pygame.K_i: librosa.note_to_hz('C5'),
    pygame.K_9: librosa.note_to_hz('C#5'),
    pygame.K_o: librosa.note_to_hz('D5'),
    pygame.K_0: librosa.note_to_hz('D#5'),
    pygame.K_p: librosa.note_to_hz('E5'),
    pygame.K_z: librosa.note_to_hz('F5'),
    pygame.K_s: librosa.note_to_hz('F#5'),
    pygame.K_x: librosa.note_to_hz('G5'),
    pygame.K_d: librosa.note_to_hz('G#5'),
    pygame.K_c: librosa.note_to_hz('A5'),
    pygame.K_f: librosa.note_to_hz('A#5'),
    pygame.K_v: librosa.note_to_hz('B5'),
    pygame.K_b: librosa.note_to_hz('C6'),
    pygame.K_h: librosa.note_to_hz('C#6'),
    pygame.K_n: librosa.note_to_hz('D6'),
    pygame.K_j: librosa.note_to_hz('D#6'),
    pygame.K_m: librosa.note_to_hz('E6'),
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
    last_notes = {}
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
            if last_notes != notes_dict:
                last_notes = notes_dict.copy()
                print(len(notes_dict), notes_dict)
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
