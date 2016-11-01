#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np
from PIL import Image


def scale(input_img, size):
    """
    scale the input image to the specific size by using bilinear interpolation
    algorithm implement according to https://en.wikipedia.org/wiki/Bilinear_interpolation
    input_img: numpy array of the image
    size: (width, height) for the output image
    return output_img in numpy array
    """
    width, height = size
    old_height, old_width = input_img.shape
    x_scale = float(height) / old_height
    y_scale = float(width) / old_width

    output_img = np.zeros((height, width), dtype=np.uint8)
    for xidx in xrange(height):
        old_x = float(xidx) / x_scale
        for yidx in xrange(width):
            old_y = float(yidx) / y_scale
            if old_x.is_integer() or old_y.is_integer():
                output_img[xidx, yidx] = input_img[int(old_x), int(old_y)]
            else:  # use bilinear interpolation
                x1 = int(np.floor(old_x))
                x2 = int(np.ceil(old_x)) if int(np.ceil(old_x)) < old_height else old_height - 1
                y1 = int(np.floor(old_y))
                y2 = int(np.ceil(old_y)) if int(np.ceil(old_y)) < old_width else old_width - 1

                q11 = input_img[x1, y1]
                q12 = input_img[x1, y2]
                q21 = input_img[x2, y1]
                q22 = input_img[x2, y2]

                output_img[xidx, yidx] = (q11 * (x2 - old_x) * (y2 - old_y)
                                        + q21 * (old_x - x1) * (y2 - old_y)
                                        + q12 * (x2 - old_x) * (old_y - y1)
                                        + q22 * (old_x - x1) * (old_y - y1)) \
                                        / ((x2 - x1) * (y2 - y1) + 1e-10)

    return output_img


def main():
    input_img = np.array(Image.open('images/72.png').convert('L'))
    sizes = [(192, 128), (96, 64), (48, 32), (24, 16), (12, 8),
            (300, 200), (450, 300), (500, 200)]

    for size in sizes:
        output_img = scale(input_img, size)
        output_img = Image.fromarray(output_img, 'L')
        img_title = "images/scale_%d_%d_72.png" % size
        # output_img.show()
        output_img.save(img_title)
        print "Successfully saved image: %s" % img_title


if __name__ == '__main__':
    main()
