from openai import OpenAI

client = OpenAI(
    #api_key = "<insert your api_key>",
)
def llm_for_mutation(trackinfo):
    assistant_info = """
        Mutation Operations for Symbolic Regression:

        We represent mathematical functions using an instruction set. For example:
        y = (x + 3)^2 is represented as ["y = x", "y = y + 3", "y = y^2"]

        Available mutation operations:
        1. add_instruction(self, index, new_instruction)  for add_instruction, 1 <= index <= len(instructions)
        2. remove_instruction(self, index)
        3. substitute_instruction(self, index, new_instruction) for substitute_instruction, 1 <= index < len(instructions)

        Instruction Set Rules:
        - (Critical!) Each instruction MUST follow the format: y = f(y) where f(y) ONLY contains y, not x.
        - f(y) must contain only one basic operation from:
            operations = ['add', 'subtract', 'multiply', 'divide', 'power', 'ln', 'sin', 'cos', 'log']
        - Example of valid instruction: "y = cos(y)"
        - Example of invalid instruction: "y = cos(y + 1)" (contains two operations)

        Task:
        Based on inference results, determine and return ONLY the appropriate mutation operation along with its specific parameters. Do not include any explanations or additional text.

        Valid response format:
        add_instruction(index, new_instruction)
        remove_instruction(index)
        substitute_instruction(index, new_instruction)

        Example responses:
        add_instruction(2, 'y = y + 3')
        remove_instruction(1)
        substitute_instruction(2, 'y = 3 * y')

        Example:
        Changing ["y = x", "y = y + 3", "y = y^2"] to ["y = x", "y = 3 * y", "y = y^2"]
        transforms the expression from y = (x + 3)^2 to y = (3 * y)^2
        """
    completion = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "You will be provided with a series of tracking information through genetic algorithms that modify the structure of a function, including the mutation operations of each generation and their corresponding scores(similarity_score). Based on this tracking information, you need to predict the direction of the next mutation (The closer the value of similarity_score is to 1, the more correct the direction of mutation is. I need a function whose score is extremely close to 1)."},
            {"role": "user", "content": "The tracking information is as follows: " + trackinfo},
            {"role": "assistant", "content": assistant_info}, 
        ],
    )
    response = completion.choices[0].message.content
    return response

def llm_for_initial_generation(list_of_numbers):
    assistant_info = """
        Symbolic Regression Task:
        
        Input: A list of numbers where the index is the independent variable (x) and the value is the dependent variable (y).

        Task: Generate a single instruction set that represents the function relating x to y.

        Instruction Set Format:
        - (Important!)First element MUST be "y = x". 
        - (Important!)If the function is constant, the first element should still be "y = x", and the second element must be "y = constant". For example: ["y = x", "y = 3"]
        - (Critical!) All subsequent elements MUST follow the format "y = f(y)" where f(y) ONLY contains y, not x.
        - f(y) must contain only ONE operation from: ['add', 'subtract', 'multiply', 'divide', 'power', 'ln', 'sin', 'cos', 'log']
        - Example: ["y = x", "y = y + 3", "y = y^2"] represents y = (x + 3)^2

        Valid instruction: "y = cos(y)"
        Invalid instruction: "y = cos(y + 1)" (contains two operations)

        Output: Provide ONLY the instruction set list, without any additional text or explanation.

        Example output:
        ["y = x", "y = y + 3", "y = y^2"]

        Note: Your response should contain nothing but a single list representing the function.
        """
    completion = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "You will be provided with a list of numbers where the independent variable is the index and the dependent variable is the corresponding value at that index. Based on this information, you need to generate a function that fits the given data."},
            {"role": "user", "content": "The list of numbers is: " + list_of_numbers},
            {"role": "assistant", "content": assistant_info}, 
        ],
    )
    response = completion.choices[0].message.content
    return response
