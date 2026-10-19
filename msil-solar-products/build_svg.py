"""Build the MSIL Solar Products poster as a layered SVG (1 px = 1 pt) for Illustrator."""
import base64, sys
from pathlib import Path

OUT = Path(sys.argv[1])
LINKS = OUT / 'links'
W, H = 423, 433

BLUE_TXT = '#0132B6'

# fonts: PostScript name first (Illustrator), family second (browsers)
F_HEAD = "font-family=\"'Montserrat-ExtraBold', 'Montserrat'\" font-weight=\"800\""
F_PILL = "font-family=\"'RobotoCondensed-Bold', 'Roboto Condensed'\" font-weight=\"700\""
F_BANNER = "font-family=\"'Roboto-Bold', 'Roboto'\" font-weight=\"700\""


def img(path, x, y, w, h, id_):
    data = base64.b64encode((LINKS / path).read_bytes()).decode()
    return (f'<image id="{id_}" x="{x}" y="{y}" width="{w}" height="{h}" '
            f'preserveAspectRatio="none" xlink:href="data:image/png;base64,{data}"/>')


def pill(id_, x0, x1, label):
    cx = (x0 + x1) / 2
    return (f'<g id="{id_}"><rect x="{x0}" y="163" width="{x1-x0}" height="19.5" rx="3" '
            f'fill="url(#pillFill)" stroke="#5E8FD8" stroke-width="0.6"/>'
            f'<text x="{cx}" y="177.3" text-anchor="middle" {F_PILL} font-size="13" fill="#FFFFFF">{label}</text></g>')


def banner(id_, x0, y0, x1, y1, label, size, base):
    cx = (x0 + x1) / 2
    return (f'<g id="{id_}"><rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="url(#greenFill)"/>'
            f'<text x="{cx}" y="{base}" text-anchor="middle" {F_BANNER} font-size="{size}" fill="#FFFFFF">{label}</text></g>')


svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <title>MSIL Solar Products</title>
  <defs>
    <linearGradient id="topBand" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#006AD9"/>
      <stop offset="0.9" stop-color="#0165D5"/>
      <stop offset="1" stop-color="#005BCD"/>
    </linearGradient>
    <linearGradient id="pillFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0A52BA"/>
      <stop offset="1" stop-color="#023C9F"/>
    </linearGradient>
    <linearGradient id="greenFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#3BAA4C"/>
      <stop offset="0.45" stop-color="#0D8E26"/>
      <stop offset="1" stop-color="#03781A"/>
    </linearGradient>
  </defs>

  <g id="Photos_raster">
    {img('photo_street_lights.png', 0, 77, W, 127, 'photo-street-lights')}
    {img('photo_heat_pump_water_heater.png', 0, 204, W, 135, 'photo-heat-pump-water-heater')}
    {img('photo_solar_wind_hybrid.png', 0, 339, W, 94, 'photo-solar-wind-hybrid')}
  </g>

  <g id="Header">
    <rect id="header-blue-band" width="{W}" height="41" fill="url(#topBand)"/>
    <text id="header-msil" x="214" y="35" text-anchor="middle" {F_HEAD} font-size="37" fill="#FFFFFF">MSIL</text>
    <rect id="header-white-band" y="41" width="{W}" height="36" fill="#FFFFFF"/>
    <text id="header-solar-products" x="214.5" y="69.2" text-anchor="middle" {F_HEAD} font-size="28" fill="{BLUE_TXT}">SOLAR PRODUCTS</text>
  </g>

  <g id="Labels">
    {pill('pill-single-arm', 22.5, 112.5, 'SINGLE ARM')}
    {pill('pill-twin-arm', 170.5, 250.5, 'TWIN ARM')}
    {pill('pill-highmast', 312, 395.5, 'HIGHMAST')}
    {banner('banner-street-lights', 103, 182.5, 315, 203.5, 'Solar Street Lights', 16.6, 199)}
    {banner('banner-heat-pump', 75, 315, 346.5, 338.5, 'Heat Pump &amp; Solar Water Heater', 17, 333)}
    {banner('banner-hybrid', 75, 410.5, 346.5, 433, '104 kW Solar&#8211;Wind Hybrid', 18, 429)}
  </g>
</svg>
'''
(OUT / 'MSIL_Solar_Products.svg').write_text(svg, encoding='utf-8')
print('ok', len(svg))
