import sys
import os
parent_dir = os.path.abspath(__file__).rsplit('\\', 2)[0]
sys.path.append( f"{parent_dir}" )
sys.path.append(r'\\wsl.localhost\Ubuntu-24.04\home\kristiancuervo\DigitalForest')
sys.path.append(r'C:\Users\ago\my_code_priv\DTU\02563\DigitalForest')
os.path.abspath(__file__)

import bpy
import numpy as np
from forestLibrary.forest import Forest
from forestLibrary.tree import Tree
from forestLibrary.lsystem_utils import realize
from forestLibrary.species_genes import SPECIES_DEFAULT_PARAMS, reduced_SPECIES


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


def tree_to_curve(tree: Tree, i: int, j: int, *, spacing: float = 5.0) -> bpy.types.Curve:
    """
    Convert an L-system tree into a standalone 3-D CURVE datablock.
    Creates continuous splines from root to each leaf for better animation.
    """
    verts, edges, radii = realize(tree.lsystem)
    
    # Update offset to position trees in the X-Y plane (since Z is now up)
    offset = np.array([0, 0, 0.0], dtype=float)
   
    curve = bpy.data.curves.new(f"tree_{i}_{j}", type='CURVE')
    curve.dimensions = '3D'
   
    # Build parent lookup (child -> parent)
    parent_map = {}
    for v1, v0 in edges:
        parent_map[v1] = v0
   
    # Build adjacency list (parent -> [children])
    adjacency_list = {}
    for i in range(len(verts)):
        adjacency_list[i] = []
   
    for v1, v0 in edges:
        adjacency_list[v0].append(v1)
   
    # Find all leaf nodes (nodes with no children)
    leaf_nodes = []
    for i in range(len(verts)):
        if i in adjacency_list and len(adjacency_list[i]) == 0:
            leaf_nodes.append(i)
   
    # Trace path from each leaf back to root
    def trace_path_to_root(node):
        path = [node]
        current = node
       
        # Follow parent references back to root
        while current in parent_map:
            current = parent_map[current]
            path.append(current)
       
        # Reverse to get path from root to leaf
        return path[::-1]
   
    # Generate all root-to-leaf paths
    paths = [trace_path_to_root(leaf) for leaf in leaf_nodes]
   
    # Create splines from paths
    for path_idx, path in enumerate(paths):
        if len(path) < 2:
            continue  # Skip paths that are too short
           
        # Create a new spline for this path
        spl = curve.splines.new('POLY')
       
        # Add points for all vertices in the path
        spl.points.add(len(path) - 1)  # Already has 1 point by default
       
        # Set the coordinates and radius for each point
        for point_idx, vert_idx in enumerate(path):
            # Set coordinates (x, y, z, w) where w is the homogeneous coordinate (1.0)
            # No need to modify the vertex coordinates, as realize() now already produces Z-up coordinates
            spl.points[point_idx].co = [*(verts[vert_idx] + offset)] + [1.0]
            # Set radius
            spl.points[point_idx].radius = radii[vert_idx]
   
    return curve


def init_blender_geonodes(species_subset=None):
    """
    Initialize the geometry nodes for each species in the subset.
    If no subset is provided, use all available species.
    """
    if species_subset is None:
        species_subset = reduced_SPECIES
    
    geonodes = {}
    
    for species_name, genes in reduced_SPECIES.items():
        if species_name not in species_subset:
            continue
        for gene in genes:
            if gene['species'] in bpy.data.node_groups:
                geonodes[gene['species']] = bpy.data.node_groups[gene['species']]
            else:
                print(f"Warning: Node group '{gene['species']}' not found in Blender")

         
    
    return geonodes


