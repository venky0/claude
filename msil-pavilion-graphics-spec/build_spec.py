"""Graphics & poster spec (inches) for the MSIL Pavilion, from MSIL_Set_Build_Dimensions_INCHES.pdf.

usage: python3 build_spec.py <out_dir> <g2_reference.png> <fonts_dir>
writes <out_dir>/spec.html (rendered to PDF separately) and MSIL_Pavilion_Graphics_Schedule.xlsx
"""
import base64, sys
from pathlib import Path

OUT, G2_IMG, FONTS = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])


# ------------------------------------------------------------------ inches helpers
def q(s):
    """'102 3/8' -> 102.375"""
    s = str(s).strip()
    neg = s.startswith('-')
    s = s.lstrip('-').strip()
    total = 0.0
    for part in s.split():
        if '/' in part:
            a, b = part.split('/')
            total += int(a) / int(b)
        else:
            total += float(part)
    return -total if neg else total


def f(v, unit='"'):
    """102.375 -> 102 3/8\" (nearest 1/8)"""
    n = round(abs(v) * 8)
    whole, rem = divmod(n, 8)
    frac = {0: '', 1: '1/8', 2: '1/4', 3: '3/8', 4: '1/2', 5: '5/8', 6: '3/4', 7: '7/8'}[rem]
    txt = (f'{whole} {frac}' if whole and frac else frac if frac else f'{whole}')
    return ('-' if v < 0 and n else '') + txt + unit


def wh(w, h):
    return f'{f(w)} × {f(h)}'


# ------------------------------------------------------------------ the schedule
# bleed per side (inches) by kind — recommendation, confirm with the printer
BLEED = {'framed': 1.0, 'display': 0.5, 'board': 1.0, 'photo': 0.5, 'canvas': 0.5, 'vector': 0.0}
# (id, item, qty, w, h, outer, bottom, top, placement, finish, kind)
GROUPS = [
    ('A', 'Interior wall banners — backlit prints in brass frames', [
        ('A1', 'Left wall banner 1', 1, '102 3/8', '102 3/8', '105 1/8 × 105 1/8 frame', '26', '128 3/8',
         'Left wall, y 203 7/8"–306 1/4" from stall front · see W1', 'Backlit print', 'framed'),
        ('A2', 'Left wall banner 2', 1, '102 3/8', '102 3/8', '105 1/8 × 105 1/8 frame', '26', '128 3/8',
         'Left wall, y 333 7/8"–436 1/4"', 'Backlit print', 'framed'),
        ('A3', 'Left wall banner 3', 1, '102 3/8', '102 3/8', '105 1/8 × 105 1/8 frame', '26', '128 3/8',
         'Left wall, y 463 3/4"–566 1/8"', 'Backlit print', 'framed'),
        ('A4', 'Right wall banner 1', 1, '102 3/8', '102 3/8', '105 1/8 × 105 1/8 frame', '26', '128 3/8',
         'Right wall, y 203 7/8"–306 1/4" · see W2', 'Backlit print', 'framed'),
        ('A5', 'Right wall banner 2', 1, '102 3/8', '102 3/8', '105 1/8 × 105 1/8 frame', '26', '128 3/8',
         'Right wall, y 333 7/8"–436 1/4"', 'Backlit print', 'framed'),
        ('A6', 'Right wall banner 3', 1, '102 3/8', '102 3/8', '105 1/8 × 105 1/8 frame', '26', '128 3/8',
         'Right wall, y 463 3/4"–566 1/8"', 'Backlit print', 'framed'),
        ('A7', 'Rear wall banner 1', 1, '79 1/2', '99 5/8', '82 1/4 × 102 3/8 frame', '31 1/8', '130 3/4',
         'Rear wall, x 83 1/8"–3 1/2" left of CL · see W3', 'Backlit print', 'framed'),
        ('A8', 'Rear wall banner 2', 1, '79 1/2', '99 5/8', '82 1/4 × 102 3/8 frame', '31 1/8', '130 3/4',
         'Rear wall, x 4 3/8"–83 7/8" right of CL', 'Backlit print', 'framed'),
        ('A9', 'Backdrop banner 1 (interior face)', 1, '84', '72', '86 3/4 × 74 3/4 frame', '16 5/8', '88 5/8',
         'Backdrop, x 98 3/8"–14 3/8" left of CL · see W4', 'Backlit print', 'framed'),
        ('A10', 'Backdrop banner 2 (interior face)', 1, '84', '72', '86 3/4 × 74 3/4 frame', '16 5/8', '88 5/8',
         'Backdrop, x 14 3/8"–98 3/8" right of CL', 'Backlit print', 'framed'),
    ]),
    ('B', 'Showroom graphics — front displays and backdrop (showroom face)', [
        ('B1', 'Stationery hero print', 1, '36 3/4', '68 1/4', 'in surround 43 5/8 × 93 3/4', '25 5/8', '94',
         'Stationery display, front left', 'Backlit / printed', 'display'),
        ('B2', 'Stationery pedestal print', 1, '36 3/8', '15 3/4', 'plinth 40 5/8 × 19 5/8 high', '7 7/8', '23 5/8',
         'Front of stationery plinth', 'Backlit / printed', 'display'),
        ('B3', 'Divisions information panel', 1, '30 5/8', '61', 'in pylon 37 1/2 × 67 5/8', '40 3/4', '101 3/4',
         'Divisions pylon, on the centre line', 'Backlit / printed', 'display'),
        ('B4', 'Solar campaign print', 1, '32 7/8', '41 3/8', 'in surround 41 1/8 × 98', '57', '98 1/4',
         'Solar display, front right', 'Backlit / printed', 'display'),
        ('B5', 'Chit Funds campaign print', 1, '32 7/8', '83 1/8', 'in surround 39 3/8 × 94', '22 1/8', '105 1/8',
         'Chit Funds display, front right end', 'Backlit / printed', 'display'),
        ('B6', 'Serving Karnataka panel', 1, '28 1/8', '65 1/8', '—', '27 1/8', '92 1/8',
         'Between the pylon and the solar display (G2)', 'Backlit / printed', 'display'),
        ('B7', 'Product collage', 1, '49 1/4', '36 1/8', '—', '48 3/4', '84 7/8',
         'Backdrop showroom face, left of the pylon (G2)', 'Backlit / printed', 'display'),
        ('B8', 'Botanical artwork', 3, '14 3/4', '25 1/8', '—', '50 1/8', '75 1/4',
         'Backdrop showroom face — 2 left, 1 right (G2)', 'Canvas print', 'canvas'),
    ]),
    ('C', 'Frontage — header board, cloth band, side panels, portraits', [
        ('C1', 'Frontage header board', 1, '575 7/8', '48', '—', '174 1/2', '222 1/2',
         '156 5/8" ahead of stall front; centred on CL · see G3', 'Printed board', 'board'),
        ('C2', 'Frontage cloth band', 1, '575 7/8', '30', '—', '144 1/2', '174 1/2',
         'Directly below the header board', 'Printed cloth', 'board'),
        ('C3', 'Left side panel (true face)', 1, '108', '139 3/4', 'plan width 102 5/8', '4 3/4', '144 1/2',
         'Raked 18° off the board line · see G3/G4', 'Printed board', 'board'),
        ('C4', 'Right side panel (true face)', 1, '108', '139 3/4', 'plan width 99 1/4', '4 3/4', '144 1/2',
         'Raked 23° off the board line · see G3/G4', 'Printed board', 'board'),
        ('C5', 'Minister portrait photo', 4, '20 3/8', '30 1/2', '24 × 34 1/8 brass frame', '185 3/8', '215 7/8',
         'On header board; frame centres 22 1/2" and 66 7/8" each side of CL', 'Photo print', 'photo'),
    ]),
    ('D', 'Logos and exterior signage', [
        ('D1', 'MSIL logo — fascia', 1, '34 5/8', '18 7/8', 'fascia 346 3/8 × 37', '118 1/2', '137 3/8',
         'Front fascia, from 19" left of CL (confirm)', 'Printed / acrylic', 'vector'),
        ('D2', 'MSIL logo — reception desk', 1, '26', '14 1/8', 'desk 69 3/4 wide', '15 3/8', '29 5/8',
         'Reception desk front, centred (G2)', 'Printed / acrylic', 'vector'),
        ('D3', 'Exterior left wall — MSIL logotype', 1, '29 7/8', '9 3/4', 'lockup zone 53 7/8 wide', '105 7/8',
         '115 5/8', 'Starts 118 5/8" from stall front · see W5', 'Printed', 'vector'),
        ('D4', 'Exterior left wall — "Everyday Essentials" block', 1, '44 1/8', '9 3/4', '—', '20', '29 3/4',
         'Under the lockup (x not dimensioned) · see W5', 'Printed', 'vector'),
        ('D5', 'Exterior right wall — MSIL logotype', 1, '29 7/8', '9 3/4', 'lockup zone 53 7/8 wide', '105 7/8',
         '115 5/8', 'Starts 119 1/8" from stall front · see W5', 'Printed', 'vector'),
    ]),
]

