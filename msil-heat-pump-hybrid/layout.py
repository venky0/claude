"""Layout of the three slides of Heat_Pump__Solar_Wind_Hybrid_3.pdf (720 x 540 pt each).

Slides 1 and 2 are a 1672 x 941 px poster stretched over the 4:3 slide, so every poster element
is measured in poster pixels and mapped to slide points with MAP[slide]. Text is set upright
(no horizontal squash) and fitted to the measured width; icons are scaled uniformly.
"""

W, H = 720, 540

# poster px -> slide pt : (x offset, x scale, y scale)
MAP = {1: (0.38252, 719.62 / 1672, 540 / 941),
       2: (0.19126, 719.62 / 1672, 540 / 941)}
ICON_GROW = 1.12            # icons drawn at x-scale * this, uniformly

NAVY = '#0D1F5E'
INK = '#1B1F33'

# style: (font family, weight, fill, mask mode, cap height px used for the inpaint box)
STYLES = {
    # slide 1
    'logo_msil':   ('Montserrat', 800, '#1414C4', 'diff', 34),
    'logo_lights': ('Montserrat', 700, '#111111', 'diff', 50),
    'feat_t':      ('Barlow Condensed', 700, '#0B1F5C', 'dark', 13),
    'feat_b':      ('Barlow Condensed', 500, '#22252F', 'dark', 13),
    'tag':         ('Barlow Condensed', 600, '#FFFFFF', 'light', 19),
    'spec_t':      ('Barlow Condensed', 700, NAVY, 'dark', 13),
    'spec_b':      ('Barlow Semi Condensed', 500, INK, 'dark', 13),
    'spec_t_w':    ('Barlow Condensed', 700, '#FFFFFF', 'light', 13),
    'spec_b_w':    ('Barlow Semi Condensed', 500, '#FFFFFF', 'light', 13),
    'ideal_btn':   ('Barlow Condensed', 700, '#FFFFFF', 'light', 19),
    'ideal':       ('Barlow Condensed', 600, '#FFFFFF', 'light', 12),
    'ge_t':        ('Barlow Condensed', 700, '#8CC83F', 'light', 15),
    'ge_b':        ('Barlow Condensed', 500, '#FFFFFF', 'light', 13),
    # slide 2
    'k_logo':      ('Noto Sans Kannada', 900, '#141414', 'diff', 30),
    'k_logo_s':    ('Noto Sans Kannada', 800, '#141414', 'diff', 14),
    'hs':          ('Montserrat', 800, '#232323', 'diff', 35),
    'hs_sub':      ('Barlow Semi Condensed', 600, '#232323', 'diff', 15),
    'msil2':       ('Montserrat', 700, '#1B2B6B', 'diff', 22),
    'f2_t':        ('Barlow Semi Condensed', 600, '#1B2440', 'dark', 12),
    'f2_b':        ('Barlow Semi Condensed', 400, '#2A3142', 'dark', 13),
    'intro':       ('Barlow Semi Condensed', 500, '#1E2A3A', 'dark', 14),
    'box_t':       ('Barlow Semi Condensed', 700, '#FFFFFF', 'light', 14),
    'box_b':       ('Barlow Semi Condensed', 400, '#FFFFFF', 'light', 14),
    'why_h':       ('Barlow Semi Condensed', 700, '#FFFFFF', 'light', 15),
    'why_b':       ('Barlow Semi Condensed', 400, '#FFFFFF', 'light', 14),
    'strip':       ('Barlow Semi Condensed', 600, '#1E2B4A', 'dark', 12),
    'slogan':      ('Barlow Semi Condensed', 700, '#FFFFFF', 'light', 21),
}


def T(id_, x, base, w, text, style, anchor='start', key=None):
    """Poster-space text: x is the left edge (anchor start) or centre (anchor middle);
    w is the measured width in poster px (None = take the group's size)."""
    return dict(id=id_, x=x, base=base, w=w, text=text, style=style, anchor=anchor, key=key or style)


