# HW2: Histogram and Spatial Filtering

## 1 Exercises

### 1.1 Histogram Equalization

**Yes**, it will.<br>
The histogram equalizaiton transformation can be expressed as
$$
s_k = T(r_k) = \sum_{j=0}^{k}n_{r_j}/n = \frac{1}{n}\sum_{j=0}^{k}n_{r_j}
$$
where $n=MN$ is the total number of pixels, and $n_{r_j}$ is the number of pixels in the input image with intensity value $r_j$.<br>
According to the formula shown above, we know that every pixel with value $r_k$ will be mapped to value $s_k$.So after the first pass, we would have $n_{s_k} = n_{r_k}$.Supposed the second pass of histogram equalization $s_k$ would produce value $v_k$, then accroding to the equation, we would have
$$
v_k = T(s_k) = \frac{1}{n}\sum_{j=0}^{k}n_{s_j}
$$
since $n_{s_j} = n_{r_j}$, it yield
$$
v_k = T(s_k) = \frac{1}{n}\sum_{j=0}^{k}n_{s_j}=\frac{1}{n}\sum_{j=0}^{k}n_{r_j} = s_k
$$
That means a second pass of histogram equalization would yield the same result as the first pass. *Note that here we have assumed to ignore round-off errors*

### 1.2 Spatial Filtering

Under constructing...
$$
\begin{bmatrix}
    x_{11}       & x_{12} & x_{13} & \dots & x_{1n} \\
    x_{21}       & x_{22} & x_{23} & \dots & x_{2n} \\
    x_{d1}       & x_{d2} & x_{d3} & \dots & x_{dn}
\end{bmatrix}
$$

## 2 Programming Tasks

### 2.2 Histogram Equalization