ROWS = []
for gid, gname, items in GROUPS:
    for (i, name, qty, w, h, outer, bot, top, place, finish, kind) in items:
        w, h, bot, top = q(w), q(h), q(bot), q(top)
        b = BLEED[kind]
        ROWS.append(dict(group=gid, gname=gname, id=i, name=name, qty=qty, w=w, h=h, outer=outer, bot=bot, top=top,
                         place=place, finish=finish, kind=kind, bleed=b, pw=w + 2 * b, ph=h + 2 * b,
                         ratio=w / h, px=(round((w + 2 * b) * 100), round((h + 2 * b) * 100))))


# ------------------------------------------------------------------ SVG drawing helpers
NAVY, GOLD, INK, MUTED, RULE = '#1B2A44', '#D9A441', '#1E2633', '#6B7280', '#9AA3B2'


class Draw:
    def __init__(self, ox, oy, s):
        self.ox, self.oy, self.s, self.el = ox, oy, s, []

    X = lambda self, x: self.ox + x * self.s
    Y = lambda self, h: self.oy - h * self.s

    def rect(self, x0, h0, x1, h1, fill='none', stroke=INK, sw=0.8, dash=None, extra=''):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.el.append(f'<rect x="{self.X(min(x0, x1)):.2f}" y="{self.Y(max(h0, h1)):.2f}" '
                       f'width="{abs(x1 - x0) * self.s:.2f}" height="{abs(h1 - h0) * self.s:.2f}" '
                       f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{extra}/>')

    def text(self, x, h, t, size=7, anchor='middle', fill=INK, weight=500, dy=0, rot=False):
        r = f' transform="rotate(-90 {self.X(x):.2f} {self.Y(h) + dy:.2f})"' if rot else ''
        self.el.append(f'<text x="{self.X(x):.2f}" y="{self.Y(h) + dy:.2f}" font-size="{size}" text-anchor="{anchor}" '
                       f'fill="{fill}" font-weight="{weight}"{r}>{t}</text>')

    def hline(self, x0, x1, h, stroke=RULE, sw=0.6, dash='3 2'):
        self.el.append(f'<line x1="{self.X(x0):.2f}" y1="{self.Y(h):.2f}" x2="{self.X(x1):.2f}" y2="{self.Y(h):.2f}" '
                       f'stroke="{stroke}" stroke-width="{sw}" stroke-dasharray="{dash}"/>')

    def dim_h(self, x0, x1, h, label=None, off=0, size=6.5, color=NAVY):
        y = self.Y(h) + off
        a, b = self.X(x0), self.X(x1)
        self.el.append(f'<g stroke="{color}" stroke-width="0.6"><line x1="{a:.2f}" y1="{y:.2f}" x2="{b:.2f}" y2="{y:.2f}"/>'
                       f'<line x1="{a - 2:.2f}" y1="{y + 2:.2f}" x2="{a + 2:.2f}" y2="{y - 2:.2f}"/>'
                       f'<line x1="{b - 2:.2f}" y1="{y + 2:.2f}" x2="{b + 2:.2f}" y2="{y - 2:.2f}"/>'
                       f'<line x1="{a:.2f}" y1="{y - 3:.2f}" x2="{a:.2f}" y2="{y + 3:.2f}"/>'
                       f'<line x1="{b:.2f}" y1="{y - 3:.2f}" x2="{b:.2f}" y2="{y + 3:.2f}"/></g>')
        lab = label if label is not None else f(x1 - x0)
        self.el.append(f'<text x="{(a + b) / 2:.2f}" y="{y - 2.5:.2f}" font-size="{size}" text-anchor="middle" '
                       f'fill="{color}" font-weight="600">{lab}</text>')

    def dim_v(self, x, h0, h1, label=None, off=0, size=6.5, color=NAVY, side='left'):
        X = self.X(x) + off
        a, b = self.Y(h0), self.Y(h1)
        self.el.append(f'<g stroke="{color}" stroke-width="0.6"><line x1="{X:.2f}" y1="{a:.2f}" x2="{X:.2f}" y2="{b:.2f}"/>'
                       f'<line x1="{X - 2:.2f}" y1="{a + 2:.2f}" x2="{X + 2:.2f}" y2="{a - 2:.2f}"/>'
                       f'<line x1="{X - 2:.2f}" y1="{b + 2:.2f}" x2="{X + 2:.2f}" y2="{b - 2:.2f}"/>'
                       f'<line x1="{X - 3:.2f}" y1="{a:.2f}" x2="{X + 3:.2f}" y2="{a:.2f}"/>'
                       f'<line x1="{X - 3:.2f}" y1="{b:.2f}" x2="{X + 3:.2f}" y2="{b:.2f}"/></g>')
        lab = label if label is not None else f(h1 - h0)
        tx = X - 3 if side == 'left' else X + 9
        self.el.append(f'<text x="{tx:.2f}" y="{(a + b) / 2:.2f}" font-size="{size}" text-anchor="middle" fill="{color}" '
                       f'font-weight="600" transform="rotate(-90 {tx:.2f} {(a + b) / 2:.2f})">{lab}</text>')

    def level(self, x0, x1, h, label, right=True):
        self.hline(x0, x1, h)
        self.el.append(f'<text x="{self.X(x1) + 4:.2f}" y="{self.Y(h) + 2.3:.2f}" font-size="6.3" fill="{MUTED}">'
                       f'{label}</text>')

    def banner(self, x0, b0, w, h, fx0, fb0, fw, fh, tag, fill='#F4E3B5'):
        self.rect(fx0, fb0, fx0 + fw, fb0 + fh, fill='#C9A24A', stroke='#8A6A22', sw=0.6)
        self.rect(x0, b0, x0 + w, b0 + h, fill=fill, stroke='#8A6A22', sw=0.5)
        self.text(x0 + w / 2, b0 + h / 2 + 6 / self.s, tag, size=15, weight=700, fill=NAVY)
        self.text(x0 + w / 2, b0 + h / 2 - 9 / self.s, f'{wh(w, h)}', size=7.5, weight=600, fill=NAVY)
        self.text(x0 + w / 2, b0 + h / 2 - 19 / self.s, 'visible print', size=6.3, fill=MUTED)

    def svg(self, w, h):
        return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
                f'font-family="Barlow Semi Condensed">' + ''.join(self.el) + '</svg>')


