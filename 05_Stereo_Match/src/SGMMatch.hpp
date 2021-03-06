#ifndef SGM_MATCH_H
#define SGM_MATCH_H

#include <iostream>
#include <algorithm>
#include <vector>
#include <cmath>
#include <ctime>
#include <opencv2/opencv.hpp>

#define SMALL_PENALTY 3
#define LARGE_PENALTY 20

class SGMMatch {
public:
    SGMMatch(cv::Mat _leftImg, cv::Mat _rightImg, unsigned short _pathNum,
            unsigned short _disparityRange, unsigned short _patchSize);
    ~SGMMatch();
    cv::Mat getDispMap(std::string directType);

private:
    cv::Mat leftImg;
    cv::Mat rightImg;
    unsigned short pathNum;
    unsigned short disparityRange;
    unsigned short patchSize;
    short          **pathDirection;
    unsigned short ***pixelCosts;
    double         ***smoothCosts;
    double         ****singlePathCosts;

    void initCosts(cv::string directType);
    void initPathDirection();
    void calculatePixelCosts(cv::string directType);
    unsigned short costSAD(const cv::Mat& patchA, const cv::Mat& patchB);
    double aggOneDireCost(int row, int col, int curDisp, short *curPathDire,
                            short curPathIdx);
    void aggAllDireCosts();
};


#endif
