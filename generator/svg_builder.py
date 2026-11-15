"""
SVG & PDF Vector Builder for Piano Learning Helpers
Renders calibrated, publication-grade Unified Matrix guides for chords, scales, and progressions.
"""

from generator.music_theory import (
    ROOT_KEYS, NOTE_NAMES_FROM_C, NOTE_TO_SEMITONE,
    is_black_semitone, get_note_name,
    CHORD_DEFINITIONS, SCALE_DEFINITIONS
)

PAGE_W = 841.89  # A4 Landscape width in points (297 mm)
PAGE_H = 595.28  # A4 Landscape height in points (210 mm)

# Exact calibrated Roland FP-30X key pitch: 13.79mm per semitone (39.08 pt)
COL_W = 39.08
LABEL_COL_W = 72.0
NUM_COLS = 18

TOTAL_TABLE_W = LABEL_COL_W + NUM_COLS * COL_W  # 775.44 pt (273.5 mm)
LEFT_MARGIN = (PAGE_W - TOTAL_TABLE_W) / 2.0     # ~33.2 pt (~11.7 mm safe margin)

THEME = {
    "bg": "#FFFFFF",
    "card_bg": "#F8FAFC",
    "border": "#E2E8F0",
    "border_strong": "#94A3B8",
    "octave_line": "#475569",
    "text_primary": "#0F172A",
    "text_secondary": "#334155",
    "text_muted": "#64748B",
    "accent": "#DC2626",          # Crimson
    "row_even_white": "#FFFFFF",
    "row_odd_white": "#F8FAFC",
    "row_even_black": "#F1F5F9",  # Zebra rail
    "row_odd_black": "#E2E8F0",
    "root_color": "#DC2626",      # Crimson
    "third_color": "#D97706",     # Warm Amber
    "fifth_color": "#059669",     # Emerald
    "seventh_color": "#2563EB",   # Royal Blue
    "kb_white_key": "#FFFFFF",
    "kb_white_stroke": "#94A3B8",
    "kb_black_key": "#1E293B",    # Ebony
    "kb_black_stroke": "#0F172A",
    "ebony_badge_bg": "#1E293B",
    "ivory_badge_bg": "#FFFFFF",
}

def get_accent_color_for_degree(deg_str):
    t = THEME
    if "Root" in deg_str or "1" in deg_str:
        return t["root_color"]
    elif "3" in deg_str or "2" in deg_str or "4" in deg_str:
        return t["third_color"]
    elif "5" in deg_str or "6" in deg_str:
        return t["fifth_color"]
    else:
        return t["seventh_color"]

def estimate_text_width(text, font_size):
    w = 0.0
    for ch in text:
        if ch in 'Ili1|! ':
            w += font_size * 0.35
        elif ch in 'MWm':
            w += font_size * 0.95
        elif ch in 'ABCDEFGHKNOPQRSTUVXYZ()0123456789♭♯-':
            w += font_size * 0.72
        else:
            w += font_size * 0.62
    return w

