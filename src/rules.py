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
        
def rule_30(grid, i, j):
    neighbours = 0
    #count number of neighbours
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
    #count number of neighbours
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
    #count number of neighbours
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
    #count number of neighbours
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