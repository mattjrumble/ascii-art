import os
import shutil
import numpy as np
from PIL import Image


def grayscale(img):
    # Convert img to grayscale.
    return img.convert('RGB').convert('L')

def average_val(pixels, y, x, y_step, x_step):
    # Return average value in pixels numpy array in the given rectangle
    # Expects rectangle coordinates to be in the range of the pixels array
    if y_step == 0:
        raise Exception('y_step must be non-zero')
    if x_step == 0:
        raise Exception('x_step must be non-zero')

    start_y = int(round(y))
    end_y = int(round(y+y_step))
    start_x = int(round(x))
    end_x= int(round(x+x_step))

    total = 0
    count = 0

    for y in range(start_y, end_y+1):
        for x in range(start_x, end_x+1):
            total += pixels[y, x]
            count += 1

    return total / count

def calculate_step_sizes(height, width):
    # Calculate how big a region of the image each ASCII char should represent,
    # so that we remain inside the max output dimensions.

    # Max number of output characters to display
    MAX_OUTPUT_WIDTH = 150
    MAX_OUTPUT_HEIGHT = 40
    # The dimensions of an ASCII char displayed in my terminal
    ASCII_CHAR_WIDTH = 10
    ASCII_CHAR_HEIGHT = 22

    # See if we can fit to max output width
    x_step = width / MAX_OUTPUT_WIDTH
    y_step = x_step * (ASCII_CHAR_HEIGHT / ASCII_CHAR_WIDTH)
    if height / y_step > MAX_OUTPUT_HEIGHT:
        # Can't fit to max output width, fit to max output height instead
        y_step = height / MAX_OUTPUT_HEIGHT
        x_step = y_step * (ASCII_CHAR_WIDTH / ASCII_CHAR_HEIGHT)

    return y_step, x_step


# File locations
sample_dir = 'samples'
sample_file = 'girl.png'
sample_path = os.path.join(sample_dir, sample_file)
output_path = 'result.txt'

# Load grayscale image
img = Image.open(sample_path)
img = grayscale(img)

pixels = np.asarray(img)
height, width = pixels.shape
y_step, x_step = calculate_step_sizes(height, width)

output = ''
for y in np.arange(0, height-y_step, y_step):
    for x in np.arange(0, width-x_step, x_step):
        val = average_val(pixels, y, x, y_step, x_step)
        if val >= 128:
            output += '#'
        else:
            output += '_'
    output += '\n'

print(output)
with open(output_path, 'w+') as f:
    f.write(output)