def render_header(title, hand_label, subtitle, legend_type="chord"):
    t = THEME
    svg = []
    
    combo_w = 345.0
    combo_x = LEFT_MARGIN + TOTAL_TABLE_W - combo_w
    max_header_w = combo_x - LEFT_MARGIN - 14.0

    clean_title = title.replace('&amp;', '&')
    clean_hand = hand_label.replace('&amp;', '&')
    badge_w = 112.0 if ('LEFT' in clean_hand and 'RIGHT' in clean_hand) else 80.0
    avail_for_title = max_header_w - badge_w - 14.0

    fs = 18.0
    while estimate_text_width(clean_title, fs) > avail_for_title and fs > 12.0:
        fs -= 0.5

    tw = estimate_text_width(clean_title, fs)
    badge_x = tw + 12.0
    badge_center_x = badge_x + badge_w / 2.0

    # Left: Title Block with dynamically positioned hand badge
    svg.append(f'''
    <g transform="translate({LEFT_MARGIN}, 16)">
      <text class="font-sans fw-heavy" x="0" y="20" font-size="{fs}" letter-spacing="-0.3" fill="{t["text_primary"]}">{title}</text>
      <rect x="{badge_x:.1f}" y="5" width="{badge_w}" height="19" rx="9.5" fill="{t["accent"]}" opacity="0.12"/>
      <text class="font-sans fw-bold" x="{badge_center_x:.1f}" y="18" font-size="8" letter-spacing="0.2" fill="{t["accent"]}" text-anchor="middle">{hand_label}</text>
      <text class="font-sans fw-regular" x="0" y="38" font-size="9" fill="{t["text_secondary"]}">{subtitle}</text>
    </g>
    ''')

    # Right: Combined Legend + Hand Diagram
    combo_w = 345
    combo_x = LEFT_MARGIN + TOTAL_TABLE_W - combo_w
    combo_h = 44
    
    finger_nums = [("1", t["root_color"]), ("2", t["card_bg"]), ("3", t["third_color"]), ("4", t["card_bg"]), ("5", t["fifth_color"])]
    hand_caption = "1=Thumb • 3=Mid • 5=Pinky" if "RIGHT" in hand_label else "5=Pinky • 3=Mid • 1=Thumb"

    svg.append(f'''
    <g transform="translate({combo_x}, 12)">
      <rect width="{combo_w}" height="{combo_h}" rx="5" fill="{t["card_bg"]}" stroke="{t["border"]}" stroke-width="1"/>
      
      <!-- Key Types -->
      <text class="font-sans fw-bold" x="12" y="12" font-size="6.5" letter-spacing="0.6" fill="{t["text_muted"]}">KEY TYPES</text>
      <text class="font-sans fw-semibold" x="12" y="24" font-size="7.5" fill="{t["text_primary"]}">○ = White Key    ● = Black Key</text>
      <text class="font-sans fw-regular" x="12" y="34" font-size="6" fill="{t["text_muted"]}">(e.g. D is ○●○ = White • Black • White)</text>

      <line x1="142" y1="6" x2="142" y2="38" stroke="{t["border"]}" stroke-width="1"/>

      <!-- Tones -->
      <text class="font-sans fw-bold" x="152" y="12" font-size="6.5" letter-spacing="0.6" fill="{t["text_muted"]}">TONE COLORS</text>
      <circle cx="158" cy="22" r="3" fill="{t["root_color"]}"/>
      <text class="font-sans fw-semibold" x="165" y="24.5" font-size="6.5" fill="{t["text_primary"]}">Root</text>
      <circle cx="158" cy="33" r="3" fill="{t["third_color"]}"/>
      <text class="font-sans fw-semibold" x="165" y="35.5" font-size="6.5" fill="{t["text_primary"]}">3rd / 2nd</text>
      <circle cx="204" cy="22" r="3" fill="{t["fifth_color"]}"/>
      <text class="font-sans fw-semibold" x="211" y="24.5" font-size="6.5" fill="{t["text_primary"]}">5th</text>
      <circle cx="204" cy="33" r="3" fill="{t["seventh_color"]}"/>
      <text class="font-sans fw-semibold" x="211" y="35.5" font-size="6.5" fill="{t["text_primary"]}">7th / 6th</text>

      <line x1="250" y1="6" x2="250" y2="38" stroke="{t["border"]}" stroke-width="1"/>

      <!-- Hand diagram -->
      <text class="font-sans fw-bold" x="296" y="12" font-size="6.5" letter-spacing="0.6" fill="{t["text_muted"]}" text-anchor="middle">{"RH FINGERS" if "RIGHT" in hand_label else "LH FINGERS"}</text>
      <g transform="translate(258, 15)">
    ''')

    for i, (fn, col) in enumerate(finger_nums):
        cx = 8 + i * 14
        cy = [14, 8, 5, 8, 12][i]
        r = 3.8
        is_fill = (col != t["card_bg"])
        svg.append(f'''
        <circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" stroke="{t["border_strong"] if not is_fill else 'none'}" stroke-width="0.7"/>
        <text class="font-sans fw-bold" x="{cx}" y="{cy + 2.2}" font-size="5.5" fill="{'#FFFFFF' if is_fill else t['text_secondary']}" text-anchor="middle">{fn}</text>
        ''')

    svg.append(f'''
      </g>
      <text class="font-sans fw-regular" x="296" y="38" font-size="5" fill="{t["text_muted"]}" text-anchor="middle">{hand_caption}</text>
    </g>
    ''')
    return '\n'.join(svg)

