#ifndef FUNCTION_H
#define FUNCTION_H

#include <vector>
#include <string>
#include <cmath>
#include <regex>
#include <stdexcept>
#include <sstream>

class Function {
public:
    Function(const std::vector<std::string>& instructions, const std::string& expression);

    static Function createFromInstructions(const std::string& instruction_string);

    std::vector<double> calculate(const std::vector<double>& x_values);

    double evaluateSimilarity(const std::vector<double>& calculated_values, const std::vector<double>& desired_output);

    void substituteInstruction(size_t index, const std::string& new_instruction);

    double getScore() const;

    const std::string& getExpression() const;

    const std::vector<std::string>& getInstructions() const;

private:
    std::vector<std::string> instructions;
    std::string expression;
    double score;

    std::string formatInstruction(const std::string& instruction);
    void updateExpression();
};

#endif // FUNCTION_H
