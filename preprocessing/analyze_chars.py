# Use a screenshot of all ASCII chars to determine the luminance value of each of them

import os
import numpy as np
import json
from math import floor
from PIL import Image

def average_val(pixels, y, x, y_step, x_step):
    # Return average value in boolean pixels numpy array in the given rectangle
    # Expects rectangle coordinates to be in the range of the pixels array
    if y_step == 0:
        raise Exception('y_step must be non-zero')
    if x_step == 0:
        raise Exception('x_step must be non-zero')

    start_y = int(floor(y))
    end_y = int(floor(y+y_step))
    start_x = int(floor(x))
    end_x= int(floor(x+x_step))

    total = 0
    count = 0

    for py in range(start_y, end_y+1):
        for px in range(start_x, end_x+1):
            if pixels[py, px]:
                total += 1
            count += 1

    return total / count

img = Image.open('chars.png').convert('1')
pixels = np.asarray(img)

# Size of each characters in the screenshot
CHAR_WIDTH = 10
CHAR_HEIGHT = 22

# Image contains character codes 33-127 inclusive, in 12 rows and 8 columns.
# The last entry is blank, we'll wrap that around to use as the space char (char code 32).

# Store average black-white value of each character code. 0 = all white, 1 = all black.
bw_value = {}

bw_value[32] = 0 # Space char

for char_code in range(33, 128):
    i = char_code - 33
    x = (i % 8) * CHAR_WIDTH
    y = (floor(i/8)) * CHAR_HEIGHT

    bw_value[char_code] = round(average_val(pixels, y, x, CHAR_HEIGHT, CHAR_WIDTH), 3)
    
# Char codes 64 and 103 (@ and g) are way too dark compared to other chars, so dominate images. Remove them.
del bw_value[64]
del bw_value[103]

# Scale the dictionary so values go between 0 and 1 inclusive.
max = max(bw_value.values())

for key in bw_value:
    bw_value[key] = bw_value[key] / max

# Generate a new dictionary of luminosity value -> best char code.
# Luminosity values are between 0 and 255 inclusive.

lum_to_char = {}
for lum in range(0, 256):
    best_char_code = None
    closest_lum = 999
    for key in bw_value:
        this_lum = bw_value[key] * 256
        if abs(lum - this_lum) < abs(lum - closest_lum):
            closest_lum = this_lum
            best_char_code = key
    lum_to_char[lum] = best_char_code

with open('luminosity_to_char.json', 'w+') as f:
    f.write(json.dumps(lum_to_char, sort_keys=True, indent=4))
