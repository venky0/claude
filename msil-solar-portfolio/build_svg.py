"""Build the MSIL Solar Product Portfolio banner as a layered SVG (1 px = 1 pt) for Illustrator.

usage: python3 build_svg.py <dir>   (reads <dir>/links/*.png, icons.json, sizes.json)
"""
import base64, json, sys
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(sys.argv[1])
LINKS = OUT / 'links'
ICONS = json.loads((OUT / 'icons.json').read_text())
SIZES = json.loads((OUT / 'sizes.json').read_text()) if (OUT / 'sizes.json').exists() else {}
W, H = 1964, 801

NAVY = '#0B1A6B'
NAVY_TXT = '#06135E'
INK = '#111633'  # body copy on light backgrounds
BAND = '#012C64'
ORANGE = '#F47A12'
BLUE = '#0372BA'
MARK_ORANGE = '#F09129'

WEIGHT = {400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold', 800: 'ExtraBold'}


def font(family, w):
    ps = family.replace(' ', '') + '-' + WEIGHT[w]
    return f"font-family=\"'{ps}', '{family}'\" font-weight=\"{w}\""


COND = lambda w: font('Barlow Condensed', w)
SEMI = lambda w: font('Barlow Semi Condensed', w)
BARLOW = lambda w: font('Barlow', w)
KN = font('Noto Sans Kannada', 800)


def T(id_, x, y, text, f, size, fill, anchor='start', key=None, fit=None, ls=None, extra=''):
    """Text element. `key` groups lines that share one calibrated size; `fit` is the measured
    source width (pt) the calibration pass scales that line to."""
    key = key or id_
    size = SIZES.get(key, size)
    a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
    l = f' letter-spacing="{ls}"' if ls else ''
    d = f' data-key="{key}"' + (f' data-fit="{fit}"' if fit else '')
    return (f'<text id="{id_}" x="{x}" y="{y}"{a} {f} font-size="{size:.2f}"{l} fill="{fill}"{d}{extra}>'
            f'{text if text.startswith("<") else escape(text)}</text>')


def lines(prefix, x, ys, texts, f, size, fill, anchor='start', key=None, fit=None):
    """Stacked lines; the first `fit` = (line index, width)."""
    out = []
    for i, (y, t) in enumerate(zip(ys, texts)):
        ft = fit[1] if fit and fit[0] == i else None
        out.append(T(f'{prefix}-{i+1}', x, y, t, f, size, fill, anchor, key or prefix, ft))
    return ''.join(out)


def img(path, x, y, w, h, id_):
    data = base64.b64encode((LINKS / path).read_bytes()).decode()
    return (f'<image id="{id_}" x="{x}" y="{y}" width="{w}" height="{h}" '
            f'preserveAspectRatio="none" xlink:href="data:image/png;base64,{data}"/>')


def icon(name):
    return (f'<g id="icon-{name.replace("_", "-")}">' +
            ''.join(f'<path fill="{l["fill"]}" fill-rule="evenodd" d="{l["d"]}"/>' for l in ICONS[name]) + '</g>')


def mark(x, y, s, id_='mark'):
    """MSIL stepped mark; native size 51 x 51."""
    return (f'<g id="{id_}" transform="translate({x} {y}) scale({s})">'
            f'<path fill="{BLUE}" d="M0 0H51V17H34V33H16V51H0Z"/>'
            f'<path fill="{MARK_ORANGE}" d="M9 9H34V16H26V24H17V33H9Z"/></g>')


def ring(cx, cy, r, stroke, sw, fill='none', fo=1):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" fill-opacity="{fo}" stroke="{stroke}" stroke-width="{sw}"/>'


def vline(x, y0, y1, c, w=1):
    return f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}" stroke="{c}" stroke-width="{w}"/>'


def hline(x0, x1, y, c, w=1):
    return f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{c}" stroke-width="{w}"/>'


