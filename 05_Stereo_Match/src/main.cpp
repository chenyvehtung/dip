#include <opencv2/opencv.hpp>
#include <iostream>
#include "DispMatch.hpp"

using namespace cv;
using namespace std;

void matchFn(const Mat& leftImg, const Mat& rightImg, string costMethod);


int main(int argc, char const *argv[]) {
    Mat leftImg = imread("images/Aloe/view1.png", CV_LOAD_IMAGE_GRAYSCALE);
    Mat rightImg = imread("images/Aloe/view5.png", CV_LOAD_IMAGE_COLOR);
    //rightImg += 10;

    //Mat mainMat;
    //leftImg.convertTo(mainMat, CV_32F);
    //Vec3f pointA = mainMat.at<Vec3f>(Point(12,6));
    //cout << abs(Mat(pointA)) << endl;
    //Vec3f pointB = mainMat.at<Vec3f>(Point(12,6));
    //cout << pointB << endl;
    //cout << pointA - pointB << endl;
    //cout << (pointA - pointB).mul(pointA - pointB) << endl;
    //cout << sum((pointA - pointB).mul(pointA - pointB)).val[0] << endl;

    //namedWindow("Display Image", WINDOW_AUTOSIZE);
    //imshow("Display Image", dispASSD);

    matchFn(leftImg, rightImg, "ASW");
    //matchFn(leftImg, rightImg, "NCC");

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
