import random
import tkinter as tk
from main_d_Star import MainApplicationDStar
from main_d_Lite import MainApplicationDStarLite
import yaml
import numpy as np

class Benchmark:
    def __init__(self):
        self.root = tk.Tk()
        self.max_grid_size = 1024

    def run_benchmark(self):
        grid_size = random.randint(100, self.max_grid_size)
        start = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
        goal = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))

        print(f"Running D* algorithm benchmark with grid size: {grid_size}, start: {start}, goal: {goal}")
        self.run_algorithm(MainApplicationDStar, 'D*', start, goal, grid_size)
        print(f"Running D* Lite algorithm benchmark with grid size: {grid_size}, start: {start}, goal: {goal}")
        self.run_algorithm(MainApplicationDStarLite, 'D* Lite', start, goal, grid_size)

    def run_algorithm(self, algorithm_class, algorithm_name, start, goal, grid_size):
        app = algorithm_class(self.root, start, goal, grid_size)
        print(f"Algorithm {algorithm_name} initialized.")

        # Store the results in a YAML file
        results = {
            'algorithm': algorithm_name,
            'window_size': [app.gui.width, app.gui.height],
            'grid_size': [app.x_dim, app.y_dim],
            'start_node': start,
            'goal_node': goal,
            'num_nodes': app.x_dim * app.y_dim,
            'num_obstacles': int(np.sum(app.gui.world.grid == -1)),
            'num_nodes_shortest_path': len(app.dstar.extract_path() if algorithm_name == 'D*' else app.dstar_lite.extract_path())
        }

        with open(f'results_{algorithm_name}.yaml', 'w') as file:
            yaml.dump(results, file)
        print(f"Results for {algorithm_name} saved to YAML file.")

if __name__ == "__main__":
    benchmark = Benchmark()
    benchmark.run_benchmark()
