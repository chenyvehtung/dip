#ifndef DISP_MATCH_H
#define DISP_MATCH_H

#include <stdio.h>
#include <opencv2/opencv.hpp>
#include <string>

class DispMatch {
public:
    DispMatch(const cv::Mat& leftImg, const cv::Mat& rightImg);
    ~DispMatch();
    cv::Mat getDispMap(std::string directType, std::string costType);
private:
    cv::Mat leftImg;
    cv::Mat rightImg;
    double costSSD(const cv::Mat& patchA, const cv::Mat& patchB);
    double costNCC(const cv::Mat& patchA, const cv::Mat& patchB);
    cv::Mat normMat(const cv::Mat& patch);
};


#endif