# ---------------------------------------------------------------- slide 1: solar street lights
S1_TEXT = []
FEAT_X = [1158, 1295, 1430, 1562.5]
for i, (t, tw, b1, w1, b2, w2) in enumerate([
        ('SOLAR POWERED', 109, '100% Clean', 70, '&amp; Renewable', 79),
        ('LITHIUM BATTERY', 111, 'Long Life &amp;', 74, 'High Performance', 110),
        ('PIR MOTION SENSOR', 115, 'Smart &amp; Energy', 96, 'Efficient', 52),
        ('BUILT TO LAST', 92, 'Rugged Design for', 112, 'All Weather', 70)]):
    cx = FEAT_X[i]
    S1_TEXT += [T(f'feature-{i+1}-title', cx, 145, tw, t, 'feat_t', 'middle'),
                T(f'feature-{i+1}-1', cx, 167, w1, b1, 'feat_b', 'middle'),
                T(f'feature-{i+1}-2', cx, 188, w2, b2, 'feat_b', 'middle')]

S1_TEXT += [T('tag-single-arm', 44, 279, 133, 'SINGLE ARM', 'tag'),
            T('tag-twin-arm', 560, 279, 111, 'TWIN ARM', 'tag'),
            T('tag-highmast', 1122, 279, 114, 'HIGHMAST', 'tag')]

SPEC_RING_X = [56, 571, 1128.5]
SPEC_TEXT_X = [92, 606.5, 1163]
SPEC_ROWS = [  # name, ring cy, title, title width, [(baseline, text, width)]
    ('pole', 445, 'POLE HEIGHT', 87.5, [(462, None, 58.5)]),
    ('battery', 512.5, 'LITHIUM BATTERY', 116.5,
     [(527.5, 'LiFePO<tspan baseline-shift="-25%" font-size="70%">4</tspan> Battery', 99),
      (546, 'Long Life (5+ Years)', 126)]),
    ('pir', 587.5, 'PIR MOTION SENSOR', 129.5,
     [(600, 'Automatically Adjusts', 129.5), (617.5, 'Brightness to Save', 111), (634, 'More Energy', 74.5)]),
    ('led', 675, 'HIGH EFFICIENCY LED', 134,
     [(689, '150+ lm/W High Brightness', 158.5), (707.5, 'Uniform Light Distribution', 153)]),
    ('shield', 752, 'ALL WEATHER PROOF', 133.5,
     [(766.5, 'Dustproof, Waterproof', 133), (785, '&amp; Corrosion Resistant', 128)]),
]
TITLE_BASE = {'pole': 442, 'battery': 507.5, 'pir': 581, 'led': 670, 'shield': 747.5}
POLE = ['6m – 7m', '6m – 8m', '9m – 12m']
for p in range(3):
    tx = SPEC_TEXT_X[p]
    st, sb = ('spec_t', 'spec_b') if p < 2 else ('spec_t_w', 'spec_b_w')
    for name, cy, title, tw, body in SPEC_ROWS:
        S1_TEXT.append(T(f'panel-{p+1}-{name}-title', tx, TITLE_BASE[name], tw if p == 0 else None, title, st,
                         key='spec_t'))
        for j, (b, txt, bw) in enumerate(body):
            S1_TEXT.append(T(f'panel-{p+1}-{name}-{j+1}', tx, b, bw if p == 0 else None, txt or POLE[p], sb,
                             key='spec_b'))

S1_TEXT.append(T('ideal-for', 28, 905, 90, 'IDEAL FOR', 'ideal_btn'))
IDEAL = [('highways', 200, 'HIGHWAYS', 58.5, (176, 862, 225, 906)),
         ('city-roads', 331, 'CITY ROADS', 66.5, (303, 860, 359, 905)),
         ('parks', 461.5, 'PARKS', 36.5, (437, 862, 486, 905)),
         ('industrial-areas', 605, 'INDUSTRIAL AREAS', 108, (580, 862, 630, 905)),
         ('campus', 747, 'CAMPUS', 48, (722, 864, 772, 907)),
         ('parking-areas', 883.5, 'PARKING AREAS', 88.5, (860, 866, 907, 905)),
         ('public-places', 1025.5, 'PUBLIC PLACES', 85.5, (1004, 866, 1047, 905))]
