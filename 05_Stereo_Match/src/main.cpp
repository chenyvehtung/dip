#include <opencv2/opencv.hpp>
#include "DispMatch.hpp"

using namespace cv;


int main(int argc, char const *argv[]) {
    Mat leftImg = imread("images/Aloe/view1.png");
    Mat rightImg = imread("images/Aloe/view5.png");

    //Mat dispASSD = getDispMap(leftImg, rightImg, "left", "SSD");
    DispMatch dispMatch(leftImg, rightImg);
    Mat dispASSD = dispMatch.getDispMap("left", "SSD");

    namedWindow("Display Image", WINDOW_AUTOSIZE);
    imshow("Display Image", dispASSD);
    //imwrite("test.png", leftImg);

    waitKey(0);
    return 0;
}
