#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def equalize_hist(input_img):
    """
    Do histogram equalization on the input image and
    return the equalized result.
    """
    height, width = input_img.shape
    output_img = np.zeros_like(input_img)

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


def save_histogram(img, img_type="input"):
    """
    Genearte the histogram of the given image and save it to disk
    """
    bin_counts = gen_histogram(img)
    plt.bar(range(256), bin_counts, width=1.0, color="green")

    plt.title("Histogram for %s gray scale image" % img_type)
    # plt.show()
    fig_title = "images/%s_hist.png" % img_type
    plt.savefig(fig_title)
    print "Successfully save histogram %s" % fig_title
    plt.close()


def main():
    # get input image histogram and save it
    input_img = np.array(Image.open('images/72.png').convert('L'))
    save_histogram(input_img)
    # equalize the given image and save its histogram
    output_img = equalize_hist(input_img)
    save_histogram(output_img, img_type="output")
    # save the equalized result to disk
    output_img = Image.fromarray(output_img, 'L')
    output_img.save('images/equalize_72.png')
    print "Successfully save output image"


if __name__ == "__main__":
    main()
