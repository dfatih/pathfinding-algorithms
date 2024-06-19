import tkinter as tk
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

        self.last_data = {'D*': {'time': '-', 'memory': '-'}, 'D* Lite': {'time': '-', 'memory': '-'}}

    def run_d_star(self):
        self.root.destroy()  # Close the menu window
        root = tk.Tk()
        app = MainApplicationDStar(root)
        start_time = time.time()
        app.update_gui()
        end_time = time.time()
        memory_usage = psutil.Process().memory_info().rss / (1024 * 1024)  # Memory usage in MB
        self.last_data['D*'] = {'time': f"{end_time - start_time:.1f} sec", 'memory': f"{memory_usage:.1f} MB"}
        self.print_table()
        root.mainloop()

    def run_d_star_lite(self):
        self.root.destroy()  # Close the menu window
        root = tk.Tk()
        app = MainApplicationDStarLite(root)
        start_time = time.time()
        app.update_gui()
        end_time = time.time()
        memory_usage = psutil.Process().memory_info().rss / (1024 * 1024)  # Memory usage in MB
        self.last_data['D* Lite'] = {'time': f"{end_time - start_time:.1f} sec", 'memory': f"{memory_usage:.1f} MB"}
        self.print_table()
        root.mainloop()

    def print_table(self):
        print("Algorithm\tTotal Time\tMemory Usage")
        for algo, data in self.last_data.items():
            print(f"{algo}\t{data['time']}\t{data['memory']}")

if __name__ == '__main__':
    root = tk.Tk()
    menu = MainMenu(root)
    root.mainloop()
