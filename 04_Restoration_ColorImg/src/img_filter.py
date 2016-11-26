#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np
from PIL import Image


class MyFilter:
    def __init__(self, filter_type, filter_size, contra_q=None):
        self.filter_type = filter_type
        self.filter_size = filter_size
        self.contra_q = contra_q

    def filtering(self, img_block):
        res = None
        if self.filter_type == "arithmetic":
            res = np.mean(img_block)
        elif self.filter_type == "harmonic":
            res = img_block.size / np.sum(1.0 / (img_block + 1e-9))
        elif self.filter_type == "contraharmonic":
            img_block += 1e-9
            res = np.sum(img_block ** (self.contra_q + 1)) / np.sum(img_block ** self.contra_q)
        elif self.filter_type == "geometric":
            res = np.prod(img_block) ** (1.0 / img_block.size)
        elif self.filter_type == "median":
            res = np.median(img_block)
        elif self.filter_type == "max":
            res = np.amax(img_block)
        elif self.filter_type == "min":
            res = np.amin(img_block)
        else:
            raise ValueError("Filter type is not supported yet.")
        return res


def filter2d(input_img, filter):
    height, width = input_img.shape
    output_img = np.zeros_like(input_img)

    # add zero-padding
    filter_len =  filter.filter_size
    pad_len = filter_len / 2
    pad_h = np.zeros((pad_len, width))
    pad_img = np.vstack((pad_h, input_img, pad_h))
    pad_v = np.zeros((height + 2 * pad_len, pad_len))
    pad_img = np.hstack((pad_v, pad_img, pad_v))
    # convolution on pad image
    for row in xrange(height):
        for col in xrange(width):
            img_patch = pad_img[row:row + filter_len, col:col + filter_len]
            output_img[row][col] = filter.filtering(img_patch)

    return output_img


def main():
    input_img = np.array(Image.open('images/task_1.png').convert('L'), dtype=np.float64)

    filters_type = ["arithmetic", "harmonic", "contraharmonic"]
    filters_size = [3, 9]
    for filter_type in filters_type:
        for filter_size in filters_size:
            if filter_type == "contraharmonic":
                cur_filter = MyFilter(filter_type, filter_size, -1.5)
            else:
                cur_filter = MyFilter(filter_type, filter_size)
            output_img = filter2d(input_img, cur_filter)
            # output_img = np.clip(output_img, 0, 255)
            output_img = Image.fromarray(output_img.astype(np.uint8), 'L')
            img_title = "images/%s_%d_%d_task_1.png" % (filter_type,
                                                        filter_size, filter_size)
            output_img.save(img_title)
            print "Successfully saved %s" % img_title


if __name__ == "__main__":
    main()