def wall_elevation(title_left, title_right, length, frames, f_bot, f_h, inset, ids, note_y, s=1.68):
    """Interior side wall: x from the backdrop face (or from the rear when mirrored)."""
    d = Draw(105, 330, s)
    d.rect(0, 5 + 3 / 8, length, 144, fill='#EEE9DF', stroke=INK, sw=0.9)
    d.rect(-6, 0, length + 6, 5 + 3 / 8, fill='#D8D2C6', stroke=INK, sw=0.6)
    for xs, label in [(0, title_left), (length, title_right)]:
        d.text(xs, 0, label, size=7.2, fill=NAVY, weight=700, anchor='start' if xs == 0 else 'end', dy=14)
    chain = []
    x = frames[0]
    for k in range(3):
        chain.append(x)
        x += frames[1] + (frames[2] if k < 2 else 0)
    fw = frames[1]
    pos = [0] + sum([[c, c + fw] for c in chain], []) + [length]
    for a, b in zip(pos, pos[1:]):
        d.dim_h(a, b, 144, off=-14)
    d.dim_h(0, length, 144, f'INTERIOR WALL LENGTH {f(length)}', off=-30, size=7.2)
    order = list(zip(chain, ids))
    for c, tag in order:
        d.banner(c + inset, f_bot + inset, fw - 2 * inset, f_h - 2 * inset, c, f_bot, fw, f_h, tag)
        d.dim_h(c + inset, c + fw - inset, f_bot, off=12, label=f'banner {f(fw - 2 * inset)}', color='#7A5A12')
        d.text(c + fw / 2, f_bot + f_h - inset - 10 / s, note_y[tag], size=6.8, fill=MUTED)
    c0 = chain[0]
    d.dim_v(length, 0, 144, f'WALL TOP {f(144)}', off=58, side='right')
    d.dim_v(length, 0, f_bot + inset, f'{f(f_bot + inset)}', off=28, side='right', color='#7A5A12')
    d.dim_v(length, f_bot + inset, f_bot + f_h - inset, f'banner {f(f_h - 2 * inset)}', off=28, side='right',
            color='#7A5A12')
    for h, lab in [(144, 'wall top 144"'), (f_bot + f_h - inset, f'banner top {f(f_bot + f_h - inset)}'),
                   (f_bot + inset, f'banner bottom {f(f_bot + inset)}'),
                   (5 + 3 / 8, 'platform top 5 3/8"'), (0, 'hall floor 0"')]:
        d.level(-6, -6, h, '')
        d.el.append(f'<text x="{d.X(-8):.2f}" y="{d.Y(h) + 2.3:.2f}" font-size="6.3" fill="{MUTED}" '
                    f'text-anchor="end">{lab}</text>')
    return d.svg(900, 395)


