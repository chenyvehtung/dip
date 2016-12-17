#include <opencv2/opencv.hpp>
#include <vector>
#include <string>
#include <iostream>
#include <algorithm>
#include <ctime>
#include <fstream>
#include <iomanip>

#include <dirent.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

#include "DispMatch.hpp"

using namespace cv;
using namespace std;


int getdir (string dir, vector<string> &subfolders);
void matchFn(DispMatch& dispMatch, string folderName, string costMethod);
void compareFn(ofstream& ofs, string folderName, const vector<string>& costMethods,
                string directType);


int main(int argc, char const *argv[]) {
    int disparityRange = 79;
    int patchSize = 5;

    string dir = string("images");
    vector<string> subfolders;
    vector<string> costMethods;
    costMethods.push_back("SSD"); costMethods.push_back("NCC");
    costMethods.push_back("ASW"); costMethods.push_back("SGM");
    getdir(dir, subfolders);

    /*--------------------------- Get disparity map --------------------------*/
    for (unsigned int i = 0; i < subfolders.size(); ++i) {
        cout << subfolders[i] << endl;
        Mat leftImg = imread(dir + "/" + subfolders[i] + "/view1.png", CV_LOAD_IMAGE_COLOR);
        Mat rightImg = imread(dir + "/" + subfolders[i] + "/view5.png", CV_LOAD_IMAGE_COLOR);
        //rightImg += 10;
        DispMatch dispMatch(leftImg, rightImg, disparityRange, patchSize);
        for (int j =  0; j < costMethods.size(); ++j)
            matchFn(dispMatch, subfolders[i], costMethods[j]);
    }

    /*------------ Compare the disparity map with groud truth ----------------*/
    ofstream ofs;
    // open an ouput file and write the header
    ofs.open("err_ratio.md", std::ofstream::out);
    ofs << "## The Percentage of Bad Pixels in Each of Disparity Maps" << endl << endl;
    ofs << setprecision(5);
    cout << setprecision(5); cout << left;
    ofs << "| Name | ";
    cout << setw(10) << "Name";
    for (int i = 0; i < 2; ++i) {
        string directType = (i == 0) ? "[L]" : "[R]";
        for (int j = 0; j < costMethods.size(); ++j) {
            ofs << costMethods[j] + directType << " |";
            cout << setw(10) << costMethods[j] + directType;
        }
    }
    ofs << endl; cout << endl;
    ofs << "|:-------:|";
    for (int i = 0; i < 2 * costMethods.size(); ++i)
        ofs << ":-------:|";
    ofs << endl;
    // calculate error ratio and write to the output file
    for (unsigned int i = 0; i < subfolders.size(); ++i) {
        ofs << "| " << subfolders[i] << " | ";
        cout << setw(10) << subfolders[i];
        compareFn(ofs, subfolders[i], costMethods, "left");
        compareFn(ofs, subfolders[i], costMethods, "right");
        ofs << endl; cout << endl;
    }
    ofs.close();

    return 0;
}


int getdir (string dir, vector<string> &subfolders)
{
    DIR *dp;
    struct dirent *dirp;
    if((dp  = opendir(dir.c_str())) == NULL) {
        cout << "Error(" << errno << ") opening " << dir << endl;
        return errno;
    }

    while ((dirp = readdir(dp)) != NULL) {
        string dirName = dirp->d_name;
        if (dirName == "." || dirName == ".." || dirName == "README.md"
            || dirName == ".gitignore")
            continue;
        subfolders.push_back(dirName);
    }
    sort(subfolders.begin(), subfolders.end());
    closedir(dp);
    return 0;
}

void matchFn(DispMatch& dispMatch, string folderName, string costMethod) {
    clock_t begin = clock();
    string namePrefix = "images/" + folderName + "/" + folderName + "_";

    Mat dispL = dispMatch.getDispMap("left", costMethod);
    string lImgName = namePrefix + "disp1_" + costMethod + ".png";
    imwrite(lImgName, dispL);
    cout << "Successfully saved " + lImgName << endl;

    Mat dispR = dispMatch.getDispMap("right", costMethod);
    string rImgName = namePrefix + "disp5_" + costMethod + ".png";
    imwrite(rImgName, dispR);
    cout << "Successfully saved " + rImgName << endl;

    clock_t end = clock();
    double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
    cout << "Done in " << elapsed_secs << " seconds." << endl;
}

void compareFn(ofstream& ofs, string folderName,const vector<string>& costMethods,
                string directType) {
    int methodNum = costMethods.size();
    string dispOrder = (directType == "left") ? "1" : "5";

    string gtMap = "images/" + folderName +"/disp" + dispOrder + ".png";
    Mat gtMapMat = imread(gtMap, CV_LOAD_IMAGE_GRAYSCALE) / 3;
    gtMapMat.convertTo(gtMapMat, CV_32F);

    for (unsigned short idx = 0; idx < methodNum; ++idx) {
        string curMap = "images/" + folderName + "/"
            + folderName + "_disp" + dispOrder + "_" + costMethods[idx] + ".png";
        Mat curMapMat = imread(curMap, CV_LOAD_IMAGE_GRAYSCALE) / 3;
        curMapMat.convertTo(curMapMat, CV_32F);

        Mat residualMat = abs(gtMapMat - curMapMat);
        threshold(residualMat, residualMat, 1.0, 1.0, THRESH_BINARY);
        double errRatio = sum(residualMat).val[0] / float(residualMat.rows * residualMat.cols);
        ofs << errRatio * 100 << "% | ";
        cout << setw(10) << errRatio;
    }
}
