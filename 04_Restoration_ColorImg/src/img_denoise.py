#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np
from PIL import Image
from random import randint
from img_filter import MyFilter, filter2d


def add_noise(img, noise_type, params):
    noisy_img = img.copy().astype(np.float)

    if noise_type == "gauss":
        gauss_mean = params.get('mean', 0)
        gauss_sigma = params.get('sigma', 1)
        gauss = np.random.normal(gauss_mean, gauss_sigma, img.size)
        gauss_min = np.amin(gauss)
        gauss_max = np.amax(gauss)
        gauss = (gauss - gauss_min) / (gauss_max - gauss_min) * (255 * 2) + (-255)
        gauss = gauss.reshape(img.shape)
        noisy_img += gauss
    elif noise_type == "s&p":
        # salt noise
        salt_prob = params.get('salt_prob', 0)
        num_salt = int(np.ceil(salt_prob * img.size))
        coords = get_random_coords(img.shape, num_salt)
        noisy_img[coords] = 255
        # pepper noise
        pepper_prob = params.get('pepper_prob', 0)
        num_pepper = int(np.ceil(pepper_prob * img.size))
        coords = get_random_coords(img.shape, num_pepper)
        noisy_img[coords] = 0
    else:
        raise ValueError("The noise type should be 'gauss' or 's&p'!")

    return noisy_img


def get_random_coords(shape, num):
    coords = []
    rows, cols = shape
    seen = set()
    for idx in xrange(num):
        x, y = randint(0, rows - 1), randint(0, cols - 1)
        while (x, y) in seen:
            x, y = randint(0, rows - 1), randint(0, cols - 1)
        seen.add((x, y))
        coords.append((x, y))
    return zip(*coords)


def save_img(img, title):
    im = np.clip(img, 0, 255).astype(np.uint8)
    im = Image.fromarray(im, 'L')
    im.save(title)
    print "Successfully saved ", title


def main():
    input_img = np.array(Image.open('images/task_2.png').convert('L'),
                         dtype=np.float64)

    # gaussian noise and denoise
    output_img = add_noise(input_img, "gauss", {'mean': 0, 'sigma': 40})
    save_img(output_img, "images/gauss_0_40_task_2.png")
    output_img = np.clip(output_img, 0, 255)
    filters_type = ["arithmetic", "geometric", "median"]
    for filter_type in filters_type:
        cur_filter = MyFilter(filter_type, 5)
        cur_img = filter2d(output_img, cur_filter)
        save_img(cur_img, "images/gauss_0_40_%s_task_2.png" % filter_type)

    # salt noise and denoise
    output_img = add_noise(input_img, "s&p", {'salt_prob': 0.2})
    save_img(output_img, "images/salt_2_task_2.png")
    output_img = np.clip(output_img, 0, 255)
    # harmonic mean filter denoise
    harmonic_filter = MyFilter("harmonic", 5)
    cur_img = filter2d(output_img, harmonic_filter)
    save_img(cur_img, "images/salt_2_harmonic_task_2.png")
    # contraharmonic mean filter
    for contra_q in [-1.5, 1.0]:
        cur_filter = MyFilter("contraharmonic", 5, contra_q)
        cur_img = filter2d(output_img, cur_filter)
        save_img(cur_img, "images/salt_2_contra_%d_task_2.png" % contra_q)

    # salt and pepper noise and denoise
    output_img = add_noise(input_img, "s&p", {'salt_prob': 0.2,
                                              'pepper_prob': 0.2})
    save_img(output_img, "images/salt_2_pepper_2_task_2.png")
    output_img = np.clip(output_img, 0, 255)
    filters_type = ["arithmetic", "geometric", "max", "min", "median"]
    for filter_type in filters_type:
        cur_filter = MyFilter(filter_type, 5)
        cur_img = filter2d(output_img, cur_filter)
        save_img(cur_img, "images/salt_2_pepper_2_%s_task_2.png" % filter_type)


if __name__ == "__main__":
    main()
