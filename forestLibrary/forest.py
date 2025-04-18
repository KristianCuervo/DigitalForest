import numpy as np
from .tree import Tree
import random as random
from .geneticAlgorithm import GeneticAlgorithm
from .species_genes import SPECIES_DEFAULT_PARAMS

class Forest:
    def __init(self, size:int, initial_population:float=0.5, spawn_probablility:float=0.15):
        # Forest is a grid of trees with boundaries of None values
        self.size = size # Tree Size
        self.grid = [
                        [None for j in range(size+2)]
                        for i in range(size+2)]# Introduces boundaries with size+2
        
        # Forest is spawned on grid with random tree species
        self.initial_population = initial_population
        self.initial_spawn()

        # Sunlight grid is a grid of sunlight values for each tree at their current growth
        self.sunlight_grid = None
        self.get_gene_pools = None

        # Spawn probability is the probability of spawning a new tree in an empty cell
        # Genetic algorithm is used to create new trees from the gene pools
        self.spawn_probability = spawn_probablility
        self.genetic_algorithm = GeneticAlgorithm()
    
    def initial_spawn(self):
        """
        Randomly spawns trees in the forest. 
        It should be investigated whether the trees should also start at
        age 1 or at random ages.
        """
        for i in range(1, self.size+2):
            for j in range(1, self.size+2):
                # 1 --> self.size+1 are the non-boundary cells
                
                if np.random.rand() < self.initial_population:
                    # Given a wanted population probability distribution, spawn random trees
                    self.grid[i][j] = Tree(genes=random.choice(SPECIES_DEFAULT_PARAMS))

        pass

    def update_sunlight(self):
        """
        Returns a grid of sunlight values for each tree in the forest.
        The sunlight value is determined by the distance to the nearest tree
        and the angle of the sun. This is required to calculate the shadow.
        """
        sunlight_grid = np.zeros((self.size, self.size))
        for i in range(1, self.size+2):
            for j in range(1, self.size+2):
                if self.grid[i, j] is not None:
                    sunlight_grid[i, j] = self.grid[i, j].sunlight
        return self.sunlight_grid

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
        for i in range(1, self.size+2):
            for j in range(1, self.size+2):
                if self.grid[i, j] is not None:
                    self.grid[i, j].shadow = np.sum(shadow_kernel*self.sunlight_grid[i-1:i+2, j-1:j+2])
    
    
    def death_or_growth(self):
        """
        Determines whether each tree in the forest survives or dies.
        The trees that die are removed from the forest.
        """
        for i in range(1, self.size+2):
            for j in range(1, self.size+2):
                if self.grid[i, j] is not None:
                    if self.grid[i, j].survival_roll() == False:
                        self.grid[i][j] = None # Kills the tree instance
                    else:
                        self.grid[i][j].grow()

    def update_gene_pools(self):
        """
        Returns seperate lists of the instances of each species in the forest.
        """
        gene_pools = {}
        for i in range(1, self.size+2):
            for j in range(1, self.size+2):
                if self.grid[i, j] is not None:
                    species = self.grid[i, j].genes # this is a string of the species name 
                    if species not in gene_pools:
                        gene_pools[species] = [] # creates a new list for the species
                    gene_pools[species].append(self.grid[i, j]) # appends tree instance to list
        self.gene_pools = gene_pools
    
    def spawn_new_trees(self):
        """
        Spawns new trees in the forest based on the gene pools and genetic algorithm.
        The trees are spawned in empty cells with a probability of spawn_probability.
        """
        self.update_gene_pools()
        for i in range(1, self.size+2):
            for j in range(1, self.size+2):
                if self.grid[i, j] is None and np.random.rand() < self.spawn_probability:
                    species = random.choice(list(self.gene_pools.keys()))
                    current_gene_pool = self.gene_pools[species]
                    # Create a child tree from gene pool
                    child_tree = self.genetic_algorithm.generate_children(current_gene_pool, 1)[0]
                    self.grid[i][j] = child_tree

    def grow_trees(self):
        """
        Grows each tree in the forest which is alive.
        """
        for i in range(1, self.size+2):
            for j in range(1, self.size+2):
                if self.grid[i, j] is not None:
                    self.grid[i, j].grow()
                