for n, cx, lab, w, _ in IDEAL:
    S1_TEXT.append(T(f'ideal-{n}-label', cx, 922.5, w, lab, 'ideal', 'middle'))
for i, (x, t, tw, l1, w1, l2, w2) in enumerate([
        (1231, 'GREEN ENERGY', 123, 'CLEAN TODAY', 87.5, 'BETTER TOMORROW', 124.5),
        (1486, 'SAFE &amp; SECURE', 127, 'RELIABLE LIGHTING', 123, 'FOR EVERY ENVIRONMENT', 156.5)]):
    S1_TEXT += [T(f'badge-{i+1}-title', x, 882.5, tw, t, 'ge_t'),
                T(f'badge-{i+1}-1', x, 905, w1, l1, 'ge_b'),
                T(f'badge-{i+1}-2', x, 924, w2, l2, 'ge_b')]

# icons: (name, (x0, y0, x1, y1) trace box, [(mode, fill)], clip circle or None, mask)
# mask: ('disc', cx, cy, r) | ('rect',) = the trace box ; ring: (cx, cy, r, stroke, stroke px, fill, fill opacity)
S1_ICONS, S1_RINGS = [], []
for i, (cx, layers) in enumerate(zip(FEAT_X, [[('orange', '#F7A21B'), ('dark', '#0B1F5C')],
                                             [('dark', '#0B1F5C'), ('green', '#21A63B')],
                                             [('dark', '#0B1F5C')], [('dark', '#0B1F5C')]])):
    S1_RINGS.append((f'feature-{i+1}-disc', cx, 79, 41, 'none', 0, '#FFFFFF', 0.92))
    S1_ICONS.append((f'feature-{i+1}', (cx - 34, 45, cx + 34, 113), layers, (cx, 79, 36), ('disc', cx, 79, 44)))
for p, cx in enumerate(SPEC_RING_X):
    for name, cy, *_ in SPEC_ROWS:
        if p < 2:
            S1_RINGS.append((f'panel-{p+1}-{name}-ring', cx, cy, 23, NAVY, 3.5, '#FFFFFF', 0.95))
            layers = [('dark', NAVY)]
        else:
            S1_RINGS.append((f'panel-{p+1}-{name}-ring', cx, cy, 23, '#FFFFFF', 3.5, '#0E2A63', 0.6))
            layers = [('light', '#FFFFFF')] + ([('green', '#3DBE4E')] if name == 'battery' else [])
        S1_ICONS.append((f'panel-{p+1}-{name}-icon', (cx - 20, cy - 20, cx + 20, cy + 20), layers,
                         (cx, cy, 18.5), ('disc', cx, cy, 27)))
for n, cx, lab, w, box in IDEAL:
    S1_ICONS.append((f'ideal-{n}-icon', box, [('light', '#FFFFFF')], None, ('rect',)))
S1_ICONS += [('badge-1-icon', (1154, 862, 1222, 930), [('green', '#4DAF3E'), ('white', '#FFFFFF')], (1188, 896, 33),
              ('disc', 1188, 896, 36)),
             ('badge-2-icon', (1410, 862, 1478, 930), [('green', '#4DAF3E'), ('white', '#FFFFFF')], (1443.5, 896, 33),
              ('disc', 1443.5, 896, 36))]
S1_LOGO_BOX = (20, 20, 400, 195)      # painted out; redrawn as vector

# ---------------------------------------------------------------- slide 2: heat pump
S2_TEXT = []
F2 = [(100, 'SOLAR ENERGY', 97.5, ['Harness free', 'solar energy'], [73.5, 73.5]),
      (242.5, 'HEAT PUMP', 74, ['Works efficiently', 'even in low', 'sunlight &amp; winter'], [96, None, 99]),
      (381.5, 'HOT WATER', 75, ['Consistent hot', 'water 24x7,', 'all year round'], [85, None, 81.5]),
      (513.5, 'ECO-FRIENDLY', 93, ['Lower energy use', '&amp; reduced', 'carbon footprint'], [104, None, 96.5])]
