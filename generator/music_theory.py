"""
Music Theory Core for Piano Learning Helpers
Provides mathematically verified interval formulas, note spelling,
enharmonics, tactile key shape detection, and fingerings.
"""

# Natural notes semitone distance from C
NOTE_TO_SEMITONE = {
    'C': 0, 'B#': 0, 'Dbb': 0,
    'C#': 1, 'Db': 1,
    'D': 2, 'C##': 2, 'Ebb': 2,
    'D#': 3, 'Eb': 3,
    'E': 4, 'Fb': 4, 'D##': 4,
    'F': 5, 'E#': 5, 'Gbb': 5,
    'F#': 6, 'Gb': 6,
    'G': 7, 'F##': 7, 'Abb': 7,
    'G#': 8, 'Ab': 8,
    'A': 9, 'G##': 9, 'Bbb': 9,
    'A#': 10, 'Bb': 10,
    'B': 11, 'Cb': 11, 'A##': 11
}

# Standard 12 chromatic root keys for display
ROOT_KEYS = [
    ("C", 0), ("Db", 1), ("D", 2), ("Eb", 3), ("E", 4), ("F", 5),
    ("Gb", 6), ("G", 7), ("Ab", 8), ("A", 9), ("Bb", 10), ("B", 11)
]

# Physical key classification (0=C is White, 1=C# is Black, etc.)
IS_BLACK_KEY_MAP = [False, True, False, True, False, False, True, False, True, False, True, False]

def is_black_semitone(semitone):
    return IS_BLACK_KEY_MAP[semitone % 12]

NOTE_NAMES_FROM_C = [
    "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B",
    "C", "C#", "D", "D#", "E", "F", "F#", "G"
]

# Standard enharmonic spelling dictionary: (root_name, semitone_offset) -> note_spelling
NOTE_SPELLINGS = {
    "C":  ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "F#"],
    "Db": ["Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G"],
    "D":  ["D", "D#", "E", "F", "F#", "G", "G#", "A", "Bb", "B", "C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#"],
    "Eb": ["Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A"],
    "E":  ["E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#"],
    "F":  ["F", "F#", "G", "Ab", "A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"],
    "Gb": ["Gb", "G", "Ab", "A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B", "C"],
    "G":  ["G", "G#", "A", "Bb", "B", "C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B", "C", "C#"],
    "Ab": ["Ab", "A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B", "C", "Db", "D"],
    "A":  ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "Bb", "B", "C", "C#", "D", "D#"],
    "Bb": ["Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B", "C", "Db", "D", "Eb", "E"],
    "B":  ["B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E", "F"]
}

def get_note_name(root_name, offset):
    """Returns standard musician-friendly note spelling for an interval offset."""
    arr = NOTE_SPELLINGS.get(root_name)
    if arr and offset < len(arr):
        return arr[offset]
    # Fallback to chromatic from C
    chromatic = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
    root_st = NOTE_TO_SEMITONE.get(root_name, 0)
    return chromatic[(root_st + offset) % 12]

