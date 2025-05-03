from board import Board
from player import Player
from game_history import GameHistory
from game_logger import GameLogger

class TicTacToeGame:
    """
    Represents a tic-tac-toe game.
    
    Attributes:
        board (Board): The game board
        players (list): A list of Player objects
        current_player_index (int): The index of the current player
        history (GameHistory): The game history
    """
    def __init__(self, player1_name=None, player2_name=None, board_size=3, logger=None):
        self._board = Board(board_size)
        self._players = [
            Player('X', player1_name),
            Player('O', player2_name)
        ]
        self._current_player_index = 0
        self._history = GameHistory()
        self._game_over = False
        self._winner = None
        self._logger = logger or GameLogger()
        self._result_logged = False
    
    @property
    def current_player(self):
        return self._players[self._current_player_index]
    
    @property
    def board(self):
        return self._board
    
    @property
    def is_game_over(self):
        return self._game_over
    
    @property
    def winner(self):
        return self._winner
    
    @property
    def is_draw(self):
        return self._game_over and not self._winner
    
    @property
    def player_names(self):
        return (self._players[0].name, self._players[1].name)
    
    def make_move(self, row, col):
        """
        Make a move at the given position.
        
        Args:
            row (int): The row index
            col (int): The column index
            
        Returns:
            bool: True if the move was made successfully, False otherwise
        """
        if self._game_over:
            return False
        
        if self._board.mark_square(row, col, self.current_player.symbol):
            self._history.add_move(self.current_player, (row, col))
            
            # Check for a winner
            winner_symbol = self._board.get_winner()
            if winner_symbol:
                self._game_over = True
                self._winner = next(player for player in self._players if player.symbol == winner_symbol)
                self._log_game_result()
            elif self._board.is_full():
                self._game_over = True
                self._log_game_result()
            else:
                # Switch to the next player
                self._current_player_index = (self._current_player_index + 1) % len(self._players)
            
            return True
        
        return False
    
    def _log_game_result(self):
        """Log the game result if the game is over."""
        if not self._result_logged and self._game_over:
            self._logger.log_result(
                self._players[0], 
                self._players[1], 
                self._winner
            )
            self._result_logged = True
    
    def reset(self):
        """Reset the game to its initial state."""
        self._board.reset()
        self._current_player_index = 0
        self._history.clear()
        self._game_over = False
        self._winner = None
        self._result_logged = False
    
    def get_game_status(self):
        """Get the current status of the game."""
        if self._winner:
            return f"{self._winner.name} wins!"
        elif self._game_over:
            return "It's a draw!"
        else:
            return f"{self.current_player.name}'s turn"