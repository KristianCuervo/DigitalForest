from forestLibrary.forest import Forest


total_generations = 100

def main():
    forest = Forest(size=10, spawn_probability=0.1)
    generation = 0

    while generation < total_generations:
        forest.update_shadows()
        forest.death_or_growth()
        forest.spawn_new_trees()
        generation += 1

if __name__ == "__main__":
    main()
