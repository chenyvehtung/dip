#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np
from PIL import Image


def filter2d(input_img, filter):
    height, width = input_img.shape
    output_img = np.zeros((height, width))
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
            output_img[row][col] = np.sum(np.multiply(filter_rt, img_patch))

    # output_img = stand_img(output_img)

    return output_img


def stand_img(img):
    """
    scale output image for display purpose and
    return the scaled image
    """
    output_img = img.copy()
    min_v = np.amin(output_img)
    output_img -= min_v
    max_v = np.amax(output_img)
    output_img *= (255.0 / max_v)
    return output_img.astype(np.uint8)


def gen_avg_filter(filter_len):
    return 1.0 / (filter_len * filter_len) * np.ones((filter_len, filter_len))


def main():
    input_img = np.array(Image.open('images/72.png').convert('L'))

    # smooth image
    for filter_len in [3, 7, 11]:
        avg_filter = gen_avg_filter(filter_len)
        output_img = filter2d(input_img, avg_filter)
        output_img = Image.fromarray(output_img.astype(np.uint8), 'L')
        img_title = "images/avg_filter_%d_%d_72.png" % (filter_len, filter_len)
        output_img.save(img_title)
        print "Successfully saved %s" % img_title

    # sharpen image using 3 × 3 Laplacian filter
    lap_filter = np.array([0, 1, 0, 1, -4, 1, 0, 1, 0]).reshape((3, 3))
    output_img = filter2d(input_img, lap_filter)
    output_img = stand_img(output_img)
    enhance_img = stand_img(input_img.astype(np.float64) - output_img)
    enhance_img = Image.fromarray(enhance_img, 'L')
    img_title = "images/sharpen_72.png"
    enhance_img.save(img_title)
    print "Successfully saved %s" % img_title

    # high boost filtering
    blur_img = filter2d(input_img, gen_avg_filter(7))
    g_mask = stand_img(input_img - blur_img)
    k = 1.3
    g_output = stand_img(input_img.astype(np.float64) + k * g_mask.astype(np.float64))
    output_img = Image.fromarray(g_output, 'L')
    img_title = "images/hboost_%.1f_72.png" % k
    output_img.save(img_title)
    print "Successfully saved %s" % img_title


if __name__ == "__main__":
    main()