# ------------------------------------------------------------------ pages
def page(n, code, title, body, notes=''):
    return f'''<section class="pg">
  <header><span class="brand">MSIL PAVILION</span><span class="sub">GRAPHICS &amp; POSTER SIZES · INCHES</span></header>
  <div class="meta">All sizes in INCHES · heights above hall floor (+0), platform top 5 3/8" · from MSIL_Set_Build_Dimensions_INCHES.pdf (model 15 Oct 2026) · supersedes earlier poster sizes</div>
  <div class="body">{body}</div>
  {f'<div class="notes">{notes}</div>' if notes else ''}
  <footer><span class="code">{code} · {title}</span><span class="num">{n:02d} / 09</span></footer>
</section>'''


def table(groups):
    head = ('<tr><th>ID</th><th>Item</th><th>Qty</th><th>Visible print<br>W × H</th><th>Frame / surround</th>'
            '<th>Print file size<br>incl. bleed*</th><th>Ratio<br>W:H</th><th>Bottom → top<br>above hall floor</th>'
            '<th>Placement</th><th>Finish</th><th>File @100 ppi<br>(px)</th></tr>')
    out = ['<table class="sched">', head]
    for gid in groups:
        rows = [r for r in ROWS if r['group'] == gid]
        out.append(f'<tr class="grp"><td colspan="11">{gid} · {rows[0]["gname"]}</td></tr>')
        for r in rows:
            out.append(
                f'<tr><td class="id">{r["id"]}</td><td class="nm">{r["name"]}</td><td class="c">{r["qty"]}</td>'
                f'<td class="sz">{wh(r["w"], r["h"])}</td><td>{r["outer"]}</td>'
                f'<td>{wh(r["pw"], r["ph"]) if r["bleed"] else "vector, no bleed"}</td>'
                f'<td class="c">{r["ratio"]:.3f}</td><td>{f(r["bot"])} → {f(r["top"])}</td><td>{r["place"]}</td>'
                f'<td>{r["finish"]}</td><td class="c">{"—" if not r["bleed"] else f"{r[chr(112)+chr(120)][0]:,} × {r[chr(112)+chr(120)][1]:,}"}</td></tr>')
    out.append('</table>')
    return ''.join(out)


BLEED_NOTE = ('*Print file size = visible print + bleed each side: framed banners and boards 1", display prints, '
              'portrait photos and canvas 1/2", logos are vector cut-to-shape. Bleed values are a recommendation — '
              'confirm with the printer/fabricator. Keep text and logos at least 2" inside the visible edge on banners '
              'and boards, 1" on display prints.')

pages = []
pages.append(page(1, 'P1', 'Graphics schedule (1/2) — wall banners and frontage', table(['A', 'C']),
                  f'<b>{sum(r["qty"] for r in ROWS if r["group"] != "D")} printed pieces (A–C) + 5 logos/signs (D).</b> {BLEED_NOTE}'))
pages.append(page(2, 'P2', 'Graphics schedule (2/2) — showroom graphics, logos and signage', table(['B', 'D']),
                  'Showroom graphics sit inside their display surrounds; the pack gives heights but not x positions for '
                  'B6–B8 and D4 — use the G2 reference (sheet P6) and confirm on site. ' + BLEED_NOTE))

LEN = q('423 1/4')
ny = {'A1': 'y 203 7/8"–306 1/4"', 'A2': 'y 333 7/8"–436 1/4"', 'A3': 'y 463 3/4"–566 1/8"',
      'A4': 'y 203 7/8"–306 1/4"', 'A5': 'y 333 7/8"–436 1/4"', 'A6': 'y 463 3/4"–566 1/8"'}
pages.append(page(3, 'P3', 'Left wall — interior face, banners A1–A3 (entry at the left)',
                  wall_elevation('← BACKDROP (entry side)', 'REAR WALL →', LEN, (30.5, q('105 1/8'), 24.75),
                                 q('24 5/8'), q('105 1/8'), q('1 3/8'), ['A1', 'A2', 'A3'], ny),
                  '<b>3 banners, each 102 3/8" × 102 3/8" visible</b>, in brass frames 105 1/8" × 105 1/8" (1 3/8" lip). '
                  'Banner bottom 26", top 128 3/8" above hall floor (20 5/8"–123" above platform). First frame 30 1/2" '
                  'from the backdrop, frames 24 3/4" apart, last frame 27 3/4" from the rear wall. y = distance from the '
                  'stall front edge.'))
pages.append(page(4, 'P4', 'Right wall — interior face, banners A4–A6 (entry at the right)',
                  wall_elevation('← REAR WALL', 'BACKDROP (entry side) →', LEN, (27.75, q('105 1/8'), 24.75),
                                 q('24 5/8'), q('105 1/8'), q('1 3/8'), ['A6', 'A5', 'A4'], ny),
                  '<b>3 banners, each 102 3/8" × 102 3/8" visible</b>, same sizes and heights as the left wall, mirrored: '
                  'A4 is nearest the backdrop. Frame 105 1/8" × 105 1/8"; banner bottom 26", top 128 3/8".'))


