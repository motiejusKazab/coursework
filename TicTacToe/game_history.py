class GameHistory:
    """
    Keeps track of the game history.
    
    Attributes:
        moves (list): A list of moves made in the game
    """
    def __init__(self):
        self._moves = []
    
    def add_move(self, player, position):
        """
        Add a move to the history.
        
        Args:
            player (Player): The player who made the move
            position (tuple): The position (row, col) where the move was made
        """
        self._moves.append((player, position))
    
    def get_moves(self):
        """Get all moves in the history."""
        return self._moves.copy()
    
    def clear(self):
        """Clear the history."""
        self._moves = []
    
    def __len__(self):
        return len(self._moves)