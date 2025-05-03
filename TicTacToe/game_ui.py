import pygame
import os
import sys

from game import TicTacToeGame
from game_logger import GameLogger
from ui_components import Button, TextInput

class GameUI:
    """
    A Pygame-based user interface for the tic-tac-toe game with menus.
    """
    # Game states
    MAIN_MENU = 0
    NAME_INPUT = 1
    OPTIONS = 2
    GAME = 3
    VIEW_LOG = 4  # New state for viewing the log
    
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (100, 100, 100)
    RED = (255, 0, 0)
    BLUE = (0, 100, 255)
    GREEN = (0, 200, 0)
    
    # Available resolutions
    RESOLUTIONS = [
        (640, 480),
        (800, 600),
        (1024, 768),
        (1280, 720)
    ]
    
    def __init__(self, log_file="game_log.txt"):
        # Initialize Pygame
        pygame.init()
        
        # Default resolution
        self._resolution_index = 1  # 800x600 by default
        self._width, self._height = self.RESOLUTIONS[self._resolution_index]
        
        # Set up the display
        self._screen = pygame.display.set_mode((self._width, self._height))
        pygame.display.set_caption("Tic-Tac-Toe")
        
        # Set up fonts
        self._title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self._menu_font = pygame.font.SysFont("Arial", 32)
        self._button_font = pygame.font.SysFont("Arial", 24)
        self._game_font = pygame.font.SysFont("Arial", 24)
        self._log_font = pygame.font.SysFont("Courier New", 16)
        
        # Game state
        self._state = self.MAIN_MENU
        self._game = None
        self._game_in_progress = False
        
        # Player names
        self._player1_name = "Player X"
        self._player2_name = "Player O"
        
        # Logger
        self._log_file = log_file
        self._logger = GameLogger(log_file)
        self._log_entries = []
        self._log_scroll_pos = 0
        
        # Clock for controlling frame rate
        self._clock = pygame.time.Clock()
        
        # Create UI elements
        self._create_ui_elements()
    
    def _create_ui_elements(self):
        """Create UI elements based on current resolution."""
        # Main menu buttons
        button_width = 200
        button_height = 50
        button_x = self._width // 2 - button_width // 2
        
        self._main_menu_buttons = []
        
        # If there's a game in progress, show "Resume Game" instead of "Play Game"
        if self._game_in_progress:
            self._main_menu_buttons.append(
                Button(button_x, self._height // 2 - 180, button_width, button_height, 
                       "Resume Game", self._button_font, self.GAME)
            )
            self._main_menu_buttons.append(
                Button(button_x, self._height // 2 - 120, button_width, button_height, 
                       "New Game", self._button_font, self.NAME_INPUT)
            )
        else:
            self._main_menu_buttons.append(
                Button(button_x, self._height // 2 - 120, button_width, button_height, 
                       "Play Game", self._button_font, self.NAME_INPUT)
            )
        
        self._main_menu_buttons.extend([
            Button(button_x, self._height // 2 - 60, button_width, button_height, 
                   "Options", self._button_font, self.OPTIONS),
            Button(button_x, self._height // 2, button_width, button_height, 
                   "View Game Log", self._button_font, self.VIEW_LOG),
            Button(button_x, self._height // 2 + 60, button_width, button_height, 
                   "Exit Game", self._button_font, "exit")
        ])
        
        # Name input elements
        input_width = 300
        input_height = 40
        input_x = self._width // 2 - input_width // 2
        
        self._player1_input = TextInput(input_x, self._height // 2 - 60, 
                                        input_width, input_height, 
                                        self._button_font, self._player1_name)
        self._player2_input = TextInput(input_x, self._height // 2, 
                                        input_width, input_height, 
                                        self._button_font, self._player2_name)
        
        self._start_game_button = Button(input_x, self._height // 2 + 60, 
                                         input_width, input_height, 
                                         "Start Game", self._button_font, self.GAME)
        
        # Back button for name input and options screens
        self._back_button = Button(20, self._height - 70, 100, 40, 
                                   "Back", self._button_font, self.MAIN_MENU)
        
        # Options menu elements
        self._resolution_buttons = []
        for i, (width, height) in enumerate(self.RESOLUTIONS):
            text = f"{width}x{height}"
            btn = Button(self._width // 2 - 100, self._height // 2 - 90 + i * 60, 
                         200, 40, text, self._button_font, f"res_{i}")
            self._resolution_buttons.append(btn)
        
        # Log view elements
        self._log_scroll_up = Button(self._width - 60, 100, 40, 40, "↑", self._button_font, "scroll_up")
        self._log_scroll_down = Button(self._width - 60, self._height - 100, 40, 40, "↓", self._button_font, "scroll_down")
        
        # Game elements
        if self._game:
            self._setup_game_elements()
    
    def _setup_game_elements(self):
        """Set up game-specific UI elements."""
        # Calculate board dimensions
        self._board_size = self._game.board.size
        self._board_size_px = min(self._width * 0.6, self._height * 0.6)
        self._cell_size = self._board_size_px / self._board_size
        self._board_x = (self._width - self._board_size_px) / 2
        self._board_y = (self._height - self._board_size_px) / 2 + 20
        
        # Reset button
        self._reset_button = Button(
            self._width // 2 - 60, 
            self._board_y + self._board_size_px + 30, 
            120, 40, "Reset Game", self._button_font, "reset"
        )
    
    def _change_resolution(self, index):
        """Change the game resolution."""
        if 0 <= index < len(self.RESOLUTIONS):
            self._resolution_index = index
            self._width, self._height = self.RESOLUTIONS[index]
            self._screen = pygame.display.set_mode((self._width, self._height))
            self._create_ui_elements()
    
    def _get_cell_from_pos(self, pos):
        """Convert screen position to board cell."""
        x, y = pos
        
        # Check if position is within board bounds
        if (self._board_x <= x <= self._board_x + self._board_size_px and
            self._board_y <= y <= self._board_y + self._board_size_px):
            
            # Calculate row and column
            col = int((x - self._board_x) // self._cell_size)
            row = int((y - self._board_y) // self._cell_size)
            
            if 0 <= row < self._board_size and 0 <= col < self._board_size:
                return row, col
        
        return None
    
    def _load_log_entries(self):
        """Load log entries from the log file."""
        self._log_entries = []
        try:
            if os.path.exists(self._log_file):
                with open(self._log_file, "r") as f:
                    self._log_entries = f.readlines()
        except Exception as e:
            print(f"Error reading log file: {e}")
            self._log_entries = [f"Error reading log file: {e}"]
    
    def _draw_x(self, row, col, winning=False):
        """Draw an X symbol in the specified cell."""
        x = self._board_x + col * self._cell_size + self._cell_size / 2
        y = self._board_y + row * self._cell_size + self._cell_size / 2
        
        size = self._cell_size * 0.3
        thickness = int(self._cell_size * 0.1)
        
        color = self.GREEN if winning else self.RED
        
        # Draw the X with lines
        pygame.draw.line(
            self._screen, 
            color,
            (x - size, y - size),
            (x + size, y + size),
            thickness
        )
        pygame.draw.line(
            self._screen, 
            color,
            (x + size, y - size),
            (x - size, y + size),
            thickness
        )
    
    def _draw_o(self, row, col, winning=False):
        """Draw an O symbol in the specified cell."""
        x = self._board_x + col * self._cell_size + self._cell_size / 2
        y = self._board_y + row * self._cell_size + self._cell_size / 2
        
        radius = int(self._cell_size * 0.3)
        thickness = int(self._cell_size * 0.1)
        
        color = self.GREEN if winning else self.BLUE
        
        # Draw the O with a circle
        pygame.draw.circle(
            self._screen,
            color,
            (int(x), int(y)),
            radius,
            thickness
        )
    
    def _draw_main_menu(self):
        """Draw the main menu."""
        # Draw background
        self._screen.fill(self.BLACK)
        
        # Draw title
        title = self._title_font.render("Tic-Tac-Toe", True, self.WHITE)
        title_rect = title.get_rect(center=(self._width // 2, 100))
        self._screen.blit(title, title_rect)
        
        # Draw buttons
        for button in self._main_menu_buttons:
            button.draw(self._screen)
    
    def _draw_name_input(self):
        """Draw the name input screen."""
        # Draw background
        self._screen.fill(self.BLACK)
        
        # Draw title
        title = self._title_font.render("Enter Player Names", True, self.WHITE)
        title_rect = title.get_rect(center=(self._width // 2, 100))
        self._screen.blit(title, title_rect)
        
        # Draw labels
        p1_label = self._menu_font.render("Player 1 (X):", True, self.RED)
        p1_label_rect = p1_label.get_rect(midright=(self._width // 2 - 160, self._height // 2 - 40))
        self._screen.blit(p1_label, p1_label_rect)
        
        p2_label = self._menu_font.render("Player 2 (O):", True, self.BLUE)
        p2_label_rect = p2_label.get_rect(midright=(self._width // 2 - 160, self._height // 2 + 20))
        self._screen.blit(p2_label, p2_label_rect)
        
        # Draw input boxes
        self._player1_input.draw(self._screen)
        self._player2_input.draw(self._screen)
        
        # Draw start button
        self._start_game_button.draw(self._screen)
        
        # Draw back button
        self._back_button.draw(self._screen)
    
    def _draw_options(self):
        """Draw the options screen."""
        # Draw background
        self._screen.fill(self.BLACK)
        
        # Draw title
        title = self._title_font.render("Options", True, self.WHITE)
        title_rect = title.get_rect(center=(self._width // 2, 100))
        self._screen.blit(title, title_rect)
        
        # Draw resolution label
        res_label = self._menu_font.render("Resolution:", True, self.WHITE)
        res_label_rect = res_label.get_rect(center=(self._width // 2, self._height // 2 - 150))
        self._screen.blit(res_label, res_label_rect)
        
        # Draw resolution buttons
        for i, button in enumerate(self._resolution_buttons):
            # Highlight current resolution
            if i == self._resolution_index:
                pygame.draw.rect(self._screen, (0, 100, 0), button.rect, border_radius=5)
            button.draw(self._screen)
        
        # Draw back button
        self._back_button.draw(self._screen)
    
    def _draw_log_view(self):
        """Draw the log view screen."""
        # Draw background
        self._screen.fill(self.BLACK)
        
        # Draw title
        title = self._title_font.render("Game Log", True, self.WHITE)
        title_rect = title.get_rect(center=(self._width // 2, 50))
        self._screen.blit(title, title_rect)
        
        # Draw log entries
        if not self._log_entries:
            self._load_log_entries()
        
        # Create a surface for the log content
        log_area = pygame.Rect(50, 100, self._width - 120, self._height - 200)
        pygame.draw.rect(self._screen, (20, 20, 20), log_area)
        pygame.draw.rect(self._screen, self.GRAY, log_area, 1)
        
        # Display log entries
        max_visible_lines = (log_area.height - 20) // 20
        start_idx = max(0, min(self._log_scroll_pos, len(self._log_entries) - max_visible_lines))
        if start_idx < 0:
            start_idx = 0
        
        for i, entry in enumerate(self._log_entries[start_idx:start_idx + max_visible_lines]):
            y_pos = log_area.y + 10 + i * 20
            log_text = self._log_font.render(entry.strip(), True, self.WHITE)
            self._screen.blit(log_text, (log_area.x + 10, y_pos))
        
        # Draw scroll buttons
        self._log_scroll_up.draw(self._screen)
        self._log_scroll_down.draw(self._screen)
        
        # Draw back button
        self._back_button.draw(self._screen)
        
        # Draw scroll info
        if self._log_entries:
            scroll_info = f"{start_idx + 1}-{min(start_idx + max_visible_lines, len(self._log_entries))} of {len(self._log_entries)}"
            info_text = self._button_font.render(scroll_info, True, self.GRAY)
            self._screen.blit(info_text, (log_area.centerx - info_text.get_width() // 2, log_area.bottom + 10))
    
    def _draw_game(self):
        """Draw the game screen."""
        # Draw background
        self._screen.fill(self.BLACK)
        
        # Draw title
        title = self._game_font.render("Tic-Tac-Toe", True, self.WHITE)
        title_rect = title.get_rect(center=(self._width // 2, 30))
        self._screen.blit(title, title_rect)
        
        # Draw board background
        board_rect = pygame.Rect(
            self._board_x, 
            self._board_y, 
            self._board_size_px, 
            self._board_size_px
        )
        pygame.draw.rect(self._screen, self.BLACK, board_rect)
        
        # Draw grid lines
        for i in range(self._board_size + 1):
            # Vertical lines
            pygame.draw.line(
                self._screen,
                self.WHITE,
                (self._board_x + i * self._cell_size, self._board_y),
                (self._board_x + i * self._cell_size, self._board_y + self._board_size_px),
                2 if i == 0 or i == self._board_size else 1
            )
            
            # Horizontal lines
            pygame.draw.line(
                self._screen,
                self.WHITE,
                (self._board_x, self._board_y + i * self._cell_size),
                (self._board_x + self._board_size_px, self._board_y + i * self._cell_size),
                2 if i == 0 or i == self._board_size else 1
            )
        
        # Get winning positions
        winning_positions = self._game.board.get_winning_positions()
        
        # Draw board marks
        for row in range(self._board_size):
            for col in range(self._board_size):
                square = self._game.board.squares[row][col]
                is_winning = winning_positions and (row, col) in winning_positions
                
                if square.value == 'X':
                    self._draw_x(row, col, winning=is_winning)
                elif square.value == 'O':
                    self._draw_o(row, col, winning=is_winning)
        
        # Draw game status
        status_text = self._game.get_game_status()
        if self._game.winner:
            status_color = self.GREEN
        elif self._game.is_draw:
            status_color = self.WHITE
        else:
            status_color = self.RED if self._game.current_player.symbol == 'X' else self.BLUE
        
        status = self._game_font.render(status_text, True, status_color)
        status_rect = status.get_rect(center=(self._width // 2, self._board_y - 20))
        self._screen.blit(status, status_rect)
        
        # Draw reset button
        self._reset_button.draw(self._screen)
        
        # Draw ESC hint
        esc_text = self._button_font.render("Press ESC for menu", True, self.GRAY)
        esc_rect = esc_text.get_rect(bottomright=(self._width - 20, self._height - 20))
        self._screen.blit(esc_text, esc_rect)
    
    def _handle_main_menu_events(self, event):
        """Handle events for the main menu."""
        if event.type == pygame.MOUSEMOTION:
            for button in self._main_menu_buttons:
                button.check_hover(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in self._main_menu_buttons:
                action = button.check_click(event.pos)
                if action:
                    if action == "exit":
                        return False
                    else:
                        self._state = action
                        # If viewing log, load the log entries
                        if action == self.VIEW_LOG:
                            self._load_log_entries()
                        # If starting a new game, reset the game
                        if action == self.NAME_INPUT and self._game_in_progress:
                            # We'll create a new game when they submit names
                            pass
                    break
        
        return True
    
    def _handle_name_input_events(self, event):
        """Handle events for the name input screen."""
        if event.type == pygame.MOUSEMOTION:
            self._start_game_button.check_hover(event.pos)
            self._back_button.check_hover(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            action = self._start_game_button.check_click(event.pos)
            if action:
                self._player1_name = self._player1_input.text if self._player1_input.text else "Player X"
                self._player2_name = self._player2_input.text if self._player2_input.text else "Player O"
                self._game = TicTacToeGame(self._player1_name, self._player2_name, logger=self._logger)
                self._game_in_progress = True
                self._setup_game_elements()
                self._state = self.GAME
            
            action = self._back_button.check_click(event.pos)
            if action:
                self._state = action
                # Recreate UI elements to ensure main menu is updated
                self._create_ui_elements()
        
        # Handle text input
        self._player1_input.handle_event(event)
        self._player2_input.handle_event(event)
        
        return True
    
    def _handle_options_events(self, event):
        """Handle events for the options screen."""
        if event.type == pygame.MOUSEMOTION:
            for button in self._resolution_buttons:
                button.check_hover(event.pos)
            self._back_button.check_hover(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(self._resolution_buttons):
                action = button.check_click(event.pos)
                if action and action.startswith("res_"):
                    index = int(action.split("_")[1])
                    self._change_resolution(index)
                    break
            
            # Check if back button was clicked
            if self._back_button.rect.collidepoint(event.pos):
                self._state = self.MAIN_MENU
                # Recreate UI elements to ensure main menu is updated
                self._create_ui_elements()
        
        return True
    
    def _handle_log_view_events(self, event):
        """Handle events for the log view screen."""
        if event.type == pygame.MOUSEMOTION:
            self._log_scroll_up.check_hover(event.pos)
            self._log_scroll_down.check_hover(event.pos)
            self._back_button.check_hover(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle scroll buttons
            action = self._log_scroll_up.check_click(event.pos)
            if action == "scroll_up":
                self._log_scroll_pos = max(0, self._log_scroll_pos - 1)
            
            action = self._log_scroll_down.check_click(event.pos)
            if action == "scroll_down":
                max_scroll = max(0, len(self._log_entries) - 10)  # Assuming 10 visible lines
                self._log_scroll_pos = min(max_scroll, self._log_scroll_pos + 1)
            
            # Handle back button
            if self._back_button.rect.collidepoint(event.pos):
                self._state = self.MAIN_MENU
                # Recreate UI elements to ensure main menu is updated
                self._create_ui_elements()
        
        # Handle mouse wheel for scrolling
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:  # Scroll up
                self._log_scroll_pos = max(0, self._log_scroll_pos - 3)
            elif event.y < 0:  # Scroll down
                max_scroll = max(0, len(self._log_entries) - 10)  # Assuming 10 visible lines
                self._log_scroll_pos = min(max_scroll, self._log_scroll_pos + 3)
        
        return True
    
    def _handle_game_events(self, event):
        """Handle events for the game screen."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Go back to main menu but keep game state
                self._state = self.MAIN_MENU
                # Recreate UI elements to show Resume Game button
                self._create_ui_elements()
        
        elif event.type == pygame.MOUSEMOTION:
            self._reset_button.check_hover(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle click on board
            cell = self._get_cell_from_pos(event.pos)
            if cell and not self._game.is_game_over:
                row, col = cell
                self._game.make_move(row, col)
            
            # Handle click on reset button
            action = self._reset_button.check_click(event.pos)
            if action == "reset":
                self._game.reset()
        
        return True
    
    def run(self):
        """Run the game loop."""
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                
                # Handle events based on current state
                if self._state == self.MAIN_MENU:
                    running = self._handle_main_menu_events(event)
                elif self._state == self.NAME_INPUT:
                    running = self._handle_name_input_events(event)
                elif self._state == self.OPTIONS:
                    running = self._handle_options_events(event)
                elif self._state == self.VIEW_LOG:
                    running = self._handle_log_view_events(event)
                elif self._state == self.GAME:
                    running = self._handle_game_events(event)
            
            # Update UI elements
            if self._state == self.NAME_INPUT:
                self._player1_input.update()
                self._player2_input.update()
            
            # Draw current screen
            if self._state == self.MAIN_MENU:
                self._draw_main_menu()
            elif self._state == self.NAME_INPUT:
                self._draw_name_input()
            elif self._state == self.OPTIONS:
                self._draw_options()
            elif self._state == self.VIEW_LOG:
                self._draw_log_view()
            elif self._state == self.GAME:
                self._draw_game()
            
            # Update display
            pygame.display.flip()
            
            # Cap the frame rate
            self._clock.tick(60)
        
        pygame.quit()