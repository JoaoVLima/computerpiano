import math
import itertools
from collections import OrderedDict
import numpy as np
import pyaudio
import pygame
import librosa
import json

BUFFER_SIZE = 128
SAMPLE_RATE = 44100

PITCHES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
OCTAVES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
FREQUENCIES = []
for octave in OCTAVES:
    for pitch in PITCHES:
        note = pitch + str(octave)
        FREQUENCIES.append(librosa.note_to_hz(note))

# 0-11 octave 0
# 12-23 octave 1
# 24-35 octave 2
# 36-47 octave 3
# 48-47 octave 4
# 60-71 octave 5
# 72-83 octave 6
# 84-95 octave 7
# 96-107 octave 8
# 108-119 octave 9

OCTAVE = 4
FIRST_NOTE = 12 * OCTAVE


with open('config.json') as config:
    config = json.loads(config.read())

keys = (config['keys'])

class Instrument:
    def __init__(self, name):
        self.name = name

