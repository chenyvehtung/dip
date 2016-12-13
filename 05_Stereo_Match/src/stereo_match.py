#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PIL import Image
import numpy as np


def get_bad_percent(test_img, gt_img):
    """
    To get the bad pixel percentage of the test_img in comparing with gt_img,
    where test_img and gt_img should be both gray Image object.
    """
    test_arr = np.array(test_img, dtype=np.float) / 3.0
    gt_arr = np.array(gt_img, dtype=np.float) / 3.0
    diff_arr = np.abs(gt_arr - test_arr)
    return float((diff_arr > 1.0).sum()) / gt_arr.size


def get_all_bad_percent(filepath):
    """
    Format 'Aloe  : Left--10%; Right--15%'
    """
    pass


def get_disp_map(left_img, right_img, direct_type, cost_func):
    def get_patch(pos, psize, arr):
        return arr[pos[0] - psize / 2 : pos[0] + psize / 2 + 1,
                   pos[1] - psize / 2 : pos[1] + psize / 2 + 1]

    dmax = 79
    patch_size = 5
    left_arr = np.array(left_img, dtype=np.float)
    right_arr = np.array(right_img, dtype=np.float)
    disp_map = np.zeros(left_arr.shape[0:2])

    main_arr = np.zeros_like(left_arr)
    compare_arr = np.zeros_like(left_arr)

    half_patch = patch_size / 2
    if direct_type == "left":
        main_arr = left_arr
        compare_arr = right_arr
        d_arr = -np.arange(dmax + 1)
    else:  # right disparity map
        main_arr = right_arr
        compare_arr = left_arr
        d_arr = np.arange(dmax + 1)

    for xidx in xrange(half_patch, left_arr.shape[0] - half_patch):
        for yidx in xrange(half_patch, left_arr.shape[1] - half_patch):
            main_patch = get_patch((xidx, yidx), patch_size, main_arr)
            min_d = 0
            min_disp = float('Inf')
            for ditem in d_arr:
                compare_y = yidx + ditem
                if compare_y < half_patch or compare_y >= left_arr.shape[1] - half_patch:
                    break
                compare_patch = get_patch((xidx, compare_y), patch_size, compare_arr)
                cur_disp = cost_func((main_patch, compare_patch))
                if cur_disp < min_disp:
                    min_disp = cur_disp
                    min_d = abs(ditem)
            disp_map[xidx - half_patch, yidx - half_patch] = min_d * 3
        # print "finish", xidx * left_arr.shape[0] + yidx
    return disp_map.astype(np.uint8)


def ssd_cost(patch_pair):
    """calculate the sums of squared difference between two patch"""
    return np.power(patch_pair[0] - patch_pair[1], 2).sum()


def save_img():
    pass


def tic():
    #Homemade version of matlab tic and toc functions
    import time
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()

def toc():
    import time
    if 'startTime_for_tictoc' in globals():
        print "Elapsed time is " + str(time.time() - startTime_for_tictoc) + " seconds."
    else:
        print "Toc: start time not set"


def main():
    left_img = Image.open("images/Aloe/view1.png")
    right_img = Image.open("images/Aloe/view5.png")
    tic()
    disp1_ssd = get_disp_map(left_img, right_img, "left", ssd_cost)
    toc()
    tic()
    disp5_ssd = get_disp_map(left_img, right_img, "right", ssd_cost)
    toc()
    Image.fromarray(disp1_ssd, 'L').show()
    Image.fromarray(disp5_ssd, 'L').show()
    print get_bad_percent(Image.fromarray(disp1_ssd, 'L'),
                          Image.open('images/Aloe/disp1.png').convert('L'))
    print get_bad_percent(Image.fromarray(disp5_ssd, 'L'),
                          Image.open('images/Aloe/disp5.png').convert('L'))



if __name__ == "__main__":
    main()
