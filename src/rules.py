def game_of_life_rule(grid, i, j):
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


def rule_30(grid, i, j):
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


def rule_90(grid, i, j):
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


def rule_110(grid, i, j):
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


def rule_184(grid, i, j):
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
