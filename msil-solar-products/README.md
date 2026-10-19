# MSIL Solar Products poster: editable Illustrator rebuild

The source PDF (`MSIL_Solar_Products_Artwork.pdf`) is one flattened 1944 × 809 px image of a three-poster mockup, cropped to a 423 × 433 pt page. It has no vectors and no live text. This folder rebuilds the poster as a layered SVG at the same size (1 px = 1 pt). Open it in Illustrator with **File › Open**.

| File | What it is |
|---|---|
| `MSIL_Solar_Products.svg` | The editable artwork. Open this in Illustrator. |
| `links/` | The 3 photo rows as separate PNGs. They are also embedded in the SVG. |
| `preview.png` | The SVG rendered at 3×. |
| `comparison_source_vs_rebuild.png` | Source on the left, rebuild on the right. |
| `build_svg.py` | Generates the SVG (`python3 build_svg.py .`). |
| `extract_photos.py` | Crops the photo rows and removes the old labels from them. |

## Layers (bottom to top)

1. `Photos_raster`: the street lights, heat pump & water heater, and solar–wind hybrid photos. The old baked-in pills and banners have been painted out.
2. `Header`: the blue band with "MSIL" and the white band with "SOLAR PRODUCTS". Vector, live text.
3. `Labels`: the 3 navy pills (SINGLE ARM, TWIN ARM, HIGHMAST) and the 3 green banners. Vector, live text.

The product branding printed on the equipment ("MSIL HEAT PUMP" and "HOTSPRING Solar Water Heater") is part of the photo, so it stays raster.

## Before you edit in Illustrator

1. **Install the fonts.** All are free on Google Fonts.
   - Montserrat ExtraBold: header
   - Roboto Condensed Bold: pills
   - Roboto Bold: banners
2. **Replace the photos before printing.** They are only about 72 ppi. Under each label the old text has been painted out, so the photo looks smeared there if you move a label. Use **Links › Relink** with the high-res originals. Each image is already the right size and position.
3. **Scale for print.** The physical print size isn't specified. The document is 423 × 433 pt (5.875 × 6.01 in), so scale it up uniformly and add bleed when you know the final size.
