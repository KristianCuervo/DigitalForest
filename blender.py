import sys
sys.path.append(r'C:\Users\ago\my_code_priv\DTU\02563\DigitalForest')


import time
import numpy as np
from forestLibrary.forest import Forest
from forestLibrary.tree import Tree
from forestLibrary.lsystem_utils import realize
import bpy

def initialize_blender_cells(size:tuple[int, int], spacing:float=5.0):
    """
    Initialize the Blender cells for the forest simulation.
    Each cell is represented by a curve object in Blender.
    """
    # Clear any existing objects in the collection
    for obj in bpy.data.collections['Cells'].objects:
        bpy.data.objects.remove(obj, do_unlink=True)
    
    
    # Create a new collection for the cells
    for i in range(size[0]):
        for j in range(size[1]):
            new_object = bpy.data.objects.new('tree', None)
            new_object.location = np.array([i*spacing, 0.0, j*spacing])
            bpy.data.collections['Cells'].objects.link(new_object)
            
    return bpy.data.collections['Cells'].objects

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
    
    return curve   


def main():
    # Simulation Parameters
    total_generations = 100
    delay            = 0.5
    spacing          = 1.0

    # Blender set up - curve has current curve of lsystem at (i,j)
    BlenderCells = bpy.data.collections['Cells'].objects
    
    # Initialize the forest
    forest = Forest(size=10, initial_population=0.5, spawn_probability=0.25, species_subset=["honda", "bush"])

    # Initialize Blender cells
    Cells = initialize_blender_cells((forest.size, forest.size), spacing=spacing)
    

    # Simulation loop
    for gen in range(total_generations):
        forest.step()
        for i in range(1, forest.size + 1):
            for j in range(1, forest.size + 1):
                tree = forest.grid[i, j]
                cell = Cells[i * forest.size + j]
                if tree is None:
                    curve_data = bpy.data.curves.new('SinglePointCurve', type='CURVE')
                    spline = curve_data.splines.new(type='BEZIER')
                    spline.bezier_points[0].co = (i, 0, j)
                    cell.data = curve_data
                    continue
                
                curve_data = tree_to_curve(tree, i, j, spacing=spacing)
                cell.data = curve_data
                
                # Store the curve of the tree in current frame
                cell.keyframe_insert(data_path="growth", frame=gen)
                
                
                
                                           # update sim
         

        time.sleep(delay) # frame rate 

if __name__ == "__main__":
    main()
