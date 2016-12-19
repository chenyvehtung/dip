# HW4: Image Restoration and Color Image Processing

## 1 Exercises

### 1.1 Color Spaces

**1.1.1**<br>
结合6.2.3节中的图6.13，我们可以得知该图像的色调(Hue)分量依次是
$$
H =
\begin{bmatrix}
    \frac{1}{6}  & \frac{5}{6}  \\
    \frac{1}{2}  & \frac{1}{3}
\end{bmatrix}
$$
0为纯黑色，1为纯白色，以此来确定上述矩阵对应的灰度图<br>
饱和度的公式为:
$$
S = 1 - \frac{3}{(R+G+B)}[min(R, G, B)]
$$
由于四个颜色的RGB分量中的最小值都是0，可知它们都是饱和色，所以他们的饱和度(Saturation)分量都是1，是一张纯白色的图<br>
最后，强度(Intensity)分量的计算公式为<br>
$$
I = \frac{1}{3}(R+G+B)
$$
所以其强度分量依次是
$$
I =
\begin{bmatrix}
    \frac{2}{3}  & \frac{2}{3}  \\
    \frac{2}{3}  & \frac{1}{3}
\end{bmatrix}
$$
同理，0为纯黑色，1为纯白色，以此来确定上述矩阵对应的灰度图<br>
**1.1.2**<br>
该图的饱和度通道的数值都是常量1，所以，对其应用算术平均滤波之后，得到的结果仍然是原图。<br>
**1.1.3**<br>
对于色调通道，由于每个方块都是常量，所以，如果整个滤波器都落在一个方块区域中，那么得到的结果仍是该常量。但是，在区域的交界处，滤波后会改变它们的值，这个值的大小，取决于每个区域在滤波器中所占的比重。所以，在区域的交界处，会呈现一个渐变的效果，从一个色调逐渐变换到另一个色调。<br>

## 2 Programming Tasks

### 2.2 Image Filtering

![](src/images/task_1.png)<br>
原图

**2.2.1 arithmetic mean filters**

![](src/images/arithmetic_3_3_task_1.png)<br>
使用 3x3 算术均值滤波器

![](src/images/arithmetic_9_9_task_1.png)<br>
使用 9x9 算术均值滤波器

图像变得模糊了，而且使用9x9的滤波器得到的结果比使用3x3得到的结果更模糊。

**2.2.2 harmonic mean filters**

![](src/images/harmonic_3_3_task_1.png)<br>
使用 3x3 几何均值滤波器

![](src/images/harmonic_9_9_task_1.png)<br>
使用 9x9 几何均值滤波器

使用3x3的滤波器得到的图像中，白条变得更瘦更短了，并且每个白条的大小应该是(222, 6)<br>
使用9x9的滤波器得到的图像中，不存在白条。由于几何均值滤波进行了累乘运算，而白条的宽为8，对于9x9的滤波器，其对应的图像块中一定存在黑色(值为0)像素，所以最终得到的必定全是0。

**2.2.3 contraharmonic mean filters with Q = −1.5**

![](src/images/contraharmonic_3_3_task_1.png)<br>
使用 3x3 Q=1.5的逆谐波均值滤波器

![](src/images/contraharmonic_9_9_task_1.png)<br>
使用 9x9 Q=1.5的逆谐波均值滤波器

得到的结果大致上与2.2.2中相同

### 2.3 Image Denoising

![](src/images/task_2.png)<br>
原图

**2.3.2 Add Gaussian noise and denoise**

![](src/images/gauss_0_40_task_2.png)<br>
加了均值为0，标准差为40的高斯噪声后的图像

![](src/images/gauss_0_40_arithmetic_task_2.png)<br>
使用5x5的算术均值滤波器去噪后的图像

![](src/images/gauss_0_40_geometric_task_2.png)<br>
使用5x5的几何均值滤波器去噪后的图像

![](src/images/gauss_0_40_median_task_2.png)<br>
使用5x5的中值滤波器去噪后的图像

使用算术均值滤波器得到的结果最好，使用几何均值滤波器得到的结果最差。

**2.3.3 Add salt noise and denoise**

![](src/images/salt_2_task_2.png)<br>
加了概率为0.2的盐噪声后的图像

![](src/images/salt_2_harmonic_task_2.png)<br>
使用5x5的谐波滤波器去噪后的图像

![](src/images/salt_2_contra_-1_task_2.png)<br>
使用5x5的 $Q=-1.5$ 逆谐波滤波器去噪后的图像

![](src/images/salt_2_contra_1_task_2.png)<br>
使用5x5的 $Q=1.0$ 逆谐波滤波器去噪后的图像

**2.3.4 Add salt-and-pepper noise and denoise**

![](src/images/salt_2_pepper_2_task_2.png)<br>
加了概率都为0.2的椒和盐噪声后的图像

![](src/images/salt_2_pepper_2_arithmetic_task_2.png)<br>
使用5x5的算术均值滤波器去噪后的图像

![](src/images/salt_2_pepper_2_geometric_task_2.png)<br>
使用5x5的几何均值滤波器去噪后的图像

![](src/images/salt_2_pepper_2_max_task_2.png)<br>
使用5x5的最大值滤波器去噪后的图像

![](src/images/salt_2_pepper_2_min_task_2.png)<br>
使用5x5的最小值滤波器去噪后的图像

![](src/images/salt_2_pepper_2_median_task_2.png)<br>
使用5x5的中值滤波器去噪后的图像

显然，中值滤波器得到的效果最好

**2.3.5 Discuss how you implement all the above filtering operations**<br>
程序中定义了一个类叫做MyFilter，创建MyFilter类对象需要指明该滤波器的类型以及滤波器的大小。类的filtering函数用来对图像块进行滤波，它接受一个图像块做为输入，返回对图像块操作后的结果。<br>
剩下的工作就很简单了，执行滤波操作时，从左向右，从上到下依次取一定大小的图像块，输入到对应类型的MyFilter滤波器中，将返回的结果做为中心像素的值即可。<br>
相应滤波器的操作严格按照书本公式实现即可，核心代码如下：

```python
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
```

### 2.4 Histogram Equalization on Color Images

![](src/images/72.png)<br>
原图

**2.4.1 Processing the R, G, B channels separately**

![](src/images/72_color_equa_1.png)<br>

**2.4.2 Using a single histogram equalization intensity transformation function**

![](src/images/72_color_equa_2.png)<br>

**2.4.3 Perform histogram equalization on intensity channel**<br>
![](src/images/72_color_equa_0.png)<br>

**2.4.4 Compare the above results**<br>
2.4.3中得到的结果优于2.4.2的，而2.4.2得到的结果优于2.4.1的结果。