# Chord Definitions
CHORD_DEFINITIONS = {
    "maj": {
        "title": "MAJOR CHORDS",
        "suffix": "maj",
        "formula_text": "1 — 3 — 5",
        "formula_desc": "Root • Major 3rd • Perfect 5th",
        "intervals_text": "[4 + 3]",
        "semitones": [0, 4, 7, 12, 16],
        "degree_names": ["Root", "3rd", "5th", "Octave", "Oct 3rd"],
        "rh_inversions": [
            ("ROOT", "1 • 3 • 5", {0: "1", 4: "3", 7: "5"}),
            ("1ST INV", "1 • 2 • 5", {4: "1", 7: "2", 12: "5"}),
            ("2ND INV", "1 • 3 • 5", {7: "1", 12: "3", 16: "5"}),
        ],
        "lh_inversions": [
            ("ROOT", "5 • 3 • 1", {0: "5", 4: "3", 7: "1"}),
            ("1ST INV", "5 • 3 • 1", {4: "5", 7: "3", 12: "1"}),
            ("2ND INV", "5 • 2 • 1", {7: "5", 12: "2", 16: "1"}),
        ]
    },
    "min": {
        "title": "MINOR CHORDS",
        "suffix": "min",
        "formula_text": "1 — ♭3 — 5",
        "formula_desc": "Root • Minor 3rd • Perfect 5th",
        "intervals_text": "[3 + 4]",
        "semitones": [0, 3, 7, 12, 15],
        "degree_names": ["Root", "♭3rd", "5th", "Octave", "Oct ♭3"],
        "rh_inversions": [
            ("ROOT", "1 • 3 • 5", {0: "1", 3: "3", 7: "5"}),
            ("1ST INV", "1 • 2 • 5", {3: "1", 7: "2", 12: "5"}),
            ("2ND INV", "1 • 3 • 5", {7: "1", 12: "3", 15: "5"}),
        ],
        "lh_inversions": [
            ("ROOT", "5 • 3 • 1", {0: "5", 3: "3", 7: "1"}),
            ("1ST INV", "5 • 3 • 1", {3: "5", 7: "3", 12: "1"}),
            ("2ND INV", "5 • 2 • 1", {7: "5", 12: "2", 15: "1"}),
        ]
    },
    "dim": {
        "title": "DIMINISHED CHORDS",
        "suffix": "dim",
        "formula_text": "1 — ♭3 — ♭5",
        "formula_desc": "Root • Minor 3rd • Diminished 5th",
        "intervals_text": "[3 + 3]",
        "semitones": [0, 3, 6, 12, 15],
        "degree_names": ["Root", "♭3rd", "♭5th", "Octave", "Oct ♭3"],
        "rh_inversions": [
            ("ROOT", "1 • 3 • 5", {0: "1", 3: "3", 6: "5"}),
            ("1ST INV", "1 • 2 • 5", {3: "1", 6: "2", 12: "5"}),
            ("2ND INV", "1 • 3 • 5", {6: "1", 12: "3", 15: "5"}),
        ],
        "lh_inversions": [
            ("ROOT", "5 • 3 • 1", {0: "5", 3: "3", 6: "1"}),
            ("1ST INV", "5 • 3 • 1", {3: "5", 6: "3", 12: "1"}),
            ("2ND INV", "5 • 2 • 1", {6: "5", 12: "2", 15: "1"}),
        ]
    },
    "aug": {
        "title": "AUGMENTED CHORDS",
        "suffix": "aug",
        "formula_text": "1 — 3 — ♯5",
        "formula_desc": "Root • Major 3rd • Augmented 5th",
        "intervals_text": "[4 + 4]",
        "semitones": [0, 4, 8, 12, 16],
        "degree_names": ["Root", "3rd", "♯5th", "Octave", "Oct 3rd"],
        "rh_inversions": [
            ("ROOT", "1 • 3 • 5", {0: "1", 4: "3", 8: "5"}),
            ("1ST INV", "1 • 2 • 5", {4: "1", 8: "2", 12: "5"}),
            ("2ND INV", "1 • 3 • 5", {8: "1", 12: "3", 16: "5"}),
        ],
        "lh_inversions": [
            ("ROOT", "5 • 3 • 1", {0: "5", 4: "3", 8: "1"}),
            ("1ST INV", "5 • 3 • 1", {4: "5", 8: "3", 12: "1"}),
            ("2ND INV", "5 • 2 • 1", {8: "5", 12: "2", 16: "1"}),
        ]
    },
    "sus2": {
        "title": "SUSPENDED 2nd CHORDS",
        "suffix": "sus2",
        "formula_text": "1 — 2 — 5",
        "formula_desc": "Root • Major 2nd • Perfect 5th",
        "intervals_text": "[2 + 5]",
        "semitones": [0, 2, 7, 12, 14],
        "degree_names": ["Root", "2nd", "5th", "Octave", "Oct 2nd"],
        "rh_inversions": [
            ("ROOT", "1 • 2 • 5", {0: "1", 2: "2", 7: "5"}),
            ("1ST INV", "1 • 3 • 5", {2: "1", 7: "3", 12: "5"}),
            ("2ND INV", "1 • 2 • 5", {7: "1", 12: "2", 14: "5"}),
        ],
        "lh_inversions": [
            ("ROOT", "5 • 4 • 1", {0: "5", 2: "4", 7: "1"}),
            ("1ST INV", "5 • 3 • 1", {2: "5", 7: "3", 12: "1"}),
            ("2ND INV", "5 • 4 • 1", {7: "5", 12: "4", 14: "1"}),
        ]
    },
    "sus4": {
        "title": "SUSPENDED 4th CHORDS",
        "suffix": "sus4",
        "formula_text": "1 — 4 — 5",
        "formula_desc": "Root • Perfect 4th • Perfect 5th",
        "intervals_text": "[5 + 2]",
        "semitones": [0, 5, 7, 12, 17],
        "degree_names": ["Root", "4th", "5th", "Octave", "Oct 4th"],
        "rh_inversions": [
            ("ROOT", "1 • 3 • 5", {0: "1", 5: "3", 7: "5"}),
            ("1ST INV", "1 • 2 • 5", {5: "1", 7: "2", 12: "5"}),
            ("2ND INV", "1 • 3 • 5", {7: "1", 12: "3", 17: "5"}),
        ],
        "lh_inversions": [
            ("ROOT", "5 • 2 • 1", {0: "5", 5: "2", 7: "1"}),
            ("1ST INV", "5 • 3 • 1", {5: "5", 7: "3", 12: "1"}),
            ("2ND INV", "5 • 2 • 1", {7: "5", 12: "2", 17: "1"}),
        ]
    },
    "dom7": {
        "title": "DOMINANT 7th CHORDS",
        "suffix": "7",
        "formula_text": "1 — 3 — 5 — ♭7",
        "formula_desc": "Root • Major 3rd • 5th • Minor 7th",
        "intervals_text": "[4 + 3 + 3]",
        "semitones": [0, 4, 7, 10, 12, 16],
        "degree_names": ["Root", "3rd", "5th", "♭7th", "Octave", "Oct 3rd"],
        "rh_inversions": [
            ("ROOT", "1 • 2 • 3 • 5", {0: "1", 4: "2", 7: "3", 10: "5"}),
            ("1ST INV", "1 • 2 • 4 • 5", {4: "1", 7: "2", 10: "4", 12: "5"}),
            ("2ND INV", "1 • 2 • 3 • 5", {7: "1", 10: "2", 12: "3", 16: "5"}),
        ],
        "lh_inversions": [
            ("ROOT", "5 • 3 • 2 • 1", {0: "5", 4: "3", 7: "2", 10: "1"}),
            ("1ST INV", "5 • 3 • 2 • 1", {4: "5", 7: "3", 10: "2", 12: "1"}),
            ("2ND INV", "5 • 4 • 2 • 1", {7: "5", 10: "4", 12: "2", 16: "1"}),
        ]
    },
    "maj7": {
        "title": "MAJOR 7th CHORDS",
        "suffix": "maj7",
        "formula_text": "1 — 3 — 5 — 7",
        "formula_desc": "Root • Major 3rd • 5th • Major 7th",
        "intervals_text": "[4 + 3 + 4]",
        "semitones": [0, 4, 7, 11, 12, 16],
        "degree_names": ["Root", "3rd", "5th", "7th", "Octave", "Oct 3rd"],
        "rh_inversions": [
            ("ROOT", "1 • 2 • 3 • 5", {0: "1", 4: "2", 7: "3", 11: "5"}),
            ("1ST INV", "1 • 2 • 4 • 5", {4: "1", 7: "2", 11: "4", 12: "5"}),
            ("2ND INV", "1 • 2 • 3 • 5", {7: "1", 11: "2", 12: "3", 16: "5"}),
        ],
        "lh_inversions": [
            ("ROOT", "5 • 3 • 2 • 1", {0: "5", 4: "3", 7: "2", 11: "1"}),
            ("1ST INV", "5 • 3 • 2 • 1", {4: "5", 7: "3", 11: "2", 12: "1"}),
            ("2ND INV", "5 • 4 • 2 • 1", {7: "5", 11: "4", 12: "2", 16: "1"}),
        ]
    },
    "min7": {
        "title": "MINOR 7th CHORDS",
        "suffix": "min7",
        "formula_text": "1 — ♭3 — 5 — ♭7",
        "formula_desc": "Root • Minor 3rd • 5th • Minor 7th",
        "intervals_text": "[3 + 4 + 3]",
        "semitones": [0, 3, 7, 10, 12, 15],
        "degree_names": ["Root", "♭3rd", "5th", "♭7th", "Octave", "Oct ♭3"],
        "rh_inversions": [
            ("ROOT", "1 • 2 • 3 • 5", {0: "1", 3: "2", 7: "3", 10: "5"}),
            ("1ST INV", "1 • 2 • 4 • 5", {3: "1", 7: "2", 10: "4", 12: "5"}),
            ("2ND INV", "1 • 2 • 3 • 5", {7: "1", 10: "2", 12: "3", 15: "5"}),
        ],
        "lh_inversions": [
            ("ROOT", "5 • 3 • 2 • 1", {0: "5", 3: "3", 7: "2", 10: "1"}),
            ("1ST INV", "5 • 3 • 2 • 1", {3: "5", 7: "3", 10: "2", 12: "1"}),
            ("2ND INV", "5 • 4 • 2 • 1", {7: "5", 10: "4", 12: "2", 15: "1"}),
        ]
    },
    "dim7": {
        "title": "DIMINISHED 7th CHORDS",
        "suffix": "dim7",
        "formula_text": "1 — ♭3 — ♭5 — 𝄫7",
        "formula_desc": "Root • Minor 3rd • ♭5th • Dim 7th",
        "intervals_text": "[3 + 3 + 3]",
        "semitones": [0, 3, 6, 9, 12, 15],
        "degree_names": ["Root", "♭3rd", "♭5th", "𝄫7th", "Octave", "Oct ♭3"],
        "rh_inversions": [
            ("ROOT", "1 • 2 • 3 • 5", {0: "1", 3: "2", 6: "3", 9: "5"}),
            ("1ST INV", "1 • 2 • 4 • 5", {3: "1", 6: "2", 9: "4", 12: "5"}),
            ("2ND INV", "1 • 2 • 3 • 5", {6: "1", 9: "2", 12: "3", 15: "5"}),
        ],
        "lh_inversions": [
            ("ROOT", "5 • 3 • 2 • 1", {0: "5", 3: "3", 6: "2", 9: "1"}),
            ("1ST INV", "5 • 3 • 2 • 1", {3: "5", 6: "3", 9: "2", 12: "1"}),
            ("2ND INV", "5 • 4 • 2 • 1", {6: "5", 9: "4", 12: "2", 15: "1"}),
        ]
    },
    "m7b5": {
        "title": "HALF-DIMINISHED CHORDS (m7♭5)",
        "suffix": "m7b5",
        "formula_text": "1 — ♭3 — ♭5 — ♭7",
        "formula_desc": "Root • Minor 3rd • ♭5th • Minor 7th",
        "intervals_text": "[3 + 3 + 4]",
        "semitones": [0, 3, 6, 10, 12, 15],
        "degree_names": ["Root", "♭3rd", "♭5th", "♭7th", "Octave", "Oct ♭3"],
        "rh_inversions": [
            ("ROOT", "1 • 2 • 3 • 5", {0: "1", 3: "2", 6: "3", 10: "5"}),
            ("1ST INV", "1 • 2 • 4 • 5", {3: "1", 6: "2", 10: "4", 12: "5"}),
            ("2ND INV", "1 • 2 • 3 • 5", {6: "1", 10: "2", 12: "3", 15: "5"}),
        ],
        "lh_inversions": [
            ("ROOT", "5 • 3 • 2 • 1", {0: "5", 3: "3", 6: "2", 10: "1"}),
            ("1ST INV", "5 • 3 • 2 • 1", {3: "5", 6: "3", 10: "2", 12: "1"}),
            ("2ND INV", "5 • 4 • 2 • 1", {6: "5", 10: "4", 12: "2", 15: "1"}),
        ]
    },
    "mM7": {
        "title": "MINOR-MAJOR 7th CHORDS",
        "suffix": "mM7",
        "formula_text": "1 — ♭3 — 5 — 7",
        "formula_desc": "Root • Minor 3rd • 5th • Major 7th",
        "intervals_text": "[3 + 4 + 4]",
        "semitones": [0, 3, 7, 11, 12, 15],
        "degree_names": ["Root", "♭3rd", "5th", "7th", "Octave", "Oct ♭3"],
        "rh_inversions": [
            ("ROOT", "1 • 2 • 3 • 5", {0: "1", 3: "2", 7: "3", 11: "5"}),
            ("1ST INV", "1 • 2 • 4 • 5", {3: "1", 7: "2", 11: "4", 12: "5"}),
            ("2ND INV", "1 • 2 • 3 • 5", {7: "1", 11: "2", 12: "3", 15: "5"}),
        ],
        "lh_inversions": [
            ("ROOT", "5 • 3 • 2 • 1", {0: "5", 3: "3", 7: "2", 11: "1"}),
            ("1ST INV", "5 • 3 • 2 • 1", {3: "5", 7: "3", 11: "2", 12: "1"}),
            ("2ND INV", "5 • 4 • 2 • 1", {7: "5", 11: "4", 12: "2", 15: "1"}),
        ]
    },
    "maj6": {
        "title": "MAJOR 6th CHORDS",
        "suffix": "6",
        "formula_text": "1 — 3 — 5 — 6",
        "formula_desc": "Root • Major 3rd • 5th • Major 6th",
        "intervals_text": "[4 + 3 + 2]",
        "semitones": [0, 4, 7, 9, 12, 16],
        "degree_names": ["Root", "3rd", "5th", "6th", "Octave", "Oct 3rd"],
        "rh_inversions": [
            ("ROOT", "1 • 2 • 3 • 5", {0: "1", 4: "2", 7: "3", 9: "5"}),
            ("1ST INV", "1 • 2 • 4 • 5", {4: "1", 7: "2", 9: "4", 12: "5"}),
            ("2ND INV", "1 • 2 • 3 • 5", {7: "1", 9: "2", 12: "3", 16: "5"}),
        ],
        "lh_inversions": [
            ("ROOT", "5 • 3 • 2 • 1", {0: "5", 4: "3", 7: "2", 9: "1"}),
            ("1ST INV", "5 • 3 • 2 • 1", {4: "5", 7: "3", 9: "2", 12: "1"}),
            ("2ND INV", "5 • 4 • 2 • 1", {7: "5", 9: "4", 12: "2", 16: "1"}),
        ]
    },
    "min6": {
        "title": "MINOR 6th CHORDS",
        "suffix": "min6",
        "formula_text": "1 — ♭3 — 5 — 6",
        "formula_desc": "Root • Minor 3rd • 5th • Major 6th",
        "intervals_text": "[3 + 4 + 2]",
        "semitones": [0, 3, 7, 9, 12, 15],
        "degree_names": ["Root", "♭3rd", "5th", "6th", "Octave", "Oct ♭3"],
        "rh_inversions": [
            ("ROOT", "1 • 2 • 3 • 5", {0: "1", 3: "2", 7: "3", 9: "5"}),
            ("1ST INV", "1 • 2 • 4 • 5", {3: "1", 7: "2", 9: "4", 12: "5"}),
            ("2ND INV", "1 • 2 • 3 • 5", {7: "1", 9: "2", 12: "3", 15: "5"}),
        ],
        "lh_inversions": [
            ("ROOT", "5 • 3 • 2 • 1", {0: "5", 3: "3", 7: "2", 9: "1"}),
            ("1ST INV", "5 • 3 • 2 • 1", {3: "5", 7: "3", 9: "2", 12: "1"}),
            ("2ND INV", "5 • 4 • 2 • 1", {7: "5", 9: "4", 12: "2", 15: "1"}),
        ]
    },
    "add9": {
        "title": "MAJOR (ADD9) CHORDS",
        "suffix": "add9",
        "formula_text": "1 — 3 — 5 — 9",
        "formula_desc": "Root • Major 3rd • 5th • Major 9th",
        "intervals_text": "[4 + 3 + 7]",
        "semitones": [0, 4, 7, 12, 14, 16],
        "degree_names": ["Root", "3rd", "5th", "Octave", "9th", "Oct 3rd"],
        "rh_inversions": [
            ("ROOT", "1 • 2 • 3 • 5", {0: "1", 4: "2", 7: "3", 14: "5"}),
            ("1ST INV", "1 • 2 • 4 • 5", {4: "1", 7: "2", 12: "4", 14: "5"}),
            ("2ND INV", "1 • 2 • 3 • 5", {7: "1", 12: "2", 14: "3", 16: "5"}),
        ],
        "lh_inversions": [
            ("ROOT", "5 • 3 • 2 • 1", {0: "5", 4: "3", 7: "2", 14: "1"}),
            ("1ST INV", "5 • 3 • 2 • 1", {4: "5", 7: "3", 12: "2", 14: "1"}),
            ("2ND INV", "5 • 4 • 2 • 1", {7: "5", 12: "4", 14: "2", 16: "1"}),
        ]
    },
    "7sus4": {
        "title": "SUSPENDED 7th CHORDS (7sus4)",
        "suffix": "7sus4",
        "formula_text": "1 — 4 — 5 — ♭7",
        "formula_desc": "Root • 4th • 5th • Minor 7th",
        "intervals_text": "[5 + 2 + 3]",
        "semitones": [0, 5, 7, 10, 12, 17],
        "degree_names": ["Root", "4th", "5th", "♭7th", "Octave", "Oct 4th"],
        "rh_inversions": [
            ("ROOT", "1 • 2 • 3 • 5", {0: "1", 5: "2", 7: "3", 10: "5"}),
            ("1ST INV", "1 • 2 • 4 • 5", {5: "1", 7: "2", 10: "4", 12: "5"}),
            ("2ND INV", "1 • 2 • 3 • 5", {7: "1", 10: "2", 12: "3", 17: "5"}),
        ],
        "lh_inversions": [
            ("ROOT", "5 • 3 • 2 • 1", {0: "5", 5: "3", 7: "2", 10: "1"}),
            ("1ST INV", "5 • 3 • 2 • 1", {5: "5", 7: "3", 10: "2", 12: "1"}),
            ("2ND INV", "5 • 4 • 2 • 1", {7: "5", 10: "4", 12: "2", 17: "1"}),
        ]
    },
    "dom9": {
        "title": "DOMINANT 9th CHORDS",
        "suffix": "9",
        "formula_text": "1 — 3 — 5 — ♭7 — 9",
        "formula_desc": "Root • Major 3rd • 5th • ♭7th • 9th",
        "intervals_text": "[4 + 3 + 3 + 4]",
        "semitones": [0, 4, 7, 10, 14, 16],
        "degree_names": ["Root", "3rd", "5th", "♭7th", "9th", "Oct 3rd"],
        "rh_inversions": [
            ("ROOT", "1 • 2 • 3 • 5", {0: "1", 4: "2", 10: "3", 14: "5"}),
            ("1ST INV", "1 • 2 • 4 • 5", {4: "1", 7: "2", 10: "4", 14: "5"}),
            ("2ND INV", "1 • 2 • 3 • 5", {7: "1", 10: "2", 14: "3", 16: "5"}),
        ],
        "lh_inversions": [
            ("ROOT", "5 • 3 • 2 • 1", {0: "5", 4: "3", 10: "2", 14: "1"}),
            ("1ST INV", "5 • 3 • 2 • 1", {4: "5", 7: "3", 10: "2", 14: "1"}),
            ("2ND INV", "5 • 4 • 2 • 1", {7: "5", 10: "4", 14: "2", 16: "1"}),
        ]
    },
    "maj9": {
        "title": "MAJOR 9th CHORDS",
        "suffix": "maj9",
        "formula_text": "1 — 3 — 5 — 7 — 9",
        "formula_desc": "Root • Major 3rd • 5th • 7th • 9th",
        "intervals_text": "[4 + 3 + 4 + 3]",
        "semitones": [0, 4, 7, 11, 14, 16],
        "degree_names": ["Root", "3rd", "5th", "7th", "9th", "Oct 3rd"],
        "rh_inversions": [
            ("ROOT", "1 • 2 • 3 • 5", {0: "1", 4: "2", 11: "3", 14: "5"}),
            ("1ST INV", "1 • 2 • 4 • 5", {4: "1", 7: "2", 11: "4", 14: "5"}),
            ("2ND INV", "1 • 2 • 3 • 5", {7: "1", 11: "2", 14: "3", 16: "5"}),
        ],
        "lh_inversions": [
            ("ROOT", "5 • 3 • 2 • 1", {0: "5", 4: "3", 11: "2", 14: "1"}),
            ("1ST INV", "5 • 3 • 2 • 1", {4: "5", 7: "3", 11: "2", 14: "1"}),
            ("2ND INV", "5 • 4 • 2 • 1", {7: "5", 11: "4", 14: "2", 16: "1"}),
        ]
    },
    "min9": {
        "title": "MINOR 9th CHORDS",
        "suffix": "min9",
        "formula_text": "1 — ♭3 — 5 — ♭7 — 9",
        "formula_desc": "Root • Minor 3rd • 5th • ♭7th • 9th",
        "intervals_text": "[3 + 4 + 3 + 4]",
        "semitones": [0, 3, 7, 10, 14, 15],
        "degree_names": ["Root", "♭3rd", "5th", "♭7th", "9th", "Oct ♭3"],
        "rh_inversions": [
            ("ROOT", "1 • 2 • 3 • 5", {0: "1", 3: "2", 10: "3", 14: "5"}),
            ("1ST INV", "1 • 2 • 4 • 5", {3: "1", 7: "2", 10: "4", 14: "5"}),
            ("2ND INV", "1 • 2 • 3 • 5", {7: "1", 10: "2", 14: "3", 15: "5"}),
        ],
        "lh_inversions": [
            ("ROOT", "5 • 3 • 2 • 1", {0: "5", 3: "3", 10: "2", 14: "1"}),
            ("1ST INV", "5 • 3 • 2 • 1", {3: "5", 7: "3", 10: "2", 14: "1"}),
            ("2ND INV", "5 • 4 • 2 • 1", {7: "5", 10: "4", 14: "2", 15: "1"}),
        ]
    },
    "7b9": {
        "title": "ALTERED 7♭9 CHORDS",
        "suffix": "7b9",
        "formula_text": "1 — 3 — 5 — ♭7 — ♭9",
        "formula_desc": "Root • Major 3rd • 5th • ♭7th • ♭9th",
        "intervals_text": "[4 + 3 + 3 + 3]",
        "semitones": [0, 4, 7, 10, 13, 16],
        "degree_names": ["Root", "3rd", "5th", "♭7th", "♭9th", "Oct 3rd"],
        "rh_inversions": [
            ("ROOT", "1 • 2 • 3 • 5", {0: "1", 4: "2", 10: "3", 13: "5"}),
            ("1ST INV", "1 • 2 • 4 • 5", {4: "1", 7: "2", 10: "4", 13: "5"}),
            ("2ND INV", "1 • 2 • 3 • 5", {7: "1", 10: "2", 13: "3", 16: "5"}),
        ],
        "lh_inversions": [
            ("ROOT", "5 • 3 • 2 • 1", {0: "5", 4: "3", 10: "2", 13: "1"}),
            ("1ST INV", "5 • 3 • 2 • 1", {4: "5", 7: "3", 10: "2", 13: "1"}),
            ("2ND INV", "5 • 4 • 2 • 1", {7: "5", 10: "4", 13: "2", 16: "1"}),
        ]
    },
    "7s9": {
        "title": "ALTERED 7♯9 CHORDS (HENDRIX)",
        "suffix": "7#9",
        "formula_text": "1 — 3 — 5 — ♭7 — ♯9",
        "formula_desc": "Root • Major 3rd • 5th • ♭7th • ♯9th",
        "intervals_text": "[4 + 3 + 3 + 5]",
        "semitones": [0, 4, 7, 10, 15, 16],
        "degree_names": ["Root", "3rd", "5th", "♭7th", "♯9th", "Oct 3rd"],
        "rh_inversions": [
            ("ROOT", "1 • 2 • 3 • 5", {0: "1", 4: "2", 10: "3", 15: "5"}),
            ("1ST INV", "1 • 2 • 4 • 5", {4: "1", 7: "2", 10: "4", 15: "5"}),
            ("2ND INV", "1 • 2 • 3 • 5", {7: "1", 10: "2", 15: "3", 16: "5"}),
        ],
        "lh_inversions": [
            ("ROOT", "5 • 3 • 2 • 1", {0: "5", 4: "3", 10: "2", 15: "1"}),
            ("1ST INV", "5 • 3 • 2 • 1", {4: "5", 7: "3", 10: "2", 15: "1"}),
            ("2ND INV", "5 • 4 • 2 • 1", {7: "5", 10: "4", 15: "2", 16: "1"}),
        ]
    }
}