def animate_tree(tree_final_state,tree_age, current_gen, generation_to_frames_ratio, obj, geo_mod, blender_sockets):
    """
    Animate the tree growth and death using keyframes.
    """

    # Calculate birth generation (when the tree first appeared)
    birth_gen = current_gen - tree_age

    # Calculate frame numbers based on birth generation
    start_frame = max(1, birth_gen * generation_to_frames_ratio)
    end_frame = current_gen * generation_to_frames_ratio
    death_frame = (current_gen + 2) * generation_to_frames_ratio

    # Set the animation values
    start_value = 0.0
    end_value = 1.0
    death_value = 0.0

    # Target input - access the input by name
    input_name = blender_sockets[tree_final_state.genes['species']]  # aka "growth ratio"

    # Set up animation keyframes
    bpy.context.scene.frame_set(start_frame)
    geo_mod[input_name] = start_value
    geo_mod.keyframe_insert(data_path=f'["{input_name}"]', frame=start_frame)

    bpy.context.scene.frame_set(end_frame)
    geo_mod[input_name] = end_value
    geo_mod.keyframe_insert(data_path=f'["{input_name}"]', frame=end_frame)

    bpy.context.scene.frame_set(death_frame)
    geo_mod[input_name] = death_value
    geo_mod.keyframe_insert(data_path=f'["{input_name}"]', frame=death_frame)

    # Hide tree before it starts growing
    obj.hide_viewport = True
    obj.hide_render = True
    obj.keyframe_insert(data_path="hide_viewport", frame=start_frame - 1)
    obj.keyframe_insert(data_path="hide_render", frame=start_frame - 1)

    # Show tree when growth starts
    obj.hide_viewport = False
    obj.hide_render = False
    obj.keyframe_insert(data_path="hide_viewport", frame=start_frame)
    obj.keyframe_insert(data_path="hide_render", frame=start_frame)

    # Keep it visible through end_frame, then hide again
    obj.hide_viewport = False
    obj.hide_render = False
    obj.keyframe_insert(data_path="hide_viewport", frame=end_frame)
    obj.keyframe_insert(data_path="hide_render", frame=end_frame)

    # Hide tree again after death_frame
    obj.hide_viewport = True
    obj.hide_render = True
    obj.keyframe_insert(data_path="hide_viewport", frame=death_frame)
    obj.keyframe_insert(data_path="hide_render", frame=death_frame)


def set_up_champions(
    champions: dict, spacing: float = 5.0, champions_position: tuple = (0.0, 0.0, 0.0)
) -> None:
    champions_collection = get_or_create_collection("Champions")

    for champion_name, champion in champions.items():
        tree_type_collection = get_or_create_collection(
            champion_name, champions_collection
        )
        for tree in champion:
            champions_position = (
                champions_position[0] + spacing,
                champions_position[1],
                champions_position[2],
            )
            tree_obj = tree_to_curve(
                tree, champions_position[0], champions_position[1], spacing=spacing
            )
            object_name = f"{champion_name}_{tree.age}"
            obj = bpy.data.objects.new(object_name, tree_obj)
            obj.location = champions_position
            tree_type_collection.objects.link(obj)