def rear_and_backdrop():
    s = 1.0
    # rear wall
    d = Draw(45, 300, s)
    W = q('351 3/8')
    d.rect(0, 5 + 3 / 8, W, 144, fill='#EEE9DF')
    d.rect(-4, 0, W + 4, 5 + 3 / 8, fill='#D8D2C6', sw=0.6)
    fx = [q('91 1/4'), q('91 1/4') + q('82 1/4') + q('5 1/8')]
    for x0, tag in zip(fx, ['A7', 'A8']):
        d.banner(x0 + q('1 3/8'), q('31 1/8'), q('79 1/2'), q('99 5/8'), x0, q('29 3/4'), q('82 1/4'), q('102 3/8'), tag)
    pos = [0, fx[0], fx[0] + q('82 1/4'), fx[1], fx[1] + q('82 1/4'), W]
    for a, b in zip(pos, pos[1:]):
        d.dim_h(a, b, 144, off=-12)
    d.dim_h(0, W, 144, f'CLEAR WIDTH {f(W)}', off=-27, size=7)
    d.dim_v(W, 0, q('31 1/8'), off=14, side='right', color='#7A5A12')
    d.dim_v(W, q('31 1/8'), q('130 3/4'), 'banner 99 5/8"', off=14, side='right', color='#7A5A12')
    d.dim_v(W, 0, 144, 'WALL TOP 144"', off=38, side='right')
    d.text(W / 2, 0, 'REAR WALL — interior face (looking at the rear wall; stall-left on the left)', size=7.5,
           weight=700, fill=NAVY, dy=16)
    # backdrop
    e = Draw(478, 300, s)
    e.rect(0, 4.75, W, q('100 5/8'), fill='#EEE9DF')
    e.rect(-4, 0, W + 4, 5 + 3 / 8, fill='#D8D2C6', sw=0.6)
    xs = [10, 10 + q('39 7/8') + 26, 10 + q('39 7/8') + 26 + q('86 3/4') + 26]
    for dx in (10, W - 10 - q('39 7/8')):
        e.rect(dx, 5 + 3 / 8, dx + q('39 7/8'), 5 + 3 / 8 + 86, fill='#FFFFFF', stroke=MUTED, sw=0.6)
        e.text(dx + q('39 7/8') / 2, 50, 'door', size=6.5, fill=MUTED)
        e.text(dx + q('39 7/8') / 2, 42, '36" × 84"', size=6.5, fill=MUTED)
    for x0, tag in zip(xs[1:], ['A10', 'A9']):
        e.banner(x0 + q('1 3/8'), q('16 5/8'), 84, 72, x0, q('15 1/4'), q('86 3/4'), q('74 3/4'), tag)
    pos = [0, 10, 10 + q('39 7/8'), xs[1], xs[1] + q('86 3/4'), xs[2], xs[2] + q('86 3/4'),
           W - 10 - q('39 7/8'), W - 10, W]
    for a, b in zip(pos, pos[1:]):
        e.dim_h(a, b, q('100 5/8'), off=-12, size=5.8)
    e.dim_h(0, W, q('100 5/8'), f'BACKDROP WIDTH {f(W)}', off=-27, size=7)
    e.dim_v(W, 0, q('16 5/8'), off=14, side='right', color='#7A5A12')
    e.dim_v(W, q('16 5/8'), q('88 5/8'), 'banner 72"', off=14, side='right', color='#7A5A12')
    e.dim_v(W, 0, q('100 5/8'), 'BACKDROP TOP 100 5/8"', off=38, side='right')
    e.text(W / 2, 0, 'BACKDROP — interior face (looking toward the entry; stall-left on the right)', size=7.5,
           weight=700, fill=NAVY, dy=16)
    return '<svg width="890" height="350" viewBox="0 0 890 350" xmlns="http://www.w3.org/2000/svg" ' \
           'font-family="Barlow Semi Condensed">' + ''.join(d.el + e.el) + '</svg>'


pages.append(page(5, 'P5', 'Rear wall (A7–A8) and backdrop interior face (A9–A10)', rear_and_backdrop(),
                  '<b>Rear wall: 2 banners 79 1/2" × 99 5/8" visible</b> (frames 82 1/4" × 102 3/8"), bottom 31 1/8", top '
                  '130 3/4"; frames 5 1/8" apart. <b>Backdrop interior: 2 banners 84" × 72" visible</b> (frames 86 3/4" × '
                  '74 3/4"), bottom 16 5/8", top 88 5/8"; frames 26" apart, between the two 36" × 84" doors. Backdrop '
                  'banner 1 (A9) is on the stall-left side, which appears on the right when facing the entry.'))

# G2 reference with tags (tag positions in the 110-dpi sheet coordinates, crop origin 160,110)
img = base64.b64encode(G2_IMG.read_bytes()).decode()
TAGS = [('B1', 300, 330), ('B2', 285, 505), ('B3', 690, 300), ('B4', 1015, 300), ('B5', 1125, 300),
        ('B6', 805, 320), ('B7', 545, 320), ('B8', 420, 355), ('B8', 470, 355), ('B8', 895, 355), ('D1', 690, 185),
        ('D2', 690, 485)]
sc = 640 / 1140
tags = ''.join(f'<g><circle cx="{(x - 160) * sc:.1f}" cy="{(y - 110) * sc:.1f}" r="10" fill="{NAVY}" stroke="#FFFFFF" '
               f'stroke-width="1.5"/><text x="{(x - 160) * sc:.1f}" y="{(y - 110) * sc + 3.2:.1f}" font-size="8.5" '
               f'font-weight="700" fill="#FFFFFF" text-anchor="middle">{t}</text></g>' for t, x, y in TAGS)
g2 = (f'<svg width="640" height="{495 * sc:.0f}" viewBox="0 0 640 {495 * sc:.0f}" xmlns="http://www.w3.org/2000/svg" '
      f'xmlns:xlink="http://www.w3.org/1999/xlink" font-family="Barlow Semi Condensed">'
      f'<image width="640" height="{495 * sc:.0f}" xlink:href="data:image/png;base64,{img}"/>{tags}</svg>')
mini = ''.join(f'<span><b>{r["id"]}</b> {r["name"]} — {wh(r["w"], r["h"])}{" ×" + str(r["qty"]) if r["qty"] > 1 else ""}, '
               f'{f(r["bot"])}→{f(r["top"])}</span>' for r in ROWS if r['group'] in 'B' or r['id'] in ('D1', 'D2'))
