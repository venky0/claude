"""MSIL Solar roll-up banner as a layered SVG (1 px of the 827 x 1902 source = 1 pt) for Illustrator.

usage: python3 build.py <source.png> <out_dir>
Step 1 paints the tagline out of the photo (links/photo_solar_water_heater.jpg).
Step 2 writes MSIL_Solar_Rollup.svg; font sizes come from fit.json when present.
"""
import base64, json, sys
from pathlib import Path

import cv2
import numpy as np

SRC, OUT = sys.argv[1], Path(sys.argv[2])
(OUT / 'links').mkdir(parents=True, exist_ok=True)
W, H = 827, 1902
PHOTO_TOP = 446
FIT = json.loads((OUT / 'fit.json').read_text()) if (OUT / 'fit.json').exists() else {}

# ---------------------------------------------------------------- photo: remove the baked-in tagline
img = cv2.imread(SRC)
photo = img[PHOTO_TOP:H]
lum = photo.astype(int).mean(2)
mask = np.zeros(lum.shape, np.uint8)
y0, y1 = 1615 - PHOTO_TOP, 1800 - PHOTO_TOP
mask[y0:y1, 55:520][lum[y0:y1, 55:520] > 185] = 255            # white letters
mask = cv2.dilate(mask, np.ones((11, 11), np.uint8))           # + their drop shadow
clean = cv2.inpaint(photo, mask, 7, cv2.INPAINT_TELEA)
cv2.imwrite(str(OUT / 'links/photo_solar_water_heater.jpg'), clean, [cv2.IMWRITE_JPEG_QUALITY, 94])

# ---------------------------------------------------------------- svg
data = base64.b64encode((OUT / 'links/photo_solar_water_heater.jpg').read_bytes()).decode()


def text(id_, x, y, body, family, ps, weight, size, fit, extra=''):
    size = FIT.get(id_, size)
    return (f'<text id="{id_}" x="{x}" y="{y}" font-family="\'{ps}\', \'{family}\'" font-weight="{weight}" '
            f'font-size="{size:.2f}" fill="#FFFFFF" data-fit="{fit}"{extra}>{body}</text>')


svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{W}pt" height="{H}pt" viewBox="0 0 {W} {H}">
  <title>MSIL Solar Rollup</title>
  <defs>
    <linearGradient id="goldRule" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#C99A2E"/><stop offset="0.35" stop-color="#F9E27A"/>
      <stop offset="0.65" stop-color="#EEBD40"/><stop offset="1" stop-color="#C08B25"/>
    </linearGradient>
    <linearGradient id="goldSheen" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset="0.3" stop-color="#FFFFFF" stop-opacity="0.18"/>
      <stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0"/><stop offset="0.75" stop-color="#FFFFFF" stop-opacity="0.18"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
    <filter id="taglineShadow" x="-5%" y="-20%" width="115%" height="150%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="2.5"/><feOffset dx="2" dy="3" result="b"/>
      <feComponentTransfer><feFuncA type="linear" slope="0.55"/></feComponentTransfer>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <g id="Photo">
    <image id="photo-solar-water-heater" x="0" y="{PHOTO_TOP}" width="{W}" height="{H - PHOTO_TOP}"
           preserveAspectRatio="none" xlink:href="data:image/jpeg;base64,{data}"/>
  </g>

  <g id="Header">
    <rect id="header-band" width="{W}" height="433" fill="#003A98"/>
    <g id="msil-mark">
      <path fill="#0A73E8" d="M300 71H427V116H385V162H340V205H300Z"/>
      <path fill="#F7931E" d="M325 96H386V118H366V141H347V162H325Z"/>
    </g>
    {text('logo-msil', 374, 233, 'MSIL', 'Barlow Semi Condensed', 'BarlowSemiCondensed-SemiBold', 600, 85, 169)}
    {text('headline', 68, 373, 'MSIL SOLAR', 'Montserrat', 'Montserrat-Bold', 700, 125, 698, ' letter-spacing="-4"')}
    <g id="gold-rule">
      <rect y="432" width="{W}" height="14" fill="url(#goldRule)"/>
      <rect y="432" width="{W}" height="14" fill="url(#goldSheen)"/>
    </g>
  </g>

  <g id="Tagline" filter="url(#taglineShadow)">
    {text('tagline-1', 70, 1692.5, 'Our Energy', 'Source Sans 3', 'SourceSans3-SemiBoldItalic', 600, 80, 440, ' font-style="italic"')}
    {text('tagline-2', 75, 1784, 'Tomorrow', 'Source Sans 3', 'SourceSans3-SemiBoldItalic', 600, 80, 425, ' font-style="italic"')}
  </g>
</svg>
'''
(OUT / 'MSIL_Solar_Rollup.svg').write_text(svg, encoding='utf-8')
print('ok')
