import random
from .tree import Tree

class HondaTree(Tree):
    def __init__(self, genes):
        axiom = [('A', 1.0, 0.2)]
        super().__init__(genes, axiom=axiom)

    def production_rule(self, sym):
        r1 = self.genes['r1']
        r2 = self.genes['r2']
        alpha1 = self.genes['alpha1']
        alpha2 = self.genes['alpha2']
        phi1 = self.genes['phi1']
        phi2 = self.genes['phi2']
        q = self.genes['q']
        e = self.genes['e']

        match sym:
            case ('A', s, w):
                w1 = w * q**e
                w2 = w * (1 - q)**e
                return [
                    ('!', w), ('F', s),
                    '[', ('+', alpha1), ('/', phi1), ('A', s * r1, w1), ']',
                    '[', ('+', alpha2), ('/', phi2), ('A', s * r2, w2), ']'
                ]
            case _:
                return [sym]

class PineTree(Tree):
    def __init__(self, genes):
        axiom = [('A', 1.2, 0.3)]
        super().__init__(genes, axiom=axiom)

    def production_rule(self, sym):
        r1 = self.genes['r1']
        r2 = self.genes['r2']
        r3 = self.genes.get('r3', 0.6)
        alpha1 = self.genes['alpha1']
        alpha2 = self.genes['alpha2']
        alpha3 = self.genes.get('alpha3', 0)
        phi1 = self.genes['phi1']
        phi2 = self.genes['phi2']
        phi3 = self.genes.get('phi3', 180)
        q = self.genes['q']
        e = self.genes['e']

        match sym:
            case ('A', s, w):
                w1 = w * q**e
                w2 = w * (1 - q)**e
                w3 = w * 0.3
                return [
                    ('!', w), ('F', s),
                    '[', ('+', alpha1), ('/', phi1), ('A', s * r1, w1), ']',
                    '[', ('+', alpha2), ('/', phi2), ('A', s * r2, w2), ']',
                    '[', ('+', alpha3), ('/', phi3), ('A', s * r3, w3), ']'
                ]
            case _:
                return [sym]

class BushTree(Tree):
    def __init__(self, genes):
        axiom = [('A', 0.7, 0.15)]
        super().__init__(genes, axiom=axiom)

    def production_rule(self, sym):
        r = self.genes['r1']
        alpha = self.genes['alpha1']
        phi = self.genes['phi1']
        q = self.genes['q']
        e = self.genes['e']

        match sym:
            case ('A', s, w):
                w_new = w * q**e
                return [
                    ('!', w), ('F', s),
                    '[', ('+', alpha), ('/', phi), ('A', s * r, w_new), ']',
                    '[', ('-', alpha), ('/', -phi), ('A', s * r, w_new), ']'
                ]
            case _:
                return [sym]

class FernTree(Tree):
    def __init__(self, genes):
        axiom = [('A', 0.6, 0.1)]
        super().__init__(genes, axiom=axiom)

    def production_rule(self, sym):
        r = self.genes['r1']
        alpha = self.genes['alpha1']
        phi = self.genes['phi1']
        q = self.genes['q']
        e = self.genes['e']

        match sym:
            case ('A', s, w):
                w_new = w * q**e
                return [
                    ('!', w), ('F', s),
                    '[', ('+', alpha), ('/', phi), ('A', s * r, w_new), ']',
                    ('F', s),
                    '[', ('-', alpha), ('/', -phi), ('A', s * r, w_new), ']',
                    ('F', s)
                ]
            case _:
                return [sym]

class BinaryTree(Tree):
    def __init__(self, genes):
        axiom = [('A', 1.0, 0.2)]
        super().__init__(genes, axiom=axiom)

    def production_rule(self, sym):
        r = self.genes['r1']
        alpha = self.genes['alpha1']
        phi = self.genes['phi1']
        q = self.genes['q']
        e = self.genes['e']

        match sym:
            case ('A', s, w):
                w_new = w * q**e
                return [
                    ('!', w), ('F', s),
                    '[', ('+', alpha), ('/', phi), ('A', s * r, w_new), ']',
                    '[', ('-', alpha), ('/', -phi), ('A', s * r, w_new), ']'
                ]
            case _:
                return [sym]

class StochasticTree(Tree):
    def __init__(self, genes):
        axiom = [('A', 1.0, 0.2)]
        super().__init__(genes, axiom=axiom)

    def production_rule(self, sym):
        r = self.genes['r1']
        alpha = self.genes['alpha1']
        phi = self.genes['phi1']
        q = self.genes['q']
        e = self.genes['e']

        match sym:
            case ('A', s, w):
                w_new = w * q**e
                options = [
                    [('!', w), ('F', s),
                     '[', ('+', alpha), ('/', phi), ('A', s * r, w_new), ']',
                     '[', ('-', alpha), ('/', -phi), ('A', s * r, w_new), ']'],
                    [('!', w), ('F', s),
                     '[', ('+', alpha), ('/', phi), ('A', s * r, w_new), ']'],
                    [('!', w), ('F', s),
                     '[', ('-', alpha), ('/', -phi), ('A', s * r, w_new), ']']
                ]
                return random.choice(options)
            case _:
                return [sym]
