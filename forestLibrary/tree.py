import numpy as np

class Tree:
    def __init__(self, genes, axiom=None):
        self.genes = genes
        self.height = None
        self.width = None
        self.lsystem = axiom if axiom else [('A', 1.0, 0.2)]
        self.age = 1

    
    def sunlight_intake(self):
        """
        Fitness function of each of the trees.
        S(h, w) = alpha*h + beta*w + gamma*sqrt(h*w)
        where h is the height and w is the width of the tree. 
        """
        alpha = 1
        beta = 1
        gamma = 1
        return alpha*self.height + beta*self.width + gamma*np.sqrt(self.height*self.width)
    

    

    def grow(self):
        
        grown_lsystem = []
        for sym in self.lsystem:
            grown_lsystem += self.production_rule(sym)
        self.lsystem = grown_lsystem
        self.age += 1
    
    


