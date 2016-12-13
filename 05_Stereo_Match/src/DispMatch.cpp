#include "DispMatch.hpp"
#include <limits>
#include <iostream>
using namespace cv;
using std::string;


DispMatch::DispMatch(const cv::Mat& leftImg, const cv::Mat& rightImg):
    leftImg(leftImg), rightImg(rightImg) {

}

DispMatch::~DispMatch(){
    //std::cout << "Release DispMatch" << std::endl;
}

cv::Mat DispMatch::getDispMap(string directType, string costType) {
    int dMax = 79;
    int patchSize = 5;
    Size s = leftImg.size();
    int imgRows = s.height;
    int imgCols = s.width;
    Mat dispMap = Mat::zeros(s, CV_8U);

    Mat mainMat = Mat::zeros(s, CV_32F);
    Mat compareMat = Mat::zeros(s, CV_32F);

    int halfPatch = patchSize / 2;
    if (directType == "left") {
        leftImg.convertTo(mainMat, CV_32F);
        rightImg.convertTo(compareMat, CV_32F);
    }
    else {
        rightImg.convertTo(mainMat, CV_32F);
        leftImg.convertTo(compareMat, CV_32F);
    }

    // The coordinate system is different from PIL in Python
    for (int yidx = 0; yidx < imgRows - patchSize; ++yidx) {
        for (int xidx = 0; xidx < imgCols - patchSize; ++xidx) {
            Mat mainPatch = Mat(mainMat, Rect(xidx, yidx, patchSize, patchSize));
            int minD = 0;
            double minDisp = std::numeric_limits<double>::infinity();
            for (int dItem = 0; dItem <= dMax; ++dItem) {
                int compareX = (directType == "left") ? xidx - dItem : xidx + dItem;
                if (compareX < 0 || compareX >= imgCols - patchSize)
                    break;

                Mat comparePatch = Mat(compareMat, Rect(compareX, yidx, patchSize, patchSize));
                double curDisp;
                if (costType == "SSD")
                    curDisp = costSSD(mainPatch, comparePatch);

                if (curDisp < minDisp) {
                    minDisp = curDisp;
                    minD = dItem;
                }
            }
            dispMap.at<char>(yidx + halfPatch, xidx + halfPatch) = minD * 3;
            //std::cout << minD << std::endl;
        }
    }
    //std::cout << "Successfully construct disp map" << std::endl;

    return dispMap;
}


double DispMatch::costSSD(const cv::Mat& patchA, const cv::Mat& patchB) {
    Mat powArr;
    pow(patchA - patchB, 2.0, powArr);
    return sum(powArr)[0];
}
