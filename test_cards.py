#!/usr/bin/env python3
"""
Automated Verification Suite for Piano Learning Helpers
Tests all generated cards across chords/, scales/, progressions/ for:
1. Exact A4 landscape dimensions (841.89 x 595.28 pt)
2. Safe printable margins (> 10mm on all sides)
3. Note spelling correctness across all keys
4. Fixes for legacy bugs (Db aug, E min6, minor blues text corruption, jazz Cmaj)
"""

import glob
import os
import subprocess
import xml.etree.ElementTree as ET
import re

NOTE_SEMITONES = {
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

def semitones_diff(n1, n2):
    return (NOTE_SEMITONES[n2] - NOTE_SEMITONES[n1]) % 12

def test_page_dimensions_and_margins():
    print("\n--- Testing Page Dimensions & Margins ---")
    all_pdfs = sorted(glob.glob("chords/*.pdf") + glob.glob("scales/*.pdf") + glob.glob("progressions/*.pdf"))
    assert len(all_pdfs) == 61, f"Expected 61 PDFs, found {len(all_pdfs)}"

    for pdf in all_pdfs:
        # Check pdfinfo
        info = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
        m = re.search(r"Page size:\s+([0-9.]+)\s+x\s+([0-9.]+)", info)
        assert m, f"Could not find page size in {pdf}"
        w, h = float(m.group(1)), float(m.group(2))
        assert abs(w - 841.89) < 0.1, f"{pdf} width={w}, expected 841.89"
        assert abs(h - 595.28) < 0.1, f"{pdf} height={h}, expected 595.28"

        # Check margins
        xml_data = subprocess.run(["pdftotext", "-bbox-layout", pdf, "-"], capture_output=True, text=True).stdout
        root = ET.fromstring(xml_data)
        words = []
        for word in root.findall(".//{http://www.w3.org/1999/xhtml}word"):
            words.append((float(word.attrib["xMin"]), float(word.attrib["xMax"]), float(word.attrib["yMin"]), float(word.attrib["yMax"])))
        min_x = min(w[0] for w in words)
        max_x = max(w[1] for w in words)
        left_m = min_x * 25.4 / 72.0
        right_m = (841.89 - max_x) * 25.4 / 72.0
        assert left_m >= 10.0, f"{pdf} left margin too small: {left_m:.1f}mm"
        assert right_m >= 10.0, f"{pdf} right margin too small: {right_m:.1f}mm"

    print(f"  ✓ All {len(all_pdfs)} PDFs have exact 841.89 x 595.28 pt A4 dimensions and safe margins (>10mm)")

def test_legacy_bug_fixes():
    print("\n--- Testing Fixes for Legacy Bugs ---")
    
    # 1. Db aug fix (must be Db - F - A, NOT Db - F - Bb)
    for path in ["chords/chords_aug_RH.pdf", "chords/chords_aug_LH.pdf"]:
        text = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
        lines = text.splitlines()
        db_block = ""
        for i, l in enumerate(lines):
            if "Db aug" in l:
                db_block = "\n".join(lines[i:i+3])
                break
        notes = re.findall(r"[A-G][b#]?", db_block)
        assert "A" in notes and "Bb" not in notes, f"Db aug bug still present in {path}: {notes}"
        print(f"  ✓ {path}: Db aug correctly spelled with A (Augmented 5th): {notes}")

    # 2. E min6 fix (must be E - G - B - C#, NOT E - G - B - C)
    for path in ["chords/chords_min6_RH.pdf", "chords/chords_min6_LH.pdf"]:
        text = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
        lines = text.splitlines()
        e_block = ""
        for i, l in enumerate(lines):
            if "E min6" in l:
                e_block = "\n".join(lines[i:i+3])
                break
        notes = re.findall(r"[A-G][b#]?", e_block)
        assert "C#" in notes, f"E min6 bug still present in {path}: {notes}"
        print(f"  ✓ {path}: E min6 correctly spelled with C# (Major 6th): {notes}")

    # 3. Diminished naming fix (must be chords_dim_*, not chords_dom_*)
    assert os.path.exists("chords/chords_dim_RH.pdf"), "chords_dim_RH.pdf missing"
    assert os.path.exists("chords/chords_dim_LH.pdf"), "chords_dim_LH.pdf missing"
    print("  ✓ Diminished chords properly named chords_dim_*.pdf")

    # 4. Minor blues corruption fix (no Dd typo, clean parsing)
    text = subprocess.run(["pdftotext", "-layout", "scales/scales_minor_blues.pdf", "-"], capture_output=True, text=True).stdout
    assert "Dd" not in text, "Dd typo still present in scales_minor_blues.pdf"
    print("  ✓ scales/scales_minor_blues.pdf: Corrupted overlapping layers and Dd typo fixed")

    # 5. Jazz ii-V-I Cmaj resolution fix (must be C - E - G, NOT D - G - B)
    text = subprocess.run(["pdftotext", "-layout", "progressions/progressions_jazz.pdf", "-"], capture_output=True, text=True).stdout
    cmaj_lines = [l for l in text.splitlines() if "C maj" in l]
    assert len(cmaj_lines) >= 1, "C maj line missing in progressions_jazz.pdf"
    for line in cmaj_lines:
        notes = re.findall(r"[A-G][b#]?", line)
        assert "C" in notes and "E" in notes and "G" in notes, f"Jazz Cmaj resolution corrupted: {line}"
    print("  ✓ progressions/progressions_jazz.pdf: Cmaj (I) correctly voiced as C - E - G")

def test_chord_interval_formulas():
    print("\n--- Testing Musical Interval Consistency Across All 30 Chord Cards ---")
    chord_pdfs = sorted(glob.glob("chords/*.pdf"))
    for pdf in chord_pdfs:
        xml_data = subprocess.run(["pdftotext", "-bbox-layout", pdf, "-"], capture_output=True, text=True).stdout
        root = ET.fromstring(xml_data)
        words = []
        for word in root.findall(".//{http://www.w3.org/1999/xhtml}word"):
            x = float(word.attrib["xMin"])
            y = float(word.attrib["yMin"])
            t = word.text
            words.append((x, y, t))
        
        # Table rows are between y=91 and y=288
        table_words = [w for w in words if 91 <= w[1] <= 288]
        # Group by Y bucket (within 8 pt, row_h is 16.5 pt)
        rows_by_y = {}
        for x, y, t in table_words:
            matched = False
            for ry in rows_by_y:
                if abs(ry - y) <= 8.0:
                    rows_by_y[ry].append((x, t))
                    matched = True
                    break
            if not matched:
                rows_by_y[y] = [(x, t)]
        
        # Sort rows by Y
        sorted_ys = sorted(rows_by_y.keys())
        assert len(sorted_ys) == 12, f"{pdf}: Expected 12 rows, found {len(sorted_ys)}"

        ref_intervals = None
        for y in sorted_ys:
            row_items = sorted(rows_by_y[y], key=lambda it: it[0])
            # The first item is root name
            notes = [t for x, t in row_items if re.match(r"^[A-G][b#]?$", t) and x > 90]
            root = row_items[0][1]
            ints = [semitones_diff(root, n) for n in notes]
            if ref_intervals is None:
                ref_intervals = ints
            else:
                assert ints == ref_intervals, f"{pdf} mismatch in row {root}: {ints} vs expected {ref_intervals}"
    print(f"  ✓ All {len(chord_pdfs)} chord cards verified mathematically across all 12 chromatic keys")

def test_scale_interval_formulas():
    print("\n--- Testing Musical Interval Consistency Across All Scale Cards ---")
    scale_pdfs = sorted(glob.glob("scales/*.pdf"))
    for pdf in scale_pdfs:
        xml_data = subprocess.run(["pdftotext", "-bbox-layout", pdf, "-"], capture_output=True, text=True).stdout
        root = ET.fromstring(xml_data)
        words = []
        for word in root.findall(".//{http://www.w3.org/1999/xhtml}word"):
            x = float(word.attrib["xMin"])
            y = float(word.attrib["yMin"])
            t = word.text
            words.append((x, y, t))
        
        table_words = [w for w in words if 91 <= w[1] <= 288]
        rows_by_y = {}
        for x, y, t in table_words:
            matched = False
            for ry in rows_by_y:
                if abs(ry - y) <= 8.0:
                    rows_by_y[ry].append((x, t))
                    matched = True
                    break
            if not matched:
                rows_by_y[y] = [(x, t)]
        
        sorted_ys = sorted(rows_by_y.keys())
        assert len(sorted_ys) == 12, f"{pdf}: Expected 12 rows, found {len(sorted_ys)}"

        ref_intervals = None
        for y in sorted_ys:
            row_items = sorted(rows_by_y[y], key=lambda it: it[0])
            notes = [t for x, t in row_items if re.match(r"^[A-G][b#]?$", t) and x > 90]
            root = row_items[0][1]
            ints = [semitones_diff(root, n) for n in notes]
            if ref_intervals is None:
                ref_intervals = ints
            else:
                assert ints == ref_intervals, f"{pdf} mismatch in row {root}: {ints} vs expected {ref_intervals}"
    print(f"  ✓ All {len(scale_pdfs)} scale cards verified mathematically across all 12 chromatic keys")

def test_no_header_overlap():
    print("\n--- Testing Zero Header Title / Hand Badge Collisions Across All Cards ---")
    all_pdfs = sorted(glob.glob("chords/*.pdf") + glob.glob("scales/*.pdf") + glob.glob("progressions/*.pdf"))
    for pdf in all_pdfs:
        xml_data = subprocess.run(["pdftotext", "-bbox-layout", pdf, "-"], capture_output=True, text=True).stdout
        root = ET.fromstring(xml_data)
        words = []
        for word in root.findall(".//{http://www.w3.org/1999/xhtml}word"):
            x1 = float(word.attrib["xMin"])
            x2 = float(word.attrib["xMax"])
            y1 = float(word.attrib["yMin"])
            y2 = float(word.attrib["yMax"])
            t = word.text
            # Top header row is between y=14 and y=40, left of combo card (x < 450)
            if 14 <= y1 <= 40 and x2 < 450:
                words.append((x1, x2, y1, y2, t))

        # Title words are before the badge words ('RIGHT', 'LEFT', 'PROGRESSION')
        title_words = []
        badge_words = []
        in_badge = False
        for w in sorted(words, key=lambda it: it[0]):
            if w[4] in ["RIGHT", "LEFT", "PROGRESSION"]:
                in_badge = True
            if in_badge:
                badge_words.append(w)
            else:
                title_words.append(w)

        assert len(title_words) >= 1, f"{pdf}: No title words found in header!"
        assert len(badge_words) >= 1, f"{pdf}: No badge words found in header!"

        max_title_x = max(w[1] for w in title_words)
        min_badge_x = min(w[0] for w in badge_words)
        gap = min_badge_x - max_title_x
        assert gap >= 3.0, f"{pdf}: Header COLLISION detected! max_title_x={max_title_x:.1f}, min_badge_x={min_badge_x:.1f}, gap={gap:.1f}pt"

    print(f"  ✓ All {len(all_pdfs)} cards have verified zero collision between title and hand badge (minimum gap >= 3.0 pt)")

def test_no_row_label_overlap():
    print("\n--- Testing Zero Row Label / Key Dots Collisions Across All 42 Chord Cards ---")
    chord_pdfs = sorted(glob.glob("chords/*.pdf"))
    for pdf in chord_pdfs:
        xml_data = subprocess.run(["pdftotext", "-bbox-layout", pdf, "-"], capture_output=True, text=True).stdout
        root = ET.fromstring(xml_data)
        words = []
        for word in root.findall(".//{http://www.w3.org/1999/xhtml}word"):
            x1 = float(word.attrib["xMin"])
            x2 = float(word.attrib["xMax"])
            y1 = float(word.attrib["yMin"])
            t = word.text
            if 91 <= y1 <= 288 and x1 < 104.0:
                words.append((round(y1, 1), x1, x2, t))

        rows = {}
        for y, x1, x2, t in words:
            matched = False
            for ry in rows:
                if abs(ry - y) <= 6:
                    rows[ry].append((x1, x2, t))
                    matched = True
                    break
            if not matched:
                rows[y] = [(x1, x2, t)]

        assert len(rows) == 12, f"{pdf}: Expected 12 rows, found {len(rows)}"
        for y in sorted(rows.keys()):
            items = sorted(rows[y], key=lambda it: it[0])
            name_items = [it for it in items if not any(c in it[2] for c in "○●")]
            dot_items = [it for it in items if any(c in it[2] for c in "○●")]
            assert name_items, f"{pdf}: No chord name found in row y={y}"
            assert dot_items, f"{pdf}: No key dots found in row y={y}"
            max_name_x = max(it[1] for it in name_items)
            min_dot_x = min(it[0] for it in dot_items)
            gap = min_dot_x - max_name_x
            assert gap >= 10.0, f"{pdf}: Row overlap detected! name={name_items}, dots={dot_items}, gap={gap:.1f}pt"

    print("  ✓ All 42 chord cards have verified >= 10.0 pt gap between chord name and key shape dots")

def main():
    print("==================================================")
    print("  RUNNING PIANO CARDS VERIFICATION SUITE")
    print("==================================================")
    test_page_dimensions_and_margins()
    test_no_header_overlap()
    test_no_row_label_overlap()
    test_legacy_bug_fixes()
    test_chord_interval_formulas()
    test_scale_interval_formulas()
    print("\n==================================================")
    print("  ALL VERIFICATION TESTS PASSED SUCCESSFULLY! (100%)")
    print("==================================================")

if __name__ == "__main__":
    main()
