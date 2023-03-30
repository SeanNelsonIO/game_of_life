class CellularAutomata:
    def __init__(self, grid_size, cell_size, rule, seed):
        self.grid_size = grid_size
        self.cell_size = cell_size #used as a metric for UI - not used in the logic
        self.rule = rule
        self.seed = seed
        self.grid = self.create_grid()
        self.populate_grid_with_seed()

    def create_grid(self):
        grid = []
        for i in range(self.grid_size[0]):
            grid.append([])
            for j in range(self.grid_size[1]):
                grid[i].append(0)
        return grid

    def populate_grid_with_seed(self):
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                self.grid[i][j] = self.seed[j]

    def populate_grid_with_state_file(self, file_path):
        file = open(file_path, "r")
        lines = file.readlines()
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                self.grid[i][j] = int(lines[i][j])
        file.close()

    def update_grid(self):
        new_grid = self.create_grid()
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                new_grid[i][j] = self.rule(self.grid, i, j)
        self.grid = new_grid

    def get_grid(self):
        return self.grid
    
    def save_grid_to_file(self, file_name):
        file = open(file_name, "w")
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                file.write(str(self.grid[i][j]))
            file.write("\n")
        file.close()

def game_of_life_rule(grid, i, j):
    neighbours = 0
    #count number of neighbours
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0:
                continue
            if grid[(i + x) % len(grid)][(j + y) % len(grid[0])] == 1:
                neighbours += 1
    if grid[i][j] == 1:
        if neighbours < 2:
            return 0
        elif neighbours > 3:
            return 0
        else:
            return 1
    else:
        if neighbours == 3:
            return 1
        else:
            return 0