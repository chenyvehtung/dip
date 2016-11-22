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