pages.append(page(6, 'P6', 'Front of the stall — showroom graphics placement (reference: sheet G2)',
                  f'<div class="g2wrap"><div class="g2">{g2}</div><div class="mini">{mini}</div></div>',
                  'Reference image is the G2 render from the set-build pack; tags mark where each graphic sits. Heights '
                  'are exact (from E2); horizontal positions of B6–B8 are not dimensioned in the pack — set them out from '
                  'G2 and confirm on site.'))


def frontage():
    s = 1.38
    d = Draw(445, 345, s)
    BW = q('575 7/8')
    d.rect(-180, q('5 3/8'), 180, q('145 3/8'), fill='none', stroke=MUTED, sw=0.6, dash='4 3')
    d.text(0, 70, 'STALL BEHIND — 360" wide', size=7, fill=MUTED, weight=600)
    d.rect(-BW / 2, q('174 1/2'), BW / 2, q('222 1/2'), fill='#F4E3B5', stroke='#8A6A22')
    d.rect(-BW / 2, q('144 1/2'), BW / 2, q('174 1/2'), fill='#E9D8EE', stroke='#8A6A22')
    d.text(-200, 196, 'C1 · HEADER BOARD 575 7/8" × 48"', size=8, weight=700, fill=NAVY)
    d.text(-200, 156, 'C2 · CLOTH BAND 575 7/8" × 30"', size=8, weight=700, fill=NAVY)
    for cx in (-q('66 7/8'), -22.5, 22.5, q('66 7/8')):
        d.rect(cx - 12, q('183 5/8'), cx + 12, q('217 3/4'), fill='#C9A24A', stroke='#8A6A22', sw=0.6)
        d.rect(cx - q('20 3/8') / 2, q('185 3/8'), cx + q('20 3/8') / 2, q('215 7/8'), fill='#FFFFFF', stroke='#8A6A22',
               sw=0.4)
        d.text(cx, 198, 'C5', size=7.5, weight=700, fill=NAVY)
    for x0, x1, tag in [(-289, q('-186 1/4'), 'C3'), (q('188 5/8'), q('287 3/4'), 'C4')]:
        d.rect(x0, q('4 3/4'), x1, q('144 1/2'), fill='#DCE6F2', stroke='#8A6A22')
        d.text((x0 + x1) / 2, 82, tag, size=14, weight=700, fill=NAVY)
        d.text((x0 + x1) / 2, 68, 'true face 108" × 139 3/4"', size=7, weight=600, fill=NAVY)
        d.text((x0 + x1) / 2, 60, '(raked — shown in plan width)', size=6.3, fill=MUTED)
    d.dim_h(-BW / 2, BW / 2, q('222 1/2'), f'HEADER BOARD WIDTH {f(BW)}', off=-12, size=7)
    d.dim_h(-q('66 7/8') - 12, -q('66 7/8') + 12, q('217 3/4'), '24"', off=-3, size=5.8)
    d.dim_h(-289, q('-186 1/4'), 0, 'plan 102 5/8"', off=12)
    d.dim_h(q('188 5/8'), q('287 3/4'), 0, 'plan 99 1/4"', off=12)
    d.dim_h(-180, 180, 0, 'STALL 360"', off=12)
    d.dim_v(BW / 2, q('174 1/2'), q('222 1/2'), '48"', off=12, side='right')
    d.dim_v(BW / 2, q('144 1/2'), q('174 1/2'), '30"', off=12, side='right')
    d.dim_v(BW / 2, 0, q('144 1/2'), '144 1/2"', off=12, side='right')
    d.dim_v(BW / 2, 0, q('222 1/2'), 'TOP 222 1/2"', off=34, side='right')
    d.dim_v(-BW / 2, q('4 3/4'), q('144 1/2'), 'panel 139 3/4"', off=-12)
    d.hline(-BW / 2 - 20, BW / 2 + 20, 0, stroke=INK, sw=0.8, dash='')
    return d.svg(890, 370)


pages.append(page(7, 'P7', 'Frontage — header board, cloth band, side panels and portraits (front elevation)',
                  frontage(),
                  '<b>C1 header board 575 7/8" × 48"</b> (174 1/2"–222 1/2") and <b>C2 cloth band 575 7/8" × 30"</b> '
                  '(144 1/2"–174 1/2"), both 156 5/8" in front of the stall and centred on it (107 7/8" overhang each side). '
                  '<b>C3/C4 side panels: print the true face 108" × 139 3/4"</b> (4 3/4"–144 1/2") — the drawing shows their '
                  'raked plan widths. <b>C5 portraits ×4:</b> photo 20 3/8" × 30 1/2" in 24" × 34 1/8" frames, frame bottom '
                  '183 5/8", centres 22 1/2" and 66 7/8" each side of the centre line; name line under each.'))