def render_bottom_keyboard_and_stand(inv_top, inv_row_h, inversions_data, active_chord_tones):
    t = THEME
    svg = []

    # Inversion rows
    svg.append(f'<g transform="translate({LEFT_MARGIN}, {inv_top})">')
    for idx, (name, finger_desc, active_map) in enumerate(inversions_data):
        inv_y = idx * inv_row_h
        bar_color = t["root_color"] if "ROOT" in name else (t["third_color"] if "1ST" in name else t["fifth_color"])
        svg.append(f'''
          <rect x="0" y="{inv_y}" width="{LABEL_COL_W}" height="{inv_row_h}" fill="{bar_color}" stroke="{t["border"]}" stroke-width="0.5"/>
          <text class="font-sans fw-heavy" x="{LABEL_COL_W/2}" y="{inv_y + 8.5}" font-size="6.5" fill="#FFFFFF" text-anchor="middle">{name}</text>
          <text class="font-sans fw-semibold" x="{LABEL_COL_W/2}" y="{inv_y + 15}" font-size="5" fill="#FFFFFF" text-anchor="middle">{finger_desc}</text>
        ''')

        svg.append(f'<g transform="translate({LABEL_COL_W}, {inv_y})">')
        for col in range(NUM_COLS):
            cx = col * COL_W
            black = is_black_semitone(col)
            bg = t["row_even_black"] if black else t["card_bg"]
            if col in active_map:
                finger = active_map[col]
                svg.append(f'''
                <rect x="{cx + 1}" y="1" width="{COL_W - 2}" height="{inv_row_h - 2}" rx="2" fill="{bar_color}" filter="url(#badge-shadow)"/>
                <text class="font-sans fw-heavy" x="{cx + COL_W/2}" y="{inv_row_h - 5.5}" font-size="9" fill="#FFFFFF" text-anchor="middle">{finger}</text>
                ''')
            else:
                svg.append(f'<rect x="{cx}" y="0" width="{COL_W}" height="{inv_row_h}" fill="{bg}" stroke="{t["border"]}" stroke-width="0.5"/>')
        svg.append('</g>')
    svg.append('</g>')

    # Piano Keyboard Bed
    kb_top = inv_top + inv_row_h * len(inversions_data)
    kb_h = 44.0

    svg.append(f'<g transform="translate({LEFT_MARGIN}, {kb_top})">')
    svg.append(f'''
      <rect x="0" y="0" width="{LABEL_COL_W}" height="{kb_h}" fill="{t["card_bg"]}" stroke="{t["border_strong"]}" stroke-width="0.8"/>
      <text class="font-sans fw-heavy" x="{LABEL_COL_W/2}" y="18" font-size="7.5" fill="{t["text_primary"]}" text-anchor="middle">PIANO KEYS</text>
      <text class="font-sans fw-bold" x="{LABEL_COL_W/2}" y="28" font-size="6" fill="{t["accent"]}" text-anchor="middle">ALIGNMENT</text>
      <text class="font-sans fw-medium" x="{LABEL_COL_W/2}" y="37" font-size="5" fill="{t["text_muted"]}" text-anchor="middle">Touch fallboard</text>
    ''')

    # White keys
    svg.append(f'<g transform="translate({LABEL_COL_W}, 0)">')
    for col in range(NUM_COLS):
        cx = col * COL_W
        black = is_black_semitone(col)
        note_name = NOTE_NAMES_FROM_C[col]
        is_active = (col in active_chord_tones)

        if not black:
            tone_tint = ""
            if is_active:
                indicator_c = t["root_color"] if col in (0, 12) else (t["third_color"] if col in (4, 16, 2, 3, 5) else t["fifth_color"])
                tone_tint = f'''
                <circle cx="{cx + COL_W/2}" cy="{kb_h - 10}" r="5.5" fill="{indicator_c}"/>
                <text class="font-sans fw-heavy" x="{cx + COL_W/2}" y="{kb_h - 7.5}" font-size="6.5" fill="#FFFFFF" text-anchor="middle">{note_name}</text>
                '''
            else:
                tone_tint = f'''
                <text class="font-sans fw-bold" x="{cx + COL_W/2}" y="{kb_h - 8}" font-size="7" fill="{t["text_muted"]}" text-anchor="middle">{note_name}</text>
                '''

            svg.append(f'''
            <rect x="{cx + 0.5}" y="0" width="{COL_W - 1}" height="{kb_h}" rx="2" fill="{t["kb_white_key"]}" stroke="{t["kb_white_stroke"]}" stroke-width="1.2"/>
            {tone_tint}
            ''')
        else:
            svg.append(f'<rect x="{cx + 0.5}" y="0" width="{COL_W - 1}" height="{kb_h}" rx="2" fill="{t["row_even_black"]}" stroke="{t["border"]}" stroke-width="0.5"/>')

    # Black keys
    black_key_h = kb_h * 0.62
    black_key_w = COL_W * 0.74
    for col in range(NUM_COLS):
        if is_black_semitone(col):
            cx = col * COL_W + (COL_W - black_key_w) / 2.0
            note_name = NOTE_NAMES_FROM_C[col]
            svg.append(f'''
            <rect x="{cx}" y="0" width="{black_key_w}" height="{black_key_h}" rx="2" fill="{t["kb_black_key"]}" stroke="{t["kb_black_stroke"]}" stroke-width="1" filter="url(#black-key-shadow)"/>
            <text class="font-sans fw-bold" x="{col * COL_W + COL_W/2}" y="{black_key_h - 6}" font-size="6" fill="#FFFFFF" text-anchor="middle">{note_name}</text>
            ''')
    svg.append('</g>')
    svg.append('</g>')

    # Octave boundary line
    octave_x = LEFT_MARGIN + LABEL_COL_W + 12 * COL_W
    svg.append(f'<line x1="{octave_x}" y1="68" x2="{octave_x}" y2="{kb_top + kb_h}" stroke="{t["octave_line"]}" stroke-width="1.8"/>')

    # Root Pointer Notch on Column 0
    root_col_center_x = LEFT_MARGIN + LABEL_COL_W + COL_W / 2.0
    svg.append(f'''
    <g transform="translate({root_col_center_x}, {kb_top + kb_h})">
      <polygon points="-5,0 5,0 0,6" fill="{t["root_color"]}"/>
      <rect x="-18" y="7" width="36" height="12" rx="2" fill="{t["root_color"]}"/>
      <text class="font-sans fw-heavy" x="0" y="15.5" font-size="6" fill="#FFFFFF" text-anchor="middle" letter-spacing="0.5">ROOT</text>
    </g>
    ''')

    # Base fold line & stand instructions
    fold_y2 = kb_top + kb_h + 3.0
    svg.append(f'''
    <g transform="translate(0, {fold_y2})">
      <line x1="{LEFT_MARGIN}" y1="0" x2="{root_col_center_x - 22}" y2="0" stroke="{t["accent"]}" stroke-width="1" stroke-dasharray="4,3"/>
      <line x1="{root_col_center_x + 22}" y1="0" x2="{LEFT_MARGIN + TOTAL_TABLE_W}" y2="0" stroke="{t["accent"]}" stroke-width="1" stroke-dasharray="4,3"/>
      <text class="font-sans fw-heavy" x="{PAGE_W/2 + 20}" y="11" font-size="7" fill="{t["accent"]}" letter-spacing="1" text-anchor="middle">▼ FOLD FORWARD 90° HERE — KEYS REST DIRECTLY BEHIND PIANO KEYS ▼</text>
    </g>
    ''')

    flap_y = fold_y2 + 24.0
    flap_h = 68.0
    svg.append(f'''
    <g transform="translate({LEFT_MARGIN}, {flap_y})">
      <rect width="{TOTAL_TABLE_W}" height="{flap_h}" rx="6" fill="{t["card_bg"]}" stroke="{t["border"]}" stroke-width="1"/>
      <path d="M 0 10 L 0 0 L 10 0" stroke="{t["border_strong"]}" stroke-width="1" fill="none"/>
      <path d="M {TOTAL_TABLE_W} 10 L {TOTAL_TABLE_W} 0 L {TOTAL_TABLE_W - 10} 0" stroke="{t["border_strong"]}" stroke-width="1" fill="none"/>
      <path d="M 0 {flap_h - 10} L 0 {flap_h} L 10 {flap_h}" stroke="{t["border_strong"]}" stroke-width="1" fill="none"/>
      <path d="M {TOTAL_TABLE_W} {flap_h - 10} L {TOTAL_TABLE_W} {flap_h} L {TOTAL_TABLE_W - 10} {flap_h}" stroke="{t["border_strong"]}" stroke-width="1" fill="none"/>

      <text class="font-sans fw-heavy" x="16" y="18" font-size="8.5" fill="{t["text_primary"]}">HOW TO USE THIS CARD ON YOUR PIANO / KEYBOARD:</text>
      <text class="font-sans fw-medium" x="16" y="32" font-size="7.5" fill="{t["text_secondary"]}">1. Fold this bottom flap forward 90° along the red dashed line so the card stands upright behind your piano keys.</text>
      <text class="font-sans fw-medium" x="16" y="44" font-size="7.5" fill="{t["text_secondary"]}">2. C Major Alignment: Place the red <tspan fill="{t["root_color"]}" font-weight="700">▼ ROOT ▼</tspan> pointer directly over any C key. The drawn keys will match your Roland keyboard 1:1.</text>
      <text class="font-sans fw-medium" x="16" y="56" font-size="7.5" fill="{t["text_secondary"]}">3. Transposition: To play in another key, slide the <tspan fill="{t["root_color"]}" font-weight="700">▼ ROOT ▼</tspan> pointer over that key (D, E♭, F, G, etc.) and read across that chord's row.</text>
      <text class="font-sans fw-regular" x="{TOTAL_TABLE_W - 16}" y="56" font-size="6.5" fill="{t["text_muted"]}" text-anchor="end">PIANO LEARNING HELPERS • ENHANCED UNIFIED MATRIX • MIT LICENSE</text>
    </g>
    ''')
    return '\n'.join(svg)

