import numpy as np
import heapq
import time

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

class DStar:
    def __init__(self, map, s_start, s_goal):
        self.map = map
        self.s_start = s_start
        self.s_goal = s_goal

        self.g = np.ones((map.x_dim, map.y_dim)) * np.inf
        self.rhs = np.ones((map.x_dim, map.y_dim)) * np.inf
        self.g[s_goal] = 0
        self.rhs[s_goal] = 0

        self.open_list = PriorityQueue()
        self.k_m = 0
        self.open_list.put(s_goal, self.calculate_key(s_goal))

        self.place_random_obstacles(10, 100)

        self.visited_nodes = []

        print(f"Initializing D* with start: {s_start}, goal: {s_goal}, map size: {map.x_dim}x{map.y_dim}")
        print("Map grid with obstacles:")
        print(self.map.grid)

    def place_random_obstacles(self, min_obstacles, max_obstacles):
        num_obstacles = np.random.randint(min_obstacles, max_obstacles)
        for _ in range(num_obstacles):
            x = np.random.randint(0, self.map.x_dim)
            y = np.random.randint(0, self.map.y_dim)
            if (x, y) != self.s_start and (x, y) != self.s_goal:
                self.map.grid[x, y] = -1
        print("Obstacles placed at:")
        for i in range(self.map.x_dim):
            for j in range(self.map.y_dim):
                if self.map.grid[i, j] == -1:
                    print(f"({i}, {j})")

    def calculate_key(self, s):
        g_rhs = min(self.g[s], self.rhs[s])
        return (g_rhs + self.heuristic(self.s_start, s) + self.k_m, g_rhs)

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def update_vertex(self, u):
        if u != self.s_goal:
            neighbors = self.get_neighbors(u)
            self.rhs[u] = min([self.g[neighbor] + 1 for neighbor in neighbors if self.map.grid[neighbor] != -1])
        self.open_list.put(u, self.calculate_key(u))

    def get_neighbors(self, s):
        x, y = s
        neighbors = []
        if x > 0 and self.map.grid[x - 1, y] != -1:
            neighbors.append((x - 1, y))
        if x < self.map.x_dim - 1 and self.map.grid[x + 1, y] != -1:
            neighbors.append((x + 1, y))
        if y > 0 and self.map.grid[x, y - 1] != -1:
            neighbors.append((x, y - 1))
        if y < self.map.y_dim - 1 and self.map.grid[x, y + 1] != -1:
            neighbors.append((x, y + 1))
        return neighbors

    def compute_shortest_path(self):
        print("Computing shortest path...")
        start_time = time.time()
        iterations = 0
        while not self.open_list.empty():
            iterations += 1
            u = self.open_list.get()
            self.visited_nodes.append(u)
            if self.g[u] > self.rhs[u]:
                self.g[u] = self.rhs[u]
                for s in self.get_neighbors(u):
                    self.update_vertex(s)
            else:
                self.g[u] = np.inf
                self.update_vertex(u)
                for s in self.get_neighbors(u):
                    self.update_vertex(s)
            if time.time() - start_time > 10:  # 10 seconds timeout for the computation
                print(f"Timeout during shortest path computation after {iterations} iterations")
                break
        print(f"Shortest path computed in {iterations} iterations.")
        return self.extract_path()

    def move_and_replan(self, robot_position):
        print(f"Moving and replanning from position: {robot_position}")
        self.s_start = robot_position
        self.k_m += self.heuristic(self.s_start, self.s_goal)
        path = self.compute_shortest_path()
        print(f"Path: {path}")
        return path, self.visited_nodes

    def extract_path(self):
        path = []
        current = self.s_start
        while current != self.s_goal:
            path.append(current)
            neighbors = self.get_neighbors(current)
            current = min(neighbors, key=lambda s: self.g[s])
            if self.g[current] == np.inf:
                print("Path blocked or goal unreachable.")
                break
        path.append(self.s_goal)
        return path
