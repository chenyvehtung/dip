#include "SGMMatch.hpp"

using namespace cv;
using std::string;
using std::cout;
using std::endl;

SGMMatch::SGMMatch(cv::Mat _leftImg, cv::Mat _rightImg, unsigned short _pathNum,
        unsigned short _disparityRange, unsigned short _patchSize) :
        pathNum(_pathNum), disparityRange(_disparityRange), patchSize(_patchSize) {
    // convert img from bgr to gray
    cvtColor(_leftImg, leftImg, CV_BGR2GRAY);
    cvtColor(_rightImg, rightImg, CV_BGR2GRAY);
}

SGMMatch::~SGMMatch() {
    int rows = leftImg.rows;
    int cols = leftImg.cols;

    for (int row = 0; row < rows; ++row) {
        for (int col = 0; col < cols; ++col) {
            delete[] smoothCosts[row][col];
            delete[] pixelCosts[row][col];
        }
    }

    for (int p = 0; p < pathNum / 2; ++p) {
        for (int row = 0; row < rows; ++row) {
            for (int col = 0; col < cols; ++col) {
                delete[] singlePathCosts[p][row][col];
            }
        }
    }
}

cv::Mat SGMMatch::getDispMap(string directType) {
    initCosts(directType);
    initPathDirection();
    aggAllDireCosts();

    Mat dispMap = Mat::zeros(Size(leftImg.cols, leftImg.rows), CV_8U);
    for (int row = 0; row < leftImg.rows; ++row) {
        for (int col = 0; col < leftImg.cols; ++col) {
            int dispItem = std::distance(smoothCosts[row][col],
                std::min_element(smoothCosts[row][col], smoothCosts[row][col] + disparityRange));
            dispMap.at<char>(row, col) = 3 * dispItem;
        }
    }

    return dispMap;
}

void SGMMatch::initCosts(string directType) {
    int rows = leftImg.rows;
    int cols = leftImg.cols;

    pixelCosts = new unsigned short **[rows];
    smoothCosts = new double **[rows];
    for (int row = 0; row < rows; ++row) {
        pixelCosts[row] = new unsigned short *[cols];
        smoothCosts[row] = new double *[cols];
        for (int col = 0; col < cols; ++col) {
            // initialize smoothed cost of all pixel to be zere
            smoothCosts[row][col] = new double [disparityRange]();

            // initialize pixel cost to be max
            pixelCosts[row][col] = new unsigned short [disparityRange];
            for (int d = 0; d < disparityRange; ++d)
                pixelCosts[row][col][d] = std::numeric_limits<unsigned short>::max();
        }
    }

    singlePathCosts = new double ***[pathNum / 2];
    for (int p = 0; p < pathNum / 2; ++p) {
        singlePathCosts[p] = new double **[rows];
        for (int row = 0; row < rows; ++row) {
            singlePathCosts[p][row] = new double *[cols];
            for (int col = 0; col < cols; ++col) {
                // initialize all single path aggregate cost to be zero
                singlePathCosts[p][row][col] = new double [disparityRange]();
            }
        }
    }

    calculatePixelCosts(directType);
}

void SGMMatch::calculatePixelCosts(string directType) {
    Mat mainMat, compareMat;
    if (directType == "left") {
        mainMat = leftImg;
        compareMat = rightImg;
    }
    else {
        mainMat = rightImg;
        compareMat = leftImg;
    }
    int rows = mainMat.rows;
    int cols = mainMat.cols;
    int halfPatch = patchSize / 2;

    for (int row = 0; row < rows - patchSize; ++row) {
        for (int col = 0; col < cols - patchSize; ++col) {
            Mat mainPatch = Mat(mainMat, Rect(col, row, patchSize, patchSize));
            for (unsigned short d = 0; d < disparityRange; ++d) {
                int compareCol = (directType == "left") ? col - d : col + d;
                if (compareCol < 0 || compareCol >= cols - patchSize)
                    break;

                Mat comparePatch = Mat(compareMat, Rect(compareCol, row, patchSize, patchSize));
                pixelCosts[row + halfPatch][col + halfPatch][d] = costSAD(mainPatch, comparePatch);
            }
        }
    }
}

unsigned short SGMMatch::costSAD(const cv::Mat& patchA, const cv::Mat& patchB) {
    return sum(abs(patchA - patchB)).val[0];
}

