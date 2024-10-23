#include <iostream>
#include <vector>
#include <string>
#include <cmath>
#include <regex>
#include <stdexcept>
#include <sstream>
#include <random>
#include <algorithm>

class Function {
public:
    Function(const std::vector<std::string>& instructions, const std::string& expression)
        : instructions(instructions), expression(expression), score(0.0) {}

    static Function createFromInstructions(const std::string& instruction_string) {
        std::vector<std::string> instructions;
        try {
            std::istringstream iss(instruction_string);
            std::string item;
            while (std::getline(iss, item, ',')) {
                instructions.push_back(item);
            }
        } catch (...) {
            throw std::invalid_argument("Invalid instruction string format");
        }

        if (instructions.empty() || instructions[0] != "y = x") {
            throw std::invalid_argument("Instructions must start with 'y = x'");
        }

        Function instance(instructions, "");
        instance.updateExpression();
        return instance;
    }

    std::vector<double> calculate(const std::vector<double>& x_values) {
        this->x_values = x_values;
        std::vector<double> y_values;
        for (double x : x_values) {
            double y = x;
            for (size_t i = 1; i < instructions.size(); ++i) {
                const std::string& instruction = instructions[i];
                if (instruction.find("y = y + ") != std::string::npos) {
                    y += std::stod(instruction.substr(instruction.find("+") + 1));
                } else if (instruction.find("y = y - ") != std::string::npos) {
                    y -= std::stod(instruction.substr(instruction.find("-") + 1));
                } else if (instruction.find("y = y * ") != std::string::npos) {
                    y *= std::stod(instruction.substr(instruction.find("*") + 1));
                } else if (instruction.find("y = y / ") != std::string::npos) {
                    y /= std::stod(instruction.substr(instruction.find("/") + 1));
                } else if (instruction.find("y = y ^ ") != std::string::npos) {
                    y = std::pow(y, std::stod(instruction.substr(instruction.find("^") + 1)));
                } else if (instruction == "y = ln(y)") {
                    y = (y > 0) ? std::log(y) : NAN;
                } else if (instruction == "y = sin(y)") {
                    y = std::sin(y);
                } else if (instruction == "y = cos(y)") {
                    y = std::cos(y);
                } else {
                    y = std::stod(instruction.substr(instruction.find("=") + 1));
                }
            }
            y_values.push_back(y);
        }
        return y_values;
    }

    double evaluateSimilarity(const std::vector<double>& calculated_values, const std::vector<double>& desired_output) {
        if (calculated_values.size() != desired_output.size()) {
            throw std::invalid_argument("Calculated values and desired output must have the same length");
        }
        double squared_diff_sum = 0.0;
        double abs_diff_sum = 0.0;
        for (size_t i = 0; i < calculated_values.size(); ++i) {
            double diff = calculated_values[i] - desired_output[i];
            squared_diff_sum += diff * diff;
            abs_diff_sum += std::abs(diff);
        }
        double rmse = std::sqrt(squared_diff_sum / calculated_values.size());
        double mae = abs_diff_sum / calculated_values.size();
        double similarity_score = 1.0 / (1.0 + rmse);
        score = similarity_score;
        return similarity_score;
    }

    void addInstruction(size_t index, const std::string& new_instruction) {
        if (index < 1 || index > instructions.size()) {
            throw std::out_of_range("Instruction index out of range");
        }
        instructions.insert(instructions.begin() + index, formatInstruction(new_instruction));
        updateExpression();
    }

    void removeInstruction(size_t index) {
        if (index < 1 || index >= instructions.size()) {
            throw std::out_of_range("Instruction index out of range");
        }
        instructions.erase(instructions.begin() + index);
        updateExpression();
    }

    void substituteInstruction(size_t index, const std::string& new_instruction) {
        if (index < 1 || index >= instructions.size()) {
            throw std::out_of_range("Instruction index out of range");
        }
        instructions[index] = formatInstruction(new_instruction);
        updateExpression();
    }

private:
    std::vector<std::string> instructions;
    std::vector<double> x_values;
    std::string expression;
    double score;

    std::string formatInstruction(const std::string& instruction) {
        std::string formatted = instruction;
        formatted = std::regex_replace(formatted, std::regex("\s*=\s*"), " = ");
        formatted = std::regex_replace(formatted, std::regex("\s*\+\s*"), " + ");
        formatted = std::regex_replace(formatted, std::regex("\s*-\s*"), " - ");
        formatted = std::regex_replace(formatted, std::regex("\s*\*\s*"), " * ");
        formatted = std::regex_replace(formatted, std::regex("\s*/\s*"), " / ");
        formatted = std::regex_replace(formatted, std::regex("\s*\^\s*"), " ^ ");
        formatted = std::regex_replace(formatted, std::regex("\b(ln|sin|cos)\s*\(\s*(.*?)\s*\)"), "$1($2)");
        return formatted;
    }

    void updateExpression() {
        expression = "x";
        for (size_t i = 1; i < instructions.size(); ++i) {
            const std::string& instruction = instructions[i];
            if (instruction.find("y = y + ") != std::string::npos) {
                expression = "(" + expression + " + " + instruction.substr(instruction.find("+") + 1) + ")";
            } else if (instruction.find("y = y - ") != std::string::npos) {
                expression = "(" + expression + " - " + instruction.substr(instruction.find("-") + 1) + ")";
            } else if (instruction.find("y = y * ") != std::string::npos) {
                expression = "(" + expression + " * " + instruction.substr(instruction.find("*") + 1) + ")";
            } else if (instruction.find("y = y / ") != std::string::npos) {
                expression = "(" + expression + " / " + instruction.substr(instruction.find("/") + 1) + ")";
            } else if (instruction.find("y = y ^ ") != std::string::npos) {
                expression = "(" + expression + ")^" + instruction.substr(instruction.find("^") + 1);
            } else if (instruction == "y = ln(y)") {
                expression = "ln(" + expression + ")";
            } else if (instruction == "y = sin(y)") {
                expression = "sin(" + expression + ")";
            } else if (instruction == "y = cos(y)") {
                expression = "cos(" + expression + ")";
            }
        }
    }
};

int main() {
    try {
        std::string instructions = "y = x, y = y + 5, y = y * 3";
        Function func = Function::createFromInstructions(instructions);
        std::vector<double> x_values = {1, 2, 3, 4};
        std::vector<double> y_values = func.calculate(x_values);

        for (double y : y_values) {
            std::cout << y << " ";
        }
        std::cout << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }

    return 0;
}
