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
        self.notes = {note: None for note in self.list_of_notes(notes)}

    def list_of_notes(self, note_range):
        # notes = 'C0'
        # notes = 'C0-B9'
        # notes = ['C0','C1']
        # return = ['C0','C1']
        if isinstance(note_range, str):
            if '-' not in note_range:
                return np.array([note_range])
            start, end = note_range.split('-', 2)
            start_note = librosa.note_to_midi(start)
            end_note = librosa.note_to_midi(end)
            return librosa.midi_to_note(range(start_note, end_note+1))
        return note_range

    def add_instrument(self, instrument_instance):
        list_of_notes = self.list_of_notes(instrument_instance.note_range)
        for note in list_of_notes:
            self.notes[note] = instrument_instance


    def play(self, note):
        instrument = self.notes[note]
        instrument.play(note)


class Instrument:
    def __init__(self, name, note_range, octave_changer=True):
        self.name = name
        self.note_range = note_range
        self.octave_changer = octave_changer

    def play(self, notes):
        print(self.name)
        if isinstance(notes, str):
            notes = [notes]
        print(notes)


class Piano(Instrument):
    def __init__(self):
        super().__init__(name='Piano', note_range='C1-B2', octave_changer=True)


if __name__ == '__main__':
    computer_piano = ComputerPiano()
    piano = Piano()
    computer_piano.add_instrument(piano)
    computer_piano.play('C1')
