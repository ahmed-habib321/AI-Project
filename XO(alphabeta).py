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

    def max_alpha_beta(self, alpha, beta):
        """
        The max player's turn using the Alpha-Beta Pruning algorithm.

        Args:
            alpha (int): The current best value for the max player.
            beta (int): The current best value for the min player.

        Returns:
            int, int, int: The best score, row, and column for the max player's move.
        """
        max_score = float('-inf')
        best_row, best_col = None, None
        result = self.is_game_over()

        if result == 'X':
            return -1, 0, 0
        elif result == 'O':
            return 1, 0, 0
        elif result == '.':
            return 0, 0, 0

        for row in range(3):
            for col in range(3):
                if self.current_state[row][col] == '.':
                    self.current_state[row][col] = 'O'
                    score, _, _ = self.min_alpha_beta(alpha, beta)
                    self.current_state[row][col] = '.'

                    if score > max_score:
                        max_score = score
                        best_row, best_col = row, col

                    if max_score >= beta:
                        return max_score, best_row, best_col

                    alpha = max(alpha, max_score)

        return max_score, best_row, best_col

    def min_alpha_beta(self, alpha, beta):
        """
        The min player's turn using the Alpha-Beta Pruning algorithm.

        Args:
            alpha (int): The current best value for the max player.
            beta (int): The current best value for the min player.

        Returns:
            int, int, int: The best score, row, and column for the min player's move.
        """
        min_score = float('inf')
        best_row, best_col = None, None
        result = self.is_game_over()

        if result == 'X':
            return -1, 0, 0
        elif result == 'O':
            return 1, 0, 0
        elif result == '.':
            return 0, 0, 0

        for row in range(3):
            for col in range(3):
                if self.current_state[row][col] == '.':
                    self.current_state[row][col] = 'X'
                    score, _, _ = self.max_alpha_beta(alpha, beta)
                    self.current_state[row][col] = '.'

                    if score < min_score:
                        min_score = score
                        best_row, best_col = row, col

                    if min_score <= alpha:
                        return min_score, best_row, best_col

                    beta = min(beta, min_score)

        return min_score, best_row, best_col

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
                    _, qx, qy = self.min_alpha_beta(float('-inf'), float('inf'))
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
                start_time = time.time()
                _, px, py = self.max_alpha_beta(float('-inf'), float('inf'))
                end_time = time.time()
                print('Calculation time: {}s'.format(round(end_time - start_time, 7)))

                self.current_state[px][py] = 'O'
                self.player_turn = 'X'


try:
    starting_player = input("If you want to go first, enter 'X'; otherwise, press enter: ")
    game = TicTacToeGame(starting_player.upper())
    game.play()
except KeyboardInterrupt:
    print('\nGame interrupted!')
