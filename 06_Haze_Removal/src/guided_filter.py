#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np
from PIL import Image


def box_filter(img, ksize, func):

    rows, cols = img.shape
    # pad the image using zero-padding
    img_pad = np.zeros((rows + ksize, cols + ksize), dtype=np.float)
    half_ksize = ksize / 2
    img_pad[half_ksize:rows + half_ksize, half_ksize:cols + half_ksize] = img

    result = np.zeros_like(img)
    for row in xrange(rows):
        for col in xrange(cols):
            result[row][col] = func(img_pad[row:row + ksize, col:col + ksize])

    return result


def single_channel_gfilter(img, guide_img, radius, epsilon):

    ksize = 2 * radius + 1
    # p mean
    mean_img = box_filter(img, ksize, np.mean)
    # I mean and I variance
    mean_gimg = box_filter(guide_img, ksize, np.mean)
    var_gimg = box_filter(guide_img, ksize, np.var)
    # mean Ip
    mean_ip = box_filter(guide_img * img, ksize, np.mean)
    # a and b
    a = (mean_ip - mean_gimg * mean_img) / (var_gimg + epsilon)  # Equation (5) in paper
    b = mean_img - a * mean_gimg  # Equation (6) in paper
    # a bar and b bar
    mean_a = box_filter(a, ksize, np.mean)
    mean_b = box_filter(b, ksize, np.mean)
    # get the result img
    result_img = mean_a * guide_img + mean_b  # Equation (7) in paper

    return result_img

def main():
    img_filename = 'images/img_smoothing/cat.bmp'
    im = Image.open(img_filename).convert('L')
    img = np.array(im).astype(np.float)
    print img
    output_img = single_channel_gfilter(img, img, 8, 0.4**2)
    output_img = np.clip(output_img, 0, 255).astype(np.uint8)

    output_img = Image.fromarray(output_img, 'L')
    output_img.show()


if __name__ == "__main__":
    main()
