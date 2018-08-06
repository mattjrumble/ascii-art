import os
import shutil
import numpy as np
import json
from math import floor
from PIL import Image


TERMINAL_DISPLAY = OutputDisplay(180, 41, 10, 22)
NOTEPAD_PLUS_BIG_DISPLAY = OutputDisplay(400, 100, 10, 18)
GITHUB_DISPLAY = OutputDisplay(223, 40, 10, 29)


class OutputDisplay:
    """Hold information about how the output will be displayed."""
    def __init__(self):
        self.max_chars_wide = max_chars_wide
        self.max_chars_high = max_chars_high
        self.char_width = char_width
        self.char_height = char_height


def grayscale(img):
    """Convert img to grayscale."""
    return img.convert('RGB').convert('L')


def average_val(pixels, y, x, y_step, x_step):
    """Return average value in pixels numpy array in the given rectangle.
    The given coordinates are floats and should be rounded appropriately.
    Expects rectangle coordinates to be in the range of the pixels array."""

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
            total += pixels[py, px]
            count += 1

    return total / count

def calculate_step_sizes(height, width):
    """Calculate how big a region of the image each ASCII char should represent,
    so that we remain inside the max output dimensions."""

    display = TERMINAL_DISPLAY

    # See if we can fit to max output width
    # Use height-1 and width-1 to avoid index out of bound errors from floating point rounding
    x_step = (width-1) / display.max_chars_wide
    y_step = x_step * (display.char_height / display.char_width)
    if (height-1) / y_step > display.max_chars_height:
        # Can't fit to max output width, fit to max output height instead
        y_step = (height-1) / MAX_OUTPUT_HEIGHT
        x_step = y_step * (display.char_width / display.char_height)

    return y_step, x_step

def get_full_path(file_dir, file_prefix):
    # Return the full path of the first file found in the given
    # with a name that starts with the given prefix.
    supported_formats = ['.jpg', '.jpeg', '.png']
    
    unsupported_files_found = False

    for f in os.listdir(file_dir):
        if f.startswith(file_prefix):
            if os.path.splitext(f)[1] in supported_formats:
                return os.path.join(file_dir, f)
            else:
                unsupported_files_found = True
    
    if unsupported_files_found:
        raise Exception("No supported file found with prefix '{}' in '{}'".format(file_prefix, file_dir))
    else:
        raise Exception("No file found with prefix '{}' in '{}'".format(file_prefix, file_dir))

def color_val_to_char(val, lum_to_char, inverted=False):
    # For the given color value, return the corresponding ASCII char.
    # Takes luminosity values between 0 and 255 inclusive.
   
    # inverted = True for black text on white background
    # inverted = False for white text on black background
    
    if inverted:
        key = str(int(255-val))
    else:
        key = str(int(val))

    char_code = lum_to_char[key]
    return chr(char_code)

def main():
    # File locations
    sample_path = get_full_path('samples', 'obama')
    output_path = 'result.txt'

    # Load grayscale image
    img = Image.open(sample_path)
    img = grayscale(img)

    pixels = np.asarray(img)
    height, width = pixels.shape
    y_step, x_step = calculate_step_sizes(height, width)
    
    # Load luminosity to char dict (dict of luminosity value -> best char code).
    with open('luminosity_to_char.json', 'r') as f:
        lum_to_char = json.load(f)

    output = ''
    for y in np.arange(0, height-y_step, y_step):
        for x in np.arange(0, width-x_step, x_step):
            val = average_val(pixels, y, x, y_step, x_step)
            output += color_val_to_char(val, lum_to_char, inverted=True)
        output += '\n'

    print(output)
    with open(output_path, 'w+') as f:
        f.write(output)

if __name__ == "__main__":
    main()
