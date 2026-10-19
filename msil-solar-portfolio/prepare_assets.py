"""Cut the photo zones out of the source banner (with baked-in text painted out)
and trace every icon to vector paths.

usage: python3 prepare_assets.py <source.png> <out_dir>
writes <out_dir>/links/*.png and <out_dir>/icons.json
"""
import json, sys
from pathlib import Path

import cv2
import numpy as np
import potrace

SRC, OUT = sys.argv[1], Path(sys.argv[2])
(OUT / 'links').mkdir(parents=True, exist_ok=True)
img = cv2.imread(SRC)                       # BGR
rgb = img[..., ::-1].astype(int)
lum = rgb.mean(2)
R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]

# ---------------------------------------------------------------- inpainting
mask = np.zeros(lum.shape, np.uint8)
text_px = (lum < 160) & (G < B + 25)          # navy or near-black ink, not foliage
white_px = lum > 175


def rect(x0, y0, x1, y1):
    mask[y0:y1, x0:x1] = 255


def pixels(sel, x0, y0, x1, y1):
    sub = np.zeros(lum.shape, bool)
    sub[y0:y1, x0:x1] = True
    mask[sub & sel] = 255


def disc(cx, cy, r):
    cv2.circle(mask, (int(cx), int(cy)), int(r), 255, -1)


SPEC_Y = [427.5, 477.5, 533, 607, 666]
# street-light panels: tags, spec icons, spec text
for x0, x1 in [(16, 146), (255, 373), (533, 652)]:
    rect(x0, 259, x1, 297)
for cx in (41, 275, 555):
    for cy in SPEC_Y:
        disc(cx, cy, 22)
pixels(text_px, 64, 408, 220, 700)
pixels(text_px, 298, 408, 452, 700)
pixels(white_px, 578, 408, 736, 700)
# heat-pump zone: headline, logo block, paragraph, icons, icon captions
sky = (lum > 165) & (B >= R)
pixels(text_px, 818, 122, 1148, 240)
pixels(~sky, 1198, 122, 1372, 250)
pixels(text_px, 808, 240, 1192, 280)
for cx in (861.5, 957.5, 1052.5, 1148.5):
    disc(cx, 321, 32)
pixels(text_px, 812, 352, 1196, 418)
mask = cv2.dilate(mask, np.ones((5, 5), np.uint8))
clean = cv2.inpaint(img, mask, 5, cv2.INPAINT_TELEA)

cv2.imwrite(str(OUT / 'links/photo_street_lights.png'), clean[253:700, 0:789])
cv2.imwrite(str(OUT / 'links/photo_heat_pump.png'), clean[110:700, 792:1391])
cv2.imwrite(str(OUT / 'links/photo_solar_wind_hybrid.png'), clean[248:700, 1393:1964])

# ---------------------------------------------------------------- icon tracing
UP = 6
MODES = {
    'dark':   lambda r, g, b, l: (l < 140) & (b > r + 10),
    'light':  lambda r, g, b, l: l > 150,
    'white':  lambda r, g, b, l: b > 105,          # white glyph on an orange disc (orange has ~no blue)
    'orange': lambda r, g, b, l: (r > 190) & (g > 90) & (g < 200) & (b < 110),
    'green':  lambda r, g, b, l: (g > r + 35) & (g > b + 15),
    'lime':   lambda r, g, b, l: (g > 150) & (r > 80) & (b < 130),
}


