import os
import shutil
import numpy as np
import json
from math import floor
from PIL import Image


class OutputDisplay:
    """Hold information about how the output will be displayed."""
    def __init__(self, max_chars_high, max_chars_wide, char_height, char_width, inverted):

        if not all([max_chars_high, max_chars_wide, char_height, char_width]):
            raise Exception('All OutputDisplay arguments must be non-zero')

        # How many characters are allowed on the display
        self.max_chars_high = max_chars_high
        self.max_chars_wide = max_chars_wide
        # Relative dimensions of a single character on the display
        self.char_height = char_height
        self.char_width = char_width
        # Whether displaying black on white (inverted) or white on black (not inverted)
        self.inverted = inverted

        
MAX_LUMINOSITY = 255
TERMINAL_DISPLAY = OutputDisplay(41, 180, 22, 10, inverted=False)
NOTEPAD_PLUS_BIG_DISPLAY = OutputDisplay(100, 400, 18, 10, inverted=False)
GITHUB_DISPLAY = OutputDisplay(40, 223, 29, 10, inverted=True)


def grayscale(img):
    """Convert img to grayscale."""
    return img.convert('RGB').convert('L')


def average_val(arr, start_y, end_y, start_x, end_x):
    """Return average value in the given numpy array in the given
    rectangle of integer points, including the endpoints.
    Coordinates are expected to be within the range of the array."""


    if start_y == end_y:
        raise Exception('start_y cannot equal end_y')
    if start_x == end_x:
        raise Exception('start_x cannot equal end_x')
    
    total = arr[start_y:end_y, start_x:end_x].sum()
    area = (end_y - start_y) * (end_x - start_x)

    return total/area


def calculate_step_sizes(height, width, display):
    """Calculate how big a region of the image each ASCII char should represent,
    so that we remain inside the output display's dimensions. Note that a region
    we look at must always be at least a step size away from the edge of the image,
    otherwise adding the step size on to that would take us out bounds.
    All arguments are integers. Return step sizes as floats."""
    
    # Try to fit to fill the display width-wise
    x_step = width / display.max_chars_wide
    y_step = x_step * (display.char_height / display.char_width)
    
    # If width-wise doesn't fit, fill the display height-wise instead
    if height / y_step >= display.max_chars_high:
        #print('height-wise')
        y_step = height / display.max_chars_high
        x_step = y_step * (display.char_width / display.char_height)

    return y_step, x_step


def get_full_path(file_dir, file_prefix):
    """Return the full path of the first file found in the given
    with a name that starts with the given prefix."""
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
    """For the given color value, return the corresponding ASCII char.
    Takes luminosity values between 0 and MAX_LUMINOSITY inclusive.
    Use the opposite color value for inverted displays."""
    
    if inverted:
        key = str(int(MAX_LUMINOSITY - val))
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
    
    # Load luminosity to char dict (dict of luminosity value -> best char code).
    with open('luminosity_to_char.json', 'r') as f:
        lum_to_char = json.load(f)
    
    # Select display output
    display = TERMINAL_DISPLAY

    pixels = np.asarray(img)
    height, width = pixels.shape
    y_step, x_step = calculate_step_sizes(height, width, display)

    # Floating point round errors can lead to an unintended final value in the range
    # that is marginally smaller than the stop argument. Remove the final value if
    # this is the case. TODO: Is this needed for any dimensions?
    y_range = np.arange(0, height-y_step, y_step)
    x_range = np.arange(0, width-x_step, x_step)

    ascii_img = ''

    for y in y_range:
        for x in x_range:
            
            # Round floating step sizes to integer start/end points
            rounded_start_y = int(floor(y))
            rounded_start_x = int(floor(x))
            rounded_end_y = int(floor(y + y_step))
            rounded_end_x = int(floor(x + x_step))
            
            lum = average_val(pixels, rounded_start_y, rounded_end_y, rounded_start_x, rounded_end_x)
            ascii_img += color_val_to_char(lum, lum_to_char, inverted=display.inverted)

        ascii_img += '\n'

    print(ascii_img)
    with open(output_path, 'w+') as f:
        f.write(ascii_img)

 
if __name__ == "__main__":
    main()