# ------------------------------------------------------------------ header
header = f'''
  <g id="Header">
    <rect id="header-bg" width="{W}" height="110" fill="#FDF6EB"/>
    {mark(540, 7, 1.45, 'header-mark')}
    {T('header-msil', 601, 83, 'MSIL', SEMI(700), 70, NAVY_TXT, fit=139)}
    {T('header-title', 767, 62, 'SOLAR PRODUCT PORTFOLIO', SEMI(700), 50, NAVY_TXT, fit=583)}
    <rect id="header-rule" x="767" y="68" width="583" height="2" fill="#3FAE49"/>
    {T('header-subtitle', 768, 93, 'MYSORE SALES INTERNATIONAL LIMITED   |   CIPD', BARLOW(500), 17, NAVY_TXT, fit=527, ls=3.2, extra=' xml:space="preserve"')}
    {icon('leaf_header')}
    {T('header-slogan', 1460, 73, 'CLEAN ENERGY. LOWER BILLS. BETTER TOMORROW.', COND(700), 28, NAVY_TXT, fit=477)}
  </g>'''

# ------------------------------------------------------------------ street lights
SPEC_Y = [427.5, 477.5, 533, 607, 666]
SPEC_TXT = [
    ('POLE HEIGHT', [None]),
    ('LITHIUM BATTERY', ['<tspan>LiFePO</tspan><tspan font-size="9" dy="2.5">4</tspan><tspan dy="-2.5"> Battery</tspan>', 'Long Life (5+ Years)']),
    ('PIR MOTION SENSOR', ['Automatically Adjusts', 'Brightness to Save', 'More Energy']),
    ('HIGH EFFICIENCY LED', ['150+ lm/W High Brightness', 'Uniform Light Distribution']),
    ('ALL WEATHER PROOF', ['Dustproof, Waterproof', '& Corrosion Resistant']),
]
TITLE_Y = [427, 470, 528.5, 602.5, 660]
POLE = ['6m – 7m', '6m – 8m', '9m – 12m']


def tag(i, x0, x1, label, fill, fo=1):
    return (f'<g id="tag-{i}"><path d="M{x0} 262H{x1}L{x1-8} 293H{x0}Z" fill="{fill}" fill-opacity="{fo}"/>'
            f'<path d="M{x1+1} 262H{x1+5}L{x1-3} 293H{x1-7}Z" fill="#34B44A"/>'
            + T(f'tag-{i}-text', x0 + 10, 287, label, COND(600), 24, '#FFFFFF', key='tag', fit=96 if i == 0 else None) + '</g>')


def spec_panel(p, ix, tx, ink, ring_fill):
    out = [f'<g id="panel-{p}-specs">']
    names = ['pole', 'battery', 'pir', 'led', 'shield']
    for k, (name, cy) in enumerate(zip(names, SPEC_Y)):
        out.append(f'<g id="panel-{p}-spec-{name}">')
        out.append(ring(ix, cy, 18.5, ink, 2.6, ring_fill, 0.92 if ring_fill != 'none' else 1))
        out.append(icon(f'spec{p}_{name}'))
        if p == 2 and name == 'battery':
            out.append(icon('spec2_battery_bolt'))
        title, body = SPEC_TXT[k]
        if name == 'pole':
            body = [POLE[p]]
        out.append(T(f'panel-{p}-{name}-title', tx, TITLE_Y[k], title, COND(700), 18, ink, key='spec-title',
                     fit=91 if (p, k) == (0, 1) else None))
        ys = [TITLE_Y[k] + 16.5 * (j + 1) - (0.5 if j else 0) for j in range(len(body))]
        for j, (y, t) in enumerate(zip(ys, body)):
            out.append(T(f'panel-{p}-{name}-{j+1}', tx, round(y, 1), t, SEMI(500), 15, INK if p < 2 else ink, key='spec-body',
                         fit=145.5 if (p, k, j) == (0, 3, 0) else None))
        out.append('</g>')
    out.append('</g>')
    return ''.join(out)


FEAT = [(445, 'feat_solar', 'SOLAR POWERED', ['100% Clean', '& Renewable']),
        (534, 'feat_battery', 'LITHIUM BATTERY', ['Long Life &', 'High Performance']),
        (628, 'feat_pir', 'PIR MOTION SENSOR', ['Smart & Energy', 'Efficient']),
        (721, 'feat_shield', 'BUILT TO LAST', ['Rugged Design for', 'All Weather'])]
