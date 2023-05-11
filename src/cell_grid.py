from typing import Callable

import pygame

from src import colours
from src.cellular_automata import CellularAutomata

from src.painter import Painter


class CellGrid:
    """
    A class used to represent a CellGrid for cellular automata simulation.
    ...

    Attributes
    ----------
    rule : Callable
        The rule to update the state of the cellular automata.
    seed : int or list[int] or None
        The seed for the cellular automata, used to generate grid.
    cell_width : int
        The width of a cell in the grid.
    cell_height : int
        The height of a cell in the grid.
    cell_margin : int
        The margin between cells in the grid.
    pad_width : int
        The width of the padding around the grid.
    pad_height : int
        The height of the padding around the grid.
    width : int
        The width of the grid in number of cells.
    height : int
        The height of the grid in number of cells.
    window_size : tuple[int, int]
        The size of the grid window.
    grid_surface : pygame.Surface
        The actual surface of the grid.
    visible_surface : pygame.Surface
        The visible surface of the grid.
    scaled_window : pygame.Surface
        The scaled window of the grid for zooming.
    allow_zoom : bool
        Whether zooming is allowed or not.
    zoom : float
        The current zoom level.
    visible_offset : tuple[int, int]
        The offset of the visible area from the top-left corner of the grid.
    bg_colour : tuple[int, int, int]
        The color of the background of the grid.
    empty_space_colour : tuple[int, int, int]
        The color of the empty spaces in the grid.
    cell_colour : tuple[int, int, int]
        The color of the cells in the grid.
    painter : Painter
        The painter object used to draw on the grid.

    Methods
    -------
    set_cell_dimensions(width, height, margin):
        Sets the dimensions of the cells in the grid.
    set_dimensions(visible_dimensions, grid_dimensions):
        Sets the dimensions of the grid.
    set_window_size():
        Sets the size of the grid window.
    toggle_zoom():
        Toggles zooming.
    zoom_in():
        Zooms in the grid.
    zoom_out():
        Zooms out the grid.
    set_zoom(out):
        Sets the zoom level of the grid.
    set_seed(seed):
        Sets the seed for the cellular automata.
    set_rule(rule):
        Sets the rule for the cellular automata.
    set_ca():
        Sets the cellular automata object.
    update():
        Updates the state of the cellular automata.
    set_painter():
        Sets the painter object.
    click(pos, padding):
        Performs a click action on the grid.
    paint(previous_pos, current_pos, padding, brush_size, shape):
        Paints on the grid.
    erase(previous_pos, current_pos, padding, brush_size):
        Erases from the grid.
    is_position_in_grid(row, col):
        Checks if a position is within the grid boundaries.
    draw(surface):
        Draws the grid.
    print_params():
        Prints the parameters of the grid.
    """

    def __init__(
        self,
        rule: Callable,
        visible_dimensions: tuple[int, int],
        grid_dimensions: tuple[int, int],
    ) -> None:
        """
        Initializes the CellGrid object with the given rule, visible_dimensions,
        and grid_dimensions.

        Parameters
        ----------
        rule : Callable
            The rule to update the state of the cellular automata.
        visible_dimensions : tuple[int, int]
            The dimensions of the visible grid, i.e., the
            part of the grid displayed on screen.
            Format: (height, width).
        grid_dimensions : tuple[int, int]
            The dimensions of the actual grid.
            This can be larger than visible_dimensions.
            Format: (height, width).

        Attributes Initialized
        ----------------------
        rule : Callable
            Rule for updating the grid.
        seed : None
            Seed for generating the initial state of the grid.
        cell_width, cell_height, cell_margin : None
            Cell dimensions and margin in the grid.
        pad_width, pad_height : None
            Padding dimensions around the grid.
        width, height : None
            Dimensions of the grid (in terms of number of cells).
        window_size : None
            Size of the window displaying the grid.
        grid_surface : None
            The pygame.Surface object representing the actual grid.
        visible_surface : None
            The pygame.Surface object representing the visible part of the grid.
        scaled_window : None
            The pygame.Surface object representing the zoomed view of the grid.
        allow_zoom : bool
            Whether zooming is allowed or not.
        zoom : float
            The current zoom level.
        visible_offset : tuple[int, int]
            The offset of the visible area from the top-left corner of the grid.
        bg_colour : tuple[int, int, int]
            The background color of the grid.
        empty_space_colour : tuple[int, int, int]
            The color of the empty spaces in the grid.
        cell_colour : tuple[int, int, int]
            The color of the cells in the grid.
        """

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
        """
        Set the dimensions for a cell in the grid.

        Parameters
        ----------
        width : int
            The width of a cell.
        height : int
            The height of a cell.
        margin : int
            The margin around a cell.
        """
        self.cell_height = height
        self.cell_width = width
        self.cell_margin = margin

    def set_dimensions(
        self, visible_dimensions: tuple[int, int], grid_dimensions: tuple[int, int]
    ) -> None:
        """
        Set the dimensions for the visible grid and the entire grid.

        Parameters
        ----------
        visible_dimensions : tuple[int, int]
            The dimensions of the visible grid.
            Format: (height, width).
        grid_dimensions : tuple[int, int]
            The dimensions of the actual grid.
            This can be larger than visible_dimensions.
            Format: (height, width).
        """
        self.height = visible_dimensions[0]
        self.width = visible_dimensions[1]

        self.grid_height = grid_dimensions[0]
        self.grid_width = grid_dimensions[1]

    def set_window_size(self) -> None:
        """
        Set the size of the window displaying the grid.

        This method calculates the size of the grid surface and the
        visible surface based on thegrid dimensions and cell dimensions,
        and then sets the window size.
        """
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
        """
        Toggle the ability to zoom in or out on the grid.

        If zoom is currently allowed, it will be disallowed, and vice versa.
        """
        self.allow_zoom = not self.allow_zoom

    def zoom_in(self) -> None:
        """
        Increase the zoom level of the grid.

        This method calls set_zoom() with False to indicate that
        the zoom level should be increased.
        """
        self.set_zoom(False)

    def zoom_out(self) -> None:
        """
        Decrease the zoom level of the grid.

        This method calls set_zoom() with True to indicate that
        the zoom level should be decreased.
        """
        self.set_zoom(True)

    def set_zoom(self, out: bool | None = None) -> None:
        """
        Set the zoom level for the grid.

        Parameters
        ----------
        out : bool, optional
            Determines the direction of the zoom. If True, the grid will
            be zoomed out. If False, the grid will be zoomed in.
            If None, the zoom level remains unchanged.
        """
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
        """
        Set the seed for the cellular automata.

        Parameters
        ----------
        seed : int or list of int or None
            The seed for the cellular automata.
        """
        self.seed = seed
        self.ca.set_seed(seed)

    def set_rule(self, rule: Callable) -> None:
        """
        Set the rule for the cellular automata.

        Parameters
        ----------
        rule : Callable
            The function that defines the rule for the cellular automata.
        """
        self.rule = rule

    def set_ca(self) -> None:
        """
        Initialize the cellular automata with the current rule and seed.
        """
        self.ca = CellularAutomata(
            [self.grid_height, self.grid_width], self.rule, self.seed
        )

    def update(self) -> None:
        """
        Update the grid of the cellular automata.
        """
        self.ca.update_grid()

    def set_painter(self) -> None:
        """
        Initialize the Painter object.
        """
        self.painter = Painter(self)

    def click(self, pos, padding) -> None:
        """
        Handle a mouse click event.

        Parameters
        ----------
        pos : tuple
            The position of the mouse click.
        padding : tuple
            The padding around the grid.
        """
        col = (pos[0] - padding[0]) // (self.cell_width + self.cell_margin)
        row = (pos[1] - padding[1]) // (self.cell_height + self.cell_margin)

        if not self.is_position_in_grid(row, col):
            return

        # invert cell state
        self.ca.grid[row][col] = not self.ca.grid[row][col]

        print(f"Mouse down: {pos} at Grid: {row},{col}")

    def paint(
        self,
        previous_pos: tuple,
        current_pos: tuple,
        padding: tuple,
        brush_size: int,
        shape: str,
    ) -> None:
        """
        Paint a shape onto the grid.

        Parameters
        ----------
        previous_pos : tuple
            The previous position of the mouse.
        current_pos : tuple
            The current position of the mouse.
        padding : tuple
            The padding around the grid.
        brush_size : int
            The size of the brush.
        shape : str
            The shape to be painted.
        """
        self.painter(previous_pos, current_pos, padding, brush_size, shape=shape)

    def erase(
        self, previous_pos: tuple, current_pos: tuple, padding: tuple, brush_size: tuple
    ) -> None:
        """
        Erase from the grid.

        Parameters
        ----------
        previous_pos : tuple
            The previous position of the mouse.
        current_pos : tuple
            The current position of the mouse.
        padding : tuple
            The padding around the grid.
        brush_size : int
            The size of the brush.
        """
        self.painter(previous_pos, current_pos, padding, brush_size, erase=True)

    def is_position_in_grid(self, row, col) -> bool:
        """
        Check if a given position is within the bounds of the grid.

        Parameters
        ----------
        row : int
            The row index.
        col : int
            The column index.

        Returns
        -------
        bool
            True if the position is within the bounds of the grid, False otherwise.
        """
        row_in_bounds = self.grid_height > row >= 0
        col_in_bounds = self.grid_width > col >= 0

        return row_in_bounds and col_in_bounds

    def draw(self, surface: pygame.Surface | None = None) -> None:
        """
        Draw the grid onto a surface.

        Parameters
        ----------
        surface : pygame.Surface, optional
            The surface onto which the grid is drawn.
            If None, the grid's surface is used.
        """
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
        """
        Print the parameters of the grid to the console for debugging.
        """
        print(
            (
                f"Cell Size: {self.cell_width} x {self.cell_height}, "
                f"Margin: {self.cell_margin}"
            )
        )
        print(f"Grid Dimensions: {self.grid_width} x {self.grid_height}")
        print(f"Grid Size: {self.grid_surface.get_size()}")
        print(f"Grid Window Size: {self.window_size}")
        print(f"Grid Background Colour: {self.bg_colour}")
        print(f"Empty Space Colour: {self.empty_space_colour}")
