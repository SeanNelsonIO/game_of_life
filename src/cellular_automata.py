from typing import Callable

import ast
import random
import numpy as np


class CellularAutomata:
    def __init__(self, grid_size: int, rule: Callable, seed: int | list[int] = None):
        self.grid_size = grid_size
        self.rule = rule
        self.seed = seed

        # Create empty grid - all values set to zero
        self.grid = self.create_grid()
        if seed:
            self.set_seed(seed)

    def create_grid(self) -> None:
        grid = []
        for i in range(self.grid_size[0]):
            grid.append([])
            for j in range(self.grid_size[1]):
                grid[i].append(0)
        return grid

    def set_seed(self, seed: int | list[int] | None):
        self.seed = seed
        # Clear grid if setting no seed
        if not seed:
            self.grid = self.create_grid()
            return

        np.random.seed(seed)
        self.populate_grid_with_seed()

    def populate_grid_with_seed(self) -> None:
        self.grid = np.random.randint(2, size=(self.grid_size[0], self.grid_size[1]))
        self.grid = self.grid.tolist()

    def populate_grid_with_state_file(
        self, file_path: str, load_seed: bool = True
    ) -> None:
        file = open(file_path, "r")
        lines = file.readlines()
        if load_seed:
            self.interpret_seed_str(lines[0])

        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                self.grid[i][j] = int(lines[i + 1][j])
        file.close()

    def interpret_seed_str(self, seed_str):
        raw_seed = seed_str.split(":")[1]
        self.seed = ast.literal_eval(raw_seed)

    def update_grid(self) -> None:
        new_grid = np.zeros((self.grid_size[0], self.grid_size[1]), dtype=int)
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                new_grid[i][j] = self.rule(self.grid, i, j)
        self.grid = new_grid

    def get_grid(self) -> list[list[int]]:
        return self.grid

    def save_grid_to_file(self, file_name: str) -> None:
        file = open(file_name, "w")
        file.write(f"Seed:{self.seed}\n")
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                file.write(str(int(self.grid[i][j])))
            file.write("\n")
        file.close()
