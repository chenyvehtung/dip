#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np
from PIL import Image
import time
import itertools
import multiprocessing


def naive_fft2d(input_img, flags='fft'):
    """A naive implement of 2d-FFT without optimizing"""
    def naive_fft1d(fx):
        """A recursive version of 1d-FFT"""
        M = fx.shape[0]
        if M == 1:
            return fx
        if M % 2 != 0:
            raise ValueError("size of fx must be power of 2")
        F_even = naive_fft1d(fx[::2])
        F_odd = naive_fft1d(fx[1::2])
        W_u_2k = np.exp(-1j * 2 * np.pi * np.arange(M / 2) / M)
        return np.concatenate((F_even + np.multiply(F_odd, W_u_2k),
                               F_even - np.multiply(F_odd, W_u_2k) ))

    if flags == 'ifft':
        input_img = np.conjugate(input_img)
    output_img = np.zeros_like(input_img, dtype=np.complex)
    x_num, y_num = input_img.shape
    # 1d fft on row
    for xidx in xrange(x_num):
        output_img[xidx, :] = naive_fft1d(input_img[xidx, :])
    # 1d fft on column
    for yidx in xrange(y_num):
        output_img[:, yidx] = naive_fft1d(output_img[:, yidx])
    if flags == 'fft':
        output_img /= float(x_num * y_num)

    return output_img


def fft1d_vec(x):
    """A vectorized, non-recursive version of the Cooley-Tukey FFT"""
    N = x.shape[0]
    if np.log2(N) % 1 > 0:
        raise ValueError("size of x must be a power of 2")
    # N_min here is equivalent to the stopping condition above,
    # and should be a power of 2
    N_min = min(N, 32)
    # Perform an O[N^2] DFT on all length-N_min sub-problems at once
    n = np.arange(N_min)
    k = n[:, None]
    M = np.exp(-2j * np.pi * n * k / N_min)
    X = np.dot(M, x.reshape((N_min, -1)))
    # build-up each level of the recursive calculation all at once
    while X.shape[0] < N:
        X_even = X[:, :X.shape[1] / 2]
        X_odd = X[:, X.shape[1] / 2:]
        factor = np.exp(-1j * np.pi * np.arange(X.shape[0])
                        / X.shape[0])[:, None]
        X = np.vstack([X_even + factor * X_odd,
                       X_even - factor * X_odd])
    return X.ravel()


def fft2d(input_img, flags):
    """2d FFT implementing with multiprocess"""
    if flags == 'ifft':
        input_img = np.conjugate(input_img)
    x_num, y_num =  input_img.shape
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    # 1d fft on row
    fft_xy = np.array(pool.map(fft1d_vec,  [input_img[xidx, :] for xidx in xrange(x_num)]))
    # 1d fft on column
    fft_xy = np.array(pool.map(fft1d_vec, [fft_xy[:, yidx] for yidx in xrange(y_num)]))
    output_img = np.transpose(fft_xy)
    if flags == 'fft':
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


def main():
    im = Image.open('images/72.png').resize((256, 256), Image.ANTIALIAS)
    im.save('images/72resized.png')
    input_img = np.array(im.convert('L'), dtype=np.float64)
    shifted_img = shift_img(input_img)

    # fft
    start_t = time.time()
    output_img = fft2d(shifted_img, "fft")
    end_t = time.time()
    print "It takes %f seconds." % (end_t - start_t)
    # print np.allclose(output_img, np.fft.fft2(shifted_img) / (256 * 256))
    # save fast Fourier transformation Spectrum
    fft_img = Image.fromarray(stand_img(output_img.real), 'L')
    img_title = "images/fft_72resized.png"
    fft_img.save(img_title)
    print "Successfully saved ", img_title

    # ifft
    start_t = time.time()
    output_img_2 = fft2d(output_img, 'ifft')
    end_t = time.time()
    print "It takes %f seconds." % (end_t - start_t)
    # get the real part, shift back and save it
    output_img_2 = shift_img(output_img_2.real)
    ifft_img = Image.fromarray(output_img_2.astype(np.uint8), "L")
    img_title = "images/ifft_72resized.png"
    ifft_img.save(img_title)
    print "Successfully saved ", img_title


if __name__ == "__main__":
    main()
