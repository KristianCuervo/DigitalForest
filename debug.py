import time
from forestLibrary.forest import Forest
from forestLibrary.visual import build_forest_graph


def main():
    "Non-visual version of main.py: allows for debugging without display"

    total_generations = 100
   
    forest = Forest(size=5, initial_population=1.0, spawn_probability=0.1, species_subset=["honda"])

    for gen in range(total_generations):
        forest.step()                                      

main()