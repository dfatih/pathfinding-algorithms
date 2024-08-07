import random
import numpy as np
import tkinter as tk
from gui import Animation, OccupancyGridMap
from d_star import DStar
from slam import SLAM
import time
import psutil
from display_window import DisplayWindow

class MainApplicationDStar:
    def __init__(self, root, start=(10, 10), goal=(40, 70), grid_size=100, random_seed=None, headless=False):
        self.root = root
        self.headless = headless
        self.display_window = DisplayWindow(self.root) if not self.headless else None
        self.total_time = 0
        self.callback = None
        self.init_gui(start, goal, grid_size, random_seed)
        if not self.headless:
            self.update_gui()
        
    def init_gui(self, start, goal, grid_size, random_seed):
        self.x_dim = grid_size
        self.y_dim = grid_size
        self.start = start
        self.goal = goal
        self.view_range = 5

        window_width = min(1920, self.x_dim * 10)
        window_height = min(1080, self.y_dim * 10)

        if random_seed is not None:
            random.seed(random_seed)
            np.random.seed(random_seed)

        if not self.headless:
            self.gui = Animation(title="D* Path Planning",
                                 width=window_width,
                                 height=window_height,
                                 margin=0,
                                 x_dim=self.x_dim,
                                 y_dim=self.y_dim,
                                 start=self.start,
                                 goal=self.goal,
                                 viewing_range=self.view_range)

        self.new_map = self.gui.world if not self.headless else OccupancyGridMap(self.x_dim, self.y_dim)
        self.old_map = self.new_map

        self.new_position = self.start
        self.last_position = self.start

        print(f"Start: {self.start}, Goal: {self.goal}, Grid Size: {self.x_dim}x{self.y_dim}")

        self.dstar = DStar(map=self.new_map, s_start=self.start, s_goal=self.goal, headless=self.headless)

        if not self.headless:
            self.slam = SLAM(map=self.new_map, view_range=self.view_range)

        self.start_time = time.time()
        self.process = psutil.Process()

    def update_gui(self):
        start_time = time.time()
        print(f"Updating GUI at time: {start_time}")

        path, visited_nodes = self.dstar.move_and_replan(robot_position=self.new_position)
        print(f"Path after replanning: {path}")

        end_time = time.time()
        elapsed_time = end_time - start_time
        self.total_time += elapsed_time
        print(f"Elapsed time for update: {elapsed_time} seconds")

        if not self.headless:
            self.display_window.update_metrics(elapsed_time, self.total_time, self.process.memory_info().rss / (1024 * 1024))

            self.gui.run_game(path=path, visited_nodes=visited_nodes)

    def goal_reached(self):
        current_position = self.new_position
        goal_position = self.goal
        distance_threshold = 1
        distance_to_goal = ((current_position[0] - goal_position[0]) ** 2 + (current_position[1] - goal_position[1]) ** 2) ** 0.5
        return distance_to_goal <= distance_threshold
