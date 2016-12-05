#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def equalize_hist(input_img, bin_counts=None):
    """
    Do histogram equalization on the input image and
    return the equalized result.
    """
    height, width = input_img.shape
    output_img = np.zeros_like(input_img)

    if not bin_counts:
        bin_counts = gen_histogram(input_img)
    cnt_len = float(height * width)
    sk = []
    cnt_sum = 0
    for item in bin_counts:
        cnt_sum += item
        sk.append(cnt_sum / cnt_len)

    for row in xrange(height):
        for col in xrange(width):
            output_img[row][col] = int(255 * sk[input_img[row][col]])

    return output_img


def gen_histogram(img):
    """
    Count up the number of per gray level value in the given image and
    return it as a list.
    """
    bin_counts = []
    for idx in xrange(256):
        bin_counts.append(0)
    for item in img.ravel():
        bin_counts[item] += 1
    return bin_counts


def color_equalize_hist(input_img, mode):
    """
    Do histogram equalization on RGB image
    mode 1 is to equalize on channel seperately
    mode 2 is to equalize using a single average histogram
    """
    sub_imgs = input_img.transpose((2, 0, 1))
    output_img = np.zeros_like(sub_imgs)
    bin_counts = []

    if mode == 2:
        for idx in xrange(3):
            bin_counts.append(gen_histogram(sub_imgs[idx]))
        bin_counts = np.mean(np.array(bin_counts), axis=0).tolist()

    for idx in xrange(3):
        output_img[idx] = equalize_hist(sub_imgs[idx], bin_counts)

    return output_img.transpose((1, 2, 0))


def save_img(img, title):
    im = Image.fromarray(img)
    im.save(title)
    print "Successfully saved", title


def main():
    img_filename = 'images/72.png'
    input_img = np.array(Image.open(img_filename))
    for mode in [1 ,2]:
        output_img = color_equalize_hist(input_img, mode)
        save_img(output_img, "images/72_color_equa_%d.png" % mode)


if __name__ == "__main__":
    main()