def build_chord_card(chord_key, hand="RH"):
    """Builds a complete Unified Matrix chord card SVG."""
    t = THEME
    cdef = CHORD_DEFINITIONS[chord_key]
    hand_title = "RIGHT HAND" if hand == "RH" else "LEFT HAND"
    inversions = [(name, desc, active_map) for name, desc, active_map in (cdef["rh_inversions"] if hand == "RH" else cdef["lh_inversions"])]

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {PAGE_W} {PAGE_H}" width="{PAGE_W}" height="{PAGE_H}">']
    svg.append('<defs>')
    svg.append('''
      <style>
        .font-sans { font-family: "Avenir Next", "Helvetica Neue", Inter, Arial, sans-serif; }
        .fw-regular { font-weight: 400; }
        .fw-medium { font-weight: 500; }
        .fw-semibold { font-weight: 600; }
        .fw-bold { font-weight: 700; }
        .fw-heavy { font-weight: 800; }
      </style>
      <filter id="badge-shadow" x="-8%" y="-8%" width="116%" height="116%">
        <feDropShadow dx="0" dy="0.75" stdDeviation="0.6" flood-opacity="0.12"/>
      </filter>
      <filter id="black-key-shadow" x="-10%" y="-10%" width="120%" height="120%">
        <feDropShadow dx="0" dy="1.5" stdDeviation="1" flood-opacity="0.28"/>
      </filter>
    ''')
    svg.append('</defs>')
    svg.append(f'<rect width="{PAGE_W}" height="{PAGE_H}" fill="{t["bg"]}"/>')

    # Top Header
    subtitle = f"Formula: {cdef['formula_text']} ({cdef['formula_desc']}) • Pitch: {cdef['intervals_text']}"
    svg.append(render_header(cdef["title"], hand_title, subtitle, "chord"))

    # Table Grid
    grid_top = 68.0
    row_h = 16.5
    header_h = 24.0

    svg.append(f'<g transform="translate({LEFT_MARGIN}, {grid_top})">')
    svg.append(f'''
      <rect x="0" y="0" width="{LABEL_COL_W}" height="{header_h}" fill="{t["card_bg"]}" stroke="{t["border"]}" stroke-width="0.5"/>
      <text class="font-sans fw-bold" x="{LABEL_COL_W/2}" y="11" font-size="7.5" fill="{t["text_primary"]}" text-anchor="middle">CHORD</text>
      <text class="font-sans fw-medium" x="{LABEL_COL_W/2}" y="20" font-size="6" fill="{t["text_muted"]}" text-anchor="middle">{cdef["intervals_text"]} • Key</text>
    ''')

    for col in range(NUM_COLS):
        cx = LABEL_COL_W + col * COL_W
        is_chord_tone = (col in cdef["semitones"])
        desc_idx = cdef["semitones"].index(col) if is_chord_tone else -1
        deg_label = cdef["degree_names"][desc_idx] if is_chord_tone else f"+{col}"

        black = is_black_semitone(col)
        hdr_bg = t["row_even_black"] if black else t["card_bg"]
        hdr_color = t["text_primary"] if is_chord_tone else t["text_muted"]
        hdr_weight = "fw-heavy" if is_chord_tone else "fw-medium"

        svg.append(f'<rect x="{cx}" y="0" width="{COL_W}" height="{header_h}" fill="{hdr_bg}" stroke="{t["border"]}" stroke-width="0.5"/>')
        svg.append(f'<text class="font-sans {hdr_weight}" x="{cx + COL_W/2}" y="10" font-size="7.5" fill="{hdr_color}" text-anchor="middle">+{col}</text>')
        deg_fill = t["accent"] if is_chord_tone else t["text_muted"]
        svg.append(f'<text class="font-sans fw-bold" x="{cx + COL_W/2}" y="19.5" font-size="6.5" fill="{deg_fill}" text-anchor="middle">{deg_label}</text>')
    svg.append('</g>')

    # 12 Chord Rows
    data_start_y = grid_top + header_h
    for row_idx, (root_name, root_st) in enumerate(ROOT_KEYS):
        ry = data_start_y + row_idx * row_h
        is_even = (row_idx % 2 == 0)
        chord_label = f"{root_name} {cdef['suffix']}"

        # Calculate tactile dots for the first 3 or 4 tones
        tones_to_check = cdef["semitones"][:3] if len(cdef["semitones"]) >= 3 else cdef["semitones"]
        tactile_dots = []
        for st in tones_to_check:
            abs_st = (root_st + st) % 12
            tactile_dots.append("●" if is_black_semitone(abs_st) else "○")
        tactile_shape = "".join(tactile_dots)

        svg.append(f'<g transform="translate({LEFT_MARGIN}, {ry})">')
        lbl_bg = t["row_even_white"] if is_even else t["row_odd_white"]
        svg.append(f'<rect x="0" y="0" width="{LABEL_COL_W}" height="{row_h}" fill="{lbl_bg}" stroke="{t["border"]}" stroke-width="0.5"/>')
        svg.append(f'<text class="font-sans fw-bold" x="5" y="11.5" font-size="7.5" fill="{t["text_primary"]}">{chord_label}</text>')
        svg.append(f'<text class="font-sans fw-bold" x="{LABEL_COL_W - 4}" y="11.5" font-size="6" fill="{t["text_secondary"]}" text-anchor="end" letter-spacing="0.4">{tactile_shape}</text>')

        # 18 Semitone cells
        chord_tones_dict = {}
        for st_idx, st in enumerate(cdef["semitones"]):
            if st < NUM_COLS:
                note_name = get_note_name(root_name, st)
                deg_name = cdef["degree_names"][st_idx]
                chord_tones_dict[st] = (note_name, deg_name)

        for col in range(NUM_COLS):
            cx = LABEL_COL_W + col * COL_W
            black = is_black_semitone(col)
            cell_bg = (t["row_even_black"] if is_even else t["row_odd_black"]) if black else (t["row_even_white"] if is_even else t["row_odd_white"])
            svg.append(f'<rect x="{cx}" y="0" width="{COL_W}" height="{row_h}" fill="{cell_bg}" stroke="{t["border"]}" stroke-width="0.5"/>')

            if col in chord_tones_dict:
                note_name, deg_name = chord_tones_dict[col]
                abs_st = (root_st + col) % 12
                is_black_note = is_black_semitone(abs_st)
                accent_c = get_accent_color_for_degree(deg_name)

                bw = COL_W - 6
                bh = row_h - 3
                bx = cx + 3
                by = 1.5

                if is_black_note:
                    svg.append(f'''
                    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="3.5" fill="{t["ebony_badge_bg"]}" stroke="{accent_c}" stroke-width="1.2" filter="url(#badge-shadow)"/>
                    <text class="font-sans fw-bold" x="{cx + COL_W/2 - 4}" y="{by + 9}" font-size="8.5" fill="#FFFFFF" text-anchor="middle">{note_name}</text>
                    <text class="font-sans fw-bold" x="{cx + COL_W/2 + bw/2 - 4.5}" y="{by + 8}" font-size="5" fill="{accent_c}">●</text>
                    ''')
                else:
                    svg.append(f'''
                    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="3.5" fill="{t["ivory_badge_bg"]}" stroke="{accent_c}" stroke-width="1.2" filter="url(#badge-shadow)"/>
                    <text class="font-sans fw-bold" x="{cx + COL_W/2 - 4}" y="{by + 9}" font-size="8.5" fill="{accent_c}" text-anchor="middle">{note_name}</text>
                    <text class="font-sans fw-bold" x="{cx + COL_W/2 + bw/2 - 4.5}" y="{by + 8}" font-size="5" fill="{accent_c}">○</text>
                    ''')

        svg.append('</g>')

    table_bottom = data_start_y + len(ROOT_KEYS) * row_h
    inv_row_h = 18.0
    active_chord_tones = cdef["semitones"]

    svg.append(render_bottom_keyboard_and_stand(table_bottom, inv_row_h, inversions, active_chord_tones))
    svg.append('</svg>')
    return '\n'.join(svg)

