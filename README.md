# Introduction

This application is a fully featured Tic-Tac-Toe game implemented in Python using the Pygame library. It provides a graphical user interface for players to enjoy the classic game of Tic-Tac-Toe with additional features such as customizable player names, game history logging, and adjustable display resolutions. The game follows the traditional rules where players take turns marking spaces on a 3×3 grid, with the objective of placing three of their marks in a horizontal, vertical, or diagonal row.

The program can be run directly using Python:

python main.py

# How to use the program?

**1\. Main Menu**: Upon launching the application, users are presented with a main menu offering options to:

Play Game (or Resume Game if a game is in progress)

Options (to adjust display resolution)

View Game Log (to see history of game results)

Exit Game

**2\. Player Setup:** Before starting a game, users can customize player names or use the default names (Player X and Player O).

**3\. Gameplay:**

1\. Players take turns clicking on the grid to place their marks (X or O)

2\. The current player's turn is displayed above the game board

3\. The game automatically detects wins or draws

4\. Players can reset the game or return to the main menu at any time

**4\. Game History:** All game results are automatically logged to a file and can be viewed through the "View Game Log" option.

# Object-Oriented Design

The application follows object-oriented programming principles with a clear separation of concerns. The program is structured into several classes, each with specific responsibilities:

**Game Logic Classes**

The core game logic is encapsulated in several classes:

From game.py

class TicTacToeGame:

"""

Represents a tic-tac-toe game.

"""

def \__init_\_(self, player1_name=None, player2_name=None, board_size=3, logger=None):

self.\_board = Board(board_size)

self.\_players = \[

Player('X', player1_name),

Player('O', player2_name)

\]

self.\_current_player_index = 0

self.\_history = GameHistory()

self.\_game_over = False

self.\_winner = None

self.\_logger = logger or GameLogger()

self.\_result_logged = False

This main game class manages the game state, players, and interactions with other components like the board and logger.

**Board Representation**

The game board is represented by a dedicated class:

From board.py

class Board:

"""

Represents the tic-tac-toe game board.

"""

def \__init_\_(self, size=3):

self.\_size = size

self.\_squares = \[\[Square() for _in range(size)\] for_ in range(size)\]

self.\_last_move = None

def get_winner(self):

"""

Check if there's a winner.

"""

\# Check rows

for row in self.\_squares:

if all(square.value == row\[0\].value and not square.is_empty for square in row):

return row\[0\].value

\# Check columns

for col in range(self.\_size):

if all(self.\_squares\[row\]\[col\].value == self.\_squares\[0\]\[col\].value and

not self.\_squares\[row\]\[col\].is_empty for row in range(self.\_size)):

return self.\_squares\[0\]\[col\].value

\# Check diagonals

\# ... \[diagonal checking code\]

return None

This implementation allows for flexible board sizes and provides methods to check for winning conditions.

**User Interface Implementation**

The UI is implemented using Pygame, with a state-based approach to manage different screens:

\# From game_ui.py

class GameUI:

"""

A Pygame-based user interface for the tic-tac-toe game with menus.

"""

\# Game states

MAIN_MENU = 0

NAME_INPUT = 1

OPTIONS = 2

GAME = 3

VIEW_LOG = 4

def run(self):

"""Run the game loop."""

running = True

while running:

\# Handle events

for event in pygame.event.get():

if event.type == pygame.QUIT:

running = False

break

\# Handle events based on current state

if self.\_state == self.MAIN_MENU:

running = self.\_handle_main_menu_events(event)

elif self.\_state == self.NAME_INPUT:

running = self.\_handle_name_input_events(event)

\# ... \[other states\]

\# Draw current screen

if self.\_state == self.MAIN_MENU:

self.\_draw_main_menu()

elif self.\_state == self.NAME_INPUT:

self.\_draw_name_input()

\# ... \[other states\]

\# Update display

pygame.display.flip()

\# Cap the frame rate

self.\_clock.tick(60)

This state-based design allows for clean separation between different screens and user interactions.

**Game Logging Functionality**

The application includes a logging system to record game results:

\# From game_logger.py

class GameLogger:

"""

Handles logging of game results to a file.

"""

def \__init_\_(self, log_file="game_log.txt"):

self.\_log_file = log_file

def log_result(self, player1, player2, winner=None):

"""

Log the result of a game.

"""

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if winner:

loser = player2 if winner.name == player1.name else player1

message = f"\[{timestamp}\] {winner.name} won against {loser.name}"

else:

message = f"\[{timestamp}\] {player1.name} and {player2.name} draw"

try:

with open(self.\_log_file, "a") as f:

f.write(message + "\\n")

return True

except Exception as e:

print(f"Error writing to log file: {e}")

return False

This logging system provides a history of game results that can be viewed through the UI.

# Implementation of Functional Requirements

**1\. Game Logic**

The game implements the standard Tic-Tac-Toe rules with win detection for rows, columns, and diagonals:

\# From board.py

def get_winner(self):

"""

Check if there's a winner.

"""

\# Check rows

for row in self.\_squares:

if all(square.value == row\[0\].value and not square.is_empty for square in row):

return row\[0\].value

\# Check columns

for col in range(self.\_size):

if all(self.\_squares\[row\]\[col\].value == self.\_squares\[0\]\[col\].value and

not self.\_squares\[row\]\[col\].is_empty for row in range(self.\_size)):

