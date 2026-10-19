# MSIL Solar roll-up banner: editable Illustrator rebuild

The source is a flattened 827 × 1902 px WebP image. This folder rebuilds it as a layered SVG at the same proportions (1 px = 1 pt, so 827 × 1902 pt). Open it in Illustrator with **File › Open**.

| File | What it is |
|---|---|
| `MSIL_Solar_Rollup.svg` | The editable artwork. Open this in Illustrator. |
| `MSIL_Solar_Rollup_proof.pdf` | A one-page PDF proof with the fonts embedded |
| `links/photo_solar_water_heater.jpg` | The photo with the old tagline painted out. It is also embedded in the SVG. |
| `preview.png`, `comparison_source_vs_rebuild.png` | Render, and source (left) vs rebuild (right) |
| `build.py`, `fit.json` | The generator, and the font sizes fitted to the original widths |

## Layers

- `Header` (vector):
  - the #003A98 blue band
  - the MSIL mark (blue #0A73E8 and orange #F7931E)
  - "MSIL" in Barlow Semi Condensed SemiBold
  - "MSIL SOLAR" in Montserrat Bold
  - the metallic gold rule (gradient)
- `Photo` (raster): the solar water heater scene. The MSIL logo on the tank is printed on the product, so it stays part of the photo.
- `Tagline` (live text): "Our Energy / Tomorrow" in Source Sans 3 SemiBold Italic, with a soft drop shadow. The shadow is a separate blurred black copy in the `Tagline_shadow` layer, so the tagline stays live text in PDFs. In Illustrator you can delete that layer and use **Effect › Stylize › Drop Shadow** on the tagline instead.

## Before printing

1. **Install the fonts.** All are free on Google Fonts: Montserrat, Barlow Semi Condensed and Source Sans 3.
2. **Scale for print.** The artwork has the proportions of a standard 850 × 2000 mm roll-up (0.435 vs 0.425 aspect), so scale it uniformly and adjust the height or crop the photo to fit. Add bleed, and keep the stand's bottom ~100 mm free of key content.
3. **Relink the photo.** It is only 827 px wide, which is far too low for an 850 mm-wide print. Use **Links › Relink** with a high-res original or an upscaled version before sending to print.
