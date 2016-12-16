#include <opencv2/opencv.hpp>
#include <vector>
#include <string>
#include <iostream>
#include <algorithm>
#include <ctime>

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


int main(int argc, char const *argv[]) {
    int disparityRange = 79;
    int patchSize = 5;

    string dir = string("images");
    vector<string> subfolders;
    getdir(dir, subfolders);
    for (unsigned int i = 0; i < subfolders.size(); ++i) {
        cout << subfolders[i] << endl;
        Mat leftImg = imread(dir + "/" + subfolders[i] + "/view1.png", CV_LOAD_IMAGE_COLOR);
        Mat rightImg = imread(dir + "/" + subfolders[i] + "/view5.png", CV_LOAD_IMAGE_COLOR);
        //rightImg += 10;
        DispMatch dispMatch(leftImg, rightImg, disparityRange, patchSize);

        matchFn(dispMatch, subfolders[i], "SSD");
        matchFn(dispMatch, subfolders[i], "NCC");
        matchFn(dispMatch, subfolders[i], "ASW");
        matchFn(dispMatch, subfolders[i], "SGM");
    }
    //namedWindow("Display Image", WINDOW_AUTOSIZE);
    //imshow("Display Image", dispASSD);
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
