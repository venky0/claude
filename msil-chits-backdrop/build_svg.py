"""Build the MSIL Chits backdrop as a layered SVG (1 px = 1 pt) for Illustrator."""
import base64, sys
from pathlib import Path

OUT = Path(sys.argv[1])
LINKS = OUT / 'links'
W, H = 1539, 473

# palette (sampled from the source artwork)
NAVY_TXT = '#2C1E5C'
RED = '#D7202C'
BLUE = '#0372BA'
ORANGE = '#F09129'
CREAM = '#FCF6E1'
HDR_CREAM = '#FBF4DE'
GOLD = '#D2AE63'
GOLD_LT = '#EEDAAE'
BAND = '#0B54A1'
BAND_TXT = '#E3C47E'
FOOTER = '#1A2443'

# fonts: PostScript name first (Illustrator), family second (browsers)
F_LOGO = "font-family=\"'Jost-Bold', 'Jost'\" font-weight=\"700\""
F_KN_LOGO = "font-family=\"'NotoSansKannada-ExtraBold', 'Noto Sans Kannada'\" font-weight=\"800\""
F_KN = "font-family=\"'NotoSansKannada-Bold', 'Noto Sans Kannada'\" font-weight=\"700\""
F_SERIF = "font-family=\"'Merriweather-Black', 'Merriweather'\" font-weight=\"900\""
def F_SANS(w):
    name = {400: 'Regular', 600: 'SemiBold', 700: 'Bold', 800: 'ExtraBold'}[w]
    return f"font-family=\"'NunitoSans-{name}', 'Nunito Sans'\" font-weight=\"{w}\""


def img(path, x, y, w, h, id_):
    data = base64.b64encode((LINKS / path).read_bytes()).decode()
    return (f'<image id="{id_}" x="{x}" y="{y}" width="{w}" height="{h}" '
            f'preserveAspectRatio="none" xlink:href="data:image/png;base64,{data}"/>')


def mark(x, y, s=1.0, id_='mark'):
    """MSIL stepped mark; native size 51 x 51."""
    blue = 'M0 0H51V17H34V33H16V51H0Z'
    orange = 'M9 9H34V16H26V24H17V33H9Z'
    return (f'<g id="{id_}" transform="translate({x} {y}) scale({s})">'
            f'<path fill="{BLUE}" d="{blue}"/><path fill="{ORANGE}" d="{orange}"/></g>')


def diamond(cx, cy, id_):
    return (f'<g id="{id_}"><path d="M{cx-5} {cy}L{cx} {cy-5}L{cx+5} {cy}L{cx} {cy+5}Z" '
            f'fill="none" stroke="{GOLD}" stroke-width="1.2"/>'
            f'<path d="M{cx-2} {cy}L{cx} {cy-2}L{cx+2} {cy}L{cx} {cy+2}Z" fill="{GOLD}"/></g>')


def lotus(cx, cy):
    # five-petal lotus, ~18 x 13
    p = (f'M{cx} {cy-7}C{cx+2.6} {cy-4} {cx+2.6} {cy+1} {cx} {cy+4}C{cx-2.6} {cy+1} {cx-2.6} {cy-4} {cx} {cy-7}Z'
         f'M{cx-1.2} {cy+4}C{cx-5} {cy+2.5} {cx-6.5} {cy-1} {cx-6} {cy-4.5}C{cx-3.5} {cy-2.5} {cx-1.8} {cy} {cx-1.2} {cy+4}Z'
         f'M{cx+1.2} {cy+4}C{cx+5} {cy+2.5} {cx+6.5} {cy-1} {cx+6} {cy-4.5}C{cx+3.5} {cy-2.5} {cx+1.8} {cy} {cx+1.2} {cy+4}Z'
         f'M{cx-2} {cy+4.5}C{cx-6} {cy+4.5} {cx-8.5} {cy+2.5} {cx-9.5} {cy}C{cx-6} {cy+0.5} {cx-3.5} {cy+2} {cx-2} {cy+4.5}Z'
         f'M{cx+2} {cy+4.5}C{cx+6} {cy+4.5} {cx+8.5} {cy+2.5} {cx+9.5} {cy}C{cx+6} {cy+0.5} {cx+3.5} {cy+2} {cx+2} {cy+4.5}Z'
         f'M{cx-4} {cy+5.5}H{cx+4}L{cx+2.5} {cy+7}H{cx-2.5}Z')
    return f'<path id="lotus" fill="{GOLD}" d="{p}"/>'


