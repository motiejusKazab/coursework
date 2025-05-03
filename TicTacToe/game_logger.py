from datetime import datetime

class GameLogger:
    """
    Handles logging of game results to a file.
    """
    def __init__(self, log_file="game_log.txt"):
        self._log_file = log_file
    
    def log_result(self, player1, player2, winner=None):
        """
        Log the result of a game.
        
        Args:
            player1 (Player): The first player
            player2 (Player): The second player
            winner (Player or None): The winning player, or None if it's a draw
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if winner:
            loser = player2 if winner.name == player1.name else player1
            message = f"[{timestamp}] {winner.name} won against {loser.name}"
        else:
            message = f"[{timestamp}] {player1.name} and {player2.name} draw"
        
        try:
            with open(self._log_file, "a") as f:
                f.write(message + "\n")
            return True
        except Exception as e:
            print(f"Error writing to log file: {e}")
            return False