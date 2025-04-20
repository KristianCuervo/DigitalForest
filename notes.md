- Using the normals for the sunlight intake
- Appending normals throughout the l-system iterations

[[0.05, 0.3, 0.05]]
[0.3, self, 0.3],
[0.05, 0.3, 0.05]]

- 1st problem: sunlight intake
--> sensitive equation 

- 2nd problem: constrained growth
--> trees shouldnt only grow very tall 
--> tall trees need more sunlight to survive
--> each iteration: if sunlight_intake > sunlight_req:
----> grows

next steps: 
- BLENDER FRONTEND
-- textures for tree species # tiago
-- leafs for lsystems generatively
-- taking the lsystems.py from the assignment and extending to a forest grid # kristian


- Finish classes in forestlibrary # kristian
-- forest.py
-- tree.py 

- Write simulation code (main.py) # tiago & johannes
-- Get a working MVP in python 
-- Finetune functions (sunlight intake and constraint) 

final notes:
- get blendit (blender for git) and add blender file 
- docs folder in git and add architecture.md files
