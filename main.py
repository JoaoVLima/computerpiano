import math
import itertools
from collections import OrderedDict
import numpy as np
import pyaudio
import pygame
import librosa

# Constants
BUFFER_SIZE = 256
SAMPLE_RATE = 44100
NOTE_AMP = 0.1

PITCHES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
OCTAVES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
OCTAVE = 4
NOTES = OrderedDict()
for pitch in PITCHES:
    for octave in OCTAVES:
        note = pitch + str(octave)
        NOTES[note] = {'freq': librosa.note_to_hz(note)}

# 0-11 octave 0
# 12-23 octave 1
# 24-35 octave 2

OCTAVE

KEYMAP = {
    'q': NOTES[0],
    '2',
    'w',
    '3',
    'e',
    'r',
    '5',
    't',
    '6',
    'y',
    '7',
    'u',
    'i',
    '9',
    'o',
    '0',
    'p',
    'z',
    's',
    'x',
    'd',
    'c',
    'f',
    'v',
    'b',
    'h',
    'n',
    'j',
    'm',
    ',',
    'l',
    '.',
    'ç',
    ';',
    '~',
    '/'
 }

KEYS = {
    ''
}
