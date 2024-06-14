import math
import itertools
from collections import OrderedDict
import numpy as np
import pyaudio
# import pygame
import librosa
import json

# midinote = index+12
# 12-23 octave 0
# 24-35 octave 1
# 36-47 octave 2
# 48-47 octave 3
# 60-71 octave 4
# 72-83 octave 5
# 84-95 octave 6
# 96-107 octave 7
# 108-119 octave 8
# 120-131 octave 9
NOTES = librosa.midi_to_note(range(12, 132))

OCTAVE = 4
FIRST_NOTE = 12 * OCTAVE

with open('config.json') as config:
    config = json.loads(config.read())


def main():
    while True:
        input()


class ComputerPiano:
    def __init__(self, notes='C0-B9'):
        self.notes = self.list_of_keys(notes)
        self.instruments = []

    def list_of_notes(self, notes):
        # notes = 'C0'
        # notes = 'C0-B9'
        # notes = ['C0','C1']
        # return = ['C0','C1']
        if isinstance(notes, str):
            if '-' not in notes:
                return np.array([notes])
            start, end = notes.split('-', 2)
            start_note = librosa.note_to_midi(start)
            end_note = librosa.note_to_midi(end)
            return librosa.midi_to_note(range(start_note, end_note+1))
        return notes


class Instrument:
    def __init__(self, name, note_range, octave_changer=True):
        self.name = name
        self.note_range = note_range
        self.octave_changer = octave_changer


if __name__ == '__main__':
    a = ComputerPiano()
    print(a.notes)
