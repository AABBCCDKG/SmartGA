import random
from function import Function, generate_random_equation
import tabulate
from callm import llm_for_mutation, llm_for_initial_generation
import re

class GeneticAlgorithm:
    def __init__(self, time_value, desired_output, population_size, generations):
        self.time_value = time_value
        self.desired_output = desired_output
        self.population_size = population_size
        self.generations = generations
        self.population = []
    
    
    #def crossover(self, parent1, parent2):
        #cut = random.randint(1, min(len(parent1.instructions), len(parent2.instructions)) - 1) # 修改交叉点的选择
        #child1_instructions = parent1.instructions[:cut] + parent2.instructions[cut:]
        #child2_instructions = parent2.instructions[:cut] + parent1.instructions[cut:]
        #return Function(child1_instructions, ""), Function(child2_instructions, "")

    def extract_index(self,input_string):
        """
        This function extracts the content between '(' and ',' in the input string.
        
        :param input_string: The string to be processed.
        :return: The extracted content.
        """
        pattern = r'\(([^,]+),'
        match = re.search(pattern, input_string)
        if match:
            return float(match.group(1))
        else:
            return None
        
    def mutate(self, function): # call_chatgpt, 输入方程对象，返回修改指令，
        print("\nMutation:\n")
        order = "function." + llm_for_mutation(str(function.track))
        order = order.replace('x', 'y')
        index = self.extract_index(order)
        def deal_with_index(function, order, index, max_attempts=100, attempt=0):
            if attempt >= max_attempts:
                return None
            
            if 'add_instruction' in order:
                if 0 < index <= len(function.instructions):
                    return order
            else:
                if 0 < index < len(function.instructions):
                    return order
            
            new_order = "function." + llm_for_mutation(str(function.track))
            new_order = new_order.replace('x', 'y')
            new_index = self.extract_index(new_order)
            
            return deal_with_index(function, new_order, new_index, max_attempts, attempt + 1)

        order = deal_with_index(function, order, index)
        if order is None:
            print("Failed to generate a valid order.")
        
        print("\norder: " )
        print(order)
        exec(order)
        function.update_expression()
        print(function.instructions)
        print(function.track)
        #function.update_expression()

    def run(self):
        # 生成初始种群
        population = [llm_for_initial_generation(str(self.desired_output)) for _ in range(self.population_size)]
        for instruction in population:
            #print("instruction: ")
            #print(instruction)
            func = Function.create_from_instructions(instruction)
            self.population.append(func)
        #print(f"Initial population for a single function: {[func.expression for func in population]}")
        for generation in range(self.generations):
            print(f'\nGeneration {generation}')
            scores = []
            for func in self.population:
                #print(f"\nEvaluating function: {func.expression}")
                result = func.calculate(self.time_value)
                #print(f"Calculation result: {result}")
                #print(f"Desired output: {self.desired_output}")
            
                score = func.evaluate_similarity(result, self.desired_output)
                #print(f"Similarity score: {score}")               
                scores.append((score, func))
                if generation == 0:
                    func.add_track(str(score['similarity_score']), result, func.instructions, func.expression, self.desired_output)
        #print("\nScores: ", [(score, func.expression) for score, func in scores])
        
            # 按 'similarity_score' 排序
            print("\nScores: ", [(score, func.expression) for score, func in scores])
            scores.sort(reverse=True, key=lambda x: x[0]["similarity_score"])
            best_functions = [func for _, func in scores[:self.population_size // 2]] #取前一半的函数
            print(f"\nBest functions: {[func.expression for func in best_functions]}\n")
        # 生成新的种群
            temp_population = best_functions.copy()
            new_population = best_functions.copy()
            for new_func in temp_population:
                temp_func = new_func
                self.mutate(new_func)
                new_population.append(new_func)
                self.mutate(temp_func)
                new_population.append(temp_func)
            self.population = new_population
            #print(f"New population: {[func.expression for func in population]}")
    
        # 找到最佳函数
        best_function = max(self.population, key=lambda func:
            func.evaluate_similarity(func.calculate(self.time_value), self.desired_output)['similarity_score'])
        
        #print(f"\nBest function found: {best_function.expression}")
        #print(f"Best function score: {best_function.evaluate_similarity(best_function.calculate(self.time_value), self.desired_output)["similarity_score"]}")
        return best_function
    