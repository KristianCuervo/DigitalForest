import sys
sys.path.append(r'\\wsl.localhost\Ubuntu-24.04\home\kristiancuervo\DigitalForest')

import bpy
import numpy as np
from forestLibrary.forest import Forest
from forestLibrary.tree import Tree
from forestLibrary.lsystem_utils import realize


# ─────────────────────────────────────────────────────────────────────────────
#  Helper functions
# ─────────────────────────────────────────────────────────────────────────────
def initialize_blender_cells(size: tuple[int, int],
                             spacing: float = 5.0,
                             collection_name: str = "Cells"):
    """
    Place a CURVE object at every grid coordinate so the layout is visible
    in the viewport (optional, but handy while modelling).
    """
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
    offset = np.array([i * spacing, 0.0, j * spacing])

    curve = bpy.data.curves.new(f"tree_{i}_{j}", type='CURVE')
    curve.dimensions = '3D'

    for v0, v1 in edges:
        spl = curve.splines.new('POLY')
        spl.points.add(1)                            # two points total
        spl.points[0].co = (* (verts[v0] + offset), 1.0)
        spl.points[0].radius = radii[v0]
        spl.points[1].co = (* (verts[v1] + offset), 1.0)
        spl.points[1].radius = radii[v1]

    return curve


# ─────────────────────────────────────────────────────────────────────────────
#  Main simulation → bakes every generation and builds a playable animation
# ─────────────────────────────────────────────────────────────────────────────
def main():
    # Simulation / animation parameters
    total_generations = 100           # becomes frame_end (frames 0 … 99)
    spacing           = 1.0

    forest = Forest(size=10,
                    initial_population=0.5,
                    spawn_probability=0.25,
                    species_subset=["honda", "bush"])

    # Optional helpers to see the grid layout while the sim runs
    initialize_blender_cells((forest.size, forest.size), spacing=spacing)

    # Clean master collection
    master_col = bpy.data.collections.get("Generations")
    if master_col is None:
        master_col = bpy.data.collections.new("Generations")
        bpy.context.scene.collection.children.link(master_col)
    else:
        for sub in list(master_col.children):
            bpy.data.collections.remove(sub, do_unlink=True)

    # ── Bake every generation to its own collection ────────────────────────
    for gen in range(total_generations):
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
                obj   = bpy.data.objects.new(
                           f"tree_{i-1}_{j-1}_g{gen:03d}", curve)
                obj.location = ((i - 1) * spacing, 0.0, (j - 1) * spacing)
                gen_col.objects.link(obj)

        # ── Create an instance and keyframe its visibility ─────────────────
        inst = bpy.data.objects.new(f"GenInst_{gen:03d}", None)
        inst.instance_type       = 'COLLECTION'
        inst.instance_collection = gen_col
        bpy.context.scene.collection.objects.link(inst)

        # Three key-frames ensure the instance is visible ONLY on frame `gen`
        start_hide = gen - 1 if gen > 0 else 0  # avoid negative frames

        # hidden before its own frame
        inst.hide_viewport = True
        inst.hide_render   = True
        inst.keyframe_insert("hide_viewport", frame=start_hide)
        inst.keyframe_insert("hide_render",   frame=start_hide)

        # shown on its frame
        inst.hide_viewport = False
        inst.hide_render   = False
        inst.keyframe_insert("hide_viewport", frame=gen)
        inst.keyframe_insert("hide_render",   frame=gen)

        # hidden afterwards
        inst.hide_viewport = True
        inst.hide_render   = True
        inst.keyframe_insert("hide_viewport", frame=gen + 1)
        inst.keyframe_insert("hide_render",   frame=gen + 1)

        # constant (step) interpolation so visibility jumps, not fades
        for fc in inst.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = 'CONSTANT'

    # Scene framing so the play-head covers the whole simulation
    scene = bpy.context.scene
    scene.frame_start = 0
    scene.frame_end   = total_generations - 1
    scene.frame_set(0)


if __name__ == "__main__":
    main()
