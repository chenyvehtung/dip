#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np
from PIL import Image
import itertools
import time
import os.path


def dft2d(input_img, flags):
    M, N = input_img.shape
    output_img = np.zeros((M, N))

    # Discrete Fourier Transform implement in vector form of numpy
    # for u in xrange(M):
    #     for v in xrange(N):
    #         s = 0.0+0.j
    #         for x in xrange(M):
    #             for y in xrange(N):
    #                 s += ((input_img[x, y] + 0.j) * np.exp(-1j * 2 * np.pi *
    #                                                       (float(u * x) / M +
    #                                                        float(v * y) / N)))
    #         output_img[u, v] = s / (M * N)
    e_u = []
    e_v = []
    if flags == "dft":
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
            e_u.append(np.exp(1j * 2 * np.pi * u / M * np.arange(M).reshape(M, 1)))
        for v in xrange(N):
            e_v.append(np.exp(1j * 2 * np.pi * v / N * np.arange(N).reshape(1, N)))

        for x, y in itertools.product(xrange(M), xrange(N)):
            e_part = np.multiply(e_u[x], e_v[y])
            output_img[x, y] = np.sum(np.multiply(input_img, e_part))

    return output_img


# -----------------------------------------------------------------------------
# I trying to improve Fourier Transform by using multiprocessing in the following
# code, it works but just a few seconds, so I choose to comment it and use the
# origin code above
# def worker(u, v):
#     e_part = np.multiply(e_u[u], e_v[v])
#     res = np.mean(np.multiply(input_img, e_part))
#     return u, v, res
# def worker_star(u_v):
#     """convert f([u, v]) to f(u, v)"""
#     return worker(*u_v)
# def mul_dft2d(img):
#     import multiprocessing
#     global e_u
#     global e_v
#     global input_img
#     input_img = img
#     M, N = input_img.shape
#     e_u = []
#     e_v = []
#     for u in xrange(M):
#         e_u.append(np.exp(-1j * 2 * np.pi * u / M * np.arange(M).reshape(M, 1)))
#     for v in xrange(N):
#         e_v.append(np.exp(-1j * 2 * np.pi * v / N * np.arange(N).reshape(1, N)))
#     output_img = np.zeros((M, N))
#     pool = multiprocessing.Pool(processes=8)
#     for u, v, val in pool.map(worker_star, itertools.product(xrange(M), xrange(N))):
#         output_img[u, v] = val
#     return output_img
# -----------------------------------------------------------------------------


def shift_img(input_img):
    """
    Shift image to centralize the Fourier Spectrum
    """
    M, N = input_img.shape
    output_img = np.zeros((M, N))
    for x, y in itertools.product(xrange(M), xrange(N)):
        output_img[x, y] = input_img[x, y] * np.power(-1, x + y)
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


def main():
    input_img = np.array(Image.open('images/72.png').convert('L'))

    # dft
    shifted_img = shift_img(input_img)
    dft_path = 'dft.npy'
    if os.path.isfile(dft_path):
        output_img = np.load(dft_path)
    else:
        start_t = time.time()
        output_img = dft2d(shifted_img, "dft")
        end_t = time.time()
        print (end_t - start_t)
        np.save(dft_path, output_img)
    dft_img = Image.fromarray(stand_img(output_img), 'L')
    img_title = "images/dft_72.png"
    dft_img.save(img_title)
    print "Successfully saved ", img_title

    # idft
    idft_path = 'idft.npy'
    if os.path.isfile(idft_path):
        output_img_2 = np.load(idft_path)
    else:
        start_t = time.time()
        output_img_2 = dft2d(output_img, 'idft')
        end_t = time.time()
        print (end_t - start_t)
        np.save(idft_path, output_img_2)
    # shift back
    output_img_2 = shift_img(output_img_2)
    idft_img = Image.fromarray(output_img_2.astype(np.uint8), "L")
    img_title = "images/idft_72.png"
    idft_img.save(img_title)
    print "Successfully saved ", img_title


if __name__ == "__main__":
    main()
