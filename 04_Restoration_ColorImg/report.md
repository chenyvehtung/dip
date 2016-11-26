# HW4: Image Restoration and Color Image Processing


## 2 Programming Tasks

### 2.2 Image Filtering

![](src/images/task_1.png)<br>
Original Image

* **2.2.1 arithmetic mean filters**

![](src/images/arithmetic_3_3_task_1.png)<br>
Using 3x3 arithmetic mean filter

![](src/images/arithmetic_9_9_task_1.png)<br>
Using 9x9 arithmetic mean filter

The images are all blurred

* **2.2.2 harmonic mean filters**

![](src/images/harmonic_3_3_task_1.png)<br>
Using 3x3 harmonic mean filter

![](src/images/harmonic_9_9_task_1.png)<br>
Using 9x9 harmonic mean filter

The white bars in the image which used 3x3 filter becomes shorter and thiner and the size of the white bars should be (222, 6)<br>
There is no white bars in the image which used 9x9 filter.

* **2.2.3 contraharmonic mean filters with Q = −1.5**

![](src/images/contraharmonic_3_3_task_1.png)<br>
Using 3x3 contraharmonic mean filter

![](src/images/contraharmonic_9_9_task_1.png)<br>
Using 9x9 contraharmonic mean filter

The same as 2.2.2

### 2.3 Image Denoising

![](src/images/task_2.png)<br>
input image for task 2

* **2.3.2 Add Gaussian noise and denoise**

![](src/images/gauss_0_40_task_2.png)<br>
Add Gaussian noise with mean = 0 and sigma = 40

![](src/images/gauss_0_40_arithmetic_task_2.png)<br>
Denoise using arithmetic mean filter with size = 5

![](src/images/gauss_0_40_geometric_task_2.png)<br>
Denoise using geometric mean filter with window size = 5

![](src/images/gauss_0_40_median_task_2.png)<br>
Denoise using median filter with window size = 5

The one with arithmetic mean filter looks best, while the one with geometric mean fitler looks worest.
