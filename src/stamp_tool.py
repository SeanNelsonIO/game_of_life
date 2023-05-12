"""
Filename: stamp_tool.py
Primary Author: Sean Nelson
"""

import json


class StampTool:
    """
    A tool for stamping predefined shapes onto a cellular automata grid.

    Attributes
    ----------
    cell_grid : CellGrid
        The cellular automata grid on which the shapes are stamped.
    shapes : dict
        The predefined shapes that can be stamped onto the grid.

    Methods
    -------
    __init__(self, cell_grid):
        Initialize the stamp tool with a given cellular automata grid.
    __call__(self, current_pos, padding, shape):
        Stamp a given shape onto the grid at the current position.
    stamp_shape(self, pos, padding, shape):
        Stamp a given shape onto the grid at a specified position.
    load_shape(self, shape_file_name):
        Load a shape from a JSON file and add it to the list of available shapes.
    export_shape(self, shape_name, shape):
        Export a given shape to a JSON file.
    """

    def __init__(self, cell_grid) -> None:
        """
        Initialize the StampTool instance.

        Parameters
        ----------
        cell_grid : CellGrid
            The cellular automata grid on which the shapes are stamped.
        last_hover : List
            A list of the cells which have been toggled as "hovered" so they can
            be removed after being drawn.
        """
        self.cell_grid = cell_grid
        self.last_hover = []
        # default shapes
        self.shapes = {
            "Block": [[1, 1], [1, 1]],
            "Beehive": [[0, 1, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0]],
            "Blinker": [[1, 1, 1]],
            "Glider": [[1, 0, 0], [0, 1, 1], [1, 1, 0]],
            "Beacon": [[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]],
        }

        # load shapes from json files - too large
        self.load_shape("GliderGun.json")
        self.load_shape("Bomb.json")
        self.load_shape("DavidHilbert.json")

    def __call__(
        self,
        current_pos: tuple[int, int],
        padding: tuple[int, int],
        shape: str,
        hover: bool = False,
    ) -> None:
        """
        Stamp a given shape onto the grid at the current position.

        Parameters
        ----------
        current_pos : tuple
            The current position on the grid where the shape should be stamped.
        padding : tuple
            The padding to be added to the position.
        shape : str
            The name of the shape to be stamped.
        """
        self.stamp_shape(current_pos, padding, shape, hover)

    def stamp_shape(
        self,
        pos: tuple[int, int],
        padding: tuple[int, int],
        shape: str,
        hover: bool = False,
    ) -> None:
        """
        Stamp a given shape onto the grid at a specified position.

        Parameters
        ----------
        pos : tuple
            The position on the grid where the shape should be stamped.
        padding : tuple
            The padding to be added to the position.
        shape : str
            The name of the shape to be stamped.
        hover: bool
            Draw a faded version of the stamp if this
        """
        shape = self.shapes[shape]

        if hover:
            self.cell_grid.reset_hovered()

        # Don't draw stamps if off grid
        if pos[0] < padding[0] or pos[1] < padding[1]:
            return

        for row_offset, row in enumerate(shape):
            for col_offset, cell in enumerate(row):
                row_index = (pos[1] - padding[1]) // (
                    self.cell_grid.cell_height + self.cell_grid.cell_margin
                ) + row_offset
                col_index = (pos[0] - padding[0]) // (
                    self.cell_grid.cell_width + self.cell_grid.cell_margin
                ) + col_offset

                if self.cell_grid.is_position_in_grid(row_index, col_index):
                    if hover:
                        # Set empty cells to 2 if part of stamp
                        if (
                            cell == 1
                            and self.cell_grid.ca.grid[row_index][col_index] == 0
                        ):
                            self.cell_grid.ca.grid[row_index][col_index] = -1
                            self.cell_grid.hovered_cells.append((row_index, col_index))

                    elif cell == 1:
                        self.cell_grid.ca.grid[row_index][col_index] = cell

    def load_shape(self, shape_file_name: str) -> None:
        """
        Load a shape from a JSON file and add it to the list of available shapes.

        Parameters
        ----------
        shape_file_name : str
            The name of the JSON file from which to load the shape.
        """
        with open("src/shapes/" + shape_file_name, "r") as shape_file:
            shape = json.load(shape_file)

        # add shape to list of shapes
        self.shapes[shape["name"]] = shape["shape"]

    def export_shape(self, shape_name: str, shape: list[list[int]]) -> None:
        """
        Export a given shape to a JSON file.

        Parameters
        ----------
        shape_name : str
            The name of the shape to be exported.
        shape : list[list[int]]
            The grid representation of the shape to be exported.
        """
        shape_dict = {"name": shape_name, "shape": shape}

        with open("src/shapes/" + shape_name + ".json", "w") as shape_file:
            json.dump(shape_dict, shape_file, indent=4)
