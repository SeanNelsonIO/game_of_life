import ast
import pygame
import pygame_gui
import random

from pygame_gui.elements import (
    UIButton,
    UIHorizontalSlider,
    UILabel,
    UIPanel,
    UITextBox,
    UITextEntryLine,
    UITooltip,
)
from pygame_gui.ui_manager import UIManager

from src import rules
from src.cell_grid import CellGrid


class CellularAutomataApp:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Cellular Automata App")

        # Setup UI elements
        self.window_size = (1000, 800)
        self.window_surface = pygame.display.set_mode(self.window_size)
        self.ui_manager = UIManager(self.window_size, "data/themes/theme.json")

        self.ui_manager.preload_fonts(
            [{"name": "fira_code", "point_size": 14, "style": "bold"}]
        )

        self.background = pygame.Surface(self.window_size)
        self.background.fill(self.ui_manager.ui_theme.get_colour("dark_bg"))

        self.fps = 60

        self.control_panel = None
        self.spped_slider_label = None
        self.speed_slider = None
        self.pause_button = None
        self.next_button = None

        self.seed_panel = None
        self.random_seed_button = None
        self.seed_text_entry = None
        self.use_seed_button = None
        self.current_seed_button = None

        self.rules_panel = None
        self.rules_dropdown = None

        self.state_panel = None
        self.save_state_button = None
        self.load_state_button = None

        self.create_ui()

        self.clock = pygame.time.Clock()
        self.is_running = True
        self.is_paused = True

    def create_ui(self) -> None:
        self.ui_manager.clear_and_reset()

        # Setup Cellular Automata Grid with defaults
        default_rule = rules.game_of_life_rule
        self.grid_padding = (266, 50)
        self.cell_grid = CellGrid(default_rule, (100, 100))

        default_panel_item_rect = pygame.Rect(10, 5, 175, 30)

        self.create_control_panel(default_panel_item_rect)
        self.create_seed_panel(default_panel_item_rect)
        self.create_rules_panel(default_panel_item_rect)
        self.create_state_panel(default_panel_item_rect)

    def create_control_panel(self, panel_item_rect: pygame.Rect) -> None:
        self.control_panel = UIPanel(
            pygame.Rect(48, 48, 200, 126),
            starting_layer_height=4,
            manager=self.ui_manager,
        )

        self.spped_slider_label = UILabel(
            panel_item_rect,
            "Speed: 60 Iterations/s",
            manager=self.ui_manager,
            container=self.control_panel,
        )

        self.speed_slider = UIHorizontalSlider(
            panel_item_rect,
            60,
            (1, 120),
            manager=self.ui_manager,
            container=self.control_panel,
            anchors={"top_target": self.spped_slider_label},
        )

        self.pause_button = UIButton(
            pygame.Rect(
                panel_item_rect.x,
                panel_item_rect.y * 2,
                83,
                panel_item_rect.height,
            ),
            "Play",
            manager=self.ui_manager,
            container=self.control_panel,
            object_id="#pause_button",
            anchors={"top_target": self.speed_slider},
        )

        self.next_button = UIButton(
            pygame.Rect(
                101,
                panel_item_rect.y * 2,
                83,
                panel_item_rect.height,
            ),
            "Next",
            manager=self.ui_manager,
            container=self.control_panel,
            object_id="#next_button",
            anchors={"top_target": self.speed_slider},
        )

    def create_seed_panel(self, panel_item_rect: pygame.Rect) -> None:
        self.seed_panel = UIPanel(
            pygame.Rect(48, 16, 200, 196),
            starting_layer_height=4,
            manager=self.ui_manager,
            anchors={"top_target": self.control_panel},
        )

        self.random_seed_button = UIButton(
            pygame.Rect(
                panel_item_rect.x,
                panel_item_rect.y * 2,
                panel_item_rect.width,
                panel_item_rect.height,
            ),
            "Generate Seed",
            manager=self.ui_manager,
            container=self.seed_panel,
            object_id="#random_seed_button",
        )

        self.seed_text_entry = UITextEntryLine(
            panel_item_rect,
            manager=self.ui_manager,
            container=self.seed_panel,
            object_id="#seed_text_entry",
            placeholder_text="     Enter Seed",
            anchors={"top_target": self.random_seed_button},
        )

        self.use_seed_button = UIButton(
            panel_item_rect,
            "Use Seed",
            manager=self.ui_manager,
            container=self.seed_panel,
            object_id="#use_seed_button",
            anchors={"top_target": self.seed_text_entry},
        )

        self.current_seed_button = UIButton(
            panel_item_rect,
            text="Current Seed",
            manager=self.ui_manager,
            container=self.seed_panel,
            object_id="#view_seed_button",
            anchors={"top_target": self.use_seed_button},
        )
        self.set_current_seed_tooltip()

        self.clear_grid_button = UIButton(
            panel_item_rect,
            text="Clear Grid",
            manager=self.ui_manager,
            container=self.seed_panel,
            object_id="#clear_grid_button",
            anchors={"top_target": self.current_seed_button},
        )

    def create_rules_panel(self, panel_item_rect: pygame.Rect) -> None:
        self.rules_panel = UIPanel(
            pygame.Rect(48, 16, 200, 196),
            starting_layer_height=4,
            manager=self.ui_manager,
            anchors={"top_target": self.seed_panel},
        )

    def create_state_panel(self, panel_item_rect: pygame.Rect) -> None:
        pass

    def set_current_seed_tooltip(self) -> None:
        if not self.cell_grid.seed:
            seed = "No Seed Used"
        else:
            seed = str(self.cell_grid.seed)

        tooltip_text = (
            "<b>Current Seed:</b>" "<br>" f"<font color=#F44336>{seed}</font>"
        )
        self.current_seed_button.tool_tip_text = tooltip_text

    def set_grid_seed(self) -> None:
        seed = None
        seed_text = self.seed_text_entry.get_text().strip()
        # print(f"Seed Text: {seed_text}")
        # print(f"Seed Type: {type(seed_text)}")

        try:
            raw_seed = ast.literal_eval(seed_text)
            # print(f"Raw Seed Type: {type(raw_seed)}")
            if isinstance(raw_seed, int):
                seed = raw_seed
            elif isinstance(raw_seed, list):
                seed = [int(s) for s in raw_seed]
        except Exception:
            # print("Cannot Decipher Seed")
            pass

        if seed is not None:
            self.cell_grid.set_seed(seed)
            self.set_current_seed_tooltip()

    def pause(self) -> None:
        if self.is_paused:
            self.pause_button.set_text("Pause")
            self.is_paused = False
        else:
            self.pause_button.set_text("Play")
            self.is_paused = True

    def next(self) -> None:
        if self.is_paused:
            self.cell_grid.update()

    def process_mouseclick(self, event) -> None:
        pos = pygame.mouse.get_pos()
        self.cell_grid.click(pos, self.grid_padding)

    def process_keypress(self, event) -> None:
        if event.key == pygame.K_SPACE:
            self.pause()
        if event.key == pygame.K_RETURN:
            self.next()

    def process_button_press(self, event):
        if event.ui_element == self.pause_button:
            self.pause()

        if event.ui_element == self.next_button:
            self.next()

        if event.ui_element == self.random_seed_button:
            new_seed = random.randint(0, 100000)
            self.seed_text_entry.set_text(str(new_seed))

        if event.ui_element == self.use_seed_button:
            self.set_grid_seed()

        if event.ui_element == self.current_seed_button:
            if not self.cell_grid.seed:
                seed = "No Seed Used"
            else:
                seed = str(self.cell_grid.seed)
            self.seed_text_entry.set_text(seed)

        if event.ui_element == self.clear_grid_button:
            self.cell_grid.set_seed(None)
            self.set_current_seed_tooltip()

    def process_text_entry(self, event):
        pass

    def process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            self.ui_manager.process_events(event)

            if event.type == pygame.KEYDOWN:
                self.process_keypress(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.process_mouseclick(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                self.process_button_press(event)
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                self.process_text_entry(event)

            if self.speed_slider.has_moved_recently:
                self.fps = self.speed_slider.get_current_value()
                self.spped_slider_label.set_text(f"Speed: {self.fps} Iterations/s")

        if not self.is_paused:
            self.cell_grid.update()

    def run(self) -> None:
        while self.is_running:
            time_delta = self.clock.tick(self.fps) / 1000.0

            self.process_events()

            self.ui_manager.update(time_delta)

            self.window_surface.blit(self.background, (0, 0))
            self.ui_manager.draw_ui(self.window_surface)

            # draw grid on window
            self.cell_grid.draw()
            self.window_surface.blit(self.cell_grid.surface, self.grid_padding)

            pygame.display.update()

        pygame.display.quit()
        pygame.quit()
