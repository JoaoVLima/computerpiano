import math
import itertools
from collections import OrderedDict
import numpy as np
import pyaudio
# import pygame
import librosa
import json

with open('config.json') as config:
    config = json.loads(config.read())

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

NOTES = librosa.midi_to_note(range(12, 131+1), unicode=False)
# ['C0',  'C♯0',  'D0',   'D♯0',  'E0',   'F0',   'F♯0',  'G0',   'G♯0',  'A0',
#  'A♯0', 'B0',   'C1',   'C♯1',  'D1',   'D♯1',  'E1',   'F1',   'F♯1',  'G1',
#  'G♯1', 'A1',   'A♯1',  'B1',   'C2',   'C♯2',  'D2',   'D♯2',  'E2',   'F2',
#  'F♯2', 'G2',   'G♯2',  'A2',   'A♯2',  'B2',   'C3',   'C♯3',  'D3',   'D♯3',
#  'E3',  'F3',   'F♯3',  'G3',   'G♯3',  'A3',   'A♯3',  'B3',   'C4',   'C♯4',
#  'D4',  'D♯4',  'E4',   'F4',   'F♯4',  'G4',   'G♯4',  'A4',   'A♯4',  'B4',
#  'C5',  'C♯5',  'D5',   'D♯5',  'E5',   'F5',   'F♯5',  'G5',   'G♯5',  'A5',
#  'A♯5', 'B5',   'C6',   'C♯6',  'D6',   'D♯6',  'E6',   'F6',   'F♯6',  'G6',
#  'G♯6', 'A6',   'A♯6',  'B6',   'C7',   'C♯7',  'D7',   'D♯7',  'E7',   'F7',
#  'F♯7', 'G7',   'G♯7',  'A7',   'A♯7',  'B7',   'C8',   'C♯8',  'D8',   'D♯8',
#  'E8',  'F8',   'F♯8',  'G8',   'G♯8',  'A8',   'A♯8',  'B8',   'C9',   'C♯9',
#  'D9',  'D♯9',  'E9',   'F9',   'F♯9',  'G9',   'G♯9',  'A9',   'A♯9',  'B9']


def list_notes(note_range):
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
        return librosa.midi_to_note(range(start_note, end_note + 1), unicode=False)
    return note_range


class ComputerPiano:
    def __init__(self, note_range='C0-B9'):
        self.note_range = note_range
        self.notes = {note: {'instrument': None, 'note': note} for note in list_notes(note_range)}

    def add_instrument(self, instrument_instance, note_range=None):
        # instrument_instance.note_range = 'B0-A4'
        # note_range = 'C0-A#3'
        if not note_range:
            note_range = instrument_instance.note_range

        list_of_notes_location = list_notes(note_range)
        for note_location, note_instrument in zip(list_of_notes_location, instrument_instance.notes.keys()):
            self.notes[note_location]['instrument'] = instrument_instance
            self.notes[note_location]['note'] = note_instrument

    def play(self, notes):
        if isinstance(notes, str):
            notes = [notes]

        notes_to_play = []

        for note in notes:
            instrument_instance = self.notes[note]['instrument']
            note_instrument = self.notes[note]['note']

            if not instrument_instance:
                continue

            note_to_play = instrument_instance.note_to_play(note_instrument)
            notes_to_play.append(note_to_play)


class Instrument:
    def __init__(self, name, note_range, octave_changer=True):
        self.name = name
        self.note_range = note_range
        self.notes = {note: None for note in list_notes(note_range)}
        self.octave_changer = octave_changer

    def note_to_play(self, note):
        return [self, note]


class Piano(Instrument):
    def __init__(self):
        super().__init__(name='Piano', note_range='C0-B9', octave_changer=True)


class Drums(Instrument):
    def __init__(self):
        super().__init__(name='Drums', note_range='B0-A4', octave_changer=False)


if __name__ == '__main__':
    computer_piano = ComputerPiano()
    computer_piano.add_instrument(Piano())
    computer_piano.add_instrument(Drums(), 'C0-A#3')
    computer_piano.play(['C0', 'B2', 'G3', 'A#4', 'D#5'])
    
