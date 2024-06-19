#main-d_Lite.py
import tkinter as tk
from gui import Animation
from d_star_lite import DStarLite
from grid import OccupancyGridMap, SLAM
import time
import psutil
from tabulate import tabulate

OBSTACLE = 255
UNOCCUPIED = 0

class DisplayWindow:
    def __init__(self, parent):
        self.parent = parent
        self.time_label = tk.Label(self.parent, text="Time taken:")
        self.time_label.pack()
        self.total_time_label = tk.Label(self.parent, text="Total Time:")
        self.total_time_label.pack()
        self.memory_label = tk.Label(self.parent, text="Memory usage:")
        self.memory_label.pack()
        self.metrics_table_label = tk.Label(self.parent, text="D* Lite Metrics Table:")
        self.metrics_table_label.pack()
        self.metrics_table = tk.Text(self.parent, height=10, width=50)
        self.metrics_table.pack()

    def update_metrics(self, elapsed_time, total_time, memory_usage):
        self.time_label.config(text=f"Time taken: {elapsed_time:.2f} seconds")
        self.total_time_label.config(text=f"Total Time: {total_time:.2f} seconds")
        self.memory_label.config(text=f"Memory usage: {memory_usage:.2f} MB")
        metrics_data = [["Elapsed Time (seconds)", f"{elapsed_time:.2f}"],
                        ["Total Time (seconds)", f"{total_time:.2f}"],
                        ["Memory usage (MB)", f"{memory_usage:.2f}"]]
        self.metrics_table.delete('1.0', tk.END)
        self.metrics_table.insert(tk.END, tabulate(metrics_data, headers=["Metric", "Value"], tablefmt="grid"))

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.display_window = DisplayWindow(self.root)
        self.total_time = 0  # Initialize total time
        self.callback = None  # Callback function to reopen menu
        self.init_gui()

    def init_gui(self):
        self.x_dim = 100
        self.y_dim = 80
        self.start = (10, 10)
        self.goal = (40, 70)
        self.view_range = 5

        self.gui = Animation(title="D* Lite Path Planning",
                             width=10,
                             height=10,
                             margin=0,
                             x_dim=self.x_dim,
                             y_dim=self.y_dim,
                             start=self.start,
                             goal=self.goal,
                             viewing_range=self.view_range)

        self.new_map = self.gui.world
        self.old_map = self.new_map

        self.new_position = self.start
        self.last_position = self.start

        self.dstar = DStarLite(map=self.new_map,
                               s_start=self.start,
                               s_goal=self.goal)

        self.slam = SLAM(map=self.new_map,
                         view_range=self.view_range)

        self.start_time = time.time()
        self.process = psutil.Process()

    def update_gui(self):
        start_time = time.time()  # Record start time for this update cycle

        path, g, rhs = self.dstar.move_and_replan(robot_position=self.new_position)

        end_time = time.time()
        elapsed_time = end_time - start_time  # Calculate elapsed time for this update cycle
        self.total_time += elapsed_time  # Add to total time

        self.display_window.update_metrics(elapsed_time, self.total_time, self.process.memory_info().rss / (1024 * 1024))

        # Run the GUI
        self.gui.run_game(path=path)
        self.root.after(100, self.update_gui)  # Schedule the next update

        self.new_position = self.gui.current
        new_observation = self.gui.observation
        self.new_map = self.gui.world

        if new_observation is not None:
            self.old_map = self.new_map
            self.slam.set_ground_truth_map(gt_map=self.new_map)

        if new_observation is not None:
            self.slam.set_ground_truth_map(gt_map=self.new_map)



        if self.new_position != self.last_position:
            self.last_position = self.new_position

            new_edges_and_old_costs, slam_map = self.slam.rescan(global_position=self.new_position)

            self.dstar.new_edges_and_old_costs = new_edges_and_old_costs
            self.dstar.sensed_map = slam_map

            self.start_time = time.time()
            path, g, rhs = self.dstar.move_and_replan(robot_position=self.new_position)
            end_time = time.time()
            elapsed_time = end_time - self.start_time  # Calculate elapsed time for replan
            self.total_time += elapsed_time  # Add to total time for replan

            self.display_window.update_metrics(elapsed_time, self.total_time, self.process.memory_info().rss / (1024 * 1024))
    
    def goal_reached(self):
        # Check if the goal state is reached
        # Replace this with your actual logic to check the goal state
        # For example, if the current position is close enough to the goal, return True
        current_position = self.new_position  # Assuming self.new_position holds the current position
        goal_position = self.goal  # Assuming self.goal holds the goal position
        distance_threshold = 1  # Adjust this threshold based on your application
        distance_to_goal = ((current_position[0] - goal_position[0]) ** 2 + (current_position[1] - goal_position[1]) ** 2) ** 0.5
        return distance_to_goal <= distance_threshold

if __name__ == '__main__':
    root = tk.Tk()
    app = MainApplication(root)
    app.update_gui()  # Start the update loop
    root.mainloop()
