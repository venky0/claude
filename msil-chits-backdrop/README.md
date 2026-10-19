# MSIL Chits Backdrop: editable Illustrator rebuild

The source PDF (`MSIL_Chits_Backdrop_Artwork.pdf`) is one flattened 1600 × 628 px JPEG, cropped to a 1539 × 473 pt page. It has no vectors and no live text. This folder rebuilds it as a layered SVG at the same size (1 px = 1 pt). Open it in Illustrator with **File › Open**.

| File | What it is |
|---|---|
| `MSIL_Chits_Backdrop.svg` | The editable artwork. Open this in Illustrator. |
| `links/` | The raster pieces as separate PNGs (4 photos and 2 palace illustrations). They are also embedded in the SVG. |
| `preview.png` | The SVG rendered at 2×. |
| `comparison_source_vs_rebuild.png` | Source on top, rebuild below. |
| `build_svg.py` | Generates the SVG (`python3 build_svg.py .`). |

## What's vector and what's raster

**Vector, with live text:** the wall gradient, the spotlight glows, the logo plate, the MSIL mark, the "MSIL ಚಿಟ್ಸ್" logotype, the company name and tagline, the gold rules with diamonds, the headline, the lotus ornament, and all four panels. Each panel has its frame, cream header with both lockups, blue category band (English and Kannada), "MSIL CHITS" pill and footer.

**Raster, cropped from the source at 72 ppi:** the 4 panel photos and the 2 Mysore Palace line-art illustrations. The palace art has its background removed, so it sits over the wall gradient.

## Layers (top-level groups)

1. `Background`: the navy wall, as a radial gradient
2. `Lighting_mockup_hide_for_print`: 6 spotlight glows copied from the source. They look like room lighting from a mockup, so hide this layer if the print shouldn't include them.
3. `Palace_art_raster`
4. `Logo_lockup`
5. `Headline`
6. `Panels`: `panel-1-marriage`, `panel-2-business`, `panel-3-vehicle`, `panel-4-home`

## Before you edit in Illustrator

1. **Install the fonts.** All are free on Google Fonts.
   - Jost Bold: "MSIL" wordmark
   - Nunito Sans Regular, SemiBold, Bold and ExtraBold: company name, tagline, band titles, pill, footers, "Chits"
   - Merriweather Black: headline
   - Noto Sans Kannada Bold and ExtraBold: all Kannada text
2. **Turn on Indic shaping, or the Kannada letters will break apart.** Go to Preferences › Type › Language Options and enable Indic options. Then select every Kannada text object and choose **Adobe World-Ready Paragraph Composer** from the Paragraph panel menu. Check that ಚಿಟ್ಸ್, ವ್ಯಾಪಾರ, ಗೃಹ ನಿರ್ಮಾಣ and ಖರೀದಿ look right.
3. **Replace the rasters before large-format printing.** The photos and palace art are 72 ppi crops from the low-res source. Use **Links › Relink** with the original high-res files. Each image is already the right size and position.
4. **Swap in the official logo.** The MSIL mark and logotype are redrawn by hand. If MSIL has an official vector logo, use it instead.
5. **Scale for print.** The document is proportional (21.375 × 6.57 in). The final physical size hasn't been confirmed, so scale up uniformly once it is, and add bleed. Convert to CMYK if the printer asks.
