class ShapeTool:
    def __init__(self, cell_grid) -> None:
        self.cell_grid = cell_grid

    def __call__(self, current_pos, padding, shape: list[list[int]]) -> None:
        self.stamp_shape(current_pos, padding, shape)

    def stamp_shape(self, pos, padding, shape: list[list[int]]) -> None:
        shape_height = len(shape)
        shape_width = len(shape[0])

        for row_offset, row in enumerate(shape):
            for col_offset, cell in enumerate(row):
                row_index = (pos[1] - padding[1]) // (
                    self.cell_grid.cell_height + self.cell_grid.cell_margin
                ) + row_offset
                col_index = (pos[0] - padding[0]) // (
                    self.cell_grid.cell_width + self.cell_grid.cell_margin
                ) + col_offset

                if self.cell_grid.is_position_in_grid(row_index, col_index):
                    self.cell_grid.ca.grid[row_index][col_index] = cell
