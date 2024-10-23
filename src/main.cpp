#include <iostream>
#include <filesystem>
#include <vector>
#include <string>
#include <algorithm>
#include "geneticalgo.h"
#include "detectobject.h"

namespace fs = std::filesystem;

std::vector<std::string> getImagePaths(const std::string& folder_path) {
    if (!fs::exists(folder_path)) {
        throw std::invalid_argument("The folder path " + folder_path + " does not exist.");
    }

    std::vector<std::string> image_files;
    for (const auto& entry : fs::directory_iterator(folder_path)) {
        if (entry.is_regular_file()) {
            auto path = entry.path().string();
            if (path.ends_with(".jpg") || path.ends_with(".png") || path.ends_with(".jpeg")) {
                image_files.push_back(path);
            }
        }
    }
    std::sort(image_files.begin(), image_files.end());
    return image_files;
}

int main() {
    try {
        std::cout << "\nStart Running\n" << std::endl;

        // std::string folder_path = "<insert your video frame folder path>";
        std::string folder_path = "<insert your video frame folder path>";
        std::vector<std::string> image_paths = getImagePaths(folder_path);

        DetectObject detector;
        auto positions_of_circles = detector.detect(image_paths, {"circle"});
        auto [desired_output, time_sequence] = detector.rowData(positions_of_circles["circle"]);

        std::vector<std::pair<std::map<std::string, std::string>, std::map<std::string, std::string>>> results;

        for (size_t i = 0; i < desired_output.size(); ++i) {
            GeneticAlgorithm row_function(time_sequence[i][0], desired_output[i][0], 5, 4);
            Function best_row_func = row_function.run();

            GeneticAlgorithm col_function(time_sequence[i][1], desired_output[i][1], 5, 4);
            Function best_col_func = col_function.run();

            results.push_back(
                {
                    {
                        {"best_function_expression", best_row_func.getExpression()},
                        {"best_function_instructions", best_row_func.getInstructions().front()},
                        {"score", std::to_string(best_row_func.evaluateSimilarity(best_row_func.calculate(time_sequence[i][0]), desired_output[i][0]))},
                        {"track_str_infor", best_row_func.getExpression()} // Assuming track is in expression (adjust accordingly)
                    },
                    {
                        {"best_function_expression", best_col_func.getExpression()},
                        {"best_function_instructions", best_col_func.getInstructions().front()},
                        {"score", std::to_string(best_col_func.evaluateSimilarity(best_col_func.calculate(time_sequence[i][1]), desired_output[i][1]))},
                        {"track_str_infor", best_col_func.getExpression()} // Assuming track is in expression (adjust accordingly)
                    }
                }
            );
        }

        // Print detailed information for each result
        for (size_t i = 0; i < results.size(); ++i) {
            std::cout << "\nDetailed information for Index " << i << ":" << std::endl;
            std::cout << "Row Function:" << std::endl;
            std::cout << "  Instructions: " << results[i].first.at("best_function_instructions") << std::endl;
            std::cout << "  Track Information:" << std::endl;
            std::cout << "    " << results[i].first.at("track_str_infor") << std::endl;

            std::cout << "\nColumn Function:" << std::endl;
            std::cout << "  Instructions: " << results[i].second.at("best_function_instructions") << std::endl;
            std::cout << "  Track Information:" << std::endl;
            std::cout << "    " << results[i].second.at("track_str_infor") << std::endl;
            std::cout << "\n" << std::string(50, '=') << "\n";
        }
    } catch (const std::exception& ex) {
        std::cerr << "Error: " << ex.what() << std::endl;
    }

    return 0;
}