def trace(box, mode, clip=None):
    x0, y0, x1, y1 = box
    crop = rgb[y0:y1, x0:x1].astype(np.float32)
    big = cv2.resize(crop, ((x1 - x0) * UP, (y1 - y0) * UP), interpolation=cv2.INTER_CUBIC)
    big = cv2.GaussianBlur(big, (0, 0), UP * 0.35)
    r, g, b = big[..., 0], big[..., 1], big[..., 2]
    m = MODES[mode](r, g, b, big.mean(2))
    if clip:  # keep only inside a circle (cx, cy, radius) in page coords
        cx, cy, rad = clip
        yy, xx = np.mgrid[0:m.shape[0], 0:m.shape[1]]
        m &= ((xx / UP + x0 - cx) ** 2 + (yy / UP + y0 - cy) ** 2) < rad ** 2
    curves = potrace.Bitmap(~m).trace(turdsize=UP * UP * 2, alphamax=1.0, opticurve=True, opttolerance=0.3)
    f = lambda p: f'{p.x / UP + x0:.2f} {p.y / UP + y0:.2f}'
    d = []
    for c in curves:
        # potracer traces the complement too; drop the frame curve
        if abs(c.start_point.x) < 1e-6 or abs(c.start_point.x - (x1 - x0) * UP) < 1e-6:
            pts = [s.end_point for s in c.segments]
            if min(p.x for p in pts) <= 0 and max(p.x for p in pts) >= (x1 - x0) * UP:
                continue
        d.append('M' + f(c.start_point))
        for s in c.segments:
            d.append(f'L{f(s.c)}L{f(s.end_point)}' if s.is_corner else f'C{f(s.c1)} {f(s.c2)} {f(s.end_point)}')
        d.append('Z')
    return ''.join(d)


NAVY, WHITE = '#0B1A6B', '#FFFFFF'
icons = {}


def add(name, box, *layers, clip=None):
    icons[name] = [{'fill': fill, 'd': trace(box, mode, clip)} for mode, fill in layers]


# top feature icons (on white discs)
add('feat_solar', (418, 132, 474, 192), ('orange', '#F7A21B'), ('dark', NAVY))
add('feat_battery', (515, 132, 555, 192), ('dark', NAVY), ('green', '#20A83C'))
add('feat_pir', (601, 132, 657, 192), ('dark', NAVY))
add('feat_shield', (695, 132, 748, 192), ('dark', NAVY))
# spec-list glyphs inside the rings
SPEC = ['pole', 'battery', 'pir', 'led', 'shield']
for p, (cx, mode, fill) in enumerate([(41, 'dark', NAVY), (275, 'dark', NAVY), (555, 'light', WHITE)]):
    for name, cy in zip(SPEC, SPEC_Y):
        add(f'spec{p}_{name}', (int(cx - 16), int(cy - 16), int(cx + 17), int(cy + 17)), (mode, fill), clip=(cx, cy, 15))
add('spec2_battery_bolt', (539, 461, 572, 494), ('green', '#3DBE4E'), clip=(555, 477.5, 15))
# heat-pump ring icons
for name, cx in zip(['solar', 'heatpump', 'water', 'eco'], (861.5, 957.5, 1052.5, 1148.5)):
    add(f'hp_{name}', (int(cx - 27), 294, int(cx + 28), 349), ('dark', NAVY), clip=(cx, 321, 25))
# orange-disc icons in the feature box
for name, cy in zip(['efficiency', 'temperature', 'quiet', 'built'], (421, 489, 560, 641)):
    add(f'or_{name}', (1241, int(cy - 21), 1285, int(cy + 22)), ('white', WHITE), clip=(1262.5, cy, 19.5))
# "ideal for" category icons
for name, cx in zip(['highways', 'cityroads', 'parks', 'industrial', 'campus', 'parking', 'public'],
                    (167, 249, 331, 425, 522, 618, 725)):
    add(f'ideal_{name}', (cx - 26, 712, cx + 26, 758), ('light', WHITE))
# "why heat pump" icons
add('why_cloud', (798, 726, 850, 784), ('light', WHITE))
add('why_bolt', (938, 726, 996, 785), ('light', WHITE), ('green', '#3CB44A'))
add('why_thermo', (1135, 725, 1188, 785), ('light', WHITE))
add('why_tools', (1314, 726, 1374, 785), ('light', WHITE))
# leaves
add('leaf_header', (1406, 36, 1457, 88), ('green', '#3AA935'))
add('leaf_footer', (1510, 726, 1562, 782), ('lime', '#9ACD3C'))

(OUT / 'icons.json').write_text(json.dumps(icons))
print('icons', len(icons), 'bytes', sum(len(l['d']) for v in icons.values() for l in v))
