import time
from forestLibrary.forest import Forest
from forestLibrary.visual import build_forest_graph


def main():
    "Non-visual version of main.py: allows for debugging without display"

    total_generations = 100
   
    forest = Forest(size=20, initial_population=0.5, spawn_probability=0.25, species_subset=["honda", "pine", "shrub"])

    for gen in range(total_generations):
        forest.step()                                      

main()