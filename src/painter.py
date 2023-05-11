from math import cos, sin
from src.stamp_tool import StampTool


class Painter:
    def __init__(self, cell_grid) -> None:
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
        shape="Circle",
    ) -> None:
        # padding = (self.cell_grid.pad_width, self.cell_grid.pad_height)

        if erase:
            self.fill_value = 0
        else:
            self.fill_value = 1

        self.paint(previous_pos, current_pos, padding, brush_size, shape)

    def paint(self, previous_pos, current_pos, padding, brush_size, shape) -> None:
        if not previous_pos or not current_pos:
            return

        if shape != "Circle":
            # Draw the shape at the current position
            self.stamp_tool(current_pos, padding, shape)
            return

        # Draw the circle at the current position
        self.draw_circle(current_pos, padding, brush_size)

        # Interpolate between the previous position and the current position
        self.interpolate_cells(previous_pos, current_pos, padding, brush_size)

    def erase(self, previous_pos, current_pos, padding, brush_size) -> None:
        if not previous_pos or not current_pos:
            return

        # Draw the circle at the current position
        self.draw_circle(current_pos, padding, brush_size)

        # Interpolate between the previous position and the current position
        self.interpolate_cells(previous_pos, current_pos, padding, brush_size)

    def draw_circle(self, pos, padding, brush_size) -> None:
        for i in range(-brush_size, brush_size + 1):
            for j in range(-brush_size, brush_size + 1):
                if i * i + j * j <= brush_size * brush_size:
                    fill_x = int(pos[0] + i)
                    fill_y = int(pos[1] + j)
                    self.fill_cell((fill_x, fill_y), padding)

    def fill_cell(self, pos, padding):
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
        row_in_bounds = self.cell_grid.grid_height > row >= 0
        col_in_bounds = self.cell_grid.grid_width > col >= 0

        return row_in_bounds and col_in_bounds
