from math import cos, sin
from src.stamp_tool import StampTool


class Painter:
    """
    A class used to represent a Painter which can paint or erase shapes on a CellGrid.
    ...

    Attributes
    ----------
    cell_grid : object
        The grid on which to paint or erase shapes.
    fill_value : int
        The value to fill the grid cells with.
    stamp_tool : object
        The tool to stamp shapes on the grid.

    Methods
    -------
    __call__(
        previous_pos, current_pos, padding, brush_size,
        erase=False, hover=False shape="Circle"
    ):
        Calls the paint method with the given parameters.
    paint(previous_pos, current_pos, padding, brush_size, shape):
        Paints or stamp a shape on the grid.
    erase(previous_pos, current_pos, padding, brush_size):
        Erases on the grid.
    draw_circle(pos, padding, brush_size):
        Draws a circle at the given position on the grid.
    fill_cell(pos, padding):
        Fills a cell at the given position on the grid.
    interpolate_cells(previous_pos, current_pos, padding, brush_size):
        Interpolates cells between two positions on the grid.
    is_position_in_grid(row, col):
        Checks if a given position is within the grid boundaries.
    """

    def __init__(self, cell_grid) -> None:
        """
        Constructs all the attributes for the Painter object.

        Parameters
        ----------
        cell_grid : object
            The grid on which to paint or erase shapes.
        """
        self.cell_grid = cell_grid
        self.fill_value = 1
        self.stamp_tool = StampTool(self.cell_grid)

    def __call__(
        self,
        previous_pos,
        current_pos,
        padding,
        brush_size,
        erase=False,
        hover=False,
        shape="Circle",
    ) -> None:
        # padding = (self.cell_grid.pad_width, self.cell_grid.pad_height)

        if erase:
            self.fill_value = 0
        elif hover:
            self.fill_value = -1
        else:
            self.fill_value = 1

        self.paint(previous_pos, current_pos, padding, brush_size, shape, hover)

    def paint(
        self, previous_pos, current_pos, padding, brush_size, shape, hover=False
    ) -> None:
        """
        Paints or stamps a shape on the grid.

        Parameters
        ----------
        previous_pos : tuple
            The previous position of the mouse on the window.
        current_pos : tuple
            The current position of the mouse on the window.
        padding : tuple
            The padding is the margin between the edge of the window and the grid.
        brush_size : int
            The size of the brush.
        shape : str
            The shape to paint.
        """
        if not hover:
            if not previous_pos or not current_pos:
                return

        if shape != "Circle":
            # Draw the shape at the current position
            self.stamp_tool(current_pos, padding, shape, hover)
            return
        elif hover:
            return

        # Draw the circle at the current position
        self.draw_circle(current_pos, padding, brush_size)

        # Interpolate between the previous position and the current position
        self.interpolate_cells(previous_pos, current_pos, padding, brush_size)

    def erase(self, previous_pos, current_pos, padding, brush_size) -> None:
        """
        Erases cells on the grid.

        Parameters
        ----------
        previous_pos : tuple
            The previous position of the mouse on the window.
        current_pos : tuple
            The current position of the mouse on the window.
        padding : tuple
            The padding is the margin between the edge of the window and the grid.
        brush_size : int
            The size of the brush.
        """
        if not previous_pos or not current_pos:
            return

        # Draw the circle at the current position
        self.draw_circle(current_pos, padding, brush_size)

        # Interpolate between the previous position and the current position
        self.interpolate_cells(previous_pos, current_pos, padding, brush_size)

    def draw_circle(self, pos, padding, brush_size) -> None:
        """
        Draws a circle at a given position on the grid.

        Parameters
        ----------
        pos : tuple
            The position on the grid to draw the circle.
        padding : tuple
            The padding is the margin between the edge of the window and the grid.
        brush_size : int
            The size of the brush (radius of the circle).
        """
        for i in range(-brush_size, brush_size + 1):
            for j in range(-brush_size, brush_size + 1):
                if i * i + j * j <= brush_size * brush_size:
                    fill_x = int(pos[0] + i)
                    fill_y = int(pos[1] + j)
                    self.fill_cell((fill_x, fill_y), padding)

    def fill_cell(self, pos, padding):
        """
        Fills a cell at a given position on the grid.

        Parameters
        ----------
        pos : tuple
            The position on the grid to fill the cell.
        padding : tuple
            The padding is the margin between the edge of the window and the grid.
        """
        col = (pos[0] - padding[0]) // (
            self.cell_grid.cell_width + self.cell_grid.cell_margin
        )
        row = (pos[1] - padding[1]) // (
            self.cell_grid.cell_height + self.cell_grid.cell_margin
        )

        if not self.is_position_in_grid(row, col):
            return

        self.cell_grid.ca.grid[row][col] = self.fill_value

    def interpolate_cells(self, previous_pos, current_pos, padding, brush_size) -> None:
        """
        Interpolates cells between two positions on the grid.

        Parameters
        ----------
        previous_pos : tuple
            The previous position of the mouse on the window.
        current_pos : tuple
            The current position of the mouse on the window.
        padding : tuple
            The padding is the margin between the edge of the window and the grid.
        brush_size : int
            The size of the brush.
        """
        dx = abs(current_pos[0] - previous_pos[0])
        dy = abs(current_pos[1] - previous_pos[1])

        if dx == 0 and dy == 0:
            return

        step_size = 1 / max(dx, dy)
        t = 0.0
        while t < 1:
            x = int((1 - t) * previous_pos[0] + (t * current_pos[0]))
            y = int((1 - t) * previous_pos[1] + (t * current_pos[1]))

            self.fill_cell((x, y), padding)
            self.draw_circle((x, y), padding, brush_size)

            t = t + step_size

    def is_position_in_grid(self, row, col) -> bool:
        """
        Checks if a given position is within the grid boundaries.

        Parameters
        ----------
        row : int
            The row number of the position.
        col : int
            The column number of the position.

        Returns
        -------
        bool
            True if the position is within the grid boundaries, False otherwise.
        """
        row_in_bounds = self.cell_grid.grid_height > row >= 0
        col_in_bounds = self.cell_grid.grid_width > col >= 0

        return row_in_bounds and col_in_bounds
