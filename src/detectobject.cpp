#include <opencv2/opencv.hpp>
#include <stdio.h>
#include <vector>
#include <map>
#include <string>
#include <algorithm>
#include <filesystem>
#include <numeric>
#include <cmath>
#include <tuple>
#include <stdexcept>

namespace fs = std::filesystem;

class DetectObject {
public:
    DetectObject() {
        detectors["circle"] = &DetectObject::detectCircles;
    }

    static std::vector<std::vector<std::vector<float>>> transformData(const std::vector<std::vector<std::pair<int, int>>>& input_data) {
        std::vector<std::vector<std::vector<float>>> result;
        for (const auto& sublist : input_data) {
            std::vector<float> x_values;
            std::vector<float> y_values;
            for (const auto& t : sublist) {
                x_values.push_back(static_cast<float>(t.first));
                y_values.push_back(static_cast<float>(t.second));
            }
            result.push_back({x_values, y_values});
        }
        return result;
    }

    std::map<std::string, std::vector<std::vector<std::pair<int, int>>>> detect(const std::vector<std::string>& image_paths, const std::vector<std::string>& shape_types) {
        std::map<std::string, std::vector<std::vector<std::pair<int, int>>>> results;
        for (const auto& path : image_paths) {
            auto image_results = detectShapesInImage(path, shape_types);
            for (const auto& shape : shape_types) {
                results[shape].push_back(image_results[shape]);
            }
        }
        return results;
    }

private:
    using DetectorFunction = std::vector<std::pair<int, int>> (DetectObject::*)(const std::string&);
    std::map<std::string, DetectorFunction> detectors;

    std::map<std::string, std::vector<std::pair<int, int>>> detectShapesInImage(const std::string& image_path, const std::vector<std::string>& shape_types) {
        std::map<std::string, std::vector<std::pair<int, int>>> results;
        for (const auto& shape : shape_types) {
            if (detectors.find(shape) == detectors.end()) {
                throw std::invalid_argument("Unsupported shape type: " + shape);
            }
            results[shape] = (this->*detectors[shape])(image_path);
        }
        return results;
    }

    std::vector<std::pair<int, int>> detectCircles(const std::string& image_path) {
        cv::Mat image = cv::imread(image_path);
        if (image.empty()) {
            printf("Could not open or find the image: %s\n", image_path.c_str());
            return {};
        }

        cv::Mat gray;
        cv::cvtColor(image, gray, cv::COLOR_BGR2GRAY);
        cv::GaussianBlur(gray, gray, cv::Size(9, 9), 2);

        std::vector<cv::Vec3f> circles;
        cv::HoughCircles(gray, circles, cv::HOUGH_GRADIENT, 1.2, 30, 50, 30, 15, 50);

        std::vector<std::pair<int, int>> circle_centers;
        for (const auto& circle : circles) {
            circle_centers.emplace_back(static_cast<int>(circle[0]), static_cast<int>(circle[1]));
        }
        return circle_centers;
    }
};

std::vector<std::string> getImagePaths(const std::string& folder_path) {
    if (!fs::exists(folder_path)) {
        throw std::invalid_argument("The folder path " + folder_path + " does not exist.");
    }

    std::vector<std::string> image_paths;
    for (const auto& entry : fs::directory_iterator(folder_path)) {
        if (entry.is_regular_file()) {
            auto path = entry.path().string();
            if (path.ends_with(".jpg") || path.ends_with(".png") || path.ends_with(".jpeg")) {
                image_paths.push_back(path);
            }
        }
    }
    std::sort(image_paths.begin(), image_paths.end());
    return image_paths;
}

int main() {
    try {
        std::string folder_path = "/Users/dong/Desktop/video/withballframes";
        auto image_paths = getImagePaths(folder_path);

        DetectObject detector;
        auto positions_of_circles = detector.detect(image_paths, {"circle"});

        // Print detected circle positions
        for (const auto& frame : positions_of_circles["circle"]) {
            for (const auto& position : frame) {
                printf("(%d, %d) ", position.first, position.second);
            }
            printf("\n");
        }
    } catch (const std::exception& ex) {
        printf("Error: %s\n", ex.what());
    }

    return 0;
}
