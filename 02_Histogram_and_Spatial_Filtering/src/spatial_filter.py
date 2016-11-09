#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np
from PIL import Image


def filter2d(input_img, filter):
    output_img = np.zeros_like(input_img)
    height, width = input_img.shape
    # rotate the filter by 180 degree
    filter_rt = np.rot90(filter, 2)
    # add zero-padding
    filter_len =  filter_rt.shape[0]
    pad_len = filter_len / 2
    pad_h = np.zeros((pad_len, width))
    pad_img = np.vstack((pad_h, input_img, pad_h))
    pad_v = np.zeros((height + 2 * pad_len, pad_len))
    pad_img = np.hstack((pad_v, pad_img, pad_v))
    # convolution on pad image
    for row in xrange(height):
        for col in xrange(width):
            img_patch = pad_img[row:row + filter_len, col:col + filter_len]
            output_img[row][col] = int(np.sum(np.multiply(filter_rt, img_patch)))

    return output_img


def gen_avg_filter(filter_len):
    return 1.0 / (filter_len * filter_len) * np.ones((filter_len, filter_len))


def main():
    input_img = np.array(Image.open('images/72.png').convert('L'))

    # smooth image
    for filter_len in [3, 7, 11]:
        avg_filter = gen_avg_filter(filter_len)
        output_img = filter2d(input_img, avg_filter)
        output_img = Image.fromarray(output_img, 'L')
        img_title = "images/avg_filter_%d_%d_72.png" % (filter_len, filter_len)
        output_img.save(img_title)
        print "Successfully saved %s" % img_title


if __name__ == "__main__":
    main()
