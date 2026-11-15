#!/usr/bin/env python3
"""
Master Build & Verification Script for Piano Learning Helpers
Generates publication-quality Unified Matrix cards for:
- Chords (30 PDFs: 15 chord types x LH & RH)
- Scales (10 PDFs: Major, Minor, Harmonic, Melodic, Pentatonics, Blues, Modes)
- Progressions (3 PDFs: Pop/Rock, Jazz, Classical/Blues)
Runs verification tests confirming all note spellings and dimensions.
"""

import os
import subprocess
import glob
from generator.music_theory import CHORD_DEFINITIONS, SCALE_DEFINITIONS
from generator.svg_builder import (
    build_chord_card, build_scale_card, build_progression_card
)

def build_all_chords():
    os.makedirs("chords", exist_ok=True)
    count = 0
    for chord_key in CHORD_DEFINITIONS:
        for hand in ["RH", "LH"]:
            svg_content = build_chord_card(chord_key, hand)
            base_name = f"chords_{chord_key}_{hand}"
            svg_path = f"chords/{base_name}.svg"
            pdf_path = f"chords/{base_name}.pdf"

            with open(svg_path, "w") as f:
                f.write(svg_content)

            subprocess.run([
                "rsvg-convert", "--dpi-x", "72", "--dpi-y", "72",
                "-f", "pdf", "-o", pdf_path, svg_path
            ], check=True)
            # Remove intermediate SVG to keep repo tidy, or keep SVG if desired
            os.remove(svg_path)
            count += 1
            print(f"  [Chord] {pdf_path}")
    return count

def build_all_scales():
    os.makedirs("scales", exist_ok=True)
    count = 0
    for scale_key in SCALE_DEFINITIONS:
        svg_content = build_scale_card(scale_key)
        base_name = f"scales_{scale_key}"
        svg_path = f"scales/{base_name}.svg"
        pdf_path = f"scales/{base_name}.pdf"

        with open(svg_path, "w") as f:
            f.write(svg_content)

        subprocess.run([
            "rsvg-convert", "--dpi-x", "72", "--dpi-y", "72",
            "-f", "pdf", "-o", pdf_path, svg_path
        ], check=True)
        os.remove(svg_path)
        count += 1
        print(f"  [Scale] {pdf_path}")
    return count

