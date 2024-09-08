# SmartGA

## Project Overview

This project enhances the Genetic Algorithm (GA) for fitting the position function of objects, primarily circles, in video frames. By leveraging the reasoning capabilities of a Large Language Model (LLM) like ChatGPT-3.5-turbo, we aim to improve the precision and efficiency of the GA. Traditional genetic algorithms typically rely on random generation of the initial population and random mutations. By incorporating the LLM's knowledge and inference abilities, we can generate more accurate initial populations and guide the direction of mutations, leading to better fitting results in less time.


## How to use it

To use this project, you need to set up your OpenAI API key. Follow these steps:

1. Obtain an API key from OpenAI if you don't already have one.
2. In the `callm.py` file, locate the following line and insert your api_key:

   ```python
   #api_key = "<insert your api_key>"
3. In the `main.py` file, locate the following line and insert your video frame folder path:

   ```python
   #folder_path = '<insert your video frame folder path>'

5. Run the `main.py` file.
