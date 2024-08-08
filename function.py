import random
import math
import re
import ast
import sys


class Function:
    def __init__(self, instructions, expression):
        self.instructions = instructions
        self.expression = expression
        self.x_values = []
        self.track = []
        self.score = 0
        self.desired_output = []
        
    @classmethod
    def create_from_instructions(cls, instruction_string):
        try:
            instructions = ast.literal_eval(instruction_string)
        except:
            raise ValueError("Invalid instruction string format")

        if not isinstance(instructions, list) or not all(isinstance(item, str) for item in instructions):
            raise ValueError("Instructions must be a list of strings")

        if not instructions or instructions[0] != "y = x":
            raise ValueError("Instructions must start with 'y = x'")
        
        instance = cls(instructions, "")
        instance.update_expression()
        return instance
    
    def calculate(self, x_values):
        self.x_values = x_values
        y_values = []
        self.instructions = [self.format_instruction(instruction) for instruction in self.instructions]
        for x in x_values:
            y = x
            for instruction in self.instructions[1:]:  # Skip the first 'y = x'
                if 'y = y + ' in instruction:
                    y += float(instruction.split('+')[1])
                elif 'y = y - ' in instruction:
                    y -= float(instruction.split('-')[1])
                elif 'y = y * ' in instruction:
                    y *= float(instruction.split('*')[1])
                elif 'y = y / ' in instruction:
                    y /= float(instruction.split('/')[1])
                elif 'y = y ^ ' in instruction:
                    y = y ** float(instruction.split('^')[1])
                elif 'y = ln(y)' in instruction:
                    y = math.log(y) if y > 0 else float('nan')
                elif 'y = sin(y)' in instruction:
                    y = math.sin(y)
                elif 'y = cos(y)' in instruction:
                    y = math.cos(y)
                else:
                    y = float(instruction.split('=')[1])
            y_values.append(y)
        return y_values

    def evaluate_similarity(self, calculated_values, desired_output): #  (less similar) 0 < similarity_score < 1(most similar)
        self.desired_output = desired_output  
        squared_diff_sum = sum((calc - desired) ** 2 for calc, desired in zip(calculated_values, desired_output))
        rmse = math.sqrt(squared_diff_sum / len(calculated_values))
        
        abs_diff_sum = sum(abs(calc - desired) for calc, desired in zip(calculated_values, desired_output))
        mae = abs_diff_sum / len(calculated_values)
        
        similarity_score = 1 / (1 + rmse)
        self.score = similarity_score
        return {
            "rmse": rmse,
            "mae": mae,
            "similarity_score": similarity_score
        }
    
    def add_instruction(self, index, new_instruction):
        old_expression = self.expression
        old_score = self.score

        new_instruction = self.format_instruction(new_instruction)
        if index < 1 or index > len(self.instructions):
            raise IndexError("Instruction index out of range")
        self.instructions.insert(index, new_instruction)
        self.update_expression()
        
        new_score = self.evaluate_similarity(self.calculate(self.x_values), self.desired_output)["similarity_score"]
        score_change = "decreased" if new_score < old_score else "remained the same" if new_score == old_score else "increased"
        self.track.append(f"Modified {old_expression} to {self.expression} by adding {new_instruction} to previous index: {index}, similarity_score {score_change} from {old_score:.8f} to {new_score:.8f}")
    
        
    def remove_instruction(self, index):
        old_expression = self.expression
        old_score = self.score
        
        if index < 1 or index >= len(self.instructions):
            raise IndexError("Instruction index out of range")
        removed_instruction = self.instructions.pop(index)
        self.update_expression()
        
        new_score = self.evaluate_similarity(self.calculate(self.x_values), self.desired_output)["similarity_score"]
        score_change = "decreased" if new_score < old_score else "remained the same" if new_score == old_score else "increased"
        self.track.append(f"Modified {old_expression} to {self.expression} by removing {removed_instruction} from previous index: {index}, similarity_score {score_change} from {old_score:.8f} to {new_score:.8f}")
    
    def add_track(self, score, result, instruction, expression, desired_output):
        track = f"The x values are {self.x_values}; \\the y values are {result};\\ the desired_output is {desired_output};\\ the initial function instruction is {instruction};\\ and corresponding expression is {expression};\\ the similarity score is {score}"
        self.track.append(track)
    
    def substitute_instruction(self, index, new_instruction):
        old_expression = self.expression
        old_score = self.score
        
        new_instruction = self.format_instruction(new_instruction)
        if index < 1 or index >= len(self.instructions):
            raise IndexError("Instruction index out of range or attempt to modify initial instruction")
        old_instruction = self.instructions[index]
        self.instructions[index] = new_instruction
        self.update_expression()
        
        new_score = self.evaluate_similarity(self.calculate(self.x_values), self.desired_output)["similarity_score"]
        score_change = "decreased" if new_score < old_score else "remained the same" if new_score == old_score else "increased"
        self.track.append(f"Modified {old_expression} to {self.expression} by changing {old_instruction} to {new_instruction} at the index: {index}, similarity_score {score_change} from {old_score:.8f} to {new_score:.8f}")


    def format_instruction(self, instruction):
        instruction = instruction.strip()
        instruction = re.sub(r'\s*=\s*', ' = ', instruction)
        instruction = re.sub(r'\s*\+\s*', ' + ', instruction)
        instruction = re.sub(r'\s*-\s*', ' - ', instruction)
        instruction = re.sub(r'\s*\*\s*', ' * ', instruction)
        instruction = re.sub(r'\s*/\s*', ' / ', instruction)
        instruction = re.sub(r'\s*\^\s*', ' ^ ', instruction)
        instruction = re.sub(r'\b(ln|sin|cos)\s*\(\s*(.*?)\s*\)', r'\1(\2)', instruction)
        return instruction
    
    def update_expression(self):
        expression = 'x'
        for instruction in self.instructions[1:]:
            if 'y = y + ' in instruction:
                value = instruction.split('+')[1].strip()
                expression = f'({expression} + {value})'
            elif 'y = y - ' in instruction:
                value = instruction.split('-')[1].strip()
                expression = f'({expression} - {value})'
            elif 'y = y * ' in instruction:
                value = instruction.split('*')[1].strip()
                expression = f'({expression} * {value})'
            elif 'y = y / ' in instruction:
                value = instruction.split('/')[1].strip()
                expression = f'({expression} / {value})'
            elif 'y = y ^ ' in instruction:
                value = instruction.split('^')[1].strip()
                expression = f'({expression})^{value}'
            elif 'y = ln(y)' in instruction:
                expression = f'ln({expression})'
            elif 'y = log(y)' in instruction:
                expression = f'log({expression})'
            elif 'y = sin(y)' in instruction:
                expression = f'sin({expression})'
            elif 'y = cos(y)' in instruction:
                expression = f'cos({expression})'
            elif 'y = ' in instruction and ' - y' in instruction:
                value = instruction.split('=')[1].split('-')[0].strip()
                expression = f'({value} - {expression})'
        self.expression = expression
        