return self.\_squares\[0\]\[col\].value

\# Check diagonals

if all(self.\_squares\[i\]\[i\].value == self.\_squares\[0\]\[0\].value and

not self.\_squares\[i\]\[i\].is_empty for i in range(self.\_size)):

return self.\_squares\[0\]\[0\].value

if all(self.\_squares\[i\]\[self.\_size - 1 - i\].value == self.\_squares\[0\]\[self.\_size - 1\].value and

not self.\_squares\[i\]\[self.\_size - 1 - i\].is_empty for i in range(self.\_size)):

return self.\_squares\[0\]\[self.\_size - 1\].value

return None

The implementation uses a flexible approach that would work for different board sizes, demonstrating good software design principles.

**2\. User Interface**

The application provides a complete graphical user interface with multiple screens:

\# From game_ui.py

def \_draw_game(self):

"""Draw the game screen."""

\# Draw background

self.\_screen.fill(self.BLACK)

\# Draw title

title = self.\_game_font.render("Tic-Tac-Toe", True, self.WHITE)

title_rect = title.get_rect(center=(self.\_width // 2, 30))

self.\_screen.blit(title, title_rect)

\# Draw board background

board_rect = pygame.Rect(

self.\_board_x,

self.\_board_y,

self.\_board_size_px,

self.\_board_size_px

)

pygame.draw.rect(self.\_screen, self.BLACK, board_rect)

\# Draw grid lines

for i in range(self.\_board_size + 1):

\# Vertical lines

pygame.draw.line(

self.\_screen,

self.WHITE,

(self.\_board_x + i \* self.\_cell_size, self.\_board_y),

(self.\_board_x + i \* self.\_cell_size, self.\_board_y + self.\_board_size_px),

2 if i == 0 or i == self.\_board_size else 1

)

\# Horizontal lines

pygame.draw.line(

self.\_screen,

self.WHITE,

(self.\_board_x, self.\_board_y + i \* self.\_cell_size),

(self.\_board_x + self.\_board_size_px, self.\_board_y + i \* self.\_cell_size),

2 if i == 0 or i == self.\_board_size else 1

)

The UI implementation includes responsive design elements that adjust to different screen resolutions.

**3\. Player Customization**

The game allows players to customize their names:

\# From game_ui.py

def \_handle_name_input_events(self, event):

"""Handle events for the name input screen."""

if event.type == pygame.MOUSEBUTTONDOWN:

action = self.\_start_game_button.check_click(event.pos)

if action:

self.\_player1_name = self.\_player1_input.text if self.\_player1_input.text else "Player X"

self.\_player2_name = self.\_player2_input.text if self.\_player2_input.text else "Player O"

self.\_game = TicTacToeGame(self.\_player1_name, self.\_player2_name, logger=self.\_logger)

self.\_game_in_progress = True

self.\_setup_game_elements()

self.\_state = self.GAME

This feature enhances the personalization of the gaming experience.

**4\. Game History and Logging**

The application maintains a history of game results:

\# From game.py

def \_log_game_result(self):

"""Log the game result if the game is over."""

if not self.\_result_logged and self.\_game_over:

self.\_logger.log_result(

self.\_players\[0\],

self.\_players\[1\],

self.\_winner

)

self.\_result_logged = True

This logging system provides a persistent record of game outcomes.

# Results and Summary

**Results**

\- Successful Implementation: The Tic-Tac-Toe game was successfully implemented with all core functionality working as expected, including game logic, UI, and logging features.

\- Modular Design: The application demonstrates good software engineering practices with a modular, object-oriented design that separates concerns and makes the code maintainable.

\- User Experience: The game provides a complete user experience with multiple screens, customization options, and visual feedback for game states.

\- Challenges: One significant challenge was implementing the win detection algorithm to work efficiently for variable board sizes while maintaining readability.

**Conclusions**

This coursework has resulted in a fully functional Tic-Tac-Toe game with a graphical user interface. The application successfully implements all the required functionality, including game logic, user interface, player customization, and game history logging. The modular, object-oriented design demonstrates good software engineering practices and makes the code maintainable and extensible.

The project has achieved its goal of creating an engaging, user-friendly implementation of the classic Tic-Tac-Toe game. The result is a polished application that provides a complete gaming experience with multiple features beyond the basic game mechanics.

**Future Extensions**

The application could be extended in several ways:

1\. Network Multiplayer: Implement networking capabilities to allow players to compete remotely.

2\. AI Opponent: Add an artificial intelligence opponent with adjustable difficulty levels.

3\. Enhanced Graphics: Improve the visual design with animations, themes, and sound effects.

4\. Larger Board Sizes: Extend the game to support larger grid sizes (4×4, 5×5) with adjustable win conditions.

5\. User Accounts: Implement a user account system to track statistics and achievements across multiple sessions.

6\. Mobile Version: Adapt the application for mobile platforms using a framework like Kivy.

# Resources and References

<https://www.pygame.org/docs/>

<http://gameprogrammingpatterns.com/>

<https://v0.dev/>

<https://chatgpt.com/>

<https://www.youtube.com/watch?v=AY9MnQ4x3zk&t=306s>

Links provided in “OOP Coursework 2025.pdf”

Friends and family
