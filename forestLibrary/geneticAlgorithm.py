import random
from .tree import Tree

class GeneticAlgorithm:
    #with a rate of 0.75 and strength 0.5, you get some interesting results
    def __init__(self, mutation_rate=0.05, mutation_strength=0.1):
        self.mutation_rate = mutation_rate
        self.mutation_strength = mutation_strength

    def generate_children(self, gene_pool, num_children) -> list:
        """
        Generates a number of children from the gene pool.
        """
        children = []
        for i in range(num_children):
            child = self.breed(gene_pool)
            children.append(child)
        return children

    def breed(self, gene_pool):
        """
        Breeds two genes from the gene pool to create a new gene.
        """
        parent1, parent2 = random.sample(gene_pool, 2)

        child_genes = self.crossover(parent1, parent2)
        child_genes = self.mutate(child_genes)
        return child_genes
    
    def crossover(self, parent1:Tree, parent2:Tree):
        """
        Performs 50/50 crossover between two genes to create a new gene
        """
        child_genes = {}
        for key in parent1.genes.keys():
            if random.random() < 0.5:
                child_genes[key] = parent1.genes[key]
            else:
                child_genes[key] = parent2.genes[key]
        return child_genes
    
    def mutate(self, child_genes):
        """
        Mutates a gene by mutation strength with a likelihood of mutation rate.
        """
        for key in child_genes.keys():
            if random.random() < self.mutation_rate and key != "species":
                child_genes[key] += random.uniform(-self.mutation_strength, self.mutation_strength) * child_genes[key]
        return child_genes
        