def game_of_life_rule(grid: list[list[int]], i: int, j: int):
    """
    Apply the Game of Life rule to a cell in a given grid.

    Parameters
    ----------
    grid : list[list[int]]
        The grid of cells.
    i : int
        The row index of the cell.
    j : int
        The column index of the cell.

    Returns
    -------
    int
        The new state of the cell (0 for dead, 1 for alive) based on the Game of Life rule.
    """
    neighbours = 0
    # count number of neighbours
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0:
                continue
            if grid[(i + x) % len(grid)][(j + y) % len(grid[0])] == 1:
                neighbours += 1
    if grid[i][j] == 1:  # if cell is alive
        if neighbours < 2:  # if cell has less than 2 neighbours, it dies
            return 0
        elif neighbours > 3:  # if cell has more than 3 neighbours, it dies
            return 0
        else:  # if cell has 2 or 3 neighbours, it lives
            return 1
    else:  # if cell is dead
        if neighbours == 3:  # if cell has 3 neighbours, it becomes alive
            return 1
        else:  # if cell has less than 3 or more than 3 neighbours, it stays dead
            return 0


def rule_30(grid: list[list[int]], i: int, j: int):
    """
    Apply Rule 30 to a cell in a given grid.

    Parameters
    ----------
    grid : list[list[int]]
        The grid of cells.
    i : int
        The row index of the cell.
    j : int
        The column index of the cell.

    Returns
    -------
    int
        The new state of the cell (0 for dead, 1 for alive) based on Rule 30.
    """
    neighbours = 0
    # count number of neighbours
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0:
                continue
            if grid[(i + x) % len(grid)][(j + y) % len(grid[0])] == 1:
                neighbours += 1
    if grid[i][j] == 1:
        if neighbours == 3:
            return 0
        else:
            return 1
    else:
        if neighbours == 1:
            return 1
        else:
            return 0


def rule_90(grid: list[list[int]], i: int, j: int):
    """
    Apply Rule 90 to a cell in a given grid.

    Parameters
    ----------
    grid : list[list[int]]
        The grid of cells.
    i : int
        The row index of the cell.
    j : int
        The column index of the cell.

    Returns
    -------
    int
        The new state of the cell (0 for dead, 1 for alive) based on Rule 90.
    """
    neighbours = 0
    # count number of neighbours
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0:
                continue
            if grid[(i + x) % len(grid)][(j + y) % len(grid[0])] == 1:
                neighbours += 1
    if grid[i][j] == 1:
        if neighbours == 2:
            return 0
        else:
            return 1
    else:
        if neighbours == 1:
            return 1
        else:
            return 0


def rule_110(grid: list[list[int]], i: int, j: int):
    """
    Apply Rule 110 to a cell in a given grid.

    Parameters
    ----------
    grid : list[list[int]]
        The grid of cells.
    i : int
        The row index of the cell.
    j : int
        The column index of the cell.

    Returns
    -------
    int
        The new state of the cell (0 for dead, 1 for alive) based on Rule 110.
    """
    neighbours = 0
    # count number of neighbours
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0:
                continue
            if grid[(i + x) % len(grid)][(j + y) % len(grid[0])] == 1:
                neighbours += 1
    if grid[i][j] == 1:
        if neighbours == 1 or neighbours == 2:
            return 0
        else:
            return 1
    else:
        if neighbours == 1:
            return 1
        else:
            return 0


def rule_184(grid: list[list[int]], i: int, j: int):
    """
    Apply Rule 184 to a cell in a given grid.

    Parameters
    ----------
    grid : list[list[int]]
        The grid of cells.
    i : int
        The row index of the cell.
    j : int
        The column index of the cell.

    Returns
    -------
    int
        The new state of the cell (0 for dead, 1 for alive) based on Rule 184.
    """
    neighbours = 0
    # count number of neighbours
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0:
                continue
            if grid[(i + x) % len(grid)][(j + y) % len(grid[0])] == 1:
                neighbours += 1
    if grid[i][j] == 1:
        if neighbours == 1 or neighbours == 3:
            return 0
        else:
            return 1
    else:
        if neighbours == 1:
            return 1
        else:
            return 0