def exterior():
    s = 1.05
    out = []
    for k, (label, front_right, logo_x, ess) in enumerate([
            ('LEFT WALL — exterior (front of stall on the right)', True, q('118 5/8'), True),
            ('RIGHT WALL — exterior (front of stall on the left)', False, q('119 1/8'), False)]):
        d = Draw(130, 180 + k * 195, s)
        X = (lambda v: 600 - v) if front_right else (lambda v: v)
        d.rect(0, q('4 3/4'), 600, 144, fill='#E4E1DA', stroke=INK, sw=0.8)
        d.text(300, 0, label, size=7.5, weight=700, fill=NAVY, dy=26)
        z0, z1 = X(q('106 7/8')), X(q('106 7/8') + q('53 7/8'))
        d.rect(min(z0, z1), q('96'), max(z0, z1), q('115 5/8'), fill='none', stroke=MUTED, sw=0.5, dash='3 2')
        l0, l1 = X(logo_x), X(logo_x + q('29 7/8'))
        d.rect(min(l0, l1), q('105 7/8'), max(l0, l1), q('115 5/8'), fill='#1B2A6B', stroke='none')
        d.text((l0 + l1) / 2, 108, 'MSIL', size=8, weight=700, fill='#FFFFFF')
        d.text((z0 + z1) / 2, 100, 'company name + Govt. line', size=5.5, fill=MUTED)
        tag = 'D3' if ess else 'D5'
        d.text(max(l0, l1) + 4 if front_right else min(l0, l1) - 4, 108,
               f'{tag} · 29 7/8" × 9 3/4", bottom 105 7/8"', size=6.5, weight=600, fill=NAVY,
               anchor='start' if front_right else 'end')
        if ess:
            c = q('106 7/8') + q('53 7/8') / 2
            e0, e1 = X(c - q('44 1/8') / 2), X(c + q('44 1/8') / 2)
            d.rect(min(e0, e1), 20, max(e0, e1), q('29 3/4'), fill='#2E7D32', stroke='none')
            d.text((e0 + e1) / 2, 22.5, 'Everyday Essentials', size=6, weight=600, fill='#FFFFFF')
            d.text(max(e0, e1) + 4, 22.5, 'D4 · 44 1/8" × 9 3/4", bottom 20"', size=6.5, weight=600, fill=NAVY,
                   anchor='start')
        d.dim_h(min(z0, z1), max(z0, z1), 144, 'lockup 53 7/8"', off=-3, size=6)
        if front_right:
            d.dim_h(z0, 600, 144, '106 7/8" to front', off=-3, size=6)
            d.dim_h(l0, 600, q('4 3/4'), f'{f(logo_x)} to front', off=12, size=6)
        else:
            d.dim_h(0, z0, 144, '106 7/8" to front', off=-3, size=6)
            d.dim_h(0, l0, q('4 3/4'), f'{f(logo_x)} to front', off=12, size=6)
        d.dim_v(600 if front_right else 0, 0, q('105 7/8'), '105 7/8"', off=14 if front_right else -14,
                side='right' if front_right else 'left')
        out += d.el
    return ('<svg width="890" height="400" viewBox="0 0 890 400" xmlns="http://www.w3.org/2000/svg" '
            'font-family="Barlow Semi Condensed">' + ''.join(out) + '</svg>')


pages.append(page(8, 'P8', 'Exterior side walls — signage D3–D5 (seen from outside)', exterior(),
                  'Each side wall is 600" long, 144" to the wall top. The MSIL logotype sits in a 53 7/8"-wide lockup '
                  'that starts 106 7/8" from the stall front, with the company name and Government line below it '
                  '(their heights are not given in the pack — confirm). The "Everyday Essentials for a Brighter '
                  'Tomorrow" block is on the left wall only, bottom 20"; it is drawn centred under the lockup as on '
                  'sheet W5 (x not dimensioned). The rear outer face carries no graphics.'))

NOTES = '''
<div class="cols">
<div><h3>Print files</h3>
<ul>
<li>Set each Illustrator artboard to the <b>print file size incl. bleed</b> (P1–P2). Visible size = trim inside the frame or surround.</li>
<li><b>Header board and cloth band are wider than Illustrator's 227" canvas limit.</b> Use <i>New Document › Large canvas</i> (1:10 scale: board artboard 57 25/32" × 5"), or build at 1:4 and tell the printer the scale.</li>
<li>Resolution at full size: 100 ppi for banners and showroom prints; 50–75 ppi is enough for the header board, cloth and side panels (viewed from distance); 150 ppi for portrait photos.</li>
<li>Logos (D1–D5) must be vector. Convert type to outlines or package fonts.</li>
<li>Backlit prints: supply CMYK with the printer's backlit profile; avoid large flat dark areas.</li>
</ul></div>
<div><h3>Confirm before printing</h3>
<ul>
<li>Bleed per side (1" framed/boards, 1/2" displays) — printer to confirm, incl. pole pockets or hems on the cloth band.</li>
<li>Fascia logo D1: "19" left of centre line" — start edge or centre?</li>
<li>Horizontal positions of B6, B7, B8 and D4; heights of the exterior company-name and Government lines.</li>
<li>Side panels C3/C4 are raked differently (18° and 23°) — artwork is the 108" true face either way.</li>
<li>Doors in the backdrop are drawn as applied frames; if real openings are cut, A9/A10 positions stay as shown.</li>
<li>Per the pack: earlier PDFs and poster files were made for an older model (two side posters, not three banners per side wall). Use these sizes.</li>
</ul></div>
<div><h3>Fit check — artworks rebuilt in this project</h3>
<table class="fit"><tr><th>Artwork (ratio)</th><th>Nearest slot (ratio)</th><th>Fit</th></tr>
<tr><td>Solar Products poster (0.977)</td><td>A1–A6 wall banner (1.000)</td><td>~2% — re-crop</td></tr>
<tr><td>Heat-pump slides (1.333)</td><td>B7 product collage (1.363)</td><td>~2% — re-crop</td></tr>
<tr><td>Solar roll-up (0.435)</td><td>B6 Serving Karnataka (0.432)</td><td>~1% — wrong content</td></tr>
<tr><td>Solar roll-up (0.435)</td><td>B5 Chit Funds print (0.396)</td><td>~10% — re-layout</td></tr>
<tr><td>Solar Portfolio banner (2.452)</td><td>— (B2 pedestal 2.310)</td><td>re-layout</td></tr>
<tr><td>Chits backdrop (3.254)</td><td>— no slot this shape</td><td>re-layout</td></tr>
</table>
<p class="small">All rebuilt artworks are far below full-size resolution (e.g. a 102 3/8" banner needs ~10,240 px at 100 ppi); photos must be relinked to high-res originals.</p>
</div></div>'''
pages.append(page(9, 'P9', 'Print notes, open items and fit check', NOTES))

ff = lambda fam, w, path: (f"@font-face{{font-family:'{fam}';font-weight:{w};"
                           f"src:url('file://{FONTS}/{path}')}}")
