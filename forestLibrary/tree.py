import numpy as np
from .lsystem_utils import realize


class Tree:
    def __init__(self, genes, axiom=None):
        self.genes   = genes
        self.lsystem = axiom if axiom else [('A', 1.0, 0.2)]
        self.age     = 1

        # geometry & ecology state (updated after each grow)
        self.height  = 0.0
        self.width   = 0.0
        self.sunlight = 0.0
        self.shadow   = 0.0
        self.survival_requirement = 0.0

        # compute initial geometry + sunlight
        self._update_geometry()
        #self.sunlight = self.sunlight_intake()
    
     # ----------------- L-SYSTEM  -----------------
    def production_rule(self, sym):
        """Must be overridden by subclasses."""
        return [sym]             # default: no rewrite
    
    def grow(self, forest_season):
        if self.age <= 8: # Stops growing at age 10 (mainly to prevent micro-branches and lag)
            grown_lsystem = []
            for sym in self.lsystem:
                grown_lsystem += self.production_rule(sym)
            self.lsystem = grown_lsystem
            self._update_geometry()
            self.sunlight = self.sunlight_intake(season=forest_season)
        self.age += 1      # Age still increases if it stops growing

    
    def _update_geometry(self):
        verts, edges, radii = realize(self.lsystem)
        if verts.size == 0:
            self.height = self.width = 0.0
            return

        # Y is the vertical axis in SpaceTurtle
        y_vals = verts[:, 1]
        self.height = float(y_vals.max() - y_vals.min())

        # Width = max horizontal spread in X–Z plane
        x_vals = verts[:, 0]
        z_vals = verts[:, 2]
        x_span = x_vals.max() - x_vals.min()
        z_span = z_vals.max() - z_vals.min()
        self.width = float(max(x_span, z_span))

        # Y is the vertical axis
        y_vals = verts[:,1]
        self.height = float(y_vals.max() - y_vals.min())

        # width in the X‑Z plane
        x_vals = verts[:,0]
        z_vals = verts[:,2]
        self.width = float(max(x_vals.max()-x_vals.min(),
                            z_vals.max()-z_vals.min()))

    # ----------------- FITNESS  -----------------
    def sunlight_intake(self, season):
        """
        Fitness function of each of the trees.
        S(h, w) = alpha*h + beta*w + gamma*sqrt(h*w)
        where h is the height and w is the width of the tree. 
        alpha --> tall factor
        beta --> wide factor
        gamma --> square factor


        """
        alpha = None
        beta = None
        gamma = None
        if season == "summer":
            # The light comes from high up in the summer, penetrates far into the forest and benefits wide trees.
            alpha = 0.25
            beta = 2.0
            gamma = 1.0

        elif season == "autumn" or season == "spring":
            # Intermediate lighting condition. Doesn't prioritise tall nor wide trees
            alpha = 0.5
            beta =  1.5
            gamma = 1.5
            pass

        elif season == "winter":
            # The light comes from a shallow angle in winter. It is better to be taller at this point.
            alpha = 1.0
            beta = 0.5
            gamma = 1
            pass
        
        return alpha*self.height + beta*self.width + gamma*np.sqrt(self.height*self.width)
    

    # ----------------- DEATH ROLLS -----------------
    def old_age_death_roll(self):
        """
        The tree dies with an increasing probability as it ages.
        """

        #chance_of_death = (self.age / 100)
        #A way for sunlight shadow to impact survival chance, but this is a bad solution
        chance_of_death = ((self.age * max({1, (self.shadow + 0.000001)/(self.sunlight + 0.000002)})) / 100)


        if np.random.rand() < chance_of_death:
            return True
        return False
    
    def survival_roll(self):
        """
        The tree dies if it does not meet the survival requirements.
        The larger a tree is, the more sunlight it needs to survive. 
        """
        effective_size = (self.height * (self.width)**2)**2 # h*w**2: volume bounding box
        self.survival_requirement = (self.shadow + effective_size)
        
        # The tree dies if it does not get enough sunlight
        #if self.sunlight < self.survival_requirement:
        #    return False
        
        # If the tree is not dead, check if it dies from old age
        if self.old_age_death_roll():
            return False
        
        # Tree survives
        return True




