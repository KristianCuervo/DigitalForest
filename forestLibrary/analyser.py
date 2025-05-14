from .forest import Forest
from .tree import Tree
from operator import attrgetter
from collections import Counter


class Analyse:
    def __init__(self, forest: Forest):
        self.forest = forest

    def population_distribution(self) -> dict[str, int]:
        """
        Returns a dict mapping species → number of currently living trees.
        """
        # Refresh the internal gene_pools so it reflects the current grid
        self.forest.update_gene_pools()

        # gene_pools is a species→[Tree, …] of living trees
        return { species: len(pool)
                 for species, pool in self.forest.gene_pools.items() }

    def reason_of_death(self) -> dict[str, dict[str, int]]:
        """
        Returns a nested dict:
            species → { 'Age': n1, 'Shadow': n2, 'Size': n3 }
        counting why each tree died.
        """
        result: dict[str, dict[str,int]] = {}
        for species, dead_list in self.forest.graveyard.items():
            # tally up the death_reason attribute
            counts = Counter(t.death_reason for t in dead_list)
            result[species] = {
                'Age':    counts.get('Age', 0),
                'Shadow': counts.get('Shadow', 0),
                'Size':   counts.get('Size', 0),
            }
        return result
                
