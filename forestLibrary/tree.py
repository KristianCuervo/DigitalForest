import numpy as np

class Tree:
    def __init__(self, genes, axiom=None):
        self.genes = genes
        self.height = None
        self.width = None
        self.lsystem = axiom if axiom else [('A', 1.0, 0.2)]
        self.age = 1

        self.sunlight = self.sunlight_intake() # Iterated each time the tree grows
        self.shadow = None # Calculated in forest class
        self.survival_requirement = None 
    
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
        self.sunlight = self.sunlight_intake()


    def old_age_death_roll(self):
        """
        The tree dies with an increasing probability as it ages.
        """
        chance_of_death = (self.age / 100)**2
        if np.random.rand() < chance_of_death:
            return True
        return False
    
    def survival_roll(self):
        """
        The tree dies if it does not meet the survival requirements.
        The larger a tree is, the more sunlight it needs to survive. 
        """
        effective_size = self.height * self.width # Some function of size
        self.survival_requirement = self.shadow + effective_size
        
        # The tree dies if it does not get enough sunlight
        if self.sunlight < self.survival_requirement:
            return False
        
        # If the tree is not dead, check if it dies from old age
        elif self.old_age_death_roll():
            return False
        
        # Tree survives
        return True




