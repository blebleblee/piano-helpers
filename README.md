# Piano Learning Helpers (Enhanced Edition)

This repository contains printable graphical helpers designed to assist with learning piano chords, scales, and chord progressions. These documents are calibrated to standard 88-key piano fallboard key pitch (13.79 mm per semitone, matching Roland FP-30X, digital pianos, and acoustic pianos). When printed and folded, they stand directly behind the piano keys to visually guide your finger placement.

---

## What's New in the Enhanced Edition

- **Unified Piano Matrix Design:** Chord tables, inversion fingerings, and realistic piano keys are seamlessly connected in a continuous, compact grid.
- **Root Alignment Pointer (`▼ ROOT ▼`):** A registration arrow at the base of Column 0 lets you line up the card with your target piano key instantly without reading labels.
- **Zebra Tracking Rails:** Subtle vertical tints on black-key columns prevent eye drift when tracking notes down to the keys.
- **Tactile Key Type Indicators:** Quick-reference `○` (White Key) and `●` (Black Key) icons show the physical hand shape for each chord (e.g., $D\text{ maj}$ is `○ ● ○` = White • Black • White).
- **Safe A4 Print Margins:** Calibrated 18-column grid with generous ~14.5 mm margins on both sides ensures 100% printable coverage on any standard printer without edge clipping.
- **100% Bug Fixes Applied:**
  - Fixed $D\flat\text{ aug}$ spelling ($D\flat - F - A$, was erroneously $B\flat$ in legacy files).
  - Fixed $E\text{ min6}$ spelling ($E - G - B - C\sharp$, was erroneously $C$).
  - Corrected misnamed diminished triads (`chords_dim_*.pdf`, previously mislabeled `dom`).
  - Fixed duplicate overlapping text layers and $Dd$ typo in Minor Blues scale.
  - Fixed $C\text{maj (I)}$ voicing in Jazz $\text{ii}-\text{V}-\text{I}$ ($C - E - G$, was duplicated $G\text{maj}$).
- **Interactive Web App & Catalog:** Zero-dependency standalone web app in [`index.html`](index.html) (compatible with Gitea Pages, GitHub Pages, or local browser).
- **Comprehensive Guide & Theory Manual:** Full in-depth documentation in [`GUIDE.md`](GUIDE.md).
- **Automated Generator Pipeline:** Declarative Python engine (`build_all.py`) and test suite (`test_cards.py`).
- **Legacy Files:** Original manual Illustrator exports are archived under [`deprecated/`](deprecated/).

---

## Interactive Web App

Open **`index.html`** in any web browser (or deploy to Gitea Pages / GitHub Pages) to:
* **Browse the 61-Card Catalog:** Instant search, category filters, and one-click PDF downloads.
* **Live Custom Card Builder:** Customize any chord or scale, select key bed pitch (Standard 88-Key vs. Mini-Keys), and print directly from your browser.
* **Interactive Usage Guide:** Illustrated guide explaining folding, sliding transposition, and tactile key shape memory.

---

## Detailed User Manual

For an in-depth walkthrough of how to fold, align, transpose, and read inversions and tactile dots, see **[`GUIDE.md`](GUIDE.md)**.

---

## Directory Structure