for i, (cx, t, tw, body, ws) in enumerate(F2):
    S2_TEXT.append(T(f'feature-{i+1}-title', cx, 365, tw, t, 'f2_t', 'middle'))
    for j, (b, w) in enumerate(zip(body, ws)):
        S2_TEXT.append(T(f'feature-{i+1}-{j+1}', cx, [387.5, 407.5, 426.5][j], w, b, 'f2_b', 'middle'))
S2_TEXT += [T('intro-1', 583.5, 227.5, 473, 'Integrated solar energy and advanced heat pump technology', 'intro'),
            T('intro-2', 583.5, 248.5, 407.5, 'delivers hot water efficiently, reliably and sustainably.', 'intro')]
BOX = [(347, [('HIGH EFFICIENCY', 335, 123.5)], [('Up to 70%', 361, None), ('energy savings', 380, 98.5)]),
       (465.5, [('WIDE TEMPERATURE', 452.5, 134), ('OPERATION', 475, None)], [('-10°C to 45°C', 501.5, 91.5)]),
       (578.5, [('SUPER QUIET', 564, 91.5), ('OPERATION', 586, None)],
        [('Low noise,', 612.5, None), ('peaceful comfort', 631, 110)]),
       (705, [('BUILT TO LAST', 693.5, 100)], [('Robust, reliable &amp;', 720, 115), ('corrosion resistant', 739, 119)])]
for i, (cy, titles, body) in enumerate(BOX):
    for j, (t, b, w) in enumerate(titles):
        S2_TEXT.append(T(f'box-{i+1}-title-{j+1}', 1505, b, w, t, 'box_t'))
    for j, (t, b, w) in enumerate(body):
        S2_TEXT.append(T(f'box-{i+1}-{j+1}', 1505, b, w, t, 'box_b'))
S2_TEXT.append(T('why-title', 150, 788.5, 376, 'WHY HEAT PUMP MAKES THE DIFFERENCE', 'why_h'))
WHY = [(128.5, [(819, 'Provides hot water', 130.5), (840, 'even on cloudy', None), (859, 'days and at night', None)]),
       (412.5, [(819, 'Consumes up to 70% less', 177.5), (840, 'electricity compared to', None),
                (859, 'conventional heaters', None)]),
       (724, [(819, 'Works efficiently in', None), (840, 'low ambient temperature', 182.5),
              (859, '(-10°C to 45°C)', None)]),
       (1046, [(825, 'Long life, low maintenance', 192), (846.5, '&amp; reliable performance', None)]),
       (1389, [(815, 'Sustainable future', 128.5), (836, 'Clean energy for', None), (857.5, 'a better tomorrow', None)])]
for i, (x, lines) in enumerate(WHY):
    for j, (b, t, w) in enumerate(lines):
        S2_TEXT.append(T(f'why-{i+1}-{j+1}', x, b, w, t, 'why_b'))
S2_TEXT += [T('strip-advanced', 86, 915, 148, 'ADVANCED TECHNOLOGY', 'strip'),
            T('strip-sustainable', 325, 915, 141, 'SUSTAINABLE SOLUTION', 'strip'),
            T('strip-endless', 556, 915, 124, 'ENDLESS HOT WATER', 'strip'),
            T('strip-perfect-1', 781, 906, 129, 'PERFECT FOR HOMES,', 'strip'),
            T('strip-perfect-2', 781, 921.5, 201.5, 'HOTELS, HOSPITALS &amp; INDUSTRIES', 'strip'),
            T('slogan', 1086, 920, 544, 'CLEAN ENERGY. LOWER BILLS. BETTER TOMORROW.', 'slogan')]

