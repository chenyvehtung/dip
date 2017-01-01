#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np
from PIL import Image


def box_filter(img, ksize, func):
    # box filter is edge preserving
    result = img.copy()
    half_ksize = ksize / 2
    for row in xrange(img.shape[0] - ksize):
        for col in xrange(img.shape[1] - ksize):
            result[row + half_ksize][col + half_ksize] =
                    func(img[row:row + ksize, col:col + ksize])
    return result


def single_channel_gfilter(img, guide_img, ksize, epsilon):

    # p mean
    mean_img = box_filter(img, ksize, np.mean)
    # I mean and I variance
    mean_gimg = box_filter(guide_img, ksize, np.mean)
    var_gimg = box_filter(guide_img, ksize, np.var)
    # mean Ip
    mean_ip = box_filter(guide_img.mul(img), ksize, np.mean)
    # a and b
    a = (mean_ip - mean_gimg * mean_img) / (var_gimg + epsilon)  # Equation (5) in paper
    b = mean_img - ak * mean_gimg  # Equation (6) in paper
    # a bar and b bar
    mean_a = box_filter(a, ksize, np.mean)
    mean_b = box_filter(b, ksize, np.mean)
    # get the result img
    tmp_result_img = mean_a * guide_img + mean_b  # Equation (7) in paper
    # filter the img by using edge preserve method
    result_img = img.copy()
    half_ksize = ksize / 2
    rows, cols = img.shape
    tmp_result_img =
    result_img[half_ksize:rows-half_ksize, half_ksize:cols-half_ksize] =
        tmp_result_img[half_ksize:rows-half_ksize, half_ksize:cols-half_ksize]

    return result_img

def main():
    pass


if __name__ == "__main__":
    main()
