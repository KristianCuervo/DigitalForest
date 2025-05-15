import time
from forestLibrary.forest import Forest
from forestLibrary.visual import build_tree
from forestLibrary.analyser import Analyse
from pygel3d import gl_display as gl

def display_champions(forest):
    champions = []
    for species in forest.champions.items():
        if len(species[-1]) != 0:
            champions.append(species[-1][-1][1])
    
    viewer = gl.Viewer()
    g = build_tree(champions)
    viewer.display(
        g,          
        bg_col=[1, 1, 1]        
    )

def display_gene_graph(forest):
    frames = []
    for frame in forest.champions.


def main():
    "Non-visual version of main.py: allows for debugging without display"

    total_generations = 101
   
    forest = Forest(size=10, initial_population=0.5, spawn_probability=0.25, species_subset=['honda', 'pine', 'shrub'], 
                    scenario='polar')

    for gen in range(total_generations):
        forest.step()            
        #print(gen)
                                  

    analyse = Analyse(forest)
    print(analyse.reason_of_death())
    print(analyse.population_distribution())
    print(forest.champions)
    display_champions(forest)


main()