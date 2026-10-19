# Heat Pump & Solar-Wind Hybrid slides: editable Illustrator rebuild

The source is `Heat_Pump__Solar_Wind_Hybrid_3.pdf`, three 720 × 540 pt PowerPoint slides. Slides 1 and 2 are each a flattened 16:9 poster image stretched onto the 4:3 slide, with a white box of live Kannada text on top. Slide 3 is a photo with a Kannada heading. This folder rebuilds all three as layered SVGs at the exact slide size. Open them in Illustrator with **File › Open**.

| File | What it is |
|---|---|
| `Slide1_All_In_One_Solar_Street_Lights.svg` | Slide 1, editable |
| `Slide2_Solar_Water_Heater_Heat_Pump.svg` | Slide 2, editable |
| `Slide3_104kW_Solar_Wind_Hybrid.svg` | Slide 3, editable |
| `MSIL_Heat_Pump_Solar_Wind_Hybrid_proof.pdf` | All three slides as a 720 × 540 pt PDF, with fonts embedded and Kannada searchable as Unicode |
| `preview_slide*.png`, `comparison_slide*.png` | Renders, and source (left) vs rebuild (right) |
| `links/` | The background photos, with the old text and icons painted out. They are also embedded in the SVGs. |
| `layout.py`, `prepare_assets.py`, `build_svg.py` | Measured layout, asset clean-up and icon tracing, and the SVG generator |

## Kannada text (Google Noto Sans Kannada)

Every Kannada line is live text set in **Noto Sans Kannada**, a Google font. The heading lines keep the PDF's exact sizes, colours, positions and underlines.

| Slide | Text | Note |
|---|---|---|
| 1 | ಆಲ್-ಇನ್-ಒನ್ ಸೌರ ಬೀದಿ / ದೀಪಗಳು / ಎಂಎಸ್ಐಎಲ್ ಲೈಟ್ಸ್ | The PDF stored line 2 as ದಿೀಪಗಳು, an invalid vowel sequence. It is corrected to ದೀಪಗಳು. |
| 2 | ಹೀಟ್ ಪಂಪ್‌ನೊಂದಿಗೆ / ಸೌರ ಜಲತಾಪಕ / ಸೌರ ಜಲತಾಪಕ | Lines 2 and 3 repeat in the source, so please confirm the intended third line. |
| 2 (logo) | ಎಂಎಸ್ಐಎಲ್ ಹಾಟ್‌ಸ್ಪ್ರಿಂಗ್ ಸೋಲಾರ್ ವಾಟರ್ ಹೀಟರ್ | The Kannada HOTSPRING lockup is rebuilt as live text, with the sun mark replacing the ಂ as in the original. |
| 3 | 104 ಕಿ.ವ್ಯಾ. ಸೌರ-ಗಾಳಿ ಹೈಬ್ರಿಡ್ | |

## What's vector and what's raster

**Vector, with live text:** all poster English text (features, panel tags, the five specs per panel, "Ideal for", the badges, the heat-pump feature box, "Why heat pump", the bottom strip and the slogan), the MSIL LIGHTS and HOTSPRING logos, the Kannada title boxes, and the slide 3 footer.

**Icons (46):** traced to vector paths, with true circular rings and discs. One leaf glyph was too small to trace cleanly, so it is drawn by hand.

**Raster:** the photos. That includes the logos printed on the products in the photos (the tank and the heat pump unit), which belong to the photo.

**Why the text is easier to read than in the PowerPoint:** PowerPoint squashed each poster to 72% of its width, which squashed all the baked-in text with it. In the rebuild the text is upright and unsquashed, using condensed fonts fitted to the original line widths. The photos keep the slide's proportions.

## Before you edit in Illustrator

1. **Install the fonts.** All are free on Google Fonts.
   - Noto Sans Kannada (Bold, ExtraBold, Black)
   - Barlow Condensed (Medium, SemiBold, Bold)
   - Barlow Semi Condensed (Regular, Medium, SemiBold, Bold)
   - Montserrat (Bold, ExtraBold)
   - Arimo (Regular, Bold), a metric match for the Arial footer
2. **Turn on Indic shaping.** Select all Kannada text and choose **Adobe World-Ready Paragraph Composer** from the Paragraph panel menu. Without it, conjuncts such as ಸ್ಪ್ರಿ, ವ್ಯಾ and ಬ್ರಿ will break apart.
3. **Shadows.** The white title boxes keep their PowerPoint drop shadow as an SVG filter. If Illustrator shows it as "SVG Filters", replace it with **Effect › Stylize › Drop Shadow**. The slide 3 heading shadow is a separate blurred copy (`title-line-1-shadow`), so the heading stays live text in PDFs.
