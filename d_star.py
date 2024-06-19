from typing import List, Tuple
from grid import OccupancyGridMap
from priority_queue import PriorityQueue, Priority
import numpy as np
from utils import heuristic, Vertex, Vertices
from tabulate import tabulate

OBSTACLE = 255
UNOCCUPIED = 0

class DStar:
    def __init__(self, map: OccupancyGridMap, s_start: Tuple[int, int], s_goal: Tuple[int, int]):
        """
        :param map: the ground truth map of the environment provided by gui
        :param s_start: start location
        :param s_goal: end location
        """
        self.s_start = s_start
        self.s_goal = s_goal
        self.k_m = 0  # accumulation
        self.U = PriorityQueue()
        self.rhs = np.ones((map.x_dim, map.y_dim)) * np.inf
        self.g = self.rhs.copy()

        self.sensed_map = OccupancyGridMap(x_dim=map.x_dim,
                                           y_dim=map.y_dim,
                                           exploration_setting='8N')

        self.rhs[self.s_goal] = 0
        self.U.insert(self.s_goal, Priority(heuristic(self.s_start, self.s_goal), 0))

    def calculate_key(self, s: Tuple[int, int]) -> Priority:
        """
        :param s: the vertex we want to calculate key
        :return: Priority class of the two keys
        """
        k1 = min(self.g[s], self.rhs[s]) + heuristic(self.s_start, s) + self.k_m
        k2 = min(self.g[s], self.rhs[s])
        return Priority(k1, k2)

    def c(self, u: Tuple[int, int], v: Tuple[int, int]) -> float:
        """
        Calculate the cost between nodes
        :param u: from vertex
        :param v: to vertex
        :return: euclidean distance to traverse. inf if obstacle in path
        """
        if not self.sensed_map.is_unoccupied(u) or not self.sensed_map.is_unoccupied(v):
            return float('inf')
        else:
            return heuristic(u, v)

    def contain(self, u: Tuple[int, int]) -> bool:
        """
        Check if vertex u is in the priority queue
        """
        return u in self.U.vertices_in_heap

    def update_vertex(self, u: Tuple[int, int]):
        """
        Update the vertex u in the priority queue
        """
        if self.g[u] != self.rhs[u] and self.contain(u):
            self.U.update(u, self.calculate_key(u))
        elif self.g[u] != self.rhs[u] and not self.contain(u):
            self.U.insert(u, self.calculate_key(u))
        elif self.g[u] == self.rhs[u] and self.contain(u):
            self.U.remove(u)

    def compute_shortest_path(self):
        """
        Compute the shortest path using the D* algorithm
        """
        iteration = 0  # Add an iteration counter for debugging
        while self.U.top_key() < self.calculate_key(self.s_start) or self.rhs[self.s_start] > self.g[self.s_start]:
            iteration += 1
            print(f"Iteration {iteration}:")
            print("Top key:", self.U.top_key())
            print("Calculate key:", self.calculate_key(self.s_start))
            print("RHS[start]:", self.rhs[self.s_start])
            print("G[start]:", self.g[self.s_start])

            u = self.U.top()
            k_old = self.U.top_key()
            k_new = self.calculate_key(u)

            if k_old < k_new:
                self.U.update(u, k_new)
            elif self.g[u] > self.rhs[u]:
                self.g[u] = self.rhs[u]
                self.U.remove(u)
                pred = self.sensed_map.succ(vertex=u)
                for s in pred:
                    if s != self.s_goal:
                        self.rhs[s] = min(self.rhs[s], self.c(s, u) + self.g[u])
                    self.update_vertex(s)
            else:
                self.g_old = self.g[u]
                self.g[u] = float('inf')
                pred = self.sensed_map.succ(vertex=u)
                pred.append(u)
                for s in pred:
                    if self.rhs[s] == self.c(s, u) + self.g_old:
                        if s != self.s_goal:
                            min_s = float('inf')
                            succ = self.sensed_map.succ(vertex=s)
                            for s_ in succ:
                                temp = self.c(s, s_) + self.g[s_]
                                if min_s > temp:
                                    min_s = temp
                            self.rhs[s] = min_s
                    self.update_vertex(u)

    def rescan(self) -> Vertices:
        """
        Perform a rescan and return new edges and old costs
        """
        new_edges_and_old_costs = self.new_edges_and_old_costs
        self.new_edges_and_old_costs = None
        return new_edges_and_old_costs

    def move_and_replan(self, robot_position: Tuple[int, int]):
        """
        Move the robot to a new position and replan the path
        """
        path = [robot_position]
        self.s_start = robot_position
        self.compute_shortest_path()

        comparison_details = []  # Initialize as an empty list

        while self.s_start != self.s_goal:
            assert (self.rhs[self.s_start] != float('inf')), "There is no known path!"

            succ = self.sensed_map.succ(self.s_start, avoid_obstacles=False)
            min_s = float('inf')
            arg_min = None

            for s_ in succ:
                temp = self.c(self.s_start, s_) + self.g[s_]
                comparison_details.append((s_, temp))  # Store comparison details
                if temp < min_s:
                    min_s = temp
                    arg_min = s_

            if arg_min is None:
                print("No valid path found.")
                return None

            self.s_start = arg_min
            path.append(self.s_start)

        # print("D* Goal reached!")
        comparison_details_table = [(f"Node {node}", cost) for node, cost in comparison_details]
        print(tabulate(comparison_details_table, headers=["Node", "Cost"]))
        return path, self.g, self.rhs

# Usage example
# Assuming map, s_start, and s_goal are appropriately defined
# map = OccupancyGridMap(...)
# s_start = (start_x, start_y)
# s_goal = (goal_x, goal_y)
# dstar = DStar(map, s_start, s_goal)
# dstar.compute_shortest_path()
# path, g_values, rhs_values = dstar.move_and_replan(robot_position=(initial_x, initial_y))
