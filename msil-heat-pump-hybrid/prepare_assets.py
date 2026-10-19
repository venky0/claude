"""Paint the baked-in text, icons and logos out of the slide 1-2 posters and trace the icons.

usage: python3 prepare_assets.py <slide1_poster.jpg> <slide2_poster.jpg> <slide3_photo.jpg> <out_dir>
writes <out_dir>/links/*.jpg and <out_dir>/icons.json
"""
import json, re, shutil, sys
from pathlib import Path

import cv2
import numpy as np
import potrace

sys.path.insert(0, str(Path(__file__).parent))
from layout import STYLES, S1_TEXT, S1_ICONS, S1_LOGO_BOX, S2_TEXT, S2_ICONS, S2_LOGO_BOXES

SRC1, SRC2, SRC3, OUT = sys.argv[1], sys.argv[2], sys.argv[3], Path(sys.argv[4])
(OUT / 'links').mkdir(parents=True, exist_ok=True)
UP = 6

MODES = {
    'dark':   lambda r, g, b, l: (l < 150) & (b > r + 5),
    'light':  lambda r, g, b, l: l > 150,
    'white':  lambda r, g, b, l: (l > 185) & (np.max([r, g, b], 0) - np.min([r, g, b], 0) < 60),
    'orange': lambda r, g, b, l: (r > 190) & (g > 90) & (g < 200) & (b < 110),
    'green':  lambda r, g, b, l: (g > r + 25) & (g > b + 15),
    'green2': lambda r, g, b, l: (g > r + 45) & (g > b + 45),          # saturated leaf green only
    'on_orange': lambda r, g, b, l: b > 110,                          # white glyph on orange (orange has ~no blue)
}


def plain(t):
    return re.sub(r'<[^>]+>', '', t).replace('&amp;', '&')


def text_box(t):
    cap = STYLES[t['style']][4]
    w = t['w'] or len(plain(t['text'])) * cap * 0.62 + 6
    x0 = t['x'] - w / 2 if t['anchor'] == 'middle' else t['x']
    return int(x0 - 3), int(t['base'] - cap * 1.45), int(x0 + w + 3), int(t['base'] + cap * 0.5)


def trace(rgb, box, mode, clip=None):
    x0, y0, x1, y1 = [int(round(v)) for v in box]
    crop = rgb[y0:y1, x0:x1].astype(np.float32)
    big = cv2.resize(crop, ((x1 - x0) * UP, (y1 - y0) * UP), interpolation=cv2.INTER_CUBIC)
    big = cv2.GaussianBlur(big, (0, 0), UP * 0.35)
    r, g, b = big[..., 0], big[..., 1], big[..., 2]
    m = MODES[mode](r, g, b, big.mean(2))
    if clip:
        cx, cy, rad = clip
        yy, xx = np.mgrid[0:m.shape[0], 0:m.shape[1]]
        m &= ((xx / UP + x0 - cx) ** 2 + (yy / UP + y0 - cy) ** 2) < rad ** 2
    curves = potrace.Bitmap(~m).trace(turdsize=UP * UP * 2, alphamax=1.0, opticurve=True, opttolerance=0.3)
    f = lambda p: f'{p.x / UP + x0:.2f} {p.y / UP + y0:.2f}'
    d = []
    for c in curves:
        pts = [s.end_point for s in c.segments]
        if min(p.x for p in pts) <= 0 and max(p.x for p in pts) >= (x1 - x0) * UP:
            continue  # frame of the complement
        d.append('M' + f(c.start_point))
        for s in c.segments:
            d.append(f'L{f(s.c)}L{f(s.end_point)}' if s.is_corner else f'C{f(s.c1)} {f(s.c2)} {f(s.end_point)}')
        d.append('Z')
    return ''.join(d)


def process(src, texts, icons, logo_boxes, name):
    img = cv2.imread(src)
    rgb = img[..., ::-1].astype(int)
    lum = rgb.mean(2)
    bg = cv2.medianBlur(img, 25)[..., ::-1].astype(int).mean(2)
    mask = np.zeros(lum.shape, np.uint8)

    def px(box, mode):
        x0, y0, x1, y1 = [max(0, v) for v in box]
        sub = np.zeros(lum.shape, bool)
        sub[y0:y1, x0:x1] = True
        sel = (bg - lum > 30) if mode in ('dark',) else (lum - bg > 30) if mode in ('light', 'white') \
            else np.abs(lum - bg) > 30
        mask[sub & sel] = 255

    for t in texts:
        px(text_box(t), STYLES[t['style']][3])
    traced = {}
    for n, box, layers, clip, m in icons:
        if m[0] == 'disc':
            cv2.circle(mask, (int(m[1]), int(m[2])), int(m[3]), 255, -1)
        else:
            x0, y0, x1, y1 = [int(round(v)) for v in box]
            mask[y0 - 2:y1 + 2, x0 - 2:x1 + 2] = 255
        traced[n] = [{'fill': fill, 'd': trace(rgb, box, mode, clip)} for mode, fill in layers]
    for x0, y0, x1, y1 in logo_boxes:
        mask[y0:y1, x0:x1] = 255
    mask = cv2.dilate(mask, np.ones((5, 5), np.uint8))
    clean = cv2.inpaint(img, mask, 5, cv2.INPAINT_TELEA)
    cv2.imwrite(str(OUT / f'links/{name}.jpg'), clean, [cv2.IMWRITE_JPEG_QUALITY, 93])
    return traced


icons = {1: process(SRC1, S1_TEXT, S1_ICONS, [S1_LOGO_BOX], 'slide1_street_lights_background'),
         2: process(SRC2, S2_TEXT, S2_ICONS, S2_LOGO_BOXES, 'slide2_heat_pump_background')}
shutil.copy(SRC3, OUT / 'links/slide3_solar_wind_hybrid_photo.jpg')
(OUT / 'icons.json').write_text(json.dumps(icons))
print({k: len(v) for k, v in icons.items()}, 'bytes', len(json.dumps(icons)))