def build_scale_card(scale_key):
    """Builds a complete Unified Matrix scale card SVG."""
    t = THEME
    sdef = SCALE_DEFINITIONS[scale_key]

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {PAGE_W} {PAGE_H}" width="{PAGE_W}" height="{PAGE_H}">']
    svg.append('<defs>')
    svg.append('''
      <style>
        .font-sans { font-family: "Avenir Next", "Helvetica Neue", Inter, Arial, sans-serif; }
        .fw-regular { font-weight: 400; }
        .fw-medium { font-weight: 500; }
        .fw-semibold { font-weight: 600; }
        .fw-bold { font-weight: 700; }
        .fw-heavy { font-weight: 800; }
      </style>
      <filter id="badge-shadow" x="-8%" y="-8%" width="116%" height="116%">
        <feDropShadow dx="0" dy="0.75" stdDeviation="0.6" flood-opacity="0.12"/>
      </filter>
      <filter id="black-key-shadow" x="-10%" y="-10%" width="120%" height="120%">
        <feDropShadow dx="0" dy="1.5" stdDeviation="1" flood-opacity="0.28"/>
      </filter>
    ''')
    svg.append('</defs>')
    svg.append(f'<rect width="{PAGE_W}" height="{PAGE_H}" fill="{t["bg"]}"/>')

    # Top Header
    subtitle = f"Formula: {sdef['formula_text']} • Intervals: {sdef['intervals_text']}"
    svg.append(render_header(sdef["title"], "RIGHT &amp; LEFT HAND", subtitle, "scale"))

    # Table Grid
    grid_top = 68.0
    row_h = 16.5
    header_h = 24.0

    svg.append(f'<g transform="translate({LEFT_MARGIN}, {grid_top})">')
    svg.append(f'''
      <rect x="0" y="0" width="{LABEL_COL_W}" height="{header_h}" fill="{t["card_bg"]}" stroke="{t["border"]}" stroke-width="0.5"/>
      <text class="font-sans fw-bold" x="{LABEL_COL_W/2}" y="11" font-size="7.5" fill="{t["text_primary"]}" text-anchor="middle">KEY</text>
      <text class="font-sans fw-medium" x="{LABEL_COL_W/2}" y="20" font-size="6" fill="{t["text_muted"]}" text-anchor="middle">Scale Degrees</text>
    ''')

    for col in range(NUM_COLS):
        cx = LABEL_COL_W + col * COL_W
        is_scale_tone = (col in sdef["semitones"])
        desc_idx = sdef["semitones"].index(col) if is_scale_tone else -1
        deg_label = sdef["degree_names"][desc_idx] if is_scale_tone else f"+{col}"

        black = is_black_semitone(col)
        hdr_bg = t["row_even_black"] if black else t["card_bg"]
        hdr_color = t["text_primary"] if is_scale_tone else t["text_muted"]
        hdr_weight = "fw-heavy" if is_scale_tone else "fw-medium"

        svg.append(f'<rect x="{cx}" y="0" width="{COL_W}" height="{header_h}" fill="{hdr_bg}" stroke="{t["border"]}" stroke-width="0.5"/>')
        svg.append(f'<text class="font-sans {hdr_weight}" x="{cx + COL_W/2}" y="10" font-size="7.5" fill="{hdr_color}" text-anchor="middle">+{col}</text>')
        deg_fill = t["accent"] if is_scale_tone else t["text_muted"]
        svg.append(f'<text class="font-sans fw-bold" x="{cx + COL_W/2}" y="19.5" font-size="6.5" fill="{deg_fill}" text-anchor="middle">{deg_label}</text>')
    svg.append('</g>')

    # 12 Scale Rows
    data_start_y = grid_top + header_h
    for row_idx, (root_name, root_st) in enumerate(ROOT_KEYS):
        ry = data_start_y + row_idx * row_h
        is_even = (row_idx % 2 == 0)

        svg.append(f'<g transform="translate({LEFT_MARGIN}, {ry})">')
        lbl_bg = t["row_even_white"] if is_even else t["row_odd_white"]
        svg.append(f'<rect x="0" y="0" width="{LABEL_COL_W}" height="{row_h}" fill="{lbl_bg}" stroke="{t["border"]}" stroke-width="0.5"/>')
        svg.append(f'<text class="font-sans fw-bold" x="{LABEL_COL_W/2}" y="11.5" font-size="8.5" fill="{t["text_primary"]}" text-anchor="middle">{root_name}</text>')

        scale_tones_dict = {}
        for st_idx, st in enumerate(sdef["semitones"]):
            if st < NUM_COLS:
                note_name = get_note_name(root_name, st)
                deg_name = sdef["degree_names"][st_idx]
                scale_tones_dict[st] = (note_name, deg_name)

        for col in range(NUM_COLS):
            cx = LABEL_COL_W + col * COL_W
            black = is_black_semitone(col)
            cell_bg = (t["row_even_black"] if is_even else t["row_odd_black"]) if black else (t["row_even_white"] if is_even else t["row_odd_white"])
            svg.append(f'<rect x="{cx}" y="0" width="{COL_W}" height="{row_h}" fill="{cell_bg}" stroke="{t["border"]}" stroke-width="0.5"/>')

            if col in scale_tones_dict:
                note_name, deg_name = scale_tones_dict[col]
                abs_st = (root_st + col) % 12
                is_black_note = is_black_semitone(abs_st)
                accent_c = get_accent_color_for_degree(deg_name)

                bw = COL_W - 6
                bh = row_h - 3
                bx = cx + 3
                by = 1.5

                if is_black_note:
                    svg.append(f'''
                    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="3.5" fill="{t["ebony_badge_bg"]}" stroke="{accent_c}" stroke-width="1.2" filter="url(#badge-shadow)"/>
                    <text class="font-sans fw-bold" x="{cx + COL_W/2 - 4}" y="{by + 9}" font-size="8.5" fill="#FFFFFF" text-anchor="middle">{note_name}</text>
                    <text class="font-sans fw-bold" x="{cx + COL_W/2 + bw/2 - 4.5}" y="{by + 8}" font-size="5" fill="{accent_c}">●</text>
                    ''')
                else:
                    svg.append(f'''
                    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="3.5" fill="{t["ivory_badge_bg"]}" stroke="{accent_c}" stroke-width="1.2" filter="url(#badge-shadow)"/>
                    <text class="font-sans fw-bold" x="{cx + COL_W/2 - 4}" y="{by + 9}" font-size="8.5" fill="{accent_c}" text-anchor="middle">{note_name}</text>
                    <text class="font-sans fw-bold" x="{cx + COL_W/2 + bw/2 - 4.5}" y="{by + 8}" font-size="5" fill="{accent_c}">○</text>
                    ''')

        svg.append('</g>')

    table_bottom = data_start_y + len(ROOT_KEYS) * row_h
    inv_row_h = 18.0

    # Scale fingerings for RH and LH
    scale_inversions = [
        ("RH FINGERS", sdef["rh_fingering"][:15], {st: f"{i+1}" for i, st in enumerate(sdef["semitones"][:8]) if i < 5}),
        ("LH FINGERS", sdef["lh_fingering"][:15], {st: f"{5-i}" for i, st in enumerate(sdef["semitones"][:8]) if i < 5}),
    ]
    active_scale_tones = sdef["semitones"]

    svg.append(render_bottom_keyboard_and_stand(table_bottom, inv_row_h, scale_inversions, active_scale_tones))
    svg.append('</svg>')
    return '\n'.join(svg)

