# genetic_algorithm_evolution_guided_by_LLM

## Project Overview

This project explores how to enhance the efficiency and accuracy of Genetic Algorithms (GA) by leveraging the reasoning capabilities of a Large Language Model (LLM), specifically GPT-3.5-turbo. Traditionally, GAs rely on random generation of the initial population and random mutations during the evolution process. By integrating the pre-trained knowledge and reasoning capabilities of an LLM, we aim to guide the generation of the initial population and the direction of mutations, leading to better optimization results in less time.

## How to use it

To use this project, you need to set up your OpenAI API key. Follow these steps:

1. Obtain an API key from OpenAI if you don't already have one.
2. In the `callm.py` file, locate the following line and insert your api_key:

   ```python
   #api_key = "<insert your api_key>"