S2_ICONS, S2_RINGS = [], []
for i, (cx, *_) in enumerate(F2):
    S2_RINGS.append((f'feature-{i+1}-ring', cx, 305, 38.5, '#2B3550', 2.5, 'none', 0))
    S2_ICONS.append((f'feature-{i+1}-icon', (cx - 33, 272, cx + 33, 338), [('dark', '#1B2A4E')], (cx, 305, 33),
                     ('disc', cx, 305, 43)))
for i, (cy, *_) in enumerate(BOX):
    S2_RINGS.append((f'box-{i+1}-disc', 1464, cy, 29, 'none', 0, '#E8661C', 1))
    S2_ICONS.append((f'box-{i+1}-icon', (1437, cy - 27, 1491, cy + 27), [('on_orange', '#FFFFFF')], (1464, cy, 26),
                     ('disc', 1464, cy, 32)))
S2_ICONS += [
    ('why-1-icon', (46, 803, 110, 859), [('light', '#FFFFFF')], None, ('rect',)),
    ('why-2-icon', (332, 802, 393, 862), [('light', '#FFFFFF'), ('green', '#3CB44A')], (362.5, 832, 30),
     ('disc', 362.5, 832, 33)),
    ('why-3-icon', (638, 803, 697, 864), [('light', '#FFFFFF')], None, ('rect',)),
    ('why-4-icon', (964, 802, 1026, 862), [('light', '#FFFFFF')], (995, 832, 30), ('disc', 995, 832, 33)),
    ('why-5-icon', (1300, 802, 1369, 868), [('light', '#FFFFFF')], None, ('rect',)),
    ('strip-1-icon', (38, 890, 77, 928), [('dark', '#22305A')], (57.5, 909, 15.5), ('disc', 57.5, 909, 22)),
    ('strip-2-icon', (276, 890, 314, 928), [('dark', '#22305A'), ('green2', '#3E9D3A')], (295, 909, 15.5),
     ('disc', 295, 909, 22)),
    ('strip-3-icon', (508, 890, 547, 928), [('dark', '#22305A')], (527.5, 909, 15.5), ('disc', 527.5, 909, 22)),
    ('strip-4-icon', (724, 891, 768, 927), [('dark', '#22305A')], None, ('rect',)),
    ('slogan-leaf', (1034, 891, 1078, 930), [('light', '#FFFFFF')], None, ('rect',)),
]
for i, cx in enumerate((57.5, 295, 527.5)):
    S2_RINGS.append((f'strip-{i+1}-ring', cx, 909, 18, '#2B3A5E', 2, 'none', 0))
S2_LOGO_BOXES = [(28, 30, 390, 145), (250, 110, 548, 245)]   # Kannada + English HOTSPRING lockups

# ---------------------------------------------------------------- Kannada titles (slide points, from the PDF)
KN_TITLES = {
    1: dict(box=(173.47, 10.84, 293.89, 111.5), cx=320.4, size=20.04,
            lines=[('ಆಲ್-ಇನ್-ಒನ್ ಸೌರ ಬೀದಿ', 50.04, '#0F3764'),
                   ('ದೀಪಗಳು', 74.04, '#0F3764'),
                   ('ಎಂಎಸ್ಐಎಲ್ ಲೈಟ್ಸ್', 98.04, '#144673')],
            uline=[52.24, 76.18, 100.18], uw=[0.84, 0.72, 0.72]),
    2: dict(box=(244.19, 2.88, 283.38, 115.63), cx=385.88, size=24,
            lines=[('ಹೀಟ್ ಪಂಪ್‌ನೊಂದಿಗೆ', 40.9, '#0F3764'),
                   ('ಸೌರ ಜಲತಾಪಕ', 69.72, '#0F3764'),
                   ('ಸೌರ ಜಲತಾಪಕ', 98.52, '#144673')],
            uline=[43.36, 72.22, 101.02], uw=[0.84, 0.96, 0.96]),
    3: dict(box=(0, 2.88, 720, 108.36), cx=360, size=24,
            lines=[('104 ಕಿ.ವ್ಯಾ. ಸೌರ-ಗಾಳಿ ಹೈಬ್ರಿಡ್', 66.07, '#17375E')],
            uline=[68.4], uw=[0.96]),
}