CSS = ''.join(ff('Barlow Semi Condensed', w,
                 f'fontsource-barlow-semi-condensed/package/files/barlow-semi-condensed-latin-{w}-normal.woff2')
              for w in (400, 500, 600, 700)) + f'''
@page{{size:960px 540px;margin:0}}
*{{box-sizing:border-box}} body{{margin:0;font-family:'Barlow Semi Condensed';color:{INK}}}
.pg{{width:960px;height:540px;position:relative;overflow:hidden;page-break-after:always;background:#FAF8F4}}
header{{height:44px;background:{NAVY};border-bottom:4px solid {GOLD};display:flex;justify-content:space-between;align-items:center;padding:0 28px;color:#fff}}
.brand{{font-weight:700;font-size:19px;letter-spacing:.3px}} .sub{{font-size:12px;letter-spacing:.6px}}
.meta{{font-size:8.5px;color:{MUTED};padding:6px 28px 0}}
.body{{padding:6px 28px 0}}
.notes{{position:absolute;left:28px;right:28px;bottom:38px;font-size:9px;line-height:1.35;color:#333;border-top:1px solid #ddd;padding-top:5px}}
footer{{position:absolute;left:28px;right:28px;bottom:10px;display:flex;justify-content:space-between;font-weight:700;font-size:13px;color:{NAVY}}}
.num{{font-weight:500;color:{MUTED};font-size:11px}}
table.sched{{width:100%;border-collapse:collapse;font-size:8.3px}}
.sched th{{background:#E9E4D8;text-align:left;padding:3px 4px;font-weight:700;font-size:7.8px;line-height:1.15;border-bottom:1px solid #bbb}}
.sched td{{padding:2.6px 4px;border-bottom:1px solid #e3e0d8;vertical-align:top}}
.sched .grp td{{background:{NAVY};color:#fff;font-weight:700;font-size:8.6px;padding:3px 5px}}
.sched .id{{font-weight:700;color:{NAVY}}} .sched .nm{{font-weight:600}} .sched .sz{{font-weight:700;color:#7A5A12;white-space:nowrap}}
.sched .c{{text-align:center}}
.g2wrap{{display:flex;gap:16px;align-items:flex-start;margin-top:4px}} .g2 svg{{border:1px solid #ddd;display:block}}
.mini{{display:flex;flex-direction:column;gap:5px;font-size:9px;line-height:1.25}}
.cols{{display:grid;grid-template-columns:1fr 1fr 1.15fr;gap:22px;font-size:9.6px;line-height:1.38}}
.cols h3{{font-size:11.5px;color:{NAVY};border-bottom:2px solid {GOLD};padding-bottom:2px;margin:6px 0 6px}}
.cols ul{{padding-left:14px;margin:0}} .cols li{{margin-bottom:5px}}
table.fit{{border-collapse:collapse;width:100%;font-size:9px}} .fit th,.fit td{{border-bottom:1px solid #ddd;padding:3px 4px;text-align:left}}
.fit th{{background:#E9E4D8}} .small{{font-size:8.6px;color:{MUTED}}}
'''
(OUT / 'spec.html').write_text(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(pages)}</body></html>',
                               encoding='utf-8')

# ------------------------------------------------------------------ xlsx
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

wb = Workbook()
ws = wb.active
ws.title = 'Graphics schedule'
cols = ['ID', 'Group', 'Item', 'Qty', 'Visible W (in)', 'Visible H (in)', 'Visible W × H', 'Frame / surround',
        'Bleed per side (in)', 'Print W incl. bleed (in)', 'Print H incl. bleed (in)', 'Print size incl. bleed',
        'Ratio W:H', 'Bottom above hall floor (in)', 'Top above hall floor (in)', 'Bottom → top',
        'Placement', 'Finish', 'File @100 ppi W (px)', 'File @100 ppi H (px)']
ws.append(cols)
for r in ROWS:
    ws.append([r['id'], r['gname'], r['name'], r['qty'], r['w'], r['h'], wh(r['w'], r['h']), r['outer'], r['bleed'],
               r['pw'], r['ph'], wh(r['pw'], r['ph']) if r['bleed'] else 'vector, no bleed', round(r['ratio'], 3),
               r['bot'], r['top'], f'{f(r["bot"])} → {f(r["top"])}', r['place'], r['finish'],
               r['px'][0] if r['bleed'] else None, r['px'][1] if r['bleed'] else None])
for c in ws[1]:
    c.font = Font(bold=True, color='FFFFFF')
    c.fill = PatternFill('solid', fgColor='1B2A44')
    c.alignment = Alignment(wrap_text=True, vertical='center')
widths = [6, 28, 34, 5, 10, 10, 18, 26, 9, 11, 11, 20, 8, 11, 11, 18, 48, 16, 11, 11]
for i, w in enumerate(widths):
    ws.column_dimensions[chr(65 + i)].width = w
ws.freeze_panes = 'D2'
ws.row_dimensions[1].height = 42
ws2 = wb.create_sheet('Notes')
for line in ['All sizes in inches; heights above the hall floor (platform top = 5 3/8").',
             'Source: MSIL_Set_Build_Dimensions_INCHES.pdf (Blender model MSIL_30x50_Frontage_Addon, 15 Oct 2026).',
             'Visible = printed area seen inside the frame or surround. Print size = visible + bleed on each side.',
             'Bleed values are recommendations (1" framed banners and boards, 1/2" display prints/photos/canvas); '
             'confirm with the printer.',
             'Header board and cloth band exceed Illustrator\'s 227" canvas: use a Large canvas document (1:10).',
             'Not dimensioned in the pack: x positions of B6, B7, B8, D4; heights of the exterior name/Government lines.']:
    ws2.append([line])
ws2.column_dimensions['A'].width = 120
wb.save(OUT / 'MSIL_Pavilion_Graphics_Schedule.xlsx')
print('rows', len(ROWS))
