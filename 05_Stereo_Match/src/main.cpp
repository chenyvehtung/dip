#include <opencv2/opencv.hpp>
#include <iostream>
#include "DispMatch.hpp"

using namespace cv;

void matchFn(const Mat& leftImg, const Mat& rightImg, string costMethod);


int main(int argc, char const *argv[]) {
    Mat leftImg = imread("images/Aloe/view1.png", CV_LOAD_IMAGE_GRAYSCALE);
    Mat rightImg = imread("images/Aloe/view5.png", CV_LOAD_IMAGE_GRAYSCALE);
    rightImg += 10;

    //namedWindow("Display Image", WINDOW_AUTOSIZE);
    //imshow("Display Image", dispASSD);

    matchFn(leftImg, rightImg, "SSD");
    matchFn(leftImg, rightImg, "NCC");

    return 0;
}

void matchFn(const Mat& leftImg, const Mat& rightImg, string costMethod) {
    DispMatch dispMatch(leftImg, rightImg);
    Mat dispL = dispMatch.getDispMap("left", costMethod);

    imwrite("images/Aloe/Aloe_disp1_" + costMethod + ".png", dispL);
    std::cout << "Saved image Aloe_disp1_" + costMethod + ".png" << std::endl;

    Mat dispR = dispMatch.getDispMap("right", costMethod);
    imwrite("images/Aloe/Aloe_disp5_" + costMethod + ".png", dispR);
    std::cout << "Saved image Aloe_disp5_" + costMethod + ".png" << std::endl;
}
