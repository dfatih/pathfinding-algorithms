import tkinter as tk
import yaml
from main_d_Star import MainApplication as MainApplicationDStar
from main_d_Lite import MainApplication as MainApplicationDStarLite
import time
import psutil

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Algorithm Selection")

        self.label = tk.Label(self.root, text="Select Algorithm:")
        self.label.pack()

        self.d_star_button = tk.Button(self.root, text="D*", command=self.run_d_star)
        self.d_star_button.pack()

        self.d_star_lite_button = tk.Button(self.root, text="D* Lite", command=self.run_d_star_lite)
        self.d_star_lite_button.pack()

        self.run_data_d_star = []  # List to store run data for D*
        self.run_data_d_star_lite = []  # List to store run data for D* Lite

        # Load previously saved data
        self.load_data("d_star_data.yaml", self.run_data_d_star)
        self.load_data("d_star_lite_data.yaml", self.run_data_d_star_lite)

    def load_data(self, filename, run_data_list):
        try:
            with open(filename, 'r') as file:
                loaded_data = yaml.safe_load(file)
                if loaded_data:
                    run_data_list.extend(loaded_data)
        except FileNotFoundError:
            pass

    def save_data(self, filename, run_data_list):
        with open(filename, 'w') as file:
            yaml.dump(run_data_list, file)

    def run_d_star(self):
        self.run_algorithm(MainApplicationDStar, self.run_data_d_star)

    def run_d_star_lite(self):
        self.run_algorithm(MainApplicationDStarLite, self.run_data_d_star_lite)

    def run_algorithm(self, algorithm_class, run_data_list):
        self.root.destroy()  # Close the menu window
        root = tk.Tk()
        app = algorithm_class(root)
        start_time = time.time()

        def check_goal_reached():
            if app.goal_reached():  # Check if the goal is reached
                end_time = time.time()
                memory_usage = psutil.Process().memory_info().rss / (1024 * 1024)  # Memory usage in MB
                algorithm_data = {'time': f"{end_time - start_time:.1f} sec", 'memory': f"{memory_usage:.1f} MB"}
                run_data_list.append(algorithm_data)
                self.save_data("d_star_data.yaml", self.run_data_d_star)
                self.save_data("d_star_lite_data.yaml", self.run_data_d_star_lite)
                self.print_table()  # Print the table immediately after the algorithm finishes
                root.destroy()  # Close the GUI window
            else:
                app.update_gui()
                root.after(100, check_goal_reached)  # Check goal reached again after 100 ms

        check_goal_reached()  # Start checking for goal reached
        root.mainloop()

    def print_table(self):
        print("Algorithm   Total Time  Memory Usage")
        self.print_algorithm_data(self.run_data_d_star, "D*")
        self.print_algorithm_data(self.run_data_d_star_lite, "D* Lite")
        self.print_combined_data()

    def print_algorithm_data(self, run_data_list, algorithm_name):
        for data in run_data_list:
            print(f"{algorithm_name}{''.ljust(8)}{data['time'].ljust(12)}{data['memory']}")

    def print_combined_data(self):
        if self.run_data_d_star and self.run_data_d_star_lite:
            print("Combined Data")
            max_runs = max(len(self.run_data_d_star), len(self.run_data_d_star_lite))
            for i in range(max_runs):
                d_star_data = self.run_data_d_star[i] if i < len(self.run_data_d_star) else {'time': '-', 'memory': '-'}
                d_star_lite_data = self.run_data_d_star_lite[i] if i < len(self.run_data_d_star_lite) else {'time': '-', 'memory': '-'}
                print(f"D*       {d_star_data['time']} sec{''.ljust(12)}{d_star_data['memory']}")
                print(f"D* Lite  {d_star_lite_data['time']} sec{''.ljust(12)}{d_star_lite_data['memory']}")

if __name__ == '__main__':
    root = tk.Tk()
    menu = MainMenu(root)
    root.mainloop()
