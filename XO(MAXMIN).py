import time

class TicTacToeGame:
    def __init__(self, turn="O"):
        """
        Initializes the Tic-Tac-Toe game.

        Args:
            turn (str): The starting player, either 'X' or 'O'. Defaults to 'O'.
        """
        self.initialize_game(turn)

    
    def initialize_game(self, turn="X"):
        """
        Initializes the game state.

        Args:
            turn (str): The starting player, either 'X' or 'O'. Defaults to 'X'.
        """
        self.current_state = [['.', '.', '.'],
                              ['.', '.', '.'],
                              ['.', '.', '.']]
        self.player_turn = turn

    def draw_board(self):
        """Draws the current game board on the console."""
        for row in self.current_state:
            print(' '.join(row))
        print()

    def is_valid_move(self, row, col):
        """
        Checks if a move is valid.

        Args:
            row (int): The row index of the move.
            col (int): The column index of the move.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        if row < 0 or row > 2 or col < 0 or col > 2:
            return False
        elif self.current_state[row][col] != '.':
            return False
        else:
            return True


    def is_game_over(self):
        """
        Checks if the game is over.

        Returns:
            str or None: The winner ('X' or 'O') if there is one, '.' for a tie, None if the game is not over.
        """
        # Check for vertical win
        for col in range(3):
            if self.current_state[0][col] != '.' and \
                    self.current_state[0][col] == self.current_state[1][col] == self.current_state[2][col]:
                return self.current_state[0][col]

        # Check for horizontal win
        for row in range(3):
            if self.current_state[row] == ['X', 'X', 'X']:
                return 'X'
            elif self.current_state[row] == ['O', 'O', 'O']:
                return 'O'

        # Check for diagonal win
        if self.current_state[0][0] != '.' and \
                self.current_state[0][0] == self.current_state[1][1] == self.current_state[2][2]:
            return self.current_state[0][0]
        if self.current_state[0][2] != '.' and \
                self.current_state[0][2] == self.current_state[1][1] == self.current_state[2][0]:
            return self.current_state[0][2]

        # Check if the board is full (tie)
        for row in self.current_state:
            if '.' in row:
                return None

        return '.'


    def minimax(self, depth, is_maximizing):
        """
        Implements the minimax algorithm to determine the best move.

        Args:
            depth (int): The current depth of the recursive algorithm.
            is_maximizing (bool): Indicates if it's the maximizing player's turn.

        Returns:
            int, int, int: The best score, row, and column for the current player's move.
        """
        scores = {
            'X': -1,
            'O': 1,
            '.': 0
        }

        if is_maximizing:
            best_score = float('-inf')
            symbol = 'O'
        else:
            best_score = float('inf')
            symbol = 'X'

        if self.is_game_over():
            return scores[self.is_game_over()], None, None

        for row in range(3):
            for col in range(3):
                if self.current_state[row][col] == '.':
                    self.current_state[row][col] = symbol
                    score, _, _ = self.minimax(depth + 1, not is_maximizing)
                    self.current_state[row][col] = '.'

                    if is_maximizing:
                        if score > best_score:
                            best_score = score
                            best_row = row
                            best_col = col
                    else:
                        if score < best_score:
                            best_score = score
                            best_row = row
                            best_col = col

        return best_score, best_row, best_col

    def play(self):
        """Starts the game and handles the main gameplay loop."""
        while True:
            self.draw_board()
            game_result = self.is_game_over()
            
            if game_result:
                if game_result == 'X':
                    print('The winner is X!')
                elif game_result == 'O':
                    print('The winner is O!')
                elif game_result == '.':
                    print("It's a tie!")
                self.initialize_game()
                return


            if self.player_turn == 'X':
                while True:
                    start = time.time()
                    _, qx, qy = self.minimax(0,False)
                    end = time.time()
                    print('Evaluation time: {}s'.format(round(end - start, 7)))
                    print('Recommended move: X = {}, Y = {}'.format(qx+1, qy+1))
                    # recieve 2 inputs the row number and col number 
                    px, py = [int(x) for x in input('Enter your move (row column): ').strip().split()]
                    
                    if self.is_valid_move(px - 1, py - 1):
                        self.current_state[px - 1][py - 1] = 'X'
                        self.player_turn = 'O'
                        break
                    else:
                        print('Invalid move! Try again.')

            else:
                start = time.time()
                _, px, py = self.minimax(0, True)
                end = time.time()
                print('calculation time: {}s'.format(round(end - start, 7)))                
                self.current_state[px][py] = 'O'
                self.player_turn = 'X'


try:
    starting_player = input("If you want to go first, enter 'X'; otherwise, press enter: ")
    game = TicTacToeGame(starting_player.capitalize())
    game.play()
except Exception as e:
    print(e)