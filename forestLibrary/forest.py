import numpy as np
from .tree import Tree

class Forest:
    def __init(self, size:int, initial_population:float):
        self.size = size # Tree Size
        self.grid = [[None for i in range(size+2) for _ in range(size+2)]] # Introduces boundaries with size+2
        self.initial_spawn()
    
    def initial_spawn(self):
        """
        Randomly spawns trees in the forest. 
        It should be investigated whether the trees should also start at
        age 1 or at random ages.
        """
        for i in range(self.size):
            for j in range(self.size):
                if np.random.rand() < self.initial_population:
                    # Spawn a tree at (i, j)
                    self.grid[i][j] = Tree(genes=random.choice(SPECIES_DEFAULT_PARAMS))


        pass

    def kill_tree(self, x, y):
        self.grid[x][y] = None
        