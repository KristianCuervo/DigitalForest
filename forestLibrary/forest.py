import numpy as np
from .tree import Tree
import random as random
from .geneticAlgorithm import GeneticAlgorithm
from .species_genes import SPECIES_DEFAULT_PARAMS, reduced_SPECIES, get_species_params
from .species import HondaTree, ShrubTree, PineTree

SPECIES_CLASS = {
    "honda"      : HondaTree,
    "oak"        : HondaTree,
    "birch"      : HondaTree,
    "shrub"      : ShrubTree,
    "pine"       : PineTree
}



class Forest:
    def __init__(self, size:int, initial_population:float=0.5, spawn_probability:float=0.15, species_subset: list[str] | None = None):
        # Forest is a grid of trees with boundaries of None values
        self.gen = 0
        self.season_initial = 0
        self.season_length = 90
        self.season_list = ['autumn', 'winter', 'spring', 'summer']
        self.season = self.season_list[self.season_initial]
        print("The season is", self.season)
        
        self.size = size # Tree Size
        self.grid = np.empty((size+2, size+2), dtype=object)

        # Forest is spawned on grid with random tree species
        self.initial_population = initial_population
        self.active_species = species_subset or list(SPECIES_CLASS.keys())
        self.initial_spawn()

        # Sunlight grid is a grid of sunlight values for each tree at their current growth
        self.sunlight_grid = None
        self.get_gene_pools = None

        # Spawn probability is the probability of spawning a new tree in an empty cell
        # Genetic algorithm is used to create new trees from the gene pools
        self.spawn_probability = spawn_probability
        self.genetic_algorithm = GeneticAlgorithm(mutation_rate=0.2, mutation_strength=0.1)
        
        self.death_pool = np.empty((size+2, size+2), dtype=object)
    
    def initial_spawn(self):
        """
        Randomly spawns trees in the forest. 
        It should be investigated whether the trees should also start at
        age 1 or at random ages.
        """
        def inner(self, i, j):
            # 1 --> self.size+1 are the non-boundary cells    
            if np.random.rand() < self.initial_population:
                # Given a wanted population probability distribution, spawn random trees
                species_name = random.choice(self.active_species)
                genes = get_species_params(species_name, param_dict=reduced_SPECIES)
                self.grid[i, j] = SPECIES_CLASS[species_name](genes=genes)

        self.go_through_forest(inner)

    def update_sunlight(self):
        """
        Returns a grid of sunlight values for each tree in the forest.
        The sunlight value is determined by the distance to the nearest tree
        and the angle of the sun. This is required to calculate the shadow.
        """
        sunlight_grid = np.zeros((self.size+2, self.size+2))
        def inner(self, i, j):
            if self.grid[i, j] is not None:
                    sunlight_grid[i, j] = self.grid[i, j].sunlight

        self.go_through_forest(inner)


        self.sunlight_grid =  sunlight_grid

    def update_shadows(self):
        """
        Returns total shadow cast at tree (x, y) by neighbouring trees
        in a 3x3 grid.
        A kernel multiplied by the sunlight of the neighbours gives an 
        approximation of the shadow cast by the neighbours.
        """
        self.update_sunlight()
        shadow_kernel = np.array([[0.05, 0.1, 0.05],
                                  [0.1, 0, 0.1],
                                  [0.05, 0.1, 0.05]])

        def inner(self, i, j):
            if self.grid[i, j] is not None:
                self.grid[i, j].shadow = np.sum(shadow_kernel*self.sunlight_grid[i-1:i+2, j-1:j+2])
        
        self.go_through_forest(inner)
    
    
    def death_or_growth(self):
        """
        Determines whether each tree in the forest survives or dies.
        The trees that die are removed from the forest.
        """
        def inner(self, i, j):
            if self.grid[i, j] is not None:
                if self.grid[i, j].survival_roll() == False:
                    self.death_pool[i, j] = self.grid[i, j] # adds the final tree state before its death to a pool for rendering
                    self.grid[i, j] = None # Kills the tree instance
                else:
                    self.grid[i, j].grow(forest_season=self.season)
        
        self.go_through_forest(inner)

    def update_gene_pools(self):
        """
        Returns seperate lists of the instances of each species in the forest.
        """
        gene_pools = {}
        def inner(self, i, j):
            if self.grid[i, j] is not None:
                species = self.grid[i, j].genes['species'] # this is a string of the species name 
                if species not in gene_pools:
                    gene_pools[species] = [] # creates a new list for the species
                gene_pools[species].append(self.grid[i, j]) # appends tree instance to list   
             
        self.go_through_forest(inner)

        self.gene_pools = gene_pools
    
    def spawn_new_trees(self):
        """
        Spawns new trees in the forest based on the gene pools and genetic algorithm.
        The trees are spawned in empty cells with a probability of spawn_probability.
        """
        self.update_gene_pools()
        
        #This solution is bad and stupid, I apologize
        shadow_kernel = np.array([[0.05, 0.1, 0.05],
                                  [0.1, 0, 0.1],
                                  [0.05, 0.1, 0.05]])

        def inner(self, i, j):
            if self.grid[i, j] is None and np.random.rand() < self.spawn_probability and self.sunlight_grid[i,j] >= np.sum(shadow_kernel*self.sunlight_grid[i-1:i+2, j-1:j+2]):
                species = random.choice(list(self.gene_pools.keys()))
                current_gene_pool = self.gene_pools[species]
                if len(current_gene_pool) < 2:
                    # Not enough parents
                    print(species, "is extinct or near.")
                    return
                # Create a child tree from gene pool
                child_genes = self.genetic_algorithm.generate_children(current_gene_pool, 1)[0]
                self.grid[i, j] = SPECIES_CLASS[species](genes=child_genes)
        
        self.go_through_forest(inner)
    
    def update_season(self):
        old_season = self.season
        season_index = int(self.season_initial + np.floor(self.gen/self.season_length)) % 4
        self.season = self.season_list[season_index]
        if old_season != self.season:
            print("New season is ", self.season)

    def reached_termination(self, i, j):
        tree_in_terminal_state = self.death_pool[i,j]
        if tree_in_terminal_state is not None:
            self.death_pool[i,j] = None
            return tree_in_terminal_state
        else:
            return None
    
    def step(self):
        """
        Runs one step of the simulation.
        """
        self.update_shadows()
        self.death_or_growth()
        self.spawn_new_trees()
        self.update_season()
        self.gen += 1
    
    def go_through_forest(self, func):
        for i in range(1, self.size+1):
            for j in range(1, self.size+1):
                func(self, i, j)