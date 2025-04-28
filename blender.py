import sys
import os
parent_dir = os.path.abspath( __file__ ).rsplit( '/', 1 )[0]
sys.path.append( f"{parent_dir}/forestLibrary" )
sys.path.append(r'\\wsl.localhost\Ubuntu-24.04\home\kristiancuervo\DigitalForest')

import bpy
import numpy as np
from forestLibrary.forest import Forest
from forestLibrary.tree import Tree
from forestLibrary.lsystem_utils import realize
from forestLibrary.species_genes import SPECIES_DEFAULT_PARAMS


# ─────────────────────────────────────────────────────────────────────────────
#  Helper functions
# ─────────────────────────────────────────────────────────────────────────────
def safe_remove_collection(collection_name: str) -> None:
    """
    Safely remove a collection and all its objects from Blender.
    """
    col = bpy.data.collections.get(collection_name)
    if col is not None:
        # First unlink and remove all objects in the collection
        for obj in list(col.objects):
            # Remove object data as well (curves, meshes, etc.)
            data = obj.data
            bpy.data.objects.remove(obj, do_unlink=True)
            if data and hasattr(data, 'users') and data.users == 0:
                if isinstance(data, bpy.types.Curve):
                    bpy.data.curves.remove(data)
                elif isinstance(data, bpy.types.Mesh):
                    bpy.data.meshes.remove(data)
        
        # Then remove the collection itself
        bpy.data.collections.remove(col)


def get_or_create_collection(collection_name: str, parent_collection=None) -> bpy.types.Collection:
    """
    Get an existing collection or create a new one if it doesn't exist.
    Optionally link it to a parent collection.
    """
    col = bpy.data.collections.get(collection_name)
    if col is None:
        col = bpy.data.collections.new(collection_name)
        if parent_collection:
            parent_collection.children.link(col)
        else:
            bpy.context.scene.collection.children.link(col)
    return col


def initialize_blender_cells(size: tuple[int, int],
                             spacing: float = 5.0,
                             collection_name: str = "Cells"):
    """
    Place a CURVE object at every grid coordinate so the layout is visible
    in the viewport (optional, but handy while modelling).
    """
    # First, safely remove any existing cells collection
    col = bpy.data.collections.get(collection_name)
    if col is None:
        col = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(col)
    else:
        for obj in list(col.objects):
            bpy.data.objects.remove(obj, do_unlink=True)

    for i in range(size[0]):
        for j in range(size[1]):
            curve = bpy.data.curves.new(f"cell_{i}_{j}", type='CURVE')
            curve.dimensions = '3D'
            spl = curve.splines.new('POLY')
            spl.points.add(0)                       # single dummy point
            spl.points[0].co = (0, 0, 0, 1)

            obj = bpy.data.objects.new(f"cell_{i}_{j}", curve)
            obj.location = (i * spacing, 0.0, j * spacing)
            col.objects.link(obj)


def tree_to_curve(tree: Tree,
                  i: int,
                  j: int,
                  *,
                  spacing: float = 5.0) -> bpy.types.Curve:
    """
    Convert an L-system tree into a standalone 3-D CURVE datablock.
    """
    verts, edges, radii = realize(tree.lsystem)
    #print("Inside tree_to_curve")
    #print(radii)
    #offset = np.array([i * spacing, 0.0, j * spacing])
    offset = 0
    curve = bpy.data.curves.new(f"tree_{i}_{j}", type='CURVE')
    curve.dimensions = '3D'

    for v0, v1 in edges:
        spl = curve.splines.new('POLY')
        spl.points.add(1)                            # two points total
        spl.points[0].co = *(verts[v0] + offset), 1.0
        spl.points[0].radius = radii[v0]
        spl.points[1].co = *(verts[v1] + offset), 1.0
        spl.points[1].radius = radii[v1]

    return curve


def init_blender_geonodes(species_subset=None):
    """
    Initialize the geometry nodes for each species in the subset.
    If no subset is provided, use all available species.
    """
    if species_subset is None:
        species_subset = SPECIES_DEFAULT_PARAMS
    
    geonodes = {}
    
    for species_name in species_subset:
        # Check if the node group exists before accessing it
        if species_name in bpy.data.node_groups:
            geonodes[species_name] = bpy.data.node_groups[species_name]
        else:
            print(f"Warning: Node group '{species_name}' not found in Blender")
    
    return geonodes


