import pygame

from cellular_automata import CellularAutomata
from rules import game_of_life_rule

HEIGHT = 5
WIDTH = 5

MARGIN = 1

GRID_HEIGHT = 100
GRID_WIDTH = 100

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()

window_height = (GRID_HEIGHT * HEIGHT) + MARGIN + (GRID_HEIGHT * MARGIN)
window_width = (GRID_WIDTH * WIDTH) + MARGIN + (GRID_WIDTH * MARGIN)

WINDOW_SIZE = [window_height, window_width]

ca = CellularAutomata([GRID_HEIGHT, GRID_WIDTH], game_of_life_rule, seed=1234)

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Game of Life")


def run_game_loop(ca) -> None:
    game_loop = True

    clock = pygame.time.Clock()

    paused = True

    while game_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Handle game exit
                game_loop = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle clicking on grid
                pos = pygame.mouse.get_pos()
                col = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)

                ca.grid[row][col] = not ca.grid[row][col]
                print(f"Mouse down: {pos} at Grid: {row},{col}")
            elif event.type == pygame.KEYDOWN:
                # Handle keypress to draw next update
                if paused and event.key == pygame.K_RETURN:
                    ca.update_grid()

                if event.key == pygame.K_SPACE:
                    paused = not paused

        if not paused:
            ca.update_grid()

        screen.fill(BLACK)

        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                colour = WHITE
                if ca.grid[row][col] == 1:
                    colour = RED
                pygame.draw.rect(
                    screen,
                    colour,
                    [
                        (MARGIN + WIDTH) * col + MARGIN,
                        (MARGIN + HEIGHT) * row + MARGIN,
                        WIDTH,
                        HEIGHT,
                    ],
                )

        clock.tick(60)
        pygame.display.flip()
    pygame.quit()


run_game_loop(ca)
