from .tree import Tree
from typing import Dict, List


class Graveyard:
    """
    This class is a collector. It collects every tree when it dies with.
    Including reason of death, age, genes, and species.
    """
    def __init__(self, species):
        self.species = species
        self._tombs: Dict[str, List[Tree]] = {s: [] for s in self.species}
    

    def collect(self, tree: Tree):
        self._tombs[tree.species].append(tree)


    def __getitem__(self, species: str) -> List[Tree]:
        return self._tombs[species]
    

    def sort_by(self, species, attr: str):
        return sorted(
            self._tomb[species],
            key=lambda x: getattr(x, attr),
            reverse=True
        )