# Scale Definitions
SCALE_DEFINITIONS = {
    "major": {
        "title": "MAJOR SCALE (IONIAN)",
        "formula_text": "W — W — H — W — W — W — H",
        "formula_desc": "Root • 2nd • 3rd • 4th • 5th • 6th • 7th",
        "intervals_text": "[2+2+1+2+2+2+1]",
        "semitones": [0, 2, 4, 5, 7, 9, 11, 12],
        "degree_names": ["1 (R)", "2", "3", "4", "5", "6", "7", "8ve"],
        "rh_fingering": "1 - 2 - 3 - 1 - 2 - 3 - 4 - 5",
        "lh_fingering": "5 - 4 - 3 - 2 - 1 - 3 - 2 - 1"
    },
    "minor": {
        "title": "NATURAL MINOR SCALE (AEOLIAN)",
        "formula_text": "W — H — W — W — H — W — W",
        "formula_desc": "Root • 2nd • ♭3rd • 4th • 5th • ♭6th • ♭7th",
        "intervals_text": "[2+1+2+2+1+2+2]",
        "semitones": [0, 2, 3, 5, 7, 8, 10, 12],
        "degree_names": ["1 (R)", "2", "♭3", "4", "5", "♭6", "♭7", "8ve"],
        "rh_fingering": "1 - 2 - 3 - 1 - 2 - 3 - 4 - 5",
        "lh_fingering": "5 - 4 - 3 - 2 - 1 - 3 - 2 - 1"
    },
    "harmonic_minor": {
        "title": "HARMONIC MINOR SCALE",
        "formula_text": "W — H — W — W — H — A2 — H",
        "formula_desc": "Root • 2nd • ♭3rd • 4th • 5th • ♭6th • 7th",
        "intervals_text": "[2+1+2+2+1+3+1]",
        "semitones": [0, 2, 3, 5, 7, 8, 11, 12],
        "degree_names": ["1 (R)", "2", "♭3", "4", "5", "♭6", "7", "8ve"],
        "rh_fingering": "1 - 2 - 3 - 1 - 2 - 3 - 4 - 5",
        "lh_fingering": "5 - 4 - 3 - 2 - 1 - 3 - 2 - 1"
    },
    "melodic_minor": {
        "title": "MELODIC MINOR SCALE (ASCENDING)",
        "formula_text": "W — H — W — W — W — W — H",
        "formula_desc": "Root • 2nd • ♭3rd • 4th • 5th • 6th • 7th",
        "intervals_text": "[2+1+2+2+2+2+1]",
        "semitones": [0, 2, 3, 5, 7, 9, 11, 12],
        "degree_names": ["1 (R)", "2", "♭3", "4", "5", "6", "7", "8ve"],
        "rh_fingering": "1 - 2 - 3 - 1 - 2 - 3 - 4 - 5",
        "lh_fingering": "5 - 4 - 3 - 2 - 1 - 3 - 2 - 1"
    },
    "major_penta": {
        "title": "MAJOR PENTATONIC SCALE",
        "formula_text": "1 — 2 — 3 — 5 — 6",
        "formula_desc": "5-Note Scale without half-steps",
        "intervals_text": "[2 + 2 + 3 + 2 + 3]",
        "semitones": [0, 2, 4, 7, 9, 12],
        "degree_names": ["1 (R)", "2", "3", "5", "6", "8ve"],
        "rh_fingering": "1 - 2 - 3 - 1 - 2 - 3",
        "lh_fingering": "5 - 4 - 3 - 2 - 1 - 2"
    },
    "minor_penta": {
        "title": "MINOR PENTATONIC SCALE",
        "formula_text": "1 — ♭3 — 4 — 5 — ♭7",
        "formula_desc": "Essential Blues & Rock Scale",
        "intervals_text": "[3 + 2 + 2 + 3 + 2]",
        "semitones": [0, 3, 5, 7, 10, 12],
        "degree_names": ["1 (R)", "♭3", "4", "5", "♭7", "8ve"],
        "rh_fingering": "1 - 3 - 1 - 2 - 3 - 1",
        "lh_fingering": "5 - 3 - 2 - 1 - 3 - 1"
    },
    "major_blues": {
        "title": "MAJOR BLUES SCALE",
        "formula_text": "1 — 2 — ♭3 — 3 — 5 — 6",
        "formula_desc": "Includes Blue ♭3 passing tone",
        "intervals_text": "[2 + 1 + 1 + 3 + 2 + 3]",
        "semitones": [0, 2, 3, 4, 7, 9, 12],
        "degree_names": ["1 (R)", "2", "♭3", "3", "5", "6", "8ve"],
        "rh_fingering": "1 - 2 - ♭3 - 1 - 2 - 3 - 5",
        "lh_fingering": "5 - 4 - 3 - 2 - 1 - 2 - 1"
    },
    "minor_blues": {
        "title": "MINOR BLUES SCALE (HEXATONIC)",
        "formula_text": "1 — ♭3 — 4 — ♭5 — 5 — ♭7",
        "formula_desc": "Minor Pentatonic + Blue Note (♭5)",
        "intervals_text": "[3 + 2 + 1 + 1 + 3 + 2]",
        "semitones": [0, 3, 5, 6, 7, 10, 12],
        "degree_names": ["1 (R)", "♭3", "4", "♭5", "5", "♭7", "8ve"],
        "rh_fingering": "1 - 2 - 3 - 4 - 1 - 3 - 1",
        "lh_fingering": "5 - 4 - 3 - 2 - 1 - 3 - 1"
    },
    "dorian": {
        "title": "DORIAN MODE",
        "formula_text": "1 — 2 — ♭3 — 4 — 5 — 6 — ♭7",
        "formula_desc": "Minor with bright Major 6th (Modal Jazz)",
        "intervals_text": "[2+1+2+2+2+1+2]",
        "semitones": [0, 2, 3, 5, 7, 9, 10, 12],
        "degree_names": ["1 (R)", "2", "♭3", "4", "5", "6", "♭7", "8ve"],
        "rh_fingering": "1 - 2 - 3 - 1 - 2 - 3 - 4 - 5",
        "lh_fingering": "5 - 4 - 3 - 2 - 1 - 3 - 2 - 1"
    },
    "mixolydian": {
        "title": "MIXOLYDIAN MODE",
        "formula_text": "1 — 2 — 3 — 4 — 5 — 6 — ♭7",
        "formula_desc": "Major with Dominant ♭7th (Blues & Jam)",
        "intervals_text": "[2+2+1+2+2+1+2]",
        "semitones": [0, 2, 4, 5, 7, 9, 10, 12],
        "degree_names": ["1 (R)", "2", "3", "4", "5", "6", "♭7", "8ve"],
        "rh_fingering": "1 - 2 - 3 - 1 - 2 - 3 - 4 - 5",
        "lh_fingering": "5 - 4 - 3 - 2 - 1 - 3 - 2 - 1"
    },
    "lydian": {
        "title": "LYDIAN MODE",
        "formula_text": "1 — 2 — 3 — ♯4 — 5 — 6 — 7",
        "formula_desc": "Major with raised ♯4 (Dreamy / Film Score)",
        "intervals_text": "[2+2+2+1+2+2+1]",
        "semitones": [0, 2, 4, 6, 7, 9, 11, 12],
        "degree_names": ["1 (R)", "2", "3", "♯4", "5", "6", "7", "8ve"],
        "rh_fingering": "1 - 2 - 3 - 4 - 1 - 2 - 3 - 4",
        "lh_fingering": "5 - 4 - 3 - 2 - 1 - 3 - 2 - 1"
    },
    "phrygian": {
        "title": "PHRYGIAN MODE",
        "formula_text": "1 — ♭2 — ♭3 — 4 — 5 — ♭6 — ♭7",
        "formula_desc": "Minor with dark ♭2 (Spanish / Flamenco)",
        "intervals_text": "[1+2+2+2+1+2+2]",
        "semitones": [0, 1, 3, 5, 7, 8, 10, 12],
        "degree_names": ["1 (R)", "♭2", "♭3", "4", "5", "♭6", "♭7", "8ve"],
        "rh_fingering": "1 - 2 - 3 - 1 - 2 - 3 - 4 - 5",
        "lh_fingering": "5 - 4 - 3 - 2 - 1 - 3 - 2 - 1"
    },
    "locrian": {
        "title": "LOCRIAN MODE",
        "formula_text": "1 — ♭2 — ♭3 — 4 — ♭5 — ♭6 — ♭7",
        "formula_desc": "Diminished mode with ♭2 and ♭5",
        "intervals_text": "[1+2+2+1+2+2+2]",
        "semitones": [0, 1, 3, 5, 6, 8, 10, 12],
        "degree_names": ["1 (R)", "♭2", "♭3", "4", "♭5", "♭6", "♭7", "8ve"],
        "rh_fingering": "1 - 2 - 3 - 4 - 1 - 2 - 3 - 4",
        "lh_fingering": "5 - 4 - 3 - 2 - 1 - 3 - 2 - 1"
    }
}
