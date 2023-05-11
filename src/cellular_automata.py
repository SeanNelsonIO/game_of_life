from typing import Callable

import ast
import random
import numpy as np


class CellularAutomata:
    def __init__(self, grid_size: list, rule: Callable, seed: int | list[int] = None):
        self.grid_size = grid_size
        self.rule = rule
        self.seed = seed

        # Create empty grid
        self.grid = np.zeros((self.grid_size[0], self.grid_size[1]), dtype=int)
        if seed:
            self.set_seed(seed)

    def set_seed(self, seed: int | list[int] | None):
        self.seed = seed
        # Clear grid if setting no seed
        if not seed:
            self.grid = np.zeros((self.grid_size[0], self.grid_size[1]), dtype=int)
            return

        np.random.seed(seed)
        self.populate_grid_with_seed()

    def populate_grid_with_seed(self) -> None:
        self.grid = np.random.randint(2, size=(self.grid_size[0], self.grid_size[1]))

    def populate_grid_with_state_file(
        self, file_path: str, load_seed: bool = True
    ) -> None:
        with open(file_path, "r") as file:
            lines = file.readlines()
        if load_seed:
            self.interpret_seed_str(lines[0])

        self.grid = np.array(
            [
                [int(lines[i + 1][j]) for j in range(self.grid_size[1])]
                for i in range(self.grid_size[0])
            ],
            dtype=int,
        )

    def interpret_seed_str(self, seed_str) -> None:
        raw_seed = seed_str.split(":")[1]
        self.seed = ast.literal_eval(raw_seed)

    def update_grid(self) -> None:
        new_grid = np.zeros(self.grid_size, dtype=int)
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                new_grid[i, j] = self.rule(self.grid, i, j)
        self.grid = new_grid

    def get_grid(self) -> np.ndarray:
        return self.grid

    def save_grid_to_file(self, file_name: str) -> None:
        with open(file_name, "w") as file:
            file.write(f"Seed:{self.seed}\n")
            for i in range(self.grid_size[0]):
                file.write(
                    "".join(str(int(self.grid[i, j])) for j in range(self.grid_size[1]))
                    + "\n"
                )
