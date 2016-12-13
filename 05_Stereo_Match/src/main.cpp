#include <opencv2/opencv.hpp>
#include <iostream>
#include "DispMatch.hpp"

using namespace cv;


int main(int argc, char const *argv[]) {
    Mat leftImg = imread("images/Aloe/view1.png", CV_LOAD_IMAGE_GRAYSCALE);
    Mat rightImg = imread("images/Aloe/view5.png", CV_LOAD_IMAGE_GRAYSCALE);

    DispMatch dispMatch(leftImg, rightImg);
    Mat dispLSSD = dispMatch.getDispMap("left", "SSD");
    //namedWindow("Display Image", WINDOW_AUTOSIZE);
    //imshow("Display Image", dispASSD);
    imwrite("images/Aloe/Aloe_disp1_SSD.png", dispLSSD);
    std::cout << "Save image Aloe_disp1_SSD.png" << std::endl;

    Mat dispRSSD = dispMatch.getDispMap("right", "SSD");
    imwrite("images/Aloe/Aloe_disp5_SSD.png", dispRSSD);
    std::cout << "Save image Aloe_disp5_SSD.png" << std::endl;

    //waitKey(0);
    return 0;
}