def panel(i, x0, en, kn, photo):
    cx = x0 + 110
    t = x0 + 126  # second lockup
    return f'''
  <g id="panel-{i}-{photo}">
    <rect id="panel-{i}-base" x="{x0+1}" y="151" width="218" height="322" fill="{FOOTER}"/>
    {img(f'photo_{photo}.png', x0+2, 231, 216, 214, f'panel-{i}-photo')}
    <rect id="panel-{i}-header" x="{x0+2}" y="152" width="216" height="33" fill="{HDR_CREAM}"/>
    <g id="panel-{i}-lockup-en">
      {mark(x0+8, 155, 1/3, f'panel-{i}-mark-en')}
      <text x="{x0+19.5}" y="178.5" {F_LOGO} font-size="15.5" letter-spacing="-0.3" fill="{NAVY_TXT}">MSIL <tspan {F_SANS(800)} fill="{RED}" letter-spacing="0">Chits</tspan></text>
    </g>
    <g id="panel-{i}-lockup-kn">
      {mark(t, 155, 1/3, f'panel-{i}-mark-kn')}
      <text x="{t+11.5}" y="178.5" {F_LOGO} font-size="15.5" letter-spacing="-0.3" fill="{NAVY_TXT}">MSIL <tspan {F_KN_LOGO} font-size="14.5" fill="{RED}" letter-spacing="0">ಚಿಟ್ಸ್</tspan></text>
    </g>
    <rect id="panel-{i}-band" x="{x0+2}" y="185" width="216" height="46" fill="{BAND}"/>
    <text id="panel-{i}-title-en" x="{cx}" y="200.5" text-anchor="middle" {F_SANS(700)} font-size="12.6" letter-spacing="0.2" fill="{BAND_TXT}">{en}</text>
    <text id="panel-{i}-title-kn" x="{cx}" y="221" text-anchor="middle" {F_KN} font-size="17" fill="#FFFFFF">{kn}</text>
    <g id="panel-{i}-pill">
      <rect x="{cx-34}" y="422.5" width="68" height="17.5" rx="8.75" fill="#FFFFFF" fill-opacity="0.94"/>
      <text x="{cx}" y="435.3" text-anchor="middle" {F_SANS(800)} font-size="10.2" fill="#2B2A45">MSIL CHITS</text>
    </g>
    <rect id="panel-{i}-footer" x="{x0+2}" y="445" width="216" height="26" fill="{FOOTER}"/>
    <text id="panel-{i}-footer-1" x="{x0+12}" y="456.5" {F_SANS(600)} font-size="6.8" fill="#FFFFFF">Mysore Sales International Limited</text>
    <text id="panel-{i}-footer-2" x="{x0+12}" y="465.8" {F_SANS(400)} font-size="5.5" fill="#8D97AD" xml:space="preserve">A Government of Karnataka Undertaking   ·   msilonline.karnataka.gov.in</text>
    <rect id="panel-{i}-frame" x="{x0+1}" y="151" width="218" height="321" fill="none" stroke="{GOLD}" stroke-width="2"/>
  </g>'''


spots = [142, 336, 525, 1007, 1186, 1380]

svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <title>MSIL Chits Backdrop</title>
  <defs>
    <radialGradient id="wall" cx="770" cy="250" r="820" gradientUnits="userSpaceOnUse"
                    gradientTransform="translate(0 112.5) scale(1 0.55)">
      <stop offset="0" stop-color="#032856"/>
      <stop offset="0.55" stop-color="#02234C"/>
      <stop offset="1" stop-color="#01193A"/>
    </radialGradient>
    <radialGradient id="spot" cx="0.5" cy="0" r="0.5">
      <stop offset="0" stop-color="#B4C7E2" stop-opacity="0.8"/>
      <stop offset="0.35" stop-color="#7F99BF" stop-opacity="0.34"/>
      <stop offset="1" stop-color="#5F7FAE" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <g id="Background">
    <rect id="wall-fill" width="{W}" height="{H}" fill="url(#wall)"/>
  </g>

  <g id="Lighting_mockup_hide_for_print" opacity="1">
    {''.join(f'<ellipse cx="{x}" cy="0" rx="85" ry="135" fill="url(#spot)"/>' for x in spots)}
  </g>

  <g id="Palace_art_raster">
    {img('palace_left.png', 0, 255, 164, 218, 'palace-left')}
    {img('palace_right.png', 1371, 255, 168, 218, 'palace-right')}
  </g>

  <g id="Logo_lockup">
    <rect id="logo-plate" x="627" y="4" width="284" height="73" rx="9" fill="{CREAM}"/>
    {mark(646, 12)}
    <text id="logo-msil" x="684" y="69" {F_LOGO} font-size="51" letter-spacing="-1" fill="{NAVY_TXT}">MSIL</text>
    <text id="logo-chits-kn" x="803" y="60.5" {F_KN_LOGO} font-size="42" fill="{RED}">ಚಿಟ್ಸ್</text>
    <text id="company-name" x="770" y="93.5" text-anchor="middle" {F_SANS(600)} font-size="17.2" fill="#FFFFFF">Mysore Sales International Limited</text>
    <text id="company-tagline" x="771" y="107" text-anchor="middle" {F_SANS(400)} font-size="11.6" fill="#FFFFFF">A Government of Karnataka Undertaking</text>
    <g id="rule-left">
      <line x1="537" y1="89" x2="610" y2="89" stroke="{GOLD}" stroke-width="1.2"/>
      {diamond(616, 89, 'diamond-left')}
    </g>
    <g id="rule-right">
      {diamond(924, 89, 'diamond-right')}
      <line x1="930" y1="89" x2="1002" y2="89" stroke="{GOLD}" stroke-width="1.2"/>
    </g>
  </g>

  <g id="Headline">
    <text id="headline" x="770" y="140" text-anchor="middle" {F_SERIF} font-size="35" fill="{GOLD_LT}">For every dream. For every milestone.</text>
    <g id="headline-rule">
      <line x1="615" y1="153.5" x2="753" y2="153.5" stroke="{GOLD}" stroke-width="1.1"/>
      {lotus(766, 152)}
      <line x1="779" y1="153.5" x2="918" y2="153.5" stroke="{GOLD}" stroke-width="1.1"/>
    </g>
  </g>

  <g id="Panels">{panel(1, 164, 'MARRIAGE', 'ಮದುವೆ', 'marriage')}{panel(2, 395, 'BUSINESS', 'ವ್ಯಾಪಾರ', 'business')}{panel(3, 922, 'VEHICLE PURCHASE', 'ವಾಹನ ಖರೀದಿ', 'vehicle')}{panel(4, 1150, 'HOME CONSTRUCTION', 'ಗೃಹ ನಿರ್ಮಾಣ', 'home')}
  </g>
</svg>
'''
(OUT / 'MSIL_Chits_Backdrop.svg').write_text(svg, encoding='utf-8')
print('ok', len(svg))
