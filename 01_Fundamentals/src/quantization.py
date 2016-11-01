#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np
from PIL import Image


def quantize(input_img, level):
    height, width = input_img.shape
    diff = 256 / level
    scale = 255 / (level - 1)
    output_img = np.zeros(input_img.shape, dtype=np.uint8)

    for xidx in xrange(height):
        for yidx in xrange(width):
            output_img[xidx, yidx] = scale * int(input_img[xidx, yidx] / diff)

    return output_img


def main():
    input_img = np.array(Image.open('images/72.png').convert('L'))
    levels = [128, 32, 8, 4, 2]
    for level in levels:
        output_img = quantize(input_img, level)
        output_img = Image.fromarray(output_img, 'L')
        img_title = "images/quantize_%d_72.png" % level
        output_img.save(img_title)
        print "Successfully saved image: %s" % img_title


if __name__ == "__main__":
    main()
