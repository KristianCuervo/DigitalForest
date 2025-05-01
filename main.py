import time
from forestLibrary.forest import Forest
from forestLibrary.visual import build_forest_graph
from pygel3d import gl_display as gl

def main():
    total_generations = 100
    delay            = 0.2
    spacing          = 2.0

    # 1) Create viewer once (no display yet)
    viewer = gl.Viewer()

    # 2) Set up your forest
    forest = Forest(size=20, initial_population=0.5, spawn_probability=0.25, species_subset=['honda','pine', 'shrub'])

    # 3) Loop in pure Python
    for gen in range(total_generations):
        forest.step()                                          # update sim
        g = build_forest_graph(forest, grid_spacing=spacing)  # rebuild graph

        # 4) Draw one frame, then return
        viewer.display(
            g,
            mode='w',           # wireframe, for instance
            smooth=True,
            bg_col=[1, 1, 1],   # white background
            reset_view=False,   # keep camera
            once=True           # <<< critical bit!
        )

        time.sleep(delay)  # slow it down so you can see it

if __name__ == "__main__":
    main()