```text
piano-helpers/
├── chords/                 # 42 Enhanced Chord Cards (21 types x RH & LH)
│   ├── chords_maj_RH.pdf / LH.pdf        # Major Triad (1, 3, 5)
│   ├── chords_min_RH.pdf / LH.pdf        # Minor Triad (1, ♭3, 5)
│   ├── chords_dim_RH.pdf / LH.pdf        # Diminished Triad (1, ♭3, ♭5)
│   ├── chords_aug_RH.pdf / LH.pdf        # Augmented Triad (1, 3, ♯5)
│   ├── chords_sus2_RH.pdf / LH.pdf       # Suspended 2nd (1, 2, 5)
│   ├── chords_sus4_RH.pdf / LH.pdf       # Suspended 4th (1, 4, 5)
│   ├── chords_dom7_RH.pdf / LH.pdf       # Dominant 7th (1, 3, 5, ♭7)
│   ├── chords_maj7_RH.pdf / LH.pdf       # Major 7th (1, 3, 5, 7)
│   ├── chords_min7_RH.pdf / LH.pdf       # Minor 7th (1, ♭3, 5, ♭7)
│   ├── chords_dim7_RH.pdf / LH.pdf       # Diminished 7th (1, ♭3, ♭5, 𝄫7)
│   ├── chords_m7b5_RH.pdf / LH.pdf       # Half-Diminished (1, ♭3, ♭5, ♭7)
│   ├── chords_mM7_RH.pdf / LH.pdf        # Minor-Major 7th (1, ♭3, 5, 7)
│   ├── chords_maj6_RH.pdf / LH.pdf       # Major 6th (1, 3, 5, 6)
│   ├── chords_min6_RH.pdf / LH.pdf       # Minor 6th (1, ♭3, 5, 6)
│   ├── chords_add9_RH.pdf / LH.pdf       # Major add9 (1, 3, 5, 9)
│   ├── chords_7sus4_RH.pdf / LH.pdf      # Suspended 7th (1, 4, 5, ♭7)
│   ├── chords_dom9_RH.pdf / LH.pdf       # Dominant 9th (1, 3, 5, ♭7, 9)
│   ├── chords_maj9_RH.pdf / LH.pdf       # Major 9th (1, 3, 5, 7, 9)
│   ├── chords_min9_RH.pdf / LH.pdf       # Minor 9th (1, ♭3, 5, ♭7, 9)
│   ├── chords_7b9_RH.pdf / LH.pdf        # Altered 7♭9 (1, 3, 5, ♭7, ♭9)
│   └── chords_7s9_RH.pdf / LH.pdf        # Altered 7♯9 / Hendrix (1, 3, 5, ♭7, ♯9)
├── scales/                 # 13 Enhanced Scale Cards
│   ├── scales_major.pdf                  # Major (Ionian)
│   ├── scales_minor.pdf                  # Natural Minor (Aeolian)
│   ├── scales_harmonic_minor.pdf         # Harmonic Minor
│   ├── scales_melodic_minor.pdf          # Melodic Minor
│   ├── scales_major_penta.pdf            # Major Pentatonic
│   ├── scales_minor_penta.pdf            # Minor Pentatonic
│   ├── scales_major_blues.pdf            # Major Blues
│   ├── scales_minor_blues.pdf            # Minor Blues (Hexatonic)
│   ├── scales_dorian.pdf                 # Dorian Mode
│   ├── scales_mixolydian.pdf             # Mixolydian Mode
│   ├── scales_lydian.pdf                 # Lydian Mode
│   ├── scales_phrygian.pdf               # Phrygian Mode
│   └── scales_locrian.pdf                # Locrian Mode
├── progressions/           # 6 Enhanced Progression Cards
│   ├── progressions_pop.pdf              # Pop & Rock (I-V-vi-IV & vi-IV-I-V)
│   ├── progressions_jazz.pdf             # Jazz Cadence (ii-V-I & Turnaround)
│   ├── progressions_classic.pdf          # Classical (Pachelbel) & 3-Chord Blues
│   ├── progressions_blues_12bar.pdf      # Full 12-Bar Blues with Turnaround
│   ├── progressions_circle_of_fifths.pdf # Circle Progression (Autumn Leaves)
│   └── progressions_jazz_rootless.pdf    # Two-Hand Rootless Jazz Voicings (Bill Evans)
├── generator/              # Python vector generator engine & music theory core
│   ├── music_theory.py
│   └── svg_builder.py
├── build_all.py            # Master card generation script
├── test_cards.py           # Automated verification test suite
├── deprecated/             # Original legacy Illustrator PDF exports
└── images/                 # Setup and demonstration photos
```

---

## Printing & Usage

1. Open any PDF from `chords/`, `scales/`, or `progressions/`.
2. Print on standard **A4 paper** at **100% scale** (do not select "Fit to page" or "Shrink to printable area").
3. Fold the bottom base flap forward 90° along the red dashed line:
   ```text
   ▼ FOLD FORWARD 90° HERE — KEYS REST DIRECTLY BEHIND PIANO KEYS ▼
   ```
4. Place the card behind your piano keys so the bottom edge rests against the fallboard:
   - **For C Major / Root:** Align the red **`▼ ROOT ▼`** arrow directly over any **C** key.
   - **To Transpose:** Slide the **`▼ ROOT ▼`** arrow over any other root key ($D, E\flat, F, G\dots$) and read across that chord's row.

---

## Building and Testing Cards

To re-generate all cards or add custom chord formulas:

```sh
# Generate all 61 production cards
python3 build_all.py

# Run the automated verification suite
python3 test_cards.py
```

### Dependencies
- Python 3
- `librsvg` (`rsvg-convert`): `brew install librsvg` (macOS) or `apt-get install librsvg2-bin` (Linux)
- `poppler` (`pdfinfo`, `pdftotext`): `brew install poppler` (macOS)

---

## Contributing

Contributions, new chord formulas, and additional progression sheets are welcome! Please submit a PR or open an issue.

## Support

If you find these piano helpers useful and want to support their ongoing development, consider buying me a coffee!

<a href="https://www.buymeacoffee.com/blebleblee" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

## License

This project is licensed under the [MIT License](LICENSE).
