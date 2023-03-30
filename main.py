from src import CellularAutomata
from src import game_of_life_rule

if __name__ == "__main__":
    ca = CellularAutomata([10, 10], 1, game_of_life_rule, seed=1234)

    print(ca.grid)
    ca.update_grid()
    print(ca.grid)