feat = ''.join(
    f'<g id="feature-{i+1}"><circle cx="{cx}" cy="161" r="30" fill="#FFFFFF" fill-opacity="0.9"/>{icon(ic)}'
    + T(f'feature-{i+1}-title', cx, 208, t, COND(600), 14, NAVY_TXT, 'middle', 'feat-title', 71.5 if i == 0 else None)
    + ''.join(T(f'feature-{i+1}-{j+1}', cx, 223 + 14 * j, b, COND(400), 13, NAVY_TXT, 'middle', 'feat-body',
                75 if (i, j) == (1, 1) else None) for j, b in enumerate(body))
    + '</g>' for i, (cx, ic, t, body) in enumerate(FEAT))

street = f'''
  <g id="Street_lights">
    <rect id="street-top-bg" y="110" width="789" height="143" fill="url(#streetTop)"/>
    <g id="street-headline-kn">
      {T('street-kn-1', 218.5, 150, 'ಆಲ್-ಇನ್-ಒನ್ ಸೌರ ಬೀದಿ', KN, 36, NAVY_TXT, 'middle', 'kn-street', 377)}
      {T('street-kn-2', 216, 189, 'ದೀಪಗಳು', KN, 36, NAVY_TXT, 'middle', 'kn-street')}
      {T('street-kn-3', 215, 230, 'ಎಂಎಸ್ಐಎಲ್ ಲೈಟ್ಸ್', KN, 36, NAVY_TXT, 'middle', 'kn-street')}
    </g>
    <g id="street-features">{feat}
      {vline(490, 160, 240, '#B3D0EA')}{vline(580, 160, 240, '#B3D0EA')}{vline(675, 160, 240, '#B3D0EA')}
    </g>
    {img('photo_street_lights.png', 0, 253, 789, 447, 'photo-street-lights')}
    {tag(0, 18, 141, 'SINGLE ARM', '#061881')}
    {tag(1, 257, 370, 'TWIN ARM', '#061881')}
    {tag(2, 535, 642, 'HIGHMAST', '#021675', 0.9)}
    {spec_panel(0, 41, 68, NAVY, '#FFFFFF')}
    {spec_panel(1, 275, 302, NAVY, '#FFFFFF')}
    {spec_panel(2, 555, 582, '#FFFFFF', 'none')}
  </g>'''

# ------------------------------------------------------------------ heat pump
HP_ICONS = [(861.5, 'solar', 'SOLAR ENERGY', ['Harness free', 'solar energy']),
            (957.5, 'heatpump', 'HEAT PUMP', ['Works efficiently', 'even in low', 'sunlight & winter']),
            (1052.5, 'water', 'HOT WATER', ['Consistent hot', 'water 24x7,', 'all year round']),
            (1148.5, 'eco', 'ECO-FRIENDLY', ['Lower energy use', '& reduced', 'carbon footprint'])]
hp_icons = ''.join(
    f'<g id="hp-feature-{n}">{ring(cx, 321, 29, NAVY, 2, "#FFFFFF", 0.35)}{icon("hp_" + n)}'
    + T(f'hp-feature-{n}-title', cx, 369, t, COND(600), 14, NAVY_TXT, 'middle', 'hp-title', 67.5 if n == 'solar' else None)
    + ''.join(T(f'hp-feature-{n}-{j+1}', cx, 384 + 14 * j, b, COND(400), 13, NAVY_TXT, 'middle', 'hp-body',
                77.5 if (n, j) == ('eco', 0) else None) for j, b in enumerate(body))
    + '</g>' for cx, n, t, body in HP_ICONS)

BOX = [(421, 'efficiency', ['HIGH EFFICIENCY'], ['Up to 70%', 'energy savings'], 414),
       (489, 'temperature', ['WIDE TEMPERATURE', 'OPERATION'], ['-10°C to 45°C'], 481),
       (560, 'quiet', ['SUPER QUIET', 'OPERATION'], ['Low noise,', 'peaceful comfort'], 550.5),
       (641, 'built', ['BUILT TO LAST'], ['Robust, reliable &', 'corrosion resistant'], 632.5)]