void SGMMatch::initPathDirection() {
    pathDirection = new short *[pathNum];
    for (short p = 0; p < pathNum; ++p) {
        pathDirection[p] = new short [2]();
    }
    /*
     * The paths direction are arranged in the following oreder, in which the
     * the even number paths are for forward calculation, while the odd number
     * paths are for backward calculation.(ori means original point)
     *
     *        10         8
     *   12    6    2    4    14
     *         0   ori   1
     *   13    7    3    5    15
     *        11         9
     *
     * The second dimension: 0 for row offset, 1 for column offset
     */
    if (pathNum >= 2) {
        pathDirection[0][0] =  0; pathDirection[0][1] = -1;
        pathDirection[1][0] =  0; pathDirection[1][1] =  1;
    }
    if (pathNum >= 4) {
        pathDirection[2][0] = -1; pathDirection[2][1] =  0;
        pathDirection[3][0] =  1; pathDirection[3][1] =  0;
    }
    if (pathNum >= 8) {
        pathDirection[4][0] = -1; pathDirection[4][1] =  1;
        pathDirection[5][0] =  1; pathDirection[5][1] =  1;
        pathDirection[6][0] = -1; pathDirection[6][1] = -1;
        pathDirection[7][0] =  1; pathDirection[7][1] = -1;
    }
    if (pathNum >= 16) {
        pathDirection[8][0] = -2; pathDirection[8][1] =  1;
        pathDirection[9][0] =  2; pathDirection[9][1] =  1;
        pathDirection[10][0]= -2; pathDirection[10][1]= -1;
        pathDirection[11][0]=  2; pathDirection[11][1]= -1;
        pathDirection[12][0]= -1; pathDirection[12][1]= -2;
        pathDirection[13][0]=  1; pathDirection[13][1]= -2;
        pathDirection[14][0]= -1; pathDirection[14][1]=  2;
        pathDirection[15][0]=  1; pathDirection[15][1]=  2;
    }
}

double SGMMatch::aggOneDireCost(int row, int col, int curDisp, short *curPathDire,
                        short curPathIdx) {
    double aggregatedCost = 0;
    aggregatedCost += pixelCosts[row][col][curDisp];

    int prevRow = row + curPathDire[0];
    int prevCol = col + curPathDire[1];
    // image border: set L(p,d) = C(b,d)
    if ((prevRow < 0 || prevRow >= leftImg.rows) ||
        (prevCol < 0 || prevCol >= leftImg.cols)) {
        singlePathCosts[curPathIdx][row][col][curDisp] += aggregatedCost;
        return singlePathCosts[curPathIdx][row][col][curDisp];
    }

    // minL(p-r, i)
    double prevMinCost = *std::min_element(singlePathCosts[curPathIdx][prevRow][prevCol],
                            singlePathCosts[curPathIdx][prevRow][prevCol] + disparityRange);
    // L(p-r, d)
    double prevCost = singlePathCosts[curPathIdx][prevRow][prevCol][curDisp];
    // L(p-r, d-1) be careful about the border
    double prevMinusCost = (curDisp - 1 >= 0) ?
                        singlePathCosts[curPathIdx][prevRow][prevCol][curDisp - 1] :
                        std::numeric_limits<double>::max();
    // L(p-r, d+1)
    double prevPlusCost = (curDisp + 1 < disparityRange) ?
                        singlePathCosts[curPathIdx][prevRow][prevCol][curDisp + 1] :
                        std::numeric_limits<double>::max();
    // L(p,d) = C(p,d)+min(L(p-r,d), L(p-r,d-1)+P1, L(p-r,d+1)+P1, minL(p-r,i)+P2)
    aggregatedCost += std::min(std::min(prevCost, prevMinusCost + SMALL_PENALTY),
                               std::min(prevPlusCost + SMALL_PENALTY, prevMinCost + LARGE_PENALTY));
    // L(p,d) -= minL(p-r, i)
    aggregatedCost -= prevMinCost;

    singlePathCosts[curPathIdx][row][col][curDisp] += aggregatedCost;
    return singlePathCosts[curPathIdx][row][col][curDisp];
}

void SGMMatch::aggAllDireCosts() {
    int rows = leftImg.rows;
    int cols = leftImg.cols;
    unsigned short pathNumPerScan = pathNum / 2;

    // forward scan cost calculation
    for (int row = 0; row < rows; ++row) {
        for (int col = 0; col < cols; ++col) {
            for (unsigned short d = 0; d < disparityRange; ++d) {
                for (unsigned short path = 0; path < pathNumPerScan; ++path) {
                    // even number path index for forward scan
                    smoothCosts[row][col][d] += aggOneDireCost(row, col, d,
                                        pathDirection[2 * path], path);
                }
            }
        }
    }

    // backward scan cost calculation
    for (int row = rows - 1; row >= 0; --row) {
        for (int col = cols - 1; col >= 0; --col) {
            for (unsigned short d = 0; d < disparityRange; ++d) {
                for (unsigned short path = 0; path < pathNumPerScan; ++path) {
                    // odd number path index for backward scan
                    smoothCosts[row][col][d] += aggOneDireCost(row, col, d,
                                        pathDirection[2 * path + 1], path);
                }
            }
        }
    }
}
