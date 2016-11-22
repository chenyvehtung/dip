# HW3: Filtering in the Frequency Domain

## 2 Programming Tasks

### 2.2 Fourier Transform

* **Perform DFT**

![](src/images/dft_72.png)<br>
I did try all of my best to improve the Fourier Transformation, but it still take times, the Spectrum above takes about 100s in my machine to generate.

* **Perform IDFT**

![](src/images/idft_72.png)<br>
After fixing the imaginary calculation error, the final idft image is near the same as input image

* **Detailedly discuss how you implement DFT / IDFT**

Just follow the formula, but remmeber to try using vector operation and multiprocessing operation, because the calculation really take times for every point would use all the pixel of the input image as input.
