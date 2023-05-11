from typing import Callable

import pygame

from src import colours
from src.cellular_automata import CellularAutomata
from math import cos, sin

from src.painter import Painter


class CellGrid:
    def __init__(self, rule: Callable, dimensions: tuple[int, int]) -> None:
        # Initialise grid parameters
        self.rule = rule
        self.seed = None

        self.cell_width = None
        self.cell_height = None
        self.cell_margin = None

        self.pad_width = None
        self.pad_height = None

        self.width = None
        self.height = None
        self.window_size = None
        self.surface = None

        # Setup cell dimension defaults
        self.set_cell_dimensions(5, 5, 1)

        # Setup default number of cells in grid
        self.set_dimensions(dimensions)
        self.set_window_size()
        self.set_ca()

        # Setup Painter object
        self.set_painter()

        # Setup grid colours
        self.bg_colour = colours.BLACK
        self.empty_space_colour = colours.WHITE
        self.cell_colour = colours.RED

        # debug
        self.print_params()

    def set_cell_dimensions(self, width: int, height: int, margin: int) -> None:
        self.cell_height = height
        self.cell_width = width
        self.cell_margin = margin

    def set_dimensions(self, dimensions: tuple[int, int]) -> None:
        self.height = dimensions[0]
        self.width = dimensions[1]

    def set_window_size(self) -> None:
        grid_window_height = (
            (self.height * self.cell_height)
            + (self.height * self.cell_margin)
            + self.cell_margin
        )

        grid_window_width = (
            (self.width * self.cell_width)
            + (self.width * self.cell_margin)
            + self.cell_margin
        )

        self.surface = pygame.Surface((grid_window_width, grid_window_height))
        self.window_size = (grid_window_width, grid_window_height)

    def set_seed(self, seed: int | list[int] | None) -> None:
        self.seed = seed
        self.ca.set_seed(seed)

    def set_rule(self, rule: Callable) -> None:
        self.rule = rule

    def set_ca(self) -> None:
        self.ca = CellularAutomata([self.height, self.width], self.rule, self.seed)

    def update(self) -> None:
        self.ca.update_grid()

    def set_painter(self) -> None:
        self.painter = Painter(self)

    def click(self, pos, padding) -> None:
        col = (pos[0] - padding[0]) // (self.cell_width + self.cell_margin)
        row = (pos[1] - padding[1]) // (self.cell_height + self.cell_margin)

        if not self.is_position_in_grid(row, col):
            return

        # invert cell state
        self.ca.grid[row][col] = not self.ca.grid[row][col]

        # self.draw_circle(pos, padding)
        print(f"Mouse down: {pos} at Grid: {row},{col}")

    # Drawing functions start
    def paint(self, previous_pos, current_pos, padding, brush_size, shape) -> None:
        self.painter(previous_pos, current_pos, padding, brush_size, shape=shape)

    def erase(self, previous_pos, current_pos, padding, brush_size) -> None:
        self.painter(previous_pos, current_pos, padding, brush_size, erase=True)

    # Drawing functions end

    def is_position_in_grid(self, row, col) -> bool:
        row_in_bounds = self.height > row >= 0
        col_in_bounds = self.width > col >= 0

        return row_in_bounds and col_in_bounds

    def draw(self, surface: pygame.Surface | None = None) -> None:
        if not surface:
            surface = self.surface
        surface.fill(self.bg_colour)
        for row in range(self.height):
            for col in range(self.width):
                colour = self.empty_space_colour
                if self.ca.grid[row][col] == 1:
                    colour = self.cell_colour
                start_pos = (
                    (self.cell_margin + self.cell_width) * col + self.cell_margin,
                    (self.cell_margin + self.cell_height) * row + self.cell_margin,
                )
                cell_rect = pygame.Rect(start_pos, (self.cell_width, self.cell_height))
                pygame.draw.rect(surface, colour, cell_rect)

    # debug
    def print_params(self) -> None:
        print(
            (
                f"Cell Size: {self.cell_width} x {self.cell_height}, "
                f"Margin: {self.cell_margin}"
            )
        )
        print(f"Grid Dimensions: {self.width} x {self.height}")
        print(f"Grid Window Size: {self.window_size}")
        print(f"Grid Background Colour: {self.bg_colour}")
        print(f"Empty Space Colour: {self.empty_space_colour}")
