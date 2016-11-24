#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np
from PIL import Image
import itertools
import time
import multiprocessing


def naive_dft2d(input_img, flags='dft'):
    M, N = input_img.shape
    output_img = np.zeros((M, N)) + 0.j
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


def dft1d(fx):
    M = fx.shape[0]
    u_arr = np.arange(M).reshape((M, 1))
    x_arr = np.arange(M).reshape((1, M))
    factor = np.exp(-2j * np.pi * u_arr * x_arr / M)
    return np.dot(factor, fx)


def dft2d(input_img, flags):
    if flags == 'idft':
        input_img = np.conjugate(input_img)
    x_num, y_num =  input_img.shape
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    # 1d dft on row
    dft_xy = np.array(pool.map(dft1d,  [input_img[xidx, :] for xidx in xrange(x_num)]))
    # 1d dft on column
    dft_xy = np.array(pool.map(dft1d, [dft_xy[:, yidx] for yidx in xrange(y_num)]))
    output_img = np.transpose(dft_xy)
    if flags == 'dft':
        output_img /= float(x_num * y_num)

    return output_img


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


def test_dft():
    a = np.arange(2000.0).reshape((40, 50))

    dft_output = dft2d(a, "dft")
    print "Is DFT right? ", np.allclose(dft_output, np.fft.fft2(a)/2000.0)

    idft_output = dft2d(dft_output, "idft")
    print "Is IDFT right? ", np.allclose(idft_output, np.fft.ifft2(dft_output)*2000.0)


def main():
    input_img = np.array(Image.open('images/72.png').convert('L'), dtype=np.float64)

    # dft
    shifted_img = shift_img(input_img)
    start_t = time.time()
    output_img = dft2d(shifted_img, "dft")
    end_t = time.time()
    print "DFT: takes %f seconds" % (end_t - start_t)
    dft_img = Image.fromarray(stand_img(output_img.real), 'L')
    img_title = "images/dft_72.png"
    dft_img.save(img_title)
    print "Successfully saved ", img_title

    # idft
    start_t = time.time()
    output_img_2 = dft2d(output_img, 'idft')
    end_t = time.time()
    print "IDFT: takes %f seconds" % (end_t - start_t)
    # get the real part and shift back
    output_img_2 = shift_img(output_img_2.real)
    idft_img = Image.fromarray(output_img_2.astype(np.uint8), "L")
    img_title = "images/idft_72.png"
    idft_img.save(img_title)
    print "Successfully saved ", img_title


if __name__ == "__main__":
    test_dft()
    main()
