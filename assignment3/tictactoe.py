class TictactoeException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class Board:
    # Class variable
    valid_moves = [
        "upper left", "upper center", "upper right", 
        "middle left", "center", "middle right", 
        "lower left", "lower center", "lower right"
    ]

    def __init__(self):
        # Create a 3x3 list
        self.board_array = [[" " for _ in range(3)] for _ in range(3)]
        self.turn = "X"

    def __str__(self):
        lines = []
        lines.append(f" {self.board_array[0][0]} | {self.board_array[0][1]} | {self.board_array[0][2]} \n")
        lines.append("-----------\n")
        lines.append(f" {self.board_array[1][0]} | {self.board_array[1][1]} | {self.board_array[1][2]} \n")
        lines.append("-----------\n")
        lines.append(f" {self.board_array[2][0]} | {self.board_array[2][1]} | {self.board_array[2][2]} \n")
        return "".join(lines)

    def move(self, move_string):
        if not move_string in Board.valid_moves:
            raise TictactoeException("That's not a valid move.")
        
        move_index = Board.valid_moves.index(move_string)
        row = move_index // 3 
        column = move_index % 3 
        
        if self.board_array[row][column] != " ":
            raise TictactoeException("That spot is taken.")
            
        self.board_array[row][column] = self.turn
        
        if self.turn == "X":
            self.turn = "O"
        else:
            self.turn = "X"

    def whats_next(self):
        # Check Cat's Game
        cat = True
        for i in range(3):
            for j in range(3):
                if self.board_array[i][j] == " ":
                    cat = False
                else:
                    continue
                break
            else:
                continue
            break
            
        # Check for Win
        win = False
        # check rows
        for i in range(3): 
            if self.board_array[i][0] != " ":
                if self.board_array[i][0] == self.board_array[i][1] and self.board_array[i][1] == self.board_array[i][2]:
                    win = True
                    break
        
        # check columns
        if not win:
            for i in range(3): 
                if self.board_array[0][i] != " ":
                    if self.board_array[0][i] == self.board_array[1][i] and self.board_array[1][i] == self.board_array[2][i]:
                        win = True
                        break
        
        # check diagonals
        if not win:
            if self.board_array[1][1] != " ": 
                if self.board_array[0][0] == self.board_array[1][1] and self.board_array[2][2] == self.board_array[1][1]:
                    win = True
                if self.board_array[0][2] == self.board_array[1][1] and self.board_array[2][0] == self.board_array[1][1]:
                    win = True
        
        # Determine Return Values
        if win:
            # If win true, the PREVIOUS won.
            
            if self.turn == "O":
                return (True, "X wins!")
            else:
                return (True, "O wins!")
        elif cat:
            return (True, "Cat's Game.")
        else:
            if self.turn == "X":
                 return (False, "X's turn.")
            else:
                return (False, "O's turn.")

# --- Mainline ---
if __name__ == "__main__":
    print("Welcome to Tic-Tac-Toe!")
    print("Valid moves: 'upper left', 'center', 'lower right', etc.")
    
    # Initialize
    game_board = Board()
    
    while True:
        # Check status before
        is_over, message = game_board.whats_next()
        
        print("\n" + str(game_board))
        
        if is_over:
            print(message)
            print("Game Over.")
            break
        
        print(message) 
        user_move = input("Enter your move: ").strip()
        
        try:
            game_board.move(user_move)
        except TictactoeException as e:
            print(f"Error: {e.message}")
            print("Please try again.")