def box_item(cy, n, titles, body, y0):
    out = [f'<g id="hp-box-{n}"><circle cx="1262.5" cy="{cy}" r="22" fill="{ORANGE}"/>{icon("or_" + n)}']
    y = y0
    for j, t in enumerate(titles):
        out.append(T(f'hp-box-{n}-title-{j+1}', 1291, y, t, COND(600), 15, '#FFFFFF', key='box-title',
                     fit=92.5 if (n, j) == ('temperature', 0) else None))
        y += 16.5
    for j, b in enumerate(body):
        out.append(T(f'hp-box-{n}-{j+1}', 1291, round(y, 1), b, SEMI(400), 13.5, '#FFFFFF', key='box-body',
                     fit=89 if (n, j) == ('built', 1) else None))
        y += 15.5
    out.append('</g>')
    return ''.join(out)


heat = f'''
  <g id="Heat_pump">
    {img('photo_heat_pump.png', 792, 110, 599, 590, 'photo-heat-pump')}
    <g id="hp-headline-kn">
      {T('hp-kn-1', 982, 157, 'ಹೀಟ್ ಪಂಪ್‌ನೊಂದಿಗೆ', KN, 34, NAVY_TXT, 'middle', 'kn-hp', 310)}
      {T('hp-kn-2', 987, 191, 'ಸೌರ ಜಲತಾಪಕ', KN, 34, NAVY_TXT, 'middle', 'kn-hp')}
      {T('hp-kn-3', 987, 226, 'ಸೌರ ಜಲತಾಪಕ', KN, 34, NAVY_TXT, 'middle', 'kn-hp')}
    </g>
    <g id="hotspring-logo">
      {mark(1207, 130, 0.66, 'hotspring-mark')}
      {T('hotspring-msil', 1229.5, 182, 'MSIL', SEMI(700), 36, NAVY_TXT, fit=72)}
      {T('hotspring-h', 1150, 224, 'H', BARLOW(800), 44, '#000000', key='hotspring')}
      <circle cx="1194" cy="208" r="15.5" fill="{ORANGE}"/>
      {vline(1194, 173, 244, '#000000', 2.4)}{hline(1172, 1216, 208, '#000000', 2.4)}
      {T('hotspring-tspring', 1212.5, 224, 'TSPRING', BARLOW(800), 44, '#000000', key='hotspring', fit=155)}
      {T('hotspring-sub', 1225, 243, 'SOLAR WATER HEATER', SEMI(700), 15, '#000000', fit=142)}
    </g>
    {lines('hp-intro', 815, [256, 272], ['Integrated solar energy and advanced heat pump technology',
                                        'delivers hot water efficiently, reliably and sustainably.'],
           SEMI(500), 15.5, '#031045', fit=(0, 370))}
    <g id="hp-features">{hp_icons}
      {vline(909, 300, 410, '#CFDDEE')}{vline(1005, 300, 410, '#CFDDEE')}{vline(1100, 300, 410, '#CFDDEE')}
    </g>
    <g id="hp-box">
      <rect x="1235" y="390" width="155" height="292" rx="7" fill="#0A2A68"/>
      {hline(1243, 1385, 455, '#3B5A8F')}{hline(1243, 1385, 528, '#3B5A8F')}{hline(1243, 1385, 610, '#3B5A8F')}
      {''.join(box_item(*b) for b in BOX)}
    </g>
  </g>'''

# ------------------------------------------------------------------ hybrid
hybrid = f'''
  <g id="Solar_wind_hybrid">
    <rect id="hybrid-top-bg" x="1393" y="110" width="571" height="138" fill="url(#hybridTop)"/>
    {T('hybrid-kn', 1684.5, 167, '104 ಕಿ.ವ್ಯಾ. ಸೌರ-ಗಾಳಿ ಹೈಬ್ರಿಡ್', KN, 34, NAVY_TXT, 'middle', fit=465)}
    {hline(1450, 1918, 178.5, NAVY_TXT, 1.6)}
    {T('hybrid-en', 1687.5, 219, '104 kW SOLAR-WIND HYBRID', COND(700), 34, NAVY_TXT, 'middle', fit=435)}
    <rect id="hybrid-green-rule" x="1603" y="232" width="177" height="2.5" fill="url(#greenFade)"/>
    {img('photo_solar_wind_hybrid.png', 1393, 248, 571, 452, 'photo-solar-wind-hybrid')}
  </g>'''

# ------------------------------------------------------------------ bottom band
IDEAL = [(167, 'highways', 'HIGHWAYS'), (249, 'cityroads', 'CITY ROADS'), (331, 'parks', 'PARKS'),
         (425, 'industrial', 'INDUSTRIAL AREAS'), (522, 'campus', 'CAMPUS'), (618, 'parking', 'PARKING AREAS'),
         (725, 'public', 'PUBLIC PLACES')]
ideal = ''.join(f'<g id="ideal-{n}">{icon("ideal_" + n)}'
                + T(f'ideal-{n}-label', cx, 775, lab, COND(500), 15, '#FFFFFF', 'middle', 'ideal-label',
                    77.5 if n == 'parking' else None) + '</g>' for cx, n, lab in IDEAL)
WHY = [('cloud', 849, ['Provides hot water', 'even on cloudy', 'days and at night']),
       ('bolt', 997, ['Consumes up to 70% less', 'electricity compared to', 'conventional heaters']),
       ('thermo', 1191, ['Works efficiently in', 'low ambient temperature', '(-10°C to 45°C)']),
       ('tools', 1373, ['Long life, low maintenance', '& reliable performance'])]
why = ''.join(f'<g id="why-{n}">{icon("why_" + n)}'
              + ''.join(T(f'why-{n}-{j+1}', x, (748 + 19 * j) if n == 'tools' else (747.5 + 16 * j), t, SEMI(400), 14,
                          '#FFFFFF', key='why-body-tools' if n == 'tools' else 'why-body', fit=121.5 if (n, j) == ('bolt', 0) else 112 if (n, j) == ('tools', 0) else None)
                        for j, t in enumerate(body)) + '</g>' for n, x, body in WHY)

bottom = f'''
  <g id="Bottom_band">
    <rect id="bottom-bg" y="701" width="{W}" height="100" fill="{BAND}"/>
    {vline(790, 701, 801, '#24508C', 2)}
    <g id="ideal-for">
      <path id="ideal-arrow" d="M18 720H112L127 747.5L112 775H18Z" fill="url(#idealGreen)"/>
      {T('ideal-text', 30, 758, 'IDEAL FOR', COND(600), 26, '#FFFFFF', fit=82)}
      {ideal}
      {''.join(vline(x, 722, 780, '#2D5590') for x in (206, 291, 370, 481, 564, 673))}
    </g>
    <g id="why-heat-pump">
      {T('why-title', 803, 720.5, 'WHY HEAT PUMP MAKES THE DIFFERENCE', SEMI(700), 19, '#FFFFFF', fit=293)}
      {why}
      {''.join(vline(x, 735, 785, '#2D5590') for x in (936, 1133, 1322))}
    </g>
    <g id="slogan-band">
      <rect x="1490" y="699.5" width="474" height="2.5" fill="#E8CB22"/>
      <path d="M1489 701H1964V801H1511Z" fill="url(#footerGreen)"/>
      <path d="M1484.5 701H1489.5L1511.5 801H1506.5Z" fill="#C9D21E"/>
      {icon('leaf_footer')}
      {T('footer-slogan', 1566, 760, 'CLEAN ENERGY. LOWER BILLS. BETTER TOMORROW.', COND(600), 26, '#FFFFFF', fit=373)}
    </g>
  </g>'''

svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <title>MSIL Solar Product Portfolio</title>
  <defs>
    <linearGradient id="streetTop" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#CFEBFD"/><stop offset="0.5" stop-color="#E0F2FD"/><stop offset="1" stop-color="#C4E5FB"/>
    </linearGradient>
    <linearGradient id="hybridTop" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#DBF0FD"/><stop offset="1" stop-color="#E0F3FE"/>
    </linearGradient>
    <linearGradient id="greenFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#3FAE49" stop-opacity="0"/><stop offset="0.5" stop-color="#3FAE49"/><stop offset="1" stop-color="#3FAE49" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="idealGreen" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#14A73C"/><stop offset="1" stop-color="#0A9532"/>
    </linearGradient>
    <linearGradient id="footerGreen" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0A8530"/><stop offset="1" stop-color="#066532"/>
    </linearGradient>
  </defs>
  <rect id="page-bg" width="{W}" height="{H}" fill="#FFFFFF"/>
{header}
{street}
{heat}
{hybrid}
{bottom}
</svg>
'''
(OUT / 'MSIL_Solar_Product_Portfolio.svg').write_text(svg, encoding='utf-8')
print('ok', len(svg))
