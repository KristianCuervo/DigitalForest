# Digital Forest Simulator

This is the final project for the DTU course **02563 Generative Methods for Computer Graphics**. 

## Project Outline 
The following section elaborates on the different sections of the simulation. 

The simulation is based on spawning an initial seed of trees onto a 2d-grid. Each tree will grow iteratively, using **L-Systems**. After each tree has grown, each tree will be looped through and it will measure its current sunlight intake, which works as a **fitness function** in this simulation. The sunlight intake is a naive equation which takes the height and width of the tree into account; if the trees sunlight intake is lower than the trees in its surroundings by a certain factor it will die due to sunlight deficiency. Furthermore, each tree has a random percentage chance of dying, which grows with each iteration as the tree gets older. 



### Tree Object (L-System)
Each tree grows iteratively using an L-System algorithm. The L-system works by growing using an axiom and a production rule. Furthermore, it grows using a set of parameters which determine the different length of branches, and at what angles they will grow at. These parameters will be seen as the "genes" of the tree, and are used to create new genetic offspring,.


### Simulation Initialisation

### Measuring light intake

#### Growth

#### Death

### Genetic Iteration

### Spawning new trees

## Contributions
The following contributors are responsible for this repository:
- Johannes Duerlund
- Kristián Cuervo
- Tiago Alfagema 