def set_up_terrain(noise_grid: np.ndarray, spacing: float = 1.0, scale: float = 20.0) -> None:
    """
    Set up the terrain based on the noise grid as a single mesh, centered around the origin.
    """
    n_rows, n_cols = noise_grid.shape
    verts = []
    faces = []

    # Compute centering offsets
    x_offset = (n_rows - 1) * spacing / 2
    y_offset = (n_cols - 1) * spacing / 2

    # Generate vertices (centered)
    for i in range(n_rows):
        for j in range(n_cols):
            x = i * spacing - x_offset
            y = j * spacing - y_offset
            z = scale * noise_grid[i, j]
            verts.append((x, y, z))

    # Generate quad faces
    for i in range(n_rows - 1):
        for j in range(n_cols - 1):
            a = i * n_cols + j
            b = a + 1
            c = a + n_cols
            d = c + 1
            faces.append((a, b, d, c))

    # Create mesh
    mesh = bpy.data.meshes.new("TerrainMesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()

    obj = bpy.data.objects.new("Terrain", mesh)

    # Clear existing terrains
    safe_remove_collection("Terrain")
    # Create a new collection for the terrain
    terrain_collection = get_or_create_collection("Terrain")
    # Link the object to the collection
    terrain_collection.objects.link(obj)
    

# ─────────────────────────────────────────────────────────────────────────────
#  Main simulation → bakes every generation and builds a playable animation
# ─────────────────────────────────────────────────────────────────────────────
def main():
    ### Set up simulation environment ###

    total_generations = 101  # becomes frame_end (frames 0 … 99)
    spacing = 2
    chosen_species = [
        "honda",
        "pine",
        #"shrub",
    ]

    # Create forest simulation
    forest = Forest(
        size=50,
        initial_population=0.5,
        spawn_probability=0.25,
        species_subset=chosen_species,
        scenario="temperate",
    )

    ### Set up Blender environment ###

    # Set up blender terrain
    #noise_grid = forest.noise_grid
    #set_up_terrain(noise_grid)
    
    # Set up Blender sockets for geometry nodes
    blender_sockets = {
        "birch": "Socket_3",
        "oak": "Socket_7",
        "pine": "Socket_3",
    }

    # Set up generation to frames ratio
    generation_to_frames_ratio = 5

    # Initialize geometry nodes
    geonodes = init_blender_geonodes(chosen_species)
    if not geonodes:
        print("Error: No valid geometry nodes found for the specified species.")
        return

    # Clean master collection - using improved collection handling
    master_col = get_or_create_collection("Forest Simulation")

    ## Create a collection for all posible generations
    for gen in range(total_generations):
        generation_name = f"Gen_{(1+gen):03d}"
        gen_col = get_or_create_collection(generation_name, master_col)

    # ── Bake every generation to its own collection ────────────────────────
    for gen in range(total_generations):
        print(f"Processing generation {gen}/{total_generations-1}...")
        forest.step()

        for i in range(1, forest.size + 1):
            for j in range(1, forest.size + 1):
                tree_final_state = forest.reached_termination(i, j)

                if tree_final_state is None:
                    continue

                tree_age = tree_final_state.age

                curve = tree_to_curve(tree_final_state, i - 1, j - 1, spacing=spacing)
                obj_name = f"tree_{i-1}_{j-1}_g{(2+gen-tree_age):03d}"
                obj = bpy.data.objects.new(obj_name, curve)
                obj.location = ((i - 1) * spacing, (j - 1) * spacing, 0.0)

                modifier_name = (
                    f"geoNode_{tree_final_state.genes['species']}_{obj_name}"
                )
                if tree_final_state.genes["species"] in geonodes:
                    mod = obj.modifiers.new(modifier_name, "NODES")
                    mod.node_group = geonodes[tree_final_state.genes["species"]]

                generation_name = f"Gen_{(2+gen-tree_age):03d}"
                gen_col = bpy.data.collections[generation_name]

                gen_col.objects.link(obj)

                geo_mod = obj.modifiers[modifier_name]

                # Animate the tree
                animate_tree(
                    tree_final_state,
                    tree_age,
                    gen,
                    generation_to_frames_ratio,
                    obj,
                    geo_mod,
                    blender_sockets,
                )

    # Add champion trees to the collection
    #champions = forest.campions
    #champions_position = (50.0, 50.0, 0.0)
    #set_up_champions(champions, spacing, champions_position)

    print(f"Forest simulation complete with {total_generations} generations.")


if __name__ == "__main__":
    main()
    #total_generations = 365  # becomes frame_end (frames 0 … 99)
    #spacing = 2
    #chosen_species = [
    #    "pine",
    #]  # , "shrub"]
#
    ## Create forest simulation
    #forest = Forest(
    #    size=100,
    #    initial_population=0.5,
    #    spawn_probability=0.25,
    #    species_subset=chosen_species,
    #)
#
    #### Set up Blender environment ###
#
    ## Set up blender terrain
    #noise_grid = forest.noise_grid
    #print(noise_grid)
    #set_up_terrain(noise_grid)