def generate_random_equation():
    operations = ['add', 'subtract', 'multiply', 'divide', 'power', 'ln', 'sin', 'cos', 'log']
    steps = random.randint(2, 5)
    instructions = ['y = x']
    expression = 'x'
    
    for _ in range(steps):
        op = random.choice(operations)
        if op in ['add', 'subtract', 'multiply', 'divide']:
            value = random.randint(1, 10)
            if op == 'add':
                instructions.append(f'y = y + {value}')
                expression = f'({expression} + {value})'
            elif op == 'subtract':
                instructions.append(f'y = y - {value}')
                expression = f'({expression} - {value})'
            elif op == 'multiply':
                instructions.append(f'y = y * {value}')
                expression = f'({expression} * {value})'
            else:
                instructions.append(f'y = y / {value}')
                expression = f'({expression} / {value})'
        elif op == 'power':
            power = random.randint(2, 4)
            instructions.append(f'y = y^{power}')
            expression = f'({expression})^{power}'
        elif op == 'ln':
            instructions.append('y = ln(y)')
            expression = f'ln({expression})'
        elif op == 'sin':
            instructions.append('y = sin(y)')
            expression = f'sin({expression})'
        else:  # cos
            instructions.append('y = cos(y)')
            expression = f'cos({expression})'
    
    return Function(instructions, expression)

time_value = [
    [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]], 
    [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]], 
    [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]], 
    [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]]
]

desired_output = [
    [[195.0, 207.0, 1073.0, 1073.0, 238.0, 1072.0, 1073.0, 267.0, 1072.0, 1072.0, 1072.0, 305.0], 
        [447.0, 443.0, 218.0, 218.0, 435.0, 217.0, 218.0, 428.0, 218.0, 218.0, 218.0, 417.0]], 
    [[1073.0, 1073.0, 218.0, 229.0, 1073.0, 247.0, 257.0, 1073.0, 277.0, 286.0, 296.0, 1072.0], 
        [219.0, 218.0, 440.0, 437.0, 218.0, 433.0, 430.0, 218.0, 425.0, 423.0, 419.0, 218.0]], 
    [[375.0, 374.0, 374.0, 374.0, 373.0, 373.0, 374.0, 374.0, 374.0, 374.0, 374.0, 374.0], 
        [219.0, 218.0, 218.0, 218.0, 218.0, 218.0, 218.0, 218.0, 218.0, 218.0, 218.0, 218.0]], 
    [[1075.0, 1073.0, 1072.0, 1072.0, 1072.0, 1072.0, 1072.0, 1075.0, 1072.0, 1072.0, 1072.0, 1072.0], 
        [67.0, 68.0, 70.0, 68.0, 68.0, 70.0, 70.0, 67.0, 68.0, 68.0, 68.0, 68.0]]
]


results = []
for i in range(len(time_value)):
    row_function = generate_random_equation()
    row_function_expression = row_function.expression
    row_function_result = row_function.calculate(time_value[i][0])
    row_function_similarity = row_function.evaluate_similarity(row_function_result, desired_output[i][0])
    
    col_function = generate_random_equation()
    col_function_expression = col_function.expression
    col_function_result = col_function.calculate(time_value[i][1])
    col_function_similarity = col_function.evaluate_similarity(col_function_result, desired_output[i][1])
    
    results.append({
        "row_function_result": row_function_result,
        "row_function_expression": row_function_expression,
        "row_function_similarity": row_function_similarity,
        "col_function_result": col_function_result,
        "col_function_expression": col_function_expression,
        "col_function_similarity": col_function_similarity
    })
