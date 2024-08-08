import os
import pandas as pd
from geneticalgo import GeneticAlgorithm
from detectobject import DetectObject

def get_image_paths(folder_path):
        if not os.path.exists(folder_path):
            raise ValueError(f"The folder path {folder_path} does not exist.")
        
        all_files = os.listdir(folder_path)
        image_files = [f for f in all_files if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.jpeg')]
        image_files.sort()
        image_paths = [os.path.join(folder_path, f) for f in image_files]
        
        return image_paths
print("\nStart Running\n")

#folder_path = '<insert your video frame folder path>'
image_paths = get_image_paths(folder_path)

detector = DetectObject()

positions_of_circles = detector.detect(image_paths, ['circle'])
desired_output, time_sequence = detector.row_data(positions_of_circles['circle'])

results = []

for i in range(len(desired_output)):
    rowfunction =GeneticAlgorithm(time_value = time_sequence[i][0], desired_output = desired_output[i][0], population_size = 5, generations = 4)
    best_row_func = rowfunction.run() 
    colfunction = GeneticAlgorithm(time_value = time_sequence[i][1], desired_output = desired_output[i][1], population_size = 5, generations = 4)
    best_col_func = colfunction.run()
    results.append(
        [
            {
            "best_function_expression": best_row_func.expression,
            "best_function_instructions": best_row_func.instructions,
            "score": best_row_func.evaluate_similarity(best_row_func.calculate(time_sequence[i][0]), desired_output[i][0])["similarity_score"],
            "track_str_infor": best_row_func.track
            },
            {
            "best_function_expression": best_col_func.expression,
            "best_function_instructions": best_col_func.instructions,
            "score": best_col_func.evaluate_similarity(best_col_func.calculate(time_sequence[i][1]), desired_output[i][1])["similarity_score"],
            "track_str_infor": best_col_func.track
            }
        ]
    )


# Print detailed information for each result
for i, result in enumerate(results):
    print(f"\nDetailed information for Index {i}:")
    print("Row Function:")
    print(f"  Instructions: {result[0]['best_function_instructions']}")
    print(f"  Track Information:")
    for track in result[0]['track_str_infor']:
        print(f"    {track}")
        
    print("\nColumn Function:")
    print(f"  Instructions: {result[1]['best_function_instructions']}")
    print(f"  Track Information:")
    for track in result[1]['track_str_infor']:
        print(f"    {track}")
    print("\n" + "="*50)
    
