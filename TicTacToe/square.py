class Square:
    """
    Represents a single square on the tic-tac-toe board.
    
    Attributes:
        value (str or None): The value of the square ('X', 'O', or None if empty)
    """
    def __init__(self):
        self._value = None
    
    @property
    def value(self):
        return self._value
    
    @property
    def is_empty(self):
        return self._value is None
    
    def mark(self, symbol):
        """Mark the square with the given symbol if it's empty."""
        if self.is_empty:
            self._value = symbol
            return True
        return False
    
    def reset(self):
        """Reset the square to empty."""
        self._value = None
    
    def __str__(self):
        return self._value if self._value else " "