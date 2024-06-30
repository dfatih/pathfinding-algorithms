import pygame
import numpy as np

class OccupancyGridMap:
    def __init__(self, x_dim, y_dim):
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.grid = np.zeros((x_dim, y_dim))

class Animation:
    def __init__(self, title, width, height, margin, x_dim, y_dim, start, goal, viewing_range):
        pygame.init()
        self.title = title
        self.width = width
        self.height = height
        self.margin = margin
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.start = start
        self.goal = goal
        self.viewing_range = viewing_range

        window_size = (self.width, self.height)
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption(self.title)

        self.world = self.create_world(self.x_dim, self.y_dim)
        self.reset_world()

    def create_world(self, x_dim, y_dim):
        return OccupancyGridMap(x_dim, y_dim)

    def reset_world(self):
        self.world.grid[self.start[0]][self.start[1]] = 1
        self.world.grid[self.goal[0]][self.goal[1]] = 2

    def run_game(self, path):
        running = True
        clock = pygame.time.Clock()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            self.screen.fill((255, 255, 255))

            for x in range(self.world.x_dim):
                for y in range(self.world.y_dim):
                    color = (200, 200, 200) if self.world.grid[x][y] == 0 else (0, 0, 0)
                    if self.world.grid[x][y] == 1:
                        color = (0, 255, 0)
                    elif self.world.grid[x][y] == 2:
                        color = (255, 0, 0)
                    pygame.draw.rect(self.screen, color, pygame.Rect(x * 10, y * 10, 10, 10))

            for (x, y) in path:
                pygame.draw.rect(self.screen, (0, 0, 255), pygame.Rect(x * 10, y * 10, 10, 10))

            pygame.display.flip()
            clock.tick(10)

        pygame.quit()
        print("Path drawn.")
