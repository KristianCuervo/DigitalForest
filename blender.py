import time
import numpy as np
from forestLibrary.forest import Forest
from forestLibrary.tree import Tree
from forestLibrary.lsystem_utils import realize
import bpy

def tree_to_curve(tree:Tree, i, j, spacing:float=5.0):
    verts, edges, radii = realize(tree.lsystem)
    offset = np.array([i * spacing, 0.0, j * spacing], dtype=float)
    vertices = [v + offset for v in verts]

    curve = bpy.data.curves.new('curve', 'CURVE')
    for v0, v1 in edges:
        spline = curve.splines.new('POLY')
        spline.points.add(1)
        spline.points[0].co[0:3] = vertices[v0]
        spline.points[0].radius = radii[v0]
        spline.points[1].co[0:3] = vertices[v1]
        spline.points[1].radius = radii[v1]    
    new_object = bpy.data.objects.new('tree', curve)
    bpy.data.collections['Cells'].objects.link(new_object)      


def main():
    # Simulation Parameters
    total_generations = 100
    delay            = 0.5
    spacing          = 1.0

    # Blender set up - curve has current curve of lsystem at (i,j)
    BlenderCells = bpy.data.collections['Cells'].objects
    
    # Initialize the forest
    forest = Forest(size=10, initial_population=0.5, spawn_probability=0.25, species_subset=["honda", "bush"])

    # Simulation loop
    for gen in range(total_generations):
        forest.step()
        for i in range(1, forest.size + 1):
            for j in range(1, forest.size + 1):
                tree = forest.grid[i, j]
                if tree is None:
                    continue
                
                idx = i * forest.size + j
                # Set location of tree
                BlenderCells[idx].location = (i * spacing, 0.0, j * spacing) # Spacing of
                # Store the curve of the tree in current frame
                BlenderCells[idx].keyframe_insert(data_path="location", frame=gen)
                
                
                
                                           # update sim
         

        time.sleep(delay) # frame rate 

if __name__ == "__main__":
    main()
