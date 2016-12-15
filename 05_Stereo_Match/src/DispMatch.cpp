#include "DispMatch.hpp"
#include <limits>
#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
using namespace cv;
using std::string;


DispMatch::DispMatch(const cv::Mat& leftImg, const cv::Mat& rightImg):
    leftImg(leftImg), rightImg(rightImg) {

}

DispMatch::~DispMatch(){
    // std::cout << "Release DispMatch" << std::endl;
}

cv::Mat DispMatch::getDispMap(string directType, string costType) {
    int dMax = 79;
    int patchSize = 5;
    Size s = leftImg.size();
    int imgRows = s.height;
    int imgCols = s.width;
    Mat dispMap = Mat::zeros(Size(imgCols, imgRows), CV_8U);

    Mat mainMat, compareMat;
    //get the CIELab color for ASW
    Mat mainMatLab, compareMatLab;

    int halfPatch = patchSize / 2;
    if (directType == "left") {
        leftImg.convertTo(mainMat, CV_32F);
        rightImg.convertTo(compareMat, CV_32F);
        cvtColor(leftImg, mainMatLab, CV_RGB2Lab);
        cvtColor(rightImg, compareMatLab, CV_RGB2Lab);
    }
    else {
        rightImg.convertTo(mainMat, CV_32F);
        leftImg.convertTo(compareMat, CV_32F);
        cvtColor(rightImg, mainMatLab, CV_RGB2Lab);
        cvtColor(leftImg, compareMatLab, CV_RGB2Lab);
    }

    // convert lab color from cv_8u to CV_32F
    mainMatLab.convertTo(mainMatLab, CV_32F);
    compareMatLab.convertTo(compareMatLab, CV_32F);

    // The coordinate system is different from PIL in Python
    for (int yidx = 0; yidx < imgRows - patchSize; ++yidx) {
        for (int xidx = 0; xidx < imgCols - patchSize; ++xidx) {
            Mat mainPatch = Mat(mainMat, Rect(xidx, yidx, patchSize, patchSize));
            // find the best d
            std::vector<double> allDisps;
            for (int dItem = 0; dItem <= dMax; ++dItem) {
                int compareX = (directType == "left") ? xidx - dItem : xidx + dItem;
                if (compareX < 0 || compareX >= imgCols - patchSize)
                    break;

                Mat comparePatch = Mat(compareMat, Rect(compareX, yidx, patchSize, patchSize));
                double curDisp;
                // calculate dissimilarity according to cost function type
                if (costType == "SSD")
                    curDisp = costSSD(mainPatch, comparePatch);
                else if (costType == "NCC")
                    curDisp = costNCC(mainPatch, comparePatch);
                else  // costType == ASW
                    curDisp = costASW(mainPatch, comparePatch,
                                Mat(mainMatLab, Rect(xidx, yidx, patchSize, patchSize)),
                                Mat(compareMatLab, Rect(compareX, yidx, patchSize, patchSize)));

                allDisps.push_back(curDisp);
            }
            dispMap.at<char>(yidx + halfPatch, xidx + halfPatch) =
                    getTargetD(allDisps, costType) * 3;
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

double DispMatch::costNCC(const cv::Mat& patchA, const cv::Mat& patchB) {
    Mat normPatchA = normMat(patchA);
    Mat normPatchB = normMat(patchB);
    return mean(normPatchA.mul(normPatchB)).val[0];
}

Mat DispMatch::normMat(const cv::Mat& patch) {
    Scalar mean, stddev;
    meanStdDev(patch, mean, stddev);
    return (patch - mean.val[0]) / stddev.val[0];
}

double DispMatch::costASW(const Mat& patchARGB, const Mat& patchBRGB,
               const Mat& patchALab, const Mat& patchBLab) {
    Size s = patchARGB.size();
    int centerX = s.width / 2;
    int centerY = s.height / 2;
    Vec3f pLab = patchALab.at<Vec3f>(Point(centerX, centerY));
    Vec3f pBarLab = patchBLab.at<Vec3f>(Point(centerX, centerY));
    Vec2f centerCoord(centerX, centerY);

    double eNumerator = 0;
    double eDenominator = 0;
    for (int yidx = 0; yidx < s.height; ++yidx) {
        for (int xidx = 0; xidx < s.width; ++xidx) {
            if (yidx == centerY && xidx == centerX)
                continue;

            Vec3f qLab = patchALab.at<Vec3f>(Point(xidx, yidx));
            Vec3f qBarLab = patchBLab.at<Vec3f>(Point(xidx, yidx));
            Vec2f curCoord(xidx, yidx);

            double ww = getSupportWeight(pLab, qLab, centerCoord, curCoord)
                    * getSupportWeight(pBarLab, qBarLab, centerCoord, curCoord);
            eDenominator += ww;

            Vec3f qRGB = patchARGB.at<Vec3f>(Point(xidx, yidx));
            Vec3f qBarRGB = patchBRGB.at<Vec3f>(Point(xidx, yidx));
            double eo = sum(abs(Mat(qRGB - qBarRGB))).val[0];
            eNumerator += ww * eo;
        }
    }
    return eNumerator / eDenominator;
}

double DispMatch::getSupportWeight(Vec3f pointALab, Vec3f pointBLab,
                                   Vec2f pointACoord, Vec2f pointBCoord) {
    double gammaC = 7.0, gammaP = 36.0, k = 1.0;
    double deltaC = sqrt(sum((pointALab - pointBLab).mul(pointALab - pointBLab)).val[0]);
    double deltaG = sqrt(sum((pointACoord - pointBCoord).mul(pointACoord - pointBCoord)).val[0]);
    return k * exp(-(deltaC / gammaC + deltaG / gammaP));
}

int DispMatch::getTargetD(const std::vector<double>& v, std::string costType) {
    if (costType == "SSD" || costType == "ASW")
        return std::distance(v.begin(), std::min_element(v.begin(), v.end()));
    else  //by now it is NCC
        return std::distance(v.begin(), std::max_element(v.begin(), v.end()));
}
