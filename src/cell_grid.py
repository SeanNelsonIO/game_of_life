from typing import Callable

import pygame

from src import colours
from src.cellular_automata import CellularAutomata
from math import cos, sin


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

    def click(self, pos, padding) -> None:
        col = (pos[0] - padding[0]) // (self.cell_width + self.cell_margin)
        row = (pos[1] - padding[1]) // (self.cell_height + self.cell_margin)

        if not self.is_position_in_grid(row, col):
            return

        # invert cell state
        self.ca.grid[row][col] = not self.ca.grid[row][col]

        # self.draw_circle(pos, padding)

        print(f"Mouse down: {pos} at Grid: {row},{col}")

    def draw_circle(self, pos, padding, brush_size, fill_value=1) -> None:
        for angle in range(1, 360):
            x1 = brush_size * cos(angle * 3.1415926535 / 180)
            y1 = brush_size * sin(angle * 3.1415926535 / 180)

            circumference_x = int(pos[0] + x1)
            circumference_y = int(pos[1] + y1)

            col = (circumference_x - padding[0]) // (self.cell_width + self.cell_margin)
            row = (circumference_y - padding[1]) // (
                self.cell_height + self.cell_margin
            )

            if not self.is_position_in_grid(row, col):
                return

            self.ca.grid[row][col] = fill_value

            self.interpolate_cells(
                pos, (circumference_x, circumference_y), padding, fill_value=fill_value
            )

    # TODO: refactor this so interpolation works correctly and more efficiently
    def paint(self, previous_pos, current_pos, padding, brush_size) -> None:
        col = (current_pos[0] - padding[0]) // (self.cell_width + self.cell_margin)
        row = (current_pos[1] - padding[1]) // (self.cell_height + self.cell_margin)

        if not self.is_position_in_grid(row, col):
            return

        # self.ca.grid[row][col] = 1
        # print(f"Mouse down: {current_pos} at Grid: {row},{col}")
        self.draw_circle(current_pos, padding, brush_size)

        # interpolate between previous and current position
        self.interpolate_cells(previous_pos, current_pos, padding)

    # TODO: refactor this so interpolation works correctly and more efficiently
    def erase(self, previous_pos, current_pos, padding, brush_size) -> None:
        col = (current_pos[0] - padding[0]) // (self.cell_width + self.cell_margin)
        row = (current_pos[1] - padding[1]) // (self.cell_height + self.cell_margin)

        if not self.is_position_in_grid(row, col):
            return

        # self.ca.grid[row][col] = 0
        # print(f"Mouse down: {current_pos} at Grid: {row},{col}")

        self.draw_circle(current_pos, padding, brush_size, fill_value=0)

        # interpolate between previous and current position
        self.interpolate_cells(previous_pos, current_pos, padding, fill_value=0)

    # TODO: refactor this so interpolation works correctly and more efficiently
    def interpolate_cells(
        self, previous_pos, current_pos, padding, fill_value=1
    ) -> None:
        if previous_pos == current_pos:
            return
        if previous_pos is None:
            return

        dx = abs(current_pos[0] - previous_pos[0])
        dy = abs(current_pos[1] - previous_pos[1])

        if dx == 0 and dy == 0:
            return

        step_size = 1 / max(dx, dy)

        t = 0.0
        while t < 1:
            x = int((1 - t) * previous_pos[0] + (t * current_pos[0]))
            y = int((1 - t) * previous_pos[1] + (t * current_pos[1]))

            col = (x - padding[0]) // (self.cell_width + self.cell_margin)
            row = (y - padding[1]) // (self.cell_height + self.cell_margin)

            if not self.is_position_in_grid(row, col):
                return

            self.ca.grid[row][col] = fill_value

            t = t + step_size

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