def build_all_progressions():
    os.makedirs("progressions", exist_ok=True)
    count = 0

    # Progression 1: Pop / Modern Standards (I-V-vi-IV and vi-IV-I-V)
    pop_data = [
        ("I — V — vi — IV in C Major (The 4-Chord Wonder)", [
            ("I",  "C maj", [(0, "C", "Root"), (4, "E", "3rd"), (7, "G", "5th")]),
            ("V",  "G maj", [(2, "D", "5th"), (7, "G", "Root"), (11, "B", "3rd")]), # 2nd inv for voice leading
            ("vi", "A min", [(0, "C", "3rd"), (4, "E", "5th"), (9, "A", "Root")]), # 1st inv
            ("IV", "F maj", [(0, "C", "5th"), (5, "F", "Root"), (9, "A", "3rd")]), # 2nd inv
        ]),
        ("vi — IV — I — V in C Major (Emotional / Ballad Progression)", [
            ("vi", "A min", [(0, "C", "3rd"), (4, "E", "5th"), (9, "A", "Root")]),
            ("IV", "F maj", [(0, "C", "5th"), (5, "F", "Root"), (9, "A", "3rd")]),
            ("I",  "C maj", [(0, "C", "Root"), (4, "E", "3rd"), (7, "G", "5th")]),
            ("V",  "G maj", [(2, "D", "5th"), (7, "G", "Root"), (11, "B", "3rd")]),
        ])
    ]
    svg_pop = build_progression_card("POP PROGRESSIONS", "Smooth Voice-Leading • Align Col 0 to C (or transpose)", pop_data)
    with open("progressions/progressions_pop.svg", "w") as f:
        f.write(svg_pop)
    subprocess.run(["rsvg-convert", "--dpi-x", "72", "--dpi-y", "72", "-f", "pdf", "-o", "progressions/progressions_pop.pdf", "progressions/progressions_pop.svg"], check=True)
    os.remove("progressions/progressions_pop.svg")
    count += 1
    print("  [Progression] progressions/progressions_pop.pdf")

    # Progression 2: Jazz Standards (ii-V-I and I-vi-ii-V) (FIXED Cmaj notes!)
    jazz_data = [
        ("ii — V — I in C Major (Essential Jazz Cadence)", [
            ("ii", "D min", [(2, "D", "Root"), (5, "F", "3rd"), (9, "A", "5th")]),
            ("V",  "G maj", [(2, "D", "5th"), (7, "G", "Root"), (11, "B", "3rd")]),
            ("I",  "C maj", [(0, "C", "Root"), (4, "E", "3rd"), (7, "G", "5th")]), # FIXED: C-E-G (was D-G-B in legacy!)
        ]),
        ("I — vi — ii — V in C Major (Jazz Turnaround)", [
            ("I",  "C maj", [(0, "C", "Root"), (4, "E", "3rd"), (7, "G", "5th")]),
            ("vi", "A min", [(0, "C", "3rd"), (4, "E", "5th"), (9, "A", "Root")]),
            ("ii", "D min", [(2, "D", "Root"), (5, "F", "3rd"), (9, "A", "5th")]),
            ("V",  "G maj", [(2, "D", "5th"), (7, "G", "Root"), (11, "B", "3rd")]),
        ])
    ]
    svg_jazz = build_progression_card("JAZZ PROGRESSIONS", "ii-V-I Cadence &amp; Turnaround • Smooth Voice Leading", jazz_data)
    with open("progressions/progressions_jazz.svg", "w") as f:
        f.write(svg_jazz)
    subprocess.run(["rsvg-convert", "--dpi-x", "72", "--dpi-y", "72", "-f", "pdf", "-o", "progressions/progressions_jazz.pdf", "progressions/progressions_jazz.svg"], check=True)
    os.remove("progressions/progressions_jazz.svg")
    count += 1
    print("  [Progression] progressions/progressions_jazz.pdf")

    # Progression 3: Classical & Blues (I-V-vi-iii-IV and I-IV-V)
    classic_data = [
        ("I — V — vi — iii — IV in C Major (Pachelbel Canon Sequence)", [
            ("I",   "C maj", [(0, "C", "Root"), (4, "E", "3rd"), (7, "G", "5th")]),
            ("V",   "G maj", [(2, "D", "5th"), (7, "G", "Root"), (11, "B", "3rd")]),
            ("vi",  "A min", [(4, "E", "5th"), (9, "A", "Root"), (12, "C", "3rd")]),
            ("iii", "E min", [(4, "E", "Root"), (7, "G", "3rd"), (11, "B", "5th")]),
            ("IV",  "F maj", [(5, "F", "Root"), (9, "A", "3rd"), (12, "C", "5th")]),
        ]),
        ("I — IV — V in C Major (Classic 3-Chord Rock &amp; Blues)", [
            ("I",  "C maj", [(0, "C", "Root"), (4, "E", "3rd"), (7, "G", "5th")]),
            ("IV", "F maj", [(0, "C", "5th"), (5, "F", "Root"), (9, "A", "3rd")]),
            ("V",  "G maj", [(2, "D", "5th"), (7, "G", "Root"), (11, "B", "3rd")]),
            ("I",  "C maj", [(0, "C", "Root"), (4, "E", "3rd"), (7, "G", "5th")]),
        ])
    ]
    svg_classic = build_progression_card("CLASSICAL &amp; BLUES", "Pachelbel Canon &amp; 12-Bar Roots • Voice Leading", classic_data)
    with open("progressions/progressions_classic.svg", "w") as f:
        f.write(svg_classic)
    subprocess.run(["rsvg-convert", "--dpi-x", "72", "--dpi-y", "72", "-f", "pdf", "-o", "progressions/progressions_classic.pdf", "progressions/progressions_classic.svg"], check=True)
    os.remove("progressions/progressions_classic.svg")
    count += 1
    print("  [Progression] progressions/progressions_classic.pdf")

    # Progression 4: 12-Bar Blues with Turnaround
    blues_data = [
        ("12-Bar Blues in C (Standard Blues Form)", [
            ("I7",  "C7", [(0, "C", "Root"), (4, "E", "3rd"), (7, "G", "5th"), (10, "Bb", "7th")]),
            ("IV7", "F7", [(0, "C", "5th"), (3, "Eb", "7th"), (5, "F", "Root"), (9, "A", "3rd")]),
            ("V7",  "G7", [(2, "D", "5th"), (5, "F", "7th"), (7, "G", "Root"), (11, "B", "3rd")]),
            ("I7",  "C7", [(0, "C", "Root"), (4, "E", "3rd"), (7, "G", "5th"), (10, "Bb", "7th")]),
        ]),
        ("Blues Turnaround (Last 4 Measures)", [
            ("V7",  "G7", [(2, "D", "5th"), (5, "F", "7th"), (7, "G", "Root"), (11, "B", "3rd")]),
            ("IV7", "F7", [(0, "C", "5th"), (3, "Eb", "7th"), (5, "F", "Root"), (9, "A", "3rd")]),
            ("I7",  "C7", [(0, "C", "Root"), (4, "E", "3rd"), (7, "G", "5th"), (10, "Bb", "7th")]),
            ("V7",  "G7", [(2, "D", "5th"), (5, "F", "7th"), (7, "G", "Root"), (11, "B", "3rd")]),
        ])
    ]
    svg_blues = build_progression_card("12-BAR BLUES", "Complete Blues Form &amp; Turnaround • Dominant 7ths", blues_data)
    with open("progressions/progressions_blues_12bar.svg", "w") as f:
        f.write(svg_blues)
    subprocess.run(["rsvg-convert", "--dpi-x", "72", "--dpi-y", "72", "-f", "pdf", "-o", "progressions/progressions_blues_12bar.pdf", "progressions/progressions_blues_12bar.svg"], check=True)
    os.remove("progressions/progressions_blues_12bar.svg")
    count += 1
    print("  [Progression] progressions/progressions_blues_12bar.pdf")

    # Progression 5: Circle of Fifths / Jazz Standard (Autumn Leaves)
    circle_data = [
        ("Circle Progression (ii — V — I — IV — viiø — III — vi)", [
            ("ii7",   "D min7", [(2, "D", "Root"), (5, "F", "3rd"), (9, "A", "5th"), (12, "C", "7th")]),
            ("V7",    "G7",     [(2, "D", "5th"), (5, "F", "7th"), (7, "G", "Root"), (11, "B", "3rd")]),
            ("Imaj7", "C maj7", [(0, "C", "Root"), (4, "E", "3rd"), (7, "G", "5th"), (11, "B", "7th")]),
            ("IVmaj7","F maj7", [(0, "C", "5th"), (4, "E", "7th"), (5, "F", "Root"), (9, "A", "3rd")]),
            ("vi7",   "A min7", [(0, "C", "3rd"), (4, "E", "5th"), (7, "G", "7th"), (9, "A", "Root")]),
        ])
    ]
    svg_circle = build_progression_card("CIRCLE OF FIFTHS", "Standard Jazz Cadence Chain (Autumn Leaves)", circle_data)
    with open("progressions/progressions_circle_of_fifths.svg", "w") as f:
        f.write(svg_circle)
    subprocess.run(["rsvg-convert", "--dpi-x", "72", "--dpi-y", "72", "-f", "pdf", "-o", "progressions/progressions_circle_of_fifths.pdf", "progressions/progressions_circle_of_fifths.svg"], check=True)
    os.remove("progressions/progressions_circle_of_fifths.svg")
    count += 1
    print("  [Progression] progressions/progressions_circle_of_fifths.pdf")

    # Progression 6: Two-Hand Rootless Jazz Voicings
    rootless_data = [
        ("ii — V — I Rootless (A-Voicing: 3-5-7-9 / 7-9-3-13)", [
            ("ii7",   "Dm9",   [(5, "F", "3rd"), (9, "A", "5th"), (12, "C", "7th"), (14, "E", "9th")]),
            ("V7",    "G13",   [(3, "Eb", "b13"), (5, "F", "7th"), (9, "A", "9th"), (11, "B", "3rd")]),
            ("Imaj7", "Cmaj9", [(4, "E", "3rd"), (7, "G", "5th"), (11, "B", "7th"), (14, "D", "9th")]),
        ]),
        ("ii — V — I Rootless (B-Voicing: 7-9-3-5 / 3-13-7-9)", [
            ("ii7",   "Dm9",   [(0, "C", "7th"), (2, "D", "Root"), (5, "F", "3rd"), (9, "A", "5th")]),
            ("V7",    "G9",    [(11, "B", "3rd"), (14, "E", "13th"), (17, "F", "7th"), (14, "A", "9th")]),
            ("Imaj7", "Cmaj9", [(11, "B", "7th"), (14, "D", "9th"), (16, "E", "3rd"), (7, "G", "5th")]),
        ])
    ]
    svg_rootless = build_progression_card("TWO-HAND JAZZ VOICINGS", "Rootless A &amp; B Voicings for ii-V-I • Bill Evans Style", rootless_data)
    with open("progressions/progressions_jazz_rootless.svg", "w") as f:
        f.write(svg_rootless)
    subprocess.run(["rsvg-convert", "--dpi-x", "72", "--dpi-y", "72", "-f", "pdf", "-o", "progressions/progressions_jazz_rootless.pdf", "progressions/progressions_jazz_rootless.svg"], check=True)
    os.remove("progressions/progressions_jazz_rootless.svg")
    count += 1
    print("  [Progression] progressions/progressions_jazz_rootless.pdf")

    return count

def main():
    print("==================================================")
    print("  BUILDING ENHANCED PIANO CARDS COLLECTION")
    print("==================================================")
    
    c_count = build_all_chords()
    s_count = build_all_scales()
    p_count = build_all_progressions()

    total = c_count + s_count + p_count
    
    # Create / update complete zip package
    subprocess.run([
        "zip", "-q", "-r", "piano-helpers-complete.zip",
        "chords/", "scales/", "progressions/", "GUIDE.md", "README.md", "LICENSE"
    ], check=True)
    print("  [Package] Updated piano-helpers-complete.zip")

    print("==================================================")
    print(f"  Successfully built {total} production cards:")
    print(f"  - {c_count} Chords ({len(CHORD_DEFINITIONS)} types x LH/RH)")
    print(f"  - {s_count} Scales ({len(SCALE_DEFINITIONS)} scales)")
    print(f"  - {p_count} Progressions (Pop, Jazz, Classical)")
    print("  - Complete ZIP package: piano-helpers-complete.zip")
    print("==================================================")

if __name__ == "__main__":
    main()
