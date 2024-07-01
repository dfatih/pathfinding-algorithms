import random
import tkinter as tk
from main_d_Star import MainApplicationDStar
from main_d_Lite import MainApplicationDStarLite
import yaml
import numpy as np
import time
import psutil

class Benchmark:
    def __init__(self, headless=False):
        self.root = tk.Tk()
        self.min_window_size = 480
        self.max_window_size = 1080
        self.headless = headless

    def run_benchmark(self):
        random_seed = random.randint(0, 10000)
        random.seed(random_seed)
        np.random.seed(random_seed)
        print(f"Random seed for this run: {random_seed}")

        window_width = random.randint(self.min_window_size, self.max_window_size)
        window_height = random.randint(self.min_window_size, self.max_window_size)
        grid_size = min(window_width, window_height) // 10  # Assuming each grid cell is 10x10 pixels
        start = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
        goal = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))

        print(f"Running D* algorithm benchmark with grid size: {grid_size}, start: {start}, goal: {goal}")
        self.run_algorithm(MainApplicationDStar, 'D_star', start, goal, grid_size, random_seed)

        random.seed(random_seed)
        np.random.seed(random_seed)

        print(f"Running D* Lite algorithm benchmark with grid size: {grid_size}, start: {start}, goal: {goal}")
        self.run_algorithm(MainApplicationDStarLite, 'D_star_Lite', start, goal, grid_size, random_seed)

    def run_algorithm(self, algorithm_class, algorithm_name, start, goal, grid_size, random_seed):
        process = psutil.Process()
        start_time = time.time()
        app = algorithm_class(self.root, start, goal, grid_size, random_seed, headless=self.headless)
        end_time = time.time()
        elapsed_time = end_time - start_time
        memory_usage = process.memory_info().rss / (1024 * 1024)

        if algorithm_name == 'D_star':
            path, visited_nodes = app.dstar.extract_path(), app.dstar.visited_nodes
        else:
            path, visited_nodes = app.dstar_lite.extract_path(), app.dstar_lite.visited_nodes

        num_obstacles_found = sum(1 for (x, y) in visited_nodes if app.gui.world.grid[x, y] == -1) if not self.headless else 0

        results = {
            'algorithm': algorithm_name,
            'random_seed': random_seed,
            'window_size': [app.gui.width, app.gui.height] if not self.headless else [0, 0],
            'grid_size': [app.x_dim, app.y_dim],
            'start_node': start,
            'goal_node': goal,
            'num_nodes': app.x_dim * app.y_dim,
            'num_obstacles_total': int(np.sum(app.gui.world.grid == -1)) if not self.headless else 0,
            'num_obstacles_found': num_obstacles_found,
            'num_nodes_shortest_path': len(path),
            'num_visited_nodes': len(visited_nodes),
            'elapsed_time': elapsed_time,
            'memory_usage': memory_usage
        }

        with open(f'results_{algorithm_name}.yaml', 'a') as file:  # Change 'w' to 'a' for appending
            yaml.dump(results, file)
        print(f"Results for {algorithm_name} saved to YAML file.")

if __name__ == "__main__":
    benchmark = Benchmark(headless=False)  # Set headless to True for no GUI
    benchmark.run_benchmark()
