#include <iostream>
#include <vector>
#include <string>
#include <regex>
#include <stdexcept>
#include <random>
#include <algorithm>
#include <cmath>
#include <sstream>
#include "function.h"

class GeneticAlgorithm {
public:
    GeneticAlgorithm(const std::vector<std::vector<double>>& time_value, const std::vector<std::vector<double>>& desired_output, int population_size, int generations)
        : time_value(time_value), desired_output(desired_output), population_size(population_size), generations(generations) {}

    void run() {
        generateInitialPopulation();
        for (int generation = 0; generation < generations; ++generation) {
            std::cout << "\nGeneration " << generation << "\n";
            evaluatePopulation();
            selectBestIndividuals();
            performMutation();
        }
        Function best_function = getBestFunction();
        std::cout << "\nBest Function: " << best_function.getExpression() << "\n";
    }

private:
    std::vector<std::vector<double>> time_value;
    std::vector<std::vector<double>> desired_output;
    int population_size;
    int generations;
    std::vector<Function> population;

    void generateInitialPopulation() {
        for (int i = 0; i < population_size; ++i) {
            std::string instructions = generateRandomInstructions();
            Function func = Function::createFromInstructions(instructions);
            population.push_back(func);
        }
    }

    std::string generateRandomInstructions() {
        static const std::vector<std::string> operations = {"y = y + 1", "y = y - 1", "y = y * 2", "y = y / 2", "y = sin(y)", "y = cos(y)", "y = ln(y)"};
        std::string instructions = "y = x";
        int steps = rand() % 4 + 2; // Between 2 to 5 instructions
        for (int i = 0; i < steps; ++i) {
            instructions += ", " + operations[rand() % operations.size()];
        }
        return instructions;
    }

    void evaluatePopulation() {
        for (Function& func : population) {
            std::vector<double> results = func.calculate(time_value[0]);
            double score = func.evaluateSimilarity(results, desired_output[0]);
            std::cout << "Function: " << func.getExpression() << ", Similarity Score: " << score << "\n";
        }
    }

    void selectBestIndividuals() {
        std::sort(population.begin(), population.end(), [](const Function& a, const Function& b) {
            return a.getScore() > b.getScore();
        });
        population.resize(population_size / 2); // Keep top 50%
    }

    void performMutation() {
        int original_size = population.size();
        for (int i = 0; i < original_size; ++i) {
            Function mutated_function = population[i];
            int index = rand() % (mutated_function.getInstructions().size() - 1) + 1;
            std::string new_instruction = generateRandomInstruction();
            mutated_function.substituteInstruction(index, new_instruction);
            population.push_back(mutated_function);
        }
    }

    std::string generateRandomInstruction() {
        static const std::vector<std::string> operations = {"y = y + 1", "y = y - 1", "y = y * 2", "y = y / 2", "y = sin(y)", "y = cos(y)", "y = ln(y)"};
        return operations[rand() % operations.size()];
    }

    Function getBestFunction() {
        return *std::max_element(population.begin(), population.end(), [](const Function& a, const Function& b) {
            return a.getScore() < b.getScore();
        });
    }
};

int main() {
    std::vector<std::vector<double>> time_value = {{1, 2, 3, 4, 5}};
    std::vector<std::vector<double>> desired_output = {{2, 4, 6, 8, 10}};
    GeneticAlgorithm ga(time_value, desired_output, 10, 5);
    ga.run();
    return 0;
}
