import sys
import cv2, numpy as np
src, out = sys.argv[1], sys.argv[2]
img = cv2.imread(src)
mask = np.zeros(img.shape[:2], np.uint8)
# label pills and green banners (page coords x0,y0,x1,y1) — removed so the photos sit clean under the vector labels
for x0, y0, x1, y1 in [(22, 163, 113, 183), (170, 163, 251, 183), (311, 163, 396, 183),
                       (102, 181, 316, 204), (74, 314, 347, 339), (74, 410, 347, 433)]:
    mask[y0-2:y1+2, x0-2:x1+2] = 255
clean = cv2.inpaint(img, mask, 6, cv2.INPAINT_TELEA)
for name, (y0, y1) in {'street_lights': (77, 204), 'heat_pump_water_heater': (204, 339), 'solar_wind_hybrid': (339, 433)}.items():
    cv2.imwrite(f'{out}/photo_{name}.png', clean[y0:y1])
