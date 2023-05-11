from typing import Callable

import pygame

from src import colours
from src.cellular_automata import CellularAutomata
from math import cos, sin

from src.painter import Painter


class CellGrid:
    def __init__(
        self,
        rule: Callable,
        visible_dimensions: tuple[int, int],
        grid_dimensions: tuple[int, int],
    ) -> None:
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
        self.grid_surface = None  # Actual grid's surface
        self.visible_surface = None  # The visible surface
        self.scaled_window = None

        # Zoom toggled off by default
        self.allow_zoom = False

        # Parameters for moving the grid
        self.zoom = 1.0
        self.visible_offset = (0, 0)

        # Setup cell dimension defaults
        self.set_cell_dimensions(5, 5, 1)

        # Setup default number of cells in grid
        self.set_dimensions(visible_dimensions, grid_dimensions)
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

    def set_dimensions(
        self, visible_dimensions: tuple[int, int], grid_dimensions: tuple[int, int]
    ) -> None:
        self.height = visible_dimensions[0]
        self.width = visible_dimensions[1]

        self.grid_height = grid_dimensions[0]
        self.grid_width = grid_dimensions[1]

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

        actual_grid_height = (
            (self.grid_height * self.cell_height)
            + (self.grid_height * self.cell_margin)
            + self.cell_margin
        )

        actual_grid_width = (
            (self.grid_width * self.cell_width)
            + (self.grid_width * self.cell_margin)
            + self.cell_margin
        )

        self.grid_surface = pygame.Surface((actual_grid_width, actual_grid_height))
        self.visible_surface = pygame.Surface((grid_window_width, grid_window_height))

        self.set_zoom()
        self.window_size = (grid_window_width, grid_window_height)

    def toggle_zoom(self) -> None:
        self.allow_zoom = not self.allow_zoom

    def zoom_in(self) -> None:
        self.set_zoom(False)

    def zoom_out(self) -> None:
        self.set_zoom(True)

    def set_zoom(self, out: bool | None = None) -> None:
        prev_zoom = self.zoom

        if out is not None:
            if out:
                self.zoom /= 1.1
            else:
                self.zoom *= 1.1

        self.zoom_size = (
            int(self.grid_surface.get_width() / self.zoom),
            int(self.grid_surface.get_height() / self.zoom),
        )

        self.zoom_area = pygame.Rect(0, 0, *self.zoom_size)
        if (
            self.zoom_area.height > self.grid_surface.get_height()
            or self.zoom_area.width > self.grid_surface.get_height()
        ):
            # Clamp max size to overall grid size
            self.zoom_area = self.grid_surface.get_rect()
            self.zoom = prev_zoom

        print(self.zoom_area)
        self.zoom_area.center = (
            int(self.grid_surface.get_width() / 2),
            int(self.grid_surface.get_height() / 2),
        )

    def set_seed(self, seed: int | list[int] | None) -> None:
        self.seed = seed
        self.ca.set_seed(seed)

    def set_rule(self, rule: Callable) -> None:
        self.rule = rule

    def set_ca(self) -> None:
        self.ca = CellularAutomata(
            [self.grid_height, self.grid_width], self.rule, self.seed
        )

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
        row_in_bounds = self.grid_height > row >= 0
        col_in_bounds = self.grid_width > col >= 0

        return row_in_bounds and col_in_bounds

    def draw(self, surface: pygame.Surface | None = None) -> None:
        if not surface:
            surface = self.grid_surface
        surface.fill(self.empty_space_colour)

        for row in range(self.grid_height):
            # Draw Horizontal Grid Lines
            row_line_start = (0, (self.cell_margin + self.cell_height) * row)
            row_line_end = (
                self.grid_surface.get_height(),
                (self.cell_margin + self.cell_height) * row,
            )
            pygame.draw.line(
                surface,
                self.bg_colour,
                row_line_start,
                row_line_end,
                self.cell_margin,
            )

            for col in range(self.grid_width):
                # Draw Vertical Grid Lines
                if row == 0:
                    col_line_start = ((self.cell_width + self.cell_margin) * col, 0)
                    col_line_end = (
                        (self.cell_width + self.cell_margin) * col,
                        self.grid_surface.get_width(),
                    )
                    pygame.draw.line(
                        surface,
                        self.bg_colour,
                        col_line_start,
                        col_line_end,
                        self.cell_margin,
                    )

                # Draw Alive Cells
                if self.ca.grid[row][col] == 0:
                    continue
                start_pos = (
                    (self.cell_margin + self.cell_width) * col + self.cell_margin,
                    (self.cell_margin + self.cell_height) * row + self.cell_margin,
                )
                cell_rect = pygame.Rect(start_pos, (self.cell_width, self.cell_height))
                pygame.draw.rect(surface, self.cell_colour, cell_rect)

        if self.allow_zoom:
            self.visible_surface.blit(self.grid_surface, (0, 0), self.zoom_area)
            self.visible_surface = pygame.transform.scale(
                self.visible_surface, self.window_size
            )
        else:
            self.visible_surface = self.grid_surface

        # self.visible_surface.blit(scaled_subsurface, self.visible_offset)

    # debug
    def print_params(self) -> None:
        print(
            (
                f"Cell Size: {self.cell_width} x {self.cell_height}, "
                f"Margin: {self.cell_margin}"
            )
        )
        print(f"Grid Dimensions: {self.grid_width} x {self.grid_height}")
        print(
            f"Grid Size: {self.grid_surface.get_width()} x {self.grid_surface.get_height()}"
        )
        print(f"Grid Window Size: {self.window_size}")
        print(f"Grid Background Colour: {self.bg_colour}")
        print(f"Empty Space Colour: {self.empty_space_colour}")
