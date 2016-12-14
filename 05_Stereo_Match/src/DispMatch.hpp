#ifndef DISP_MATCH_H
#define DISP_MATCH_H

#include <stdio.h>
#include <opencv2/opencv.hpp>
#include <string>
#include <vector>

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
    double costASW(const cv::Mat& patchARGB, const cv::Mat& patchBRGB,
                   const cv::Mat& patchALab, const cv::Mat& patchBLab);
    double getSupportWeight(cv::Vec3f pointALab, cv::Vec3f pointBLab,
                            cv::Vec2f pointACoord, cv::Vec2f pointBCoord);
    int getTargetD(const std::vector<double>& v, std::string costType);
};


#endif
