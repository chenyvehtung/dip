# HW3: Filtering in the Frequency Domain

## Exercises

### 1.1 Rotation

The complex conjugate simply changes $j$ to $−j$ in the inverse transform, so the image on the right is given by
$$
\begin{align}
\mathscr{F}^{-1}[F^*(u, v)] &= \sum_{x=0}^{M-1}\sum_{y=0}^{N-1}F(u, v)e^{-j2\pi(ux/M+vy/N)} \\
&=\sum_{x=0}^{M-1}\sum_{y=0}^{N-1}F(u, v)e^{j2\pi(u(-x)/M+v(-y)/N)} \\
&=f(-x, -y)
\end{align}
$$
which simply mirrors $f(x, y)$ about the origin, thus producing the image on the right.

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

### 2.3 Bonus: Fast Fourier Transform

* **Perform FFT**

![](src/images/72resized.png)<br>
Resize the original image to 256x256

![](src/images/fft_72resized.png)<br>

* **Perform IFFT**

![](src/images/ifft_72resized.png)<br>

* **Detailedly discuss how you implement FFT / IFFT**<br>
Reference:<br> [https://jakevdp.github.io/blog/2013/08/28/understanding-the-fft/](https://jakevdp.github.io/blog/2013/08/28/understanding-the-fft/)<br>
[http://math.stackexchange.com/questions/77118/non-power-of-2-ffts](http://math.stackexchange.com/questions/77118/non-power-of-2-ffts)<br>
[http://stackoverflow.com/questions/11333454/2d-fft-using-1d-fft](http://stackoverflow.com/questions/11333454/2d-fft-using-1d-fft)
