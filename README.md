# SmartGA
Check out this [link](https://github.com/AABBCCDKG/SmartGA_Python) for python-based SmartGA which is integrated with ChatGPT-3.5-turbo to generate the initial population and perform reasoning-based mutation.
## Overview
This project focuses on optimizing a Genetic Algorithm implemented in C++ to efficiently discover mathematical formulas based on variable values. The main features of the project include decomposing formulas into independently modifiable components, utilizing an instruction set, and improving mutation efficiency through multi-threading. The project also integrates OpenCV for object detection tasks.

## Features
- **Genetic Algorithm for Formula Discovery**: Optimized a Genetic Algorithm in C++ to efficiently find mathematical formulas from given variable values.
- **Instruction Set-Based Decomposition**: Utilized an instruction set to decompose mathematical formulas into array elements, allowing each element to be independently modified. This enables O(1) time complexity for locating the components that need modification.
- **Multi-threaded Mutation Mechanism**: Implemented a mutation mechanism that utilizes evolutionary data to mutate mathematical formulas, with optimization through multi-threading. This increased function fitting efficiency by 30%.

## Project Structure
- **`include/`**: Contains all the header files (`.h`) for the project.
- **`src/`**: Contains the implementation files (`.cpp`), including:
  - `detectobject.cpp`: Handles object detection using OpenCV.
  - `geneticalgo.cpp`: Implements the Genetic Algorithm logic.
  - `main.cpp`: The main entry point of the project.
- **`build/`**: Stores compiled files and executable.
