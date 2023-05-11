import ast
import os
import pygame
import pygame_gui
import random

from pygame_gui.elements import (
    UIButton,
    UIDropDownMenu,
    UIHorizontalSlider,
    UILabel,
    UIPanel,
    UITextBox,
    UITextEntryLine,
    UITooltip,
)
from pygame_gui.ui_manager import UIManager
from pygame_gui.windows import UIFileDialog, UIConfirmationDialog

from src import rules
from src.cell_grid import CellGrid


class CellularAutomataApp:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Cellular Automata App")

        # Setup UI elements
        self.window_size = (1400, 1000)
        self.window_surface = pygame.display.set_mode(self.window_size)
        # self.zoom_size = (int(self.window_size[0]/self.zoom), int(self.window_size[1]/self.zoom))

        self.ui_manager = UIManager(self.window_size, "data/themes/theme.json")

        self.ui_manager.preload_fonts(
            [{"name": "fira_code", "point_size": 14, "style": "bold"}]
        )

        self.background = pygame.Surface(self.window_size)
        self.background.fill(self.ui_manager.ui_theme.get_colour("dark_bg"))

        self.fps = 60
        self.debug_mode = False

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
        self.rules_label = None
        self.rules_dropdown = None

        self.state_panel = None
        self.save_state_button = None
        self.load_state_button = None
        self.file_dialog = None
        self.overwrite_dialog = None

        self.create_ui()

        self.clock = pygame.time.Clock()
        self.is_running = True
        self.is_paused = True

    def create_ui(self) -> None:
        self.ui_manager.clear_and_reset()

        # Setup Cellular Automata Grid with defaults
        default_rule = rules.game_of_life_rule
        self.grid_padding = (266, 50)
        self.cell_grid = CellGrid(default_rule, (100, 100), (150, 150))

        default_panel_item_rect = pygame.Rect(10, 5, 175, 30)

        self.create_control_panel(default_panel_item_rect)
        self.create_seed_panel(default_panel_item_rect)
        self.create_rules_panel(default_panel_item_rect)

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
        print(self.use_seed_button.get_object_ids())

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
            pygame.Rect(48, 16, 200, 191),
            starting_layer_height=4,
            manager=self.ui_manager,
            anchors={"top_target": self.seed_panel},
        )

        self.rules_label = UILabel(
            panel_item_rect,
            "Rule:",
            manager=self.ui_manager,
            container=self.rules_panel,
        )

        self.rules_dropdown = UIDropDownMenu(
            ["Game of Life", "Rule 30", "Rule 90", "Rule 110", "Rule 184"],
            "Game of Life",
            panel_item_rect,
            manager=self.ui_manager,
            container=self.rules_panel,
            anchors={"top_target": self.rules_label},
        )

        self.rules_state_button = UIButton(
            panel_item_rect,
            "Load Rule State",
            manager=self.ui_manager,
            container=self.rules_panel,
            anchors={"top_target": self.rules_dropdown},
        )

        self.save_state_button = UIButton(
            panel_item_rect,
            "Save Grid State",
            manager=self.ui_manager,
            container=self.rules_panel,
            anchors={"top_target": self.rules_state_button},
        )

        self.load_state_button = UIButton(
            panel_item_rect,
            "Load Grid State",
            manager=self.ui_manager,
            container=self.rules_panel,
            anchors={"top_target": self.save_state_button},
        )

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

        try:
            raw_seed = ast.literal_eval(seed_text)
            if isinstance(raw_seed, int):
                seed = raw_seed
            elif isinstance(raw_seed, list):
                seed = [int(s) for s in raw_seed]
        except Exception:
            pass

        if seed is not None:
            self.cell_grid.set_seed(seed)
            self.set_current_seed_tooltip()

    def set_cell_rule(self, rule_string: str) -> None:
        rule = None
        if rule_string == "Game of Life":
            rule = rules.game_of_life_rule
        elif rule_string == "Rule 30":
            rule = rules.rule_30
        elif rule_string == "Rule 90":
            rule = rules.rule_90
        elif rule_string == "Rule 110":
            rule = rules.rule_110
        elif rule_string == "Rule 184":
            rule = rules.rule_184

        if rule:
            self.cell_grid.set_rule(rule)

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

    def save_state(self, path: str) -> None:
        if os.path.isfile(path):
            dialog_text = (
                f"The specified file at path: <b>{path}</b> "
                "already exists, are you sure you want to overwrite this file?"
            )
            self.overwrite_dialog = UIConfirmationDialog(
                pygame.Rect(160, 50, 440, 250),
                manager=self.ui_manager,
                window_title="Confirm Overwrite",
                action_short_name="Overwrite",
                action_long_desc=dialog_text,
                blocking=True,
            )
            self.overwrite_dialog.overwrite_path = path
            return

        _, ext = os.path.splitext(path)
        if not ext == ".state":
            path += ".state"

        self.cell_grid.ca.save_grid_to_file(path)

    def load_state(self, path: str) -> None:
        self.cell_grid.ca.populate_grid_with_state_file(path)
        if self.cell_grid.ca.seed:
            self.seed_text_entry.set_text(str(self.cell_grid.ca.seed))

    def create_file_dialog(self, load: bool) -> None:
        if load:
            title = "Load Grid State"
        else:
            title = "Save Grid State"

        self.file_dialog = UIFileDialog(
            pygame.Rect(160, 50, 440, 500),
            self.ui_manager,
            window_title=title,
            initial_file_path="grid_states/",
            allow_picking_directories=False,
            allow_existing_files_only=load,
            allowed_suffixes={".state"},
        )
        self.file_dialog.load = load

    def process_mouseclick(self, event: pygame.event.Event) -> None:
        pos = pygame.mouse.get_pos()
        if self.file_dialog or self.overwrite_dialog:
            return

        if event.button == 4:  # scroll up
            self.cell_grid.zoom_in()
        elif event.button == 5:  # scroll down
            self.cell_grid.zoom_out()
        if event.button == 1:  # Mouse click
            self.cell_grid.click(pos, self.grid_padding)

    def process_keypress(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_SPACE:
            self.pause()
        if event.key == pygame.K_RETURN:
            self.next()
        if event.key == pygame.K_d:
            self.debug_mode = not self.debug_mode
            self.ui_manager.set_visual_debug_mode(self.debug_mode)

    def process_button_press(self, event: pygame.event.Event) -> None:
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

        if event.ui_element == self.rules_state_button:
            rule_string = self.cell_grid.rule.__name__
            rule_state_path = f"grid_states/rule_defaults/{rule_string}.state"
            self.load_state(rule_state_path)

        if event.ui_element == self.save_state_button:
            self.create_file_dialog(False)
            self.save_state_button.disable()
            self.load_state_button.disable()
        if event.ui_element == self.load_state_button:
            self.create_file_dialog(True)
            self.save_state_button.disable()
            self.load_state_button.disable()

    def process_dropdown_change(self, event: pygame.event.Event) -> None:
        if event.ui_element == self.rules_dropdown:
            self.set_cell_rule(self.rules_dropdown.selected_option)

    def process_window_close(self, event: pygame.event.Event) -> None:
        if event.ui_element == self.file_dialog:
            self.save_state_button.enable()
            self.load_state_button.enable()
            self.file_dialog = None

        if event.ui_element == self.overwrite_dialog:
            self.overwrite_dialog = None

    def process_file_dialog_selection(self, event: pygame.event.Event) -> None:
        if not self.file_dialog.load:
            self.save_state(event.text)

        else:
            self.load_state(event.text)
        print(event.text)

    def process_confirmation_dialog_confirmed(self, event: pygame.event.Event):
        self.cell_grid.ca.save_grid_to_file(self.overwrite_dialog.overwrite_path)

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
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                self.process_dropdown_change(event)
            if event.type == pygame_gui.UI_WINDOW_CLOSE:
                self.process_window_close(event)
            if event.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
                self.process_file_dialog_selection(event)
            if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                self.process_confirmation_dialog_confirmed(event)

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

            # draw grid on window
            self.cell_grid.draw()

            self.window_surface.blit(self.cell_grid.visible_surface, self.grid_padding)
            self.ui_manager.draw_ui(self.window_surface)

            pygame.display.update()

        pygame.display.quit()
        pygame.quit()
