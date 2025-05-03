class Player:
    """
    Represents a player in the tic-tac-toe game.
    
    Attributes:
        symbol (str): The player's symbol ('X' or 'O')
        name (str): The player's name
    """
    def __init__(self, symbol, name=None):
        self._symbol = symbol
        self._name = name if name else f"Player {symbol}"
    
    @property
    def symbol(self):
        return self._symbol
    
    @property
    def name(self):
        return self._name
    
    def __str__(self):
        return f"{self._name} ({self._symbol})"