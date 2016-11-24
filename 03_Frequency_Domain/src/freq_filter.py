#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np
from PIL import Image


def filter2d_freq(input_img, filter):
    # step 1: get padding params
    M, N = input_img.shape
    P = 2 * M
    Q = 2 * N
    # step 2: pad Image
    pad_img = np.zeros((P, Q))
    pad_img[:M, :N] = input_img
    # step 3: center transform
    shifted_img = shift_img(pad_img)
    # step4: image dft
    dft_img = np.fft.fft2(shifted_img)
    Image.fromarray(shift_img(np.fft.ifft2(dft_img).real).astype(np.uint8), 'L').show()
    # TODO how to get frequency filter from space filter
    # step5: form freq filter and Perform array multiplication
    # step5.1 pad filter
    h_f, w_f = filter.shape
    pad_filter = np.zeros((P, Q))
    pad_filter[:h_f, :w_f] = filter
    # step5.2 center filter
    shifted_filter = shift_img(pad_filter)
    # step5.3 get frequency filter through DFT
    dft_filter = np.fft.fft2(shifted_img)
    # step5.4 get imaginary part of freq filter
    dft_filter = dft_filter.imag
    # step5.5 shift back filter
    dft_filter = shift_img(dft_filter)
    # step5.6 Perform array multiplication
    g_img = dft_filter * dft_img
    # step6: obtain processed image
    idft_img = np.fft.ifft2(g_img)
    idft_img = shift_img(idft_img.real)
    # step7: extract top left part
    output_img = idft_img[:M, :N]
    return output_img


def shift_img(input_img):
    height, width = input_img.shape
    row_idx = np.arange(height).reshape((height, 1))
    col_idx = np.arange(width).reshape((1, width))
    factor = (-1) ** (row_idx + col_idx)
    return factor * input_img


def gen_avg_filter(filter_len):
    return 1.0 / (filter_len * filter_len) * np.ones((filter_len, filter_len))


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


def show_img(img):
    im = Image.fromarray(stand_img(img), "L")
    im.show()


def main():
    input_img = np.array(Image.open('images/72.png').convert('L'), dtype=np.float64)

    # smooth image
    avg_filter = gen_avg_filter(7)
    output_img = filter2d_freq(input_img, avg_filter)
    # print output_img
    filtered_img = Image.fromarray(stand_img(output_img), "L")
    filtered_img.show()


if __name__ == "__main__":
    main()
