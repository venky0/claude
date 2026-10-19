"""Build the three slides as layered SVGs (720 x 540 pt) for Illustrator.

usage: python3 build_svg.py <dir>   (reads layout.py, links/, icons.json, fit.json)
fit.json holds the calibrated font sizes and measured Kannada line widths written by the preview renderer.
"""
import base64, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from layout import (W, H, MAP, ICON_GROW, STYLES, S1_TEXT, S1_ICONS, S1_RINGS, S2_TEXT, S2_ICONS, S2_RINGS,
                    KN_TITLES)

OUT = Path(sys.argv[1])
ICONS = json.loads((OUT / 'icons.json').read_text())
# glyphs too small in the source to trace cleanly, drawn by hand (poster px)
ICONS['2']['strip-2-icon'][1]['d'] = ('M291.5 917C291.5 906 297.5 899.5 306 897.5C306.5 907 300.5 914.5 291.5 917Z'
                                      'M290 917C285 916.5 282 912 283 906.5C287.5 907.5 290.5 911.5 290 917Z')
FIT = json.loads((OUT / 'fit.json').read_text()) if (OUT / 'fit.json').exists() else {'size': {}, 'width': {}}
WEIGHT = {400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold', 800: 'ExtraBold', 900: 'Black'}
KANNADA = "font-family=\"'NotoSansKannada-Bold', 'Noto Sans Kannada'\" font-weight=\"700\""


def font(family, weight):
    return f"font-family=\"'{family.replace(' ', '')}-{WEIGHT[weight]}', '{family}'\" font-weight=\"{weight}\""


def img(path, x, y, w, h, id_):
    data = base64.b64encode((OUT / 'links' / path).read_bytes()).decode()
    return (f'<image id="{id_}" x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
            f'preserveAspectRatio="none" xlink:href="data:image/jpeg;base64,{data}"/>')


def text(id_, x, y, body, style, size, key, anchor='start', fit=None, extra=''):
    fam, wt, fill = STYLES[style][:3]
    size = FIT['size'].get(key, size)
    a = ' text-anchor="middle"' if anchor == 'middle' else ''
    f = f' data-fit="{fit:.2f}"' if fit else ''
    return (f'<text id="{id_}" x="{x:.2f}" y="{y:.2f}"{a} {font(fam, wt)} font-size="{size:.2f}" fill="{fill}"'
            f' data-key="{key}"{f}{extra}>{body}</text>')


class Slide:
    def __init__(self, n):
        self.n = n
        self.ox, self.sx, self.sy = MAP.get(n, (0, 1, 1))
        self.s = self.sx * ICON_GROW

    X = lambda self, x: self.ox + x * self.sx
    Y = lambda self, y: y * self.sy

    def uniform(self, cx, cy, s=None):
        s = s or self.s
        return f'transform="translate({self.X(cx):.2f} {self.Y(cy):.2f}) scale({s:.4f}) translate({-cx} {-cy})"'

    def texts(self, items):
        out = []
        for t in items:
            cap = STYLES[t['style']][4]
            out.append(text(t['id'], self.X(t['x']), self.Y(t['base']), t['text'], t['style'],
                            cap * self.sx / 0.62, f'{self.n}:{t["key"]}', t['anchor'],
                            t['w'] * self.sx if t['w'] else None))
        return ''.join(out)

    def icons(self, items, rings):
        out = []
        for n, cx, cy, r, stroke, sw, fill, fo in rings:
            st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke != 'none' else ''
            out.append(f'<circle id="{n}" cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" fill-opacity="{fo}"{st} '
                       f'{self.uniform(cx, cy)}/>')
        for n, box, layers, clip, _ in items:
            cx, cy = (clip[0], clip[1]) if clip else ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
            paths = ''.join(f'<path fill="{l["fill"]}" fill-rule="evenodd" d="{l["d"]}"/>'
                            for l in ICONS[str(self.n)][n])
            out.append(f'<g id="{n}" {self.uniform(cx, cy)}>{paths}</g>')
        return ''.join(out)


def msil_mark(x, y, size, id_):
    s = size / 51
    return (f'<g id="{id_}" transform="translate({x} {y}) scale({s:.4f})">'
            f'<path fill="#0372BA" d="M0 0H51V17H34V33H16V51H0Z"/>'
            f'<path fill="#F09129" d="M9 9H34V16H26V24H17V33H9Z"/></g>')


def sun_mark(cx, cy, r, vx, vy0, vy1, hy, hx0, hx1, w, id_):
    star = (f'M{vx} {hy - r * 0.3}Q{vx + r * 0.05} {hy - r * 0.05} {vx + r * 0.3} {hy}'
            f'Q{vx + r * 0.05} {hy + r * 0.05} {vx} {hy + r * 0.3}Q{vx - r * 0.05} {hy + r * 0.05} {vx - r * 0.3} {hy}'
            f'Q{vx - r * 0.05} {hy - r * 0.05} {vx} {hy - r * 0.3}Z')
    return (f'<g id="{id_}"><circle cx="{cx}" cy="{cy}" r="{r}" fill="#F26B10"/>'
            f'<line x1="{vx}" y1="{vy0}" x2="{vx}" y2="{vy1}" stroke="#111111" stroke-width="{w}"/>'
            f'<line x1="{hx0}" y1="{hy}" x2="{hx1}" y2="{hy}" stroke="#111111" stroke-width="{w}"/>'
            f'<path d="{star}" fill="#111111"/></g>')


def ltext(id_, x, y, body, style, key, fit=None, anchor='start'):
    """logo text in poster px (inside a uniform group); fit is in poster px."""
    return text(id_, x, y, body, style, STYLES[style][4] / 0.7, key, anchor, fit)


def kannada_title(n):
    k = KN_TITLES[n]
    bx, by, bw, bh = k['box']
    out = [f'<g id="Kannada_title">',
           f'<rect id="title-box" x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="#FFFFFF" filter="url(#boxShadow)"/>']
    for i, ((line, base, color), uy, uw) in enumerate(zip(k['lines'], k['uline'], k['uw'])):
        key = f'{n}:kn-{i + 1}'
        w = FIT['width'].get(key, len(line) * k['size'] * 0.5)
        line_svg = (f'<text x="{k["cx"]}" y="{base}" text-anchor="middle" {KANNADA} font-size="{k["size"]}" '
                    f'fill="{color}" data-key="{key}" data-measure="1">{line}</text>'
                    f'<rect x="{k["cx"] - w / 2:.2f}" y="{uy - uw / 2:.2f}" width="{w:.2f}" height="{uw}" fill="{color}"/>')
        if n == 3:  # PowerPoint text shadow, kept as a separate blurred copy so the text itself stays live in PDFs
            shadow = line_svg.replace(f'fill="{color}"', 'fill="#000000"').replace(' data-measure="1"', '')
            out.append(f'<g id="title-line-{i + 1}-shadow" transform="translate(0.9 1.1)" filter="url(#shadowBlur)" '
                       f'opacity="0.35">{shadow}</g>')
        out.append(f'<g id="title-line-{i + 1}">{line_svg}</g>')
    out.append('</g>')
    return ''.join(out)


DEFS = '''<defs>
    <filter id="boxShadow" x="-10%" y="-20%" width="120%" height="150%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="1.8"/><feOffset dx="0.6" dy="2.2" result="b"/>
      <feComponentTransfer><feFuncA type="linear" slope="0.38"/></feComponentTransfer>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="shadowBlur" x="-5%" y="-30%" width="110%" height="160%">
      <feGaussianBlur stdDeviation="0.5"/>
    </filter>
  </defs>'''


def wrap(title, body):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{W}pt" height="{H}pt" viewBox="0 0 {W} {H}">
  <title>{title}</title>
  {DEFS}
  <rect id="slide-bg" width="{W}" height="{H}" fill="#FFFFFF"/>
{body}
</svg>
'''


# ------------------------------------------------------------------ slide 1
s1 = Slide(1)
logo1 = (f'<g id="MSIL_Lights_logo" {s1.uniform(210, 105, s1.sx * 1.05)}>'
         + msil_mark(111, 26, 44, 'logo-mark')
         + ltext('logo-msil', 156, 95, 'MSIL', 'logo_msil', '1:logo_msil', 147)
         + sun_mark(74, 134, 42, 74, 74, 191, 152, 26, 121, 5, 'logo-sun')
         + ltext('logo-lights', 133, 162, 'LIGHTS', 'logo_lights', '1:logo_lights', 263) + '</g>')
slide1 = f'''  <g id="Poster_background">{img('slide1_street_lights_background.jpg', s1.ox, 0, 1672 * s1.sx, 540, 'poster-photo')}</g>
  <g id="Logo">{logo1}</g>
  <g id="Icons">{s1.icons(S1_ICONS, S1_RINGS)}</g>
  <g id="Poster_text">{s1.texts(S1_TEXT)}</g>
  {kannada_title(1)}'''

# ------------------------------------------------------------------ slide 2
s2 = Slide(2)
logo_kn = (f'<g id="Hotspring_logo_kannada" {s2.uniform(205, 85, s2.sx * 1.05)}>'
           + ltext('logo-kn-msil', 100, 52, 'ಎಂಎಸ್ಐಎಲ್', 'k_logo_s', '2:k_logo_s', 172.5)
           + ltext('logo-kn-hotspri', 32, 97, 'ಹಾಟ್‌ಸ್ಪ್ರಿ', 'k_logo', '2:k_logo', 220)
           + sun_mark(282, 80, 28, 287, 44, 116, 92.5, 250, 315, 4, 'logo-kn-sun')
           + ltext('logo-kn-g', 315, 97, 'ಗ್', 'k_logo', '2:k_logo')
           + ltext('logo-kn-sub', 32, 127, 'ಸೋಲಾರ್ ವಾಟರ್ ಹೀಟರ್', 'k_logo_s', '2:k_logo_s2', 168) + '</g>')
logo_en = (f'<g id="Hotspring_logo" {s2.uniform(400, 190, s2.sx * 1.05)}>'
           + msil_mark(352, 116, 37, 'hs-mark')
           + ltext('hs-msil', 375, 164, 'MSIL', 'msil2', '2:msil2', 74)
           + ltext('hs-h', 259, 216, 'H', 'hs', '2:hs')
           + sun_mark(318.5, 199, 28, 320, 161, 237, 216, 290, 347, 4, 'hs-sun')
           + ltext('hs-tspring', 345, 216, 'TSPRING', 'hs', '2:hs', 194)
           + ltext('hs-sub', 352, 237, 'SOLAR WATER HEATER', 'hs_sub', '2:hs_sub', 190) + '</g>')
slide2 = f'''  <g id="Poster_background">{img('slide2_heat_pump_background.jpg', s2.ox, 0, 1672 * s2.sx, 540, 'poster-photo')}</g>
  <g id="Logos">{logo_kn}{logo_en}</g>
  <g id="Icons">{s2.icons(S2_ICONS, S2_RINGS)}</g>
  <g id="Poster_text">{s2.texts(S2_TEXT)}</g>
  {kannada_title(2)}'''

# ------------------------------------------------------------------ slide 3
ARIMO_B = "font-family=\"'Arimo-Bold', 'Arimo'\" font-weight=\"700\""
ARIMO = "font-family=\"'Arimo-Regular', 'Arimo'\" font-weight=\"400\""
slide3 = f'''  <g id="Photo">{img('slide3_solar_wind_hybrid_photo.jpg', 0, 0, 720, 506.2, 'hybrid-photo')}</g>
  {kannada_title(3)}
  <g id="Footer">
    <text id="footer-left" x="29.71" y="522" {ARIMO_B} font-size="8.04" letter-spacing="0.4" fill="#64748B" xml:space="preserve">MYSORE SALES INTERNATIONAL LIMITED  |  CIPD</text>
    <text id="footer-right" x="562.1" y="522" {ARIMO} font-size="8.04" letter-spacing="0.4" fill="#94A3B8">SOLAR PRODUCT PORTFOLIO</text>
  </g>'''

for n, name, body in [(1, 'Slide1_All_In_One_Solar_Street_Lights', slide1),
                      (2, 'Slide2_Solar_Water_Heater_Heat_Pump', slide2),
                      (3, 'Slide3_104kW_Solar_Wind_Hybrid', slide3)]:
    (OUT / f'{name}.svg').write_text(wrap(name.replace('_', ' '), body), encoding='utf-8')
print('ok')
