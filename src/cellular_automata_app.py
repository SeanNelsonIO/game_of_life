import pygame
import pygame_gui

from pygame_gui.ui_manager import UIManager

from src import rules
from src import colours
from src.cellular_automata import CellularAutomata


class CellularAutomataApp:
    def __init__(self) -> None:
        pygame.init()

        # Setup cell dimension defaults
        self.set_cell_dimensions(5, 5, 1)

        # Setup default number of cells in grid
        self.set_grid_dimensions(100, 100)
        self.set_grid_padding(100, 100)
        self.set_grid_window_size()

        # Setup grid colours
        self.bg_grid_colour = colours.BLACK
        self.empty_space_colour = colours.WHITE
        self.cell_colour = colours.RED

        # Setup Cellular Automata defaults
        self.rule = rules.game_of_life_rule
        self.seed = None
        self.set_ca()

        # Setup UI elements
        self.window_size = (800, 800)
        self.window_surface = pygame.display.set_mode(self.window_size)
        self.ui_manager = UIManager(self.window_size, "data/themes/theme.json")

        self.background = pygame.Surface(self.window_size)
        self.background.fill(self.ui_manager.ui_theme.get_colour("dark_bg"))

        self.create_ui()

        self.clock = pygame.time.Clock()
        self.is_running = True
        self.is_paused = True

        self.print_params()

    def create_ui(self) -> None:
        pass

    def set_cell_dimensions(self, width: int, height: int, margin: int) -> None:
        self.cell_height = height
        self.cell_width = width
        self.cell_margin = margin

    def set_grid_dimensions(self, width: int, height: int) -> None:
        self.grid_height = height
        self.grid_width = width

    def set_grid_padding(self, width: int = 0, height: int = 0) -> None:
        self.pad_width = width
        self.pad_height = height

    def set_grid_window_size(self) -> None:
        grid_window_height = (
            (self.grid_height * self.cell_height)
            + (self.grid_height * self.cell_margin)
            + self.cell_margin
        )

        grid_window_width = (
            (self.grid_width * self.cell_width)
            + (self.grid_width * self.cell_margin)
            + self.cell_margin
        )

        self.grid_surface = pygame.Surface((grid_window_width, grid_window_height))
        self.grid_window_size = (grid_window_width, grid_window_height)

    # debug
    def print_params(self) -> None:
        print(
            (
                f"Cell Size: {self.cell_width} x {self.cell_height}, "
                f"Margin: {self.cell_margin}"
            )
        )
        print(f"Grid Dimensions: {self.grid_width} x {self.grid_height}")
        print(f"Grid Window Size: {self.grid_window_size}")
        print(f"Grid Background Colour: {self.bg_grid_colour}")
        print(f"Empty Space Colour: {self.empty_space_colour}")

    def set_ca(self) -> None:
        self.ca = CellularAutomata(
            [self.grid_height, self.grid_width], self.rule, self.seed
        )

    def pause(self) -> None:
        self.is_paused = not self.is_paused

    def process_mouseclick(self) -> None:
        pos = pygame.mouse.get_pos()
        col = (pos[0] - self.pad_width) // (self.cell_width + self.cell_margin)
        row = (pos[1] - self.pad_height) // (self.cell_height + self.cell_margin)

        if not self.is_position_in_grid(row, col):
            return

        # invert cell state
        self.ca.grid[row][col] = not self.ca.grid[row][col]
        print(f"Mouse down: {pos} at Grid: {row},{col}")

    def is_position_in_grid(self, row, col) -> bool:

        row_in_bounds = self.grid_height > row >= 0
        col_in_bounds = self.grid_width > col >= 0

        return row_in_bounds and col_in_bounds

    def process_keypress(self, key) -> None:
        if key == pygame.K_SPACE:
            self.pause()
        if self.is_paused and key == pygame.K_RETURN:
            self.ca.update_grid()

    def process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                self.process_keypress(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.process_mouseclick()

            self.ui_manager.process_events(event)

        if not self.is_paused:
            self.ca.update_grid()

    def draw_grid(self, surface: pygame.Surface) -> None:
        surface.fill(self.bg_grid_colour)
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                colour = self.empty_space_colour
                if self.ca.grid[row][col] == 1:
                    colour = self.cell_colour
                start_pos = (
                    (self.cell_margin + self.cell_width) * col + self.cell_margin,
                    (self.cell_margin + self.cell_height) * row + self.cell_margin,
                )
                cell_rect = pygame.Rect(start_pos, (self.cell_width, self.cell_height))
                pygame.draw.rect(surface, colour, cell_rect)

    def run(self) -> None:
        while self.is_running:
            time_delta = self.clock.tick(60) / 1000.0

            self.process_events()

            self.ui_manager.update(time_delta)

            self.window_surface.blit(self.background, (0, 0))
            self.ui_manager.draw_ui(self.window_surface)

            self.draw_grid(self.grid_surface)
            self.window_surface.blit(
                self.grid_surface, (self.pad_width, self.pad_height)
            )

            pygame.display.update()
