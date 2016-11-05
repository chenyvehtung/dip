#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def equalize_hist(input_img):
    height, width = input_img.shape
    output_img = np.zeros_like(input_img)
    # bin_counts, bin_edges = np.histogram(input_img, bins=np.arange(257))
    bin_counts = []
    for idx in xrange(256):
        bin_counts.append(0)
    for item in input_img.ravel():
        bin_counts[item] += 1

    cnt_len = float(height * width)
    sk = []
    cnt_sum = 0
    for item in bin_counts:
        cnt_sum += item
        sk.append(cnt_sum / cnt_len)
    print sk

    for row in xrange(height):
        for col in xrange(width):
            output_img[row][col] = int(255 * sk[input_img[row][col]])

    return output_img


def show_histogram(img, img_type="input"):
    plt.hist(img.ravel(), 256, [0, 256])
    plt.title("Histogram for %s gray scale image" % img_type)
    # plt.show()
    fig_title = "images/%s_hist.png" % img_type
    plt.savefig(fig_title)
    print "Successfully save histogram %s" % fig_title
    plt.close()


def main():
    input_img = np.array(Image.open('images/72.png').convert('L'))
    show_histogram(input_img)
    output_img = equalize_hist(input_img)
    show_histogram(output_img, img_type="output")
    
    output_img = Image.fromarray(output_img, 'L')
    output_img.save('images/equalize_72.png')
    print "Successfully save output image"


if __name__ == "__main__":
    main()