def build_progression_card(title, subtitle, progressions_data):
    """
    Builds a Unified Matrix progression card with voice leading and chord voicing tracks.
    progressions_data: list of (prog_title, [(chord_numeral, chord_name, [(st_offset, note_name, degree)])])
    """
    t = THEME
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {PAGE_W} {PAGE_H}" width="{PAGE_W}" height="{PAGE_H}">']
    svg.append('<defs>')
    svg.append('''
      <style>
        .font-sans { font-family: "Avenir Next", "Helvetica Neue", Inter, Arial, sans-serif; }
        .fw-regular { font-weight: 400; }
        .fw-medium { font-weight: 500; }
        .fw-semibold { font-weight: 600; }
        .fw-bold { font-weight: 700; }
        .fw-heavy { font-weight: 800; }
      </style>
      <filter id="badge-shadow" x="-8%" y="-8%" width="116%" height="116%">
        <feDropShadow dx="0" dy="0.75" stdDeviation="0.6" flood-opacity="0.12"/>
      </filter>
      <filter id="black-key-shadow" x="-10%" y="-10%" width="120%" height="120%">
        <feDropShadow dx="0" dy="1.5" stdDeviation="1" flood-opacity="0.28"/>
      </filter>
    ''')
    svg.append('</defs>')
    svg.append(f'<rect width="{PAGE_W}" height="{PAGE_H}" fill="{t["bg"]}"/>')

    # Top Header
    svg.append(render_header(title, "PROGRESSION", subtitle, "progression"))

    grid_top = 68.0
    row_h = 18.0
    header_h = 24.0

    # Header Row
    svg.append(f'<g transform="translate({LEFT_MARGIN}, {grid_top})">')
    svg.append(f'''
      <rect x="0" y="0" width="{LABEL_COL_W}" height="{header_h}" fill="{t["card_bg"]}" stroke="{t["border"]}" stroke-width="0.5"/>
      <text class="font-sans fw-bold" x="{LABEL_COL_W/2}" y="11" font-size="7.5" fill="{t["text_primary"]}" text-anchor="middle">CHORD</text>
      <text class="font-sans fw-medium" x="{LABEL_COL_W/2}" y="20" font-size="6" fill="{t["text_muted"]}" text-anchor="middle">Voicing</text>
    ''')

    for col in range(NUM_COLS):
        cx = LABEL_COL_W + col * COL_W
        black = is_black_semitone(col)
        hdr_bg = t["row_even_black"] if black else t["card_bg"]
        note_at_c = NOTE_NAMES_FROM_C[col]
        svg.append(f'<rect x="{cx}" y="0" width="{COL_W}" height="{header_h}" fill="{hdr_bg}" stroke="{t["border"]}" stroke-width="0.5"/>')
        svg.append(f'<text class="font-sans fw-heavy" x="{cx + COL_W/2}" y="10" font-size="7.5" fill="{t["text_primary"]}" text-anchor="middle">+{col}</text>')
        svg.append(f'<text class="font-sans fw-bold" x="{cx + COL_W/2}" y="19.5" font-size="6.5" fill="{t["text_muted"]}" text-anchor="middle">{note_at_c}</text>')
    svg.append('</g>')

    current_y = grid_top + header_h
    all_chord_tones = set()

    for prog_idx, (section_title, chords) in enumerate(progressions_data):
        # Section Header banner
        svg.append(f'''
        <g transform="translate({LEFT_MARGIN}, {current_y})">
          <rect x="0" y="0" width="{TOTAL_TABLE_W}" height="16" fill="{t["card_bg"]}" stroke="{t["border"]}" stroke-width="0.5"/>
          <text class="font-sans fw-bold" x="12" y="11" font-size="7.5" fill="{t["accent"]}" letter-spacing="0.5">PROGRESSION: {section_title}</text>
        </g>
        ''')
        current_y += 16

        for ch_idx, (numeral, name, chord_notes) in enumerate(chords):
            is_even = (ch_idx % 2 == 0)
            svg.append(f'<g transform="translate({LEFT_MARGIN}, {current_y})">')
            lbl_bg = t["row_even_white"] if is_even else t["row_odd_white"]
            svg.append(f'<rect x="0" y="0" width="{LABEL_COL_W}" height="{row_h}" fill="{lbl_bg}" stroke="{t["border"]}" stroke-width="0.5"/>')
            svg.append(f'<text class="font-sans fw-bold" x="6" y="12" font-size="8" fill="{t["text_primary"]}">{name}</text>')
            svg.append(f'<text class="font-sans fw-heavy" x="{LABEL_COL_W - 6}" y="12" font-size="7" fill="{t["accent"]}" text-anchor="end">{numeral}</text>')

            notes_dict = {st: (n_name, deg) for st, n_name, deg in chord_notes}
            for col in range(NUM_COLS):
                cx = LABEL_COL_W + col * COL_W
                black = is_black_semitone(col)
                cell_bg = (t["row_even_black"] if is_even else t["row_odd_black"]) if black else (t["row_even_white"] if is_even else t["row_odd_white"])
                svg.append(f'<rect x="{cx}" y="0" width="{COL_W}" height="{row_h}" fill="{cell_bg}" stroke="{t["border"]}" stroke-width="0.5"/>')

                if col in notes_dict:
                    all_chord_tones.add(col)
                    note_name, deg_name = notes_dict[col]
                    abs_st = NOTE_TO_SEMITONE.get(note_name, col)
                    is_black_note = is_black_semitone(abs_st)
                    accent_c = get_accent_color_for_degree(deg_name)

                    bw = COL_W - 6
                    bh = row_h - 3
                    bx = cx + 3
                    by = 1.5

                    if is_black_note:
                        svg.append(f'''
                        <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="3.5" fill="{t["ebony_badge_bg"]}" stroke="{accent_c}" stroke-width="1.2" filter="url(#badge-shadow)"/>
                        <text class="font-sans fw-bold" x="{cx + COL_W/2 - 4}" y="{by + 9}" font-size="8.5" fill="#FFFFFF" text-anchor="middle">{note_name}</text>
                        <text class="font-sans fw-bold" x="{cx + COL_W/2 + bw/2 - 4.5}" y="{by + 8}" font-size="5" fill="{accent_c}">●</text>
                        ''')
                    else:
                        svg.append(f'''
                        <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="3.5" fill="{t["ivory_badge_bg"]}" stroke="{accent_c}" stroke-width="1.2" filter="url(#badge-shadow)"/>
                        <text class="font-sans fw-bold" x="{cx + COL_W/2 - 4}" y="{by + 9}" font-size="8.5" fill="{accent_c}" text-anchor="middle">{note_name}</text>
                        <text class="font-sans fw-bold" x="{cx + COL_W/2 + bw/2 - 4.5}" y="{by + 8}" font-size="5" fill="{accent_c}">○</text>
                        ''')

            svg.append('</g>')
            current_y += row_h

        current_y += 4

    inv_row_h = 18.0
    prog_inversions = [
        ("COMMON TONES", "Sustained keys across progression", {col: "★" for col in [0, 4, 7] if col in all_chord_tones}),
    ]

    svg.append(render_bottom_keyboard_and_stand(current_y, inv_row_h, prog_inversions, list(all_chord_tones)))
    svg.append('</svg>')
    return '\n'.join(svg)
