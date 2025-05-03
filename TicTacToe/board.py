from square import Square

class Board:
    """
    Represents the tic-tac-toe game board.
    
    Attributes:
        size (int): The size of the board (default is 3x3)
        squares (list): A 2D list of Square objects
    """
    def __init__(self, size=3):
        self._size = size
        self._squares = [[Square() for _ in range(size)] for _ in range(size)]
        self._last_move = None
    
    @property
    def size(self):
        return self._size
    
    @property
    def squares(self):
        return self._squares
    
    def mark_square(self, row, col, symbol):
        """
        Mark a square at the given position with the given symbol.
        
        Args:
            row (int): The row index
            col (int): The column index
            symbol (str): The symbol to mark ('X' or 'O')
            
        Returns:
            bool: True if the square was marked successfully, False otherwise
        """
        if 0 <= row < self._size and 0 <= col < self._size:
            if self._squares[row][col].mark(symbol):
                self._last_move = (row, col)
                return True
        return False
    
    def is_full(self):
        """Check if the board is full."""
        return all(not square.is_empty for row in self._squares for square in row)
    
    def reset(self):
        """Reset the board to its initial state."""
        for row in self._squares:
            for square in row:
                square.reset()
        self._last_move = None
    
    def get_winner(self):
        """
        Check if there's a winner.
        
        Returns:
            str or None: The winning symbol ('X' or 'O') or None if there's no winner
        """
        # Check rows
        for row in self._squares:
            if all(square.value == row[0].value and not square.is_empty for square in row):
                return row[0].value
        
        # Check columns
        for col in range(self._size):
            if all(self._squares[row][col].value == self._squares[0][col].value and 
                   not self._squares[row][col].is_empty for row in range(self._size)):
                return self._squares[0][col].value
        
        # Check diagonals
        if all(self._squares[i][i].value == self._squares[0][0].value and 
               not self._squares[i][i].is_empty for i in range(self._size)):
            return self._squares[0][0].value
        
        if all(self._squares[i][self._size - 1 - i].value == self._squares[0][self._size - 1].value and 
               not self._squares[i][self._size - 1 - i].is_empty for i in range(self._size)):
            return self._squares[0][self._size - 1].value
        
        return None
    
    def get_winning_positions(self):
        """
        Get the positions of the winning squares.
        
        Returns:
            list or None: A list of (row, col) tuples representing the winning positions,
                         or None if there's no winner
        """
        # Check rows
        for i, row in enumerate(self._squares):
            if all(square.value == row[0].value and not square.is_empty for square in row):
                return [(i, j) for j in range(self._size)]
        
        # Check columns
        for col in range(self._size):
            if all(self._squares[row][col].value == self._squares[0][col].value and 
                   not self._squares[row][col].is_empty for row in range(self._size)):
                return [(row, col) for row in range(self._size)]
        
        # Check diagonals
        if all(self._squares[i][i].value == self._squares[0][0].value and 
               not self._squares[i][i].is_empty for i in range(self._size)):
            return [(i, i) for i in range(self._size)]
        
        if all(self._squares[i][self._size - 1 - i].value == self._squares[0][self._size - 1].value and 
               not self._squares[i][self._size - 1 - i].is_empty for i in range(self._size)):
            return [(i, self._size - 1 - i) for i in range(self._size)]
        
        return None