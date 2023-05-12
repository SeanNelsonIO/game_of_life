from typing import Callable

import ast
import numpy as np


class CellularAutomata:
    """
    A class to model a cellular automaton grid and its evolution over time.

    Attributes
    ----------
    grid_size : list
        Size of the grid for the cellular automaton.
    rule : Callable
        Rule function to evolve the cellular automaton.
    seed : int | list[int] | None
        Seed for the random number generator or specific initial grid.
    grid : np.ndarray
        Grid for the cellular automaton.

    Methods
    -------
    set_seed(seed: int | list[int] | None)
        Set the seed for the random number generator or specific initial grid.
    populate_grid_with_seed()
        Populate the grid using the current seed.
    populate_grid_with_state_file(file_path: str, load_seed: bool = True)
        Populate the grid with state from a specified file.
    interpret_seed_str(seed_str)
        Interpret and set the seed from a string.
    update_grid()
        Update the grid based on the rule function.
    get_grid()
        Get the current grid.
    save_grid_to_file(file_name: str)
        Save the current grid to a file.
    """

    def __init__(self, grid_size: list, rule: Callable, seed: int | list[int] = None):
        """
        Initialize the CellularAutomata class.

        Parameters
        ----------
        grid_size : list
            The size of the grid for the cellular automaton.
        rule : Callable
            The function defining the rule of the cellular automaton.
        seed : int, list[int], optional
            The seed for the random number generator or specific initial grid. Default is None.
        """
        self.grid_size = grid_size
        self.rule = rule
        self.seed = seed

        # Create empty grid
        self.grid = np.zeros((self.grid_size[0], self.grid_size[1]), dtype=int)
        if seed:
            self.set_seed(seed)

    def set_seed(self, seed: int | list[int] | None):
        """
        Set the seed for the random number generator or specific initial grid.

        Parameters
        ----------
        seed : int, list[int], None
            The seed for the random number generator or specific initial grid.
        """
        self.seed = seed
        # Clear grid if setting no seed
        if not seed:
            self.grid = np.zeros((self.grid_size[0], self.grid_size[1]), dtype=int)
            return

        np.random.seed(seed)
        self.populate_grid_with_seed()

    def populate_grid_with_seed(self) -> None:
        """
        Populate the grid using the current seed.
        """
        self.grid = np.random.randint(2, size=(self.grid_size[0], self.grid_size[1]))

    def populate_grid_with_state_file(
        self, file_path: str, load_seed: bool = True
    ) -> None:
        """
        Populate the grid with the state from a specified file.

        Parameters
        ----------
        file_path : str
            The path to the file.
        load_seed : bool, default is True
            If true, load the seed from the file.
        """
        with open(file_path, "r") as file:
            lines = file.readlines()
        if load_seed:
            self.interpret_seed_str(lines[0])

        state_width = len(lines[1]) - 1
        state_height = len(lines) - 1
        self.grid = np.zeros(self.grid_size)

        for i in range(min(self.grid_size[0], state_height)):
            for j in range(min(self.grid_size[1], state_width)):
                self.grid[i][j] = lines[i + 1][j]

    def interpret_seed_str(self, seed_str) -> None:
        """
        Interpret and set the seed from a string.

        Parameters
        ----------
        seed_str : str
            The string from which to interpret the seed.
        """
        raw_seed = seed_str.split(":")[1]
        self.seed = ast.literal_eval(raw_seed)

    def update_grid(self) -> None:
        """
        Update the grid based on the rule function.
        """
        new_grid = np.zeros(self.grid_size, dtype=int)
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                new_grid[i, j] = self.rule(self.grid, i, j)
        self.grid = new_grid

    def get_grid(self) -> np.ndarray:
        """
        Get the current grid.

        Returns
        -------
        np.ndarray
            The current grid of the cellular automaton.
        """
        return self.grid

    def save_grid_to_file(self, file_name: str) -> None:
        """
        Save the current grid to a file.

        Parameters
        ----------
        file_name : str
            The name of the file to which the grid should be saved.
        """
        with open(file_name, "w") as file:
            file.write(f"Seed:{self.seed}\n")
            for i in range(self.grid_size[0]):
                file.write(
                    "".join(str(int(self.grid[i, j])) for j in range(self.grid_size[1]))
                    + "\n"
                )