def clean_animation_instance_objects(pattern="GenInst_"):
    """
    Remove all instance objects matching the given pattern.
    """
    objs_to_remove = [obj for obj in bpy.data.objects if obj.name.startswith(pattern)]
    
    for obj in objs_to_remove:
        # Remove any animation data
        if obj.animation_data and obj.animation_data.action:
            bpy.data.actions.remove(obj.animation_data.action)
        # Remove the object
        bpy.data.objects.remove(obj, do_unlink=True)


# ─────────────────────────────────────────────────────────────────────────────
#  Main simulation → bakes every generation and builds a playable animation
# ─────────────────────────────────────────────────────────────────────────────
def main():
    # Simulation / animation parameters
    total_generations = 100           # becomes frame_end (frames 0 … 99)
    spacing = 1.0
    chosen_species = ["honda"]

    # First, remove any existing animation instances to avoid conflicts
    clean_animation_instance_objects()

    # Initialize geometry nodes
    geonodes = init_blender_geonodes(chosen_species)
    if not geonodes:
        print("Error: No valid geometry nodes found for the specified species.")
        return
    
    # Create forest simulation - using size=2 as in the updated version
    forest = Forest(size=2,
                    initial_population=0.5,
                    spawn_probability=0.25,
                    species_subset=chosen_species)

    # Optional helpers to see the grid layout while the sim runs
    initialize_blender_cells((forest.size, forest.size), spacing=spacing)

    # Clean master collection - using improved collection handling
    master_col = bpy.data.collections.get("Generations")
    if master_col is None:
        master_col = bpy.data.collections.new("Generations")
        bpy.context.scene.collection.children.link(master_col)
    else:
        for sub in list(master_col.children):
            bpy.data.collections.remove(sub, do_unlink=True)

    # ── Bake every generation to its own collection ────────────────────────
    for gen in range(total_generations):
        print(f"Processing generation {gen}/{total_generations-1}...")
        forest.step()

        # Sub-collection holding *real* curve objects for this generation
        gen_col = bpy.data.collections.new(f"Gen_{gen:03d}")
        master_col.children.link(gen_col)

        for i in range(1, forest.size + 1):
            for j in range(1, forest.size + 1):
                tree = forest.grid[i, j]
                if tree is None:
                    continue

                curve = tree_to_curve(tree, i - 1, j - 1, spacing=spacing)
                obj_name = f"tree_{i-1}_{j-1}_g{gen:03d}"
                obj = bpy.data.objects.new(obj_name, curve)
                obj.location = ((i - 1) * spacing, 0.0, (j - 1) * spacing)
                
                # Only add modifier if the species has a valid geometry node group
                if tree.genes['species'] in geonodes:
                    mod = obj.modifiers.new(f"geoNode_{tree.genes['species']}_{obj_name}", 'NODES')
                    mod.node_group = geonodes[tree.genes['species']]
                gen_col.objects.link(obj)

        # ── Create an instance and keyframe its visibility ─────────────────
        inst = bpy.data.objects.new(f"GenInst_{gen:03d}", None)
        inst.instance_type = 'COLLECTION'
        inst.instance_collection = gen_col
        bpy.context.scene.collection.objects.link(inst)

        # Three key-frames ensure the instance is visible ONLY on frame `gen`
        start_hide = gen - 1 if gen > 0 else 0  # avoid negative frames

        # Check if animation data exists, create if not
        if not inst.animation_data:
            inst.animation_data_create()

        # hidden before its own frame
        inst.hide_viewport = True
        inst.hide_render = True
        inst.keyframe_insert("hide_viewport", frame=start_hide)
        inst.keyframe_insert("hide_render", frame=start_hide)

        # shown on its frame
        inst.hide_viewport = False
        inst.hide_render = False
        inst.keyframe_insert("hide_viewport", frame=gen)
        inst.keyframe_insert("hide_render", frame=gen)

        # hidden afterwards
        inst.hide_viewport = True
        inst.hide_render = True
        inst.keyframe_insert("hide_viewport", frame=gen + 1)
        inst.keyframe_insert("hide_render", frame=gen + 1)

        # Check if animation data and action exist before modifying
        if inst.animation_data and inst.animation_data.action:
            # constant (step) interpolation so visibility jumps, not fades
            for fc in inst.animation_data.action.fcurves:
                for kp in fc.keyframe_points:
                    kp.interpolation = 'CONSTANT'

    # Scene framing so the play-head covers the whole simulation
    scene = bpy.context.scene
    scene.frame_start = 0
    scene.frame_end = total_generations - 1
    scene.frame_set(0)

    print(f"Forest simulation complete with {total_generations} generations.")


if __name__ == "__main__":
    main()