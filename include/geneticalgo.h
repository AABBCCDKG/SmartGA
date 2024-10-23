#ifndef GENETICALGO_H
#define GENETICALGO_H

#include <vector>
#include <string>
#include "function.h"

class GeneticAlgorithm {
public:
    GeneticAlgorithm(const std::vector<std::vector<double>>& time_value, const std::vector<std::vector<double>>& desired_output, int population_size, int generations);

    void run();

private:
    std::vector<std::vector<double>> time_value;
    std::vector<std::vector<double>> desired_output;
    int population_size;
    int generations;
    std::vector<Function> population;

    void generateInitialPopulation();
    std::string generateRandomInstructions();
    void evaluatePopulation();
    void selectBestIndividuals();
    void performMutation();
    std::string generateRandomInstruction();
    Function getBestFunction();
};

#endif // GENETICALGO_H
