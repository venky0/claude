# MSIL Solar Product Portfolio banner: editable Illustrator rebuild

The source is a flattened 1964 × 801 px WebP image with no vectors and no live text. This folder rebuilds it as a layered SVG at the same size (1 px = 1 pt). Open it in Illustrator with **File › Open**.

| File | What it is |
|---|---|
| `MSIL_Solar_Product_Portfolio.svg` | The editable artwork. Open this in Illustrator. |
| `links/` | The 3 photo zones as separate PNGs, with the old text painted out. They are also embedded in the SVG. |
| `preview.png` | The SVG rendered at 2×. |
| `comparison_source_vs_rebuild.png` | Source on top, rebuild below. |
| `prepare_assets.py` | Crops the photos from the source, paints out the old text, and traces the icons into `icons.json`. |
| `build_svg.py` | Generates the SVG from `links/`, `icons.json` and `sizes.json` (the fitted font sizes). |

## What's vector and what's raster

**Vector, with live text:** everything except the three photos. That includes the header, every heading and spec line (English and Kannada), the panel tags, the icon rings and discs, the orange feature box, the HOTSPRING logo, the "Ideal for" and "Why heat pump" bands, and the green slogan band.

**Icons (41):** auto-traced from the source into filled vector paths, so you can recolour and resize them. Because they were traced from a low-resolution image, some fine detail is simplified. Swap in the brand's original icon set if you have it.

**Raster (72 ppi):** the street-light panel photos (`photo_street_lights.png`), the heat pump and water heater scene (`photo_heat_pump.png`), and the wind turbines (`photo_solar_wind_hybrid.png`). The old baked-in text and icons were painted out, so the photo looks smeared under each label. That only shows if you move a label.

## Layers (top-level groups)

`Header` · `Street_lights` · `Heat_pump` · `Solar_wind_hybrid` · `Bottom_band`. Each block inside is a named sub-group, for example `panel-2-spec-pir` or `hp-box-quiet`.

## Before you edit in Illustrator

1. **Install the fonts.** All are free on Google Fonts.
   - Barlow (Medium, ExtraBold)
   - Barlow Condensed (Regular, Medium, SemiBold, Bold)
   - Barlow Semi Condensed (Regular, Medium, Bold)
   - Noto Sans Kannada ExtraBold
2. **Turn on Indic shaping for the Kannada text.** Select all Kannada text and choose **Adobe World-Ready Paragraph Composer** from the Paragraph panel menu. Without it, the Kannada letters will break apart.
3. **Relink the photos.** They are low resolution, so use **Links › Relink** with the high-res originals before printing.
4. **Check the copy.** The heat pump heading repeats "ಸೌರ ಜಲತಾಪಕ" on lines 2 and 3, exactly as in the source. One of those lines is probably meant to say something else.
