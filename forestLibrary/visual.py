import numpy as np
from pygel3d import graph, gl_display as gl
from forestLibrary.lsystem_utils import realize
from forestLibrary.forest import Forest

def build_forest_graph(forest: Forest, grid_spacing: float = 5.0) -> graph.Graph:
    g = graph.Graph()
    for i in range(1, forest.size + 1):
        for j in range(1, forest.size + 1):
            tree = forest.grid[i, j]
            if tree is None:
                continue

            verts, edges, _ = realize(tree.lsystem)
            offset = np.array([i * grid_spacing, 0.0, j * grid_spacing], dtype=float)
            base   = len(g.nodes())
            
            for v in verts:
                g.add_node(v + offset)
            for child, parent in edges:
                g.connect_nodes(base + child, base + parent)

    return g