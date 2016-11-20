#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np
from PIL import Image
import itertools
import time


def dft2d(input_img, flags):
    M, N = input_img.shape
    output_img = np.zeros((M, N))

    # for u in xrange(M):
    #     for v in xrange(N):
    #         s = 0.0+0.j
    #         for x in xrange(M):
    #             for y in xrange(N):
    #                 s += ((input_img[x, y] + 0.j) * np.exp(-1j * 2 * np.pi *
    #                                                       (float(u * x) / M +
    #                                                        float(v * y) / N)))
    #         output_img[u, v] = s / (M * N)

    # Discrete Fourier Transform implement in vector form of numpy
    if flags == "dft":
        e_u = []
        e_v = []
        for u in xrange(M):
            e_u.append(np.exp(-1j * 2 * np.pi * u / M * np.arange(M).reshape(M, 1)))
        for v in xrange(N):
            e_v.append(np.exp(-1j * 2 * np.pi * v / N * np.arange(N).reshape(1, N)))

        for u, v in itertools.product(xrange(M), xrange(N)):
            # print u, v
            e_part = np.multiply(e_u[u], e_v[v])
            output_img[u, v] = np.mean(np.multiply(input_img, e_part))

    # Inverse Discrete Fourier Transform (IDFT)
    else:
        for u in xrange(M):
            for v in xrange(N):
                s = 0.0+0.j
                for x in xrange(M):
                    for y in xrange(N):
                        s += ((input_img[x, y] + 0.j) * np.exp(-1j * 2 * np.pi *
                                                              (float(u * x) / M +
                                                               float(v * y) / N)))
                output_img[u, v] = s / (M * N)

    return output_img


def stand_img(img):
    """
    scale output image for display purpose and
    return the scaled image
    """
    min_v = np.amin(img)
    img -= min_v
    max_v = np.amax(img)
    output_img = 255.0 / max_v * img
    return output_img.astype(np.uint8)


def main():
    input_img = np.array(Image.open('images/72.png').convert('L'))
    # input_img = np.array([0.4, 0.6, 0.8, 0.2]).reshape((2, 2))

    start_t = time.time()
    output_img = dft2d(input_img, "dft")
    end_t = time.time()
    print (end_t - start_t)
    print output_img

    start_t = time.time()
    output_img = dft2d(input_img, "flags")
    end_t = time.time()
    print (end_t - start_t)
    print output_img


if __name__ == "__main__":
    main()
