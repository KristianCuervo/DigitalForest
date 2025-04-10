# Digital Forest Simulator

This is the final project for the DTU course **02563 Generative Methods for Computer Graphics**. It combines the topics of **Recursive Structures** by implementing L-Systems, **Cellular Automata** through the use of life and death on a cellular grid, and **Evolutionary Methods** by integrating genetic algorithms in the iteration of tree types. 

## Project Outline 
The following section elaborates on the different sections of the simulation. 

The simulation is based on spawning an initial seed of trees onto a 2d-grid. Each tree will grow iteratively, using **L-Systems**. After each tree has grown, each tree will be looped through and it will measure its current sunlight intake, which works as a **fitness function** in this simulation. The sunlight intake is a naive equation which takes the height and width of the tree into account; if the trees sunlight intake is lower than the trees in its surroundings by a certain factor it will die due to sunlight deficiency. Furthermore, each tree has a random percentage chance of dying, which grows with each iteration as the tree gets older. 

![Diagram](https://github.com/KristianCuervo/DigitalForest/blob/master/gengraph.png) 

### Tree Object (L-System)
Each tree grows iteratively using an L-System algorithm. The L-system works by growing using an axiom and a production rule. Furthermore, it grows using a set of parameters which determine the different length of branches, and at what angles they will grow at. These parameters will be seen as the "genes" of the tree, and are used to create new genetic offspring,.


### Simulation Initialisation

The simulation is initialised on a n x n grid. The grid is randomly populated using trees with random parameters. Cells are thus divided into either None or Tree objects, where it is only possible for the trees to grow on the cells 

### Measuring light intake

The light measurement equation is a naive equation which takes into account the height of the tree, and the width of its branches. This does not take into consideration the neighbouring trees; however the neighbouring trees and their sunlight intake will influence the growth and death of the current tree.


```python
for each tree in grid:
    tree.sunlight = sunlight(grid(i,j))
    
    for each neighbour: 
        neighbours.sunlight = sum(sunlight(neighbours))
    
    # The following equation determines if the neighbours are taking too much sun in comparison to the current tree. 
    if neighbours.sunlight > 2*tree.sunlight: 
        tree.death()
    else:
        tree.growth()

```

#### Growth

If the tree has enough sunlight in comparison to its neighbours, then it simply stays alive and it iterates its l-system one one more time.

#### Death

If the tree does not have enoguh sunlight, it is removed from the domain and replaced with a dead cell.

### Spawning new trees
In-between each iteration, new trees will spawn. Trees will spawn in random dead cells. It is possible that it will occupy a non-optimal cell, which is heavily shaded by neighbours; in this case it is likely to due at an early iteration. However, if it spawns in a cell with more sunlight, it is likely to survive more iterations. The parameters of the spawned tree is dependent on a gene pool which is created using a genetic algorithm. 

### Genetic Algorithm

The genetic iteration occurs at the end of each iteration. It takes the current alive trees, which creates a gene pool. For each tree which is to be spawned, a child tree will be created based on two randomly chosen parent trees. The parent trees have their genotypes mixed (their L-System parameters). 

## Contributions
The following contributors are responsible for this repository:
- Johannes Duerlund
- Kristián Cuervo
- Tiago Alfagema 
