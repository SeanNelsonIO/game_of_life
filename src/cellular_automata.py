import random
import numpy as np


class CellularAutomata:
    def __init__(self, grid_size, cell_size, rule, seed=None):
        self.grid_size = grid_size
        self.cell_size = cell_size  # used as a metric for UI - not used in the logic
        self.rule = rule

        # Create empty grid - all values set to zero
        self.grid = self.create_grid()

        if seed is not None:
            np.random.seed(seed)
            self.populate_grid_with_seed()

    def create_grid(self):
        grid = []
        for i in range(self.grid_size[0]):
            grid.append([])
            for j in range(self.grid_size[1]):
                grid[i].append(0)
        return grid

    def populate_grid_with_seed(self):
        self.grid = np.random.randint(2, size=(self.grid_size[0], self.grid_size[1]))

    def populate_grid_with_state_file(self, file_path):
        file = open(file_path, "r")
        lines = file.readlines()
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                self.grid[i][j] = int(lines[i][j])
        file.close()

    def update_grid(self):
        new_grid = np.zeros((self.grid_size[0], self.grid_size[1]), dtype=int)
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                new_grid[i][j] = self.rule(self.grid, i, j)
        self.grid = new_grid

    def get_grid(self):
        return self.grid

    def save_grid_to_file(self, file_name):
        file = open(file_name, "w")
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                file.write(str(self.grid[i][j]))
            file.write("\n")
        file.close()
