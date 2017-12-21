import random


def float_eq(lhs, rhs):
    return abs(lhs - rhs) < 0.000001


class Tile:
    def __init__(self):
        self.id = ' '

    id = ' '


class Game:
    __board = [[Tile() for x in range(3)] for y in range(3)]

    def __init__(self):
        self.__is_x_turn = True

    def print_board(self):
        for i in range(0, 5):
            if i % 2 == 0:
                print(self.__board[i / 2][0].id + "|" +
                      self.__board[i / 2][1].id + "|" +
                      self.__board[i / 2][2].id)
            else:
                print("-" * 5)
        print '\n'

    def print_winner(self):
        if self.__someone_won():
            if self.__is_x_turn:
                print("Game over - O wins!!")
            else:
                print("Game over - X wins!!")
        else:
            print("Game over - draw")

    def __someone_won(self):
        for i in range(0, 3):
            if (self.__board[i][0].id == self.__board[i][1].id == self.__board[i][2].id != ' ' or
                    self.__board[0][i].id == self.__board[1][i].id == self.__board[2][i].id != ' '):
                return True
        if (self.__board[0][0].id == self.__board[1][1].id == self.__board[2][2].id != ' ' or
                self.__board[0][2].id == self.__board[1][1].id == self.__board[2][0].id != ' '):
            return True
        return False

    def __stalemate(self):
        for i in range(0, 3):
            for j in range(0, 3):
                if self.__board[i][j].id == ' ':
                    return False
        return True

    # Makes a move on the board - NOTE: 0-8, although interface is 1-9
    def __make_move(self, num_in, is_x):
        while num_in < 0 or num_in > 8:
            num_in = int(raw_input("Invalid input")) - 1
        while self.__id_at(num_in) != ' ':
            num_in = int(raw_input("That square is filled")) - 1
        if is_x:
            self.__board[num_in // 3][num_in % 3].id = 'X'
        else:
            self.__board[num_in // 3][num_in % 3].id = 'O'

    def __revert_move(self, num_in):
        self.__board[num_in // 3][num_in % 3].id = ' '

    def __id_at(self, num_in):
        return self.__board[num_in // 3][num_in % 3].id

    def __is_empty(self, num_in):
        return self.__id_at(num_in) == ' '

    def run_game(self, player_num):
        self.print_board()
        if player_num == 0:
            self.__run_0p_game()
        elif player_num == 1:
            self.__run_1p_game()
        elif player_num == 2:
            self.__run_2p_game()
        else:
            print("ERROR: You can't play Tic-Tac-Toe with that many people, you dunce")
        self.clear_board()

    @staticmethod
    def __run_0p_game():
        print("not made yet")

    def __run_1p_game(self):
        player_char = raw_input("Do you want to be X or O?")
        if player_char == 'X':
            while not self.__someone_won() and not self.__stalemate():
                if self.__is_x_turn:
                    self.__make_move(int(raw_input("X's turn to move:")) - 1, self.__is_x_turn)
                else:
                    self.__make_ai_move3(self.__is_x_turn)
                self.__is_x_turn = not self.__is_x_turn
                self.print_board()
        elif player_char == 'O':
            while not self.__someone_won() and not self.__stalemate():
                if self.__is_x_turn:
                    self.__make_ai_move3(self.__is_x_turn)
                else:
                    self.__make_move(int(raw_input("O's turn to move:")) - 1, self.__is_x_turn)
                self.__is_x_turn = not self.__is_x_turn
                self.print_board()
        self.print_winner()

    def __run_2p_game(self):
        char = 'X'
        while not self.__someone_won():
            char = 'X' if self.__is_x_turn else 'O'
            self.__make_move(int(raw_input(char + "'s turn to move:")) - 1, self.__is_x_turn)
            self.__is_x_turn = not self.__is_x_turn
            self.print_board()
        print(char + " wins!")

    # Uses minimax algorithm to assess strength of possible moves.  Selects a move which has the worst best move for
    # the enemy and decides between ties based off of number of mistakes enemy can make from your theoretical move
    def __make_ai_move2(self, is_x):
        if is_x:
            poss_moves = [{'best': -2, 'avg': -2}] * 9
            best_moves = []
            best_poss = -2
            best_avg = -2
            # loop through the board making all legal moves to assess their strengths
            # then find the best possible outcome in poss_moves
            for i in range(0, 9):
                if self.__is_empty(i):
                    self.__make_move(i, is_x)
                    poss_moves[i] = self.__minimax2(False)
                    self.__revert_move(i)
                    if poss_moves[i]['best'] > best_poss:
                        best_poss = poss_moves[i]['best']
                    if poss_moves[i]['avg'] > best_avg:
                        best_avg = poss_moves[i]['avg']

            # find moves that can reach best outcome level and put the one with best average outcome in best_moves
            for i in range(0, 9):
                if self.__is_empty(i):
                    if poss_moves[i]['best'] == best_poss and float_eq(poss_moves[i]['avg'], best_avg):
                        best_moves.append(i)
            self.__make_move(best_moves[random.randint(0, len(best_moves) - 1)], is_x)
        else:
            poss_moves = [{'best': 2, 'avg': 2}] * 9
            best_moves = []
            # loop through the board making all legal moves to assess their strengths
            for i in range(0, 9):
                if self.__is_empty(i):
                    self.__make_move(i, is_x)
                    poss_moves[i] = self.__minimax2(True)
                    self.__revert_move(i)
            # find the best possible outcome in poss_moves
            best_poss = 2
            best_avg = 2
            for i in range(0, 9):
                if self.__is_empty(i):
                    if poss_moves[i]['best'] < best_poss:
                        best_poss = poss_moves[i]['best']
                    if poss_moves[i]['avg'] < best_avg:
                        best_avg = poss_moves[i]['avg']
            # find moves that can reach best outcome level and put the one with best average outcome in best_moves
            for i in range(0, 9):
                if self.__is_empty(i):
                    if poss_moves[i]['best'] == best_poss and float_eq(poss_moves[i]['avg'], best_avg):
                        best_moves.append(i)
            self.__make_move(best_moves[random.randint(0, len(best_moves) - 1)], is_x)

    def __make_ai_move3(self, is_x):
        if is_x:
            poss_moves = [{'best': -2, 'avg': -2}] * 9
            best_poss = -2
            best_avg = -2
        else:
            poss_moves = [{'best': 2, 'avg': 2}] * 9
            best_poss = 2
            best_avg = 2

        # loop through the board making all legal moves to assess their strengths
        # then find the best possible outcome in poss_moves
        for i in range(0, 9):
            if self.__is_empty(i):
                self.__make_move(i, is_x)
                if is_x:
                    poss_moves[i] = self.__minimax3(False)
                    if poss_moves[i]['best'] > best_poss:
                        best_poss = poss_moves[i]['best']
                    if poss_moves[i]['avg'] > best_avg:
                        best_avg = poss_moves[i]['avg']
                else:
                    poss_moves[i] = self.__minimax3(True)
                    if poss_moves[i]['best'] < best_poss:
                        best_poss = poss_moves[i]['best']
                    if poss_moves[i]['avg'] < best_avg:
                        best_avg = poss_moves[i]['avg']
                self.__revert_move(i)

        best_moves = []
        # find moves that can reach best outcome level and put the ones with best average outcome in best_moves
        for i in range(0, 9):
            if self.__is_empty(i):
                if poss_moves[i]['best'] == best_poss and float_eq(poss_moves[i]['avg'], best_avg):
                    best_moves.append(i)
        self.__make_move(best_moves[random.randint(0, len(best_moves) - 1)], is_x)

    def __minimax2(self, is_x):
        # If someone has won, return 1 or -1 depending on who won
        if is_x:
            if self.__someone_won():
                return {'best': -1, 'avg': -1}
        else:
            if self.__someone_won():
                return {'best': 1, 'avg': 1}
        if self.__stalemate():
            return {'best': 0, 'avg': 0}

        # Recursive calls based on whose turn it is
        if is_x:
            their_minimax = []
            for i in range(0, 9):
                if self.__id_at(i) == ' ':
                    self.__make_move(i, is_x)
                    move_val = self.__minimax2(False)
                    their_minimax.append(move_val['best'])
                    self.__revert_move(i)
            return {'best': max(their_minimax), 'avg': sum(their_minimax) / len(their_minimax)}
        else:
            their_minimax = []
            for i in range(0, 9):
                if self.__id_at(i) == ' ':
                    self.__make_move(i, is_x)
                    move_val = self.__minimax2(True)
                    their_minimax.append(move_val['best'])
                    self.__revert_move(i)
            return {'best': min(their_minimax), 'avg': sum(their_minimax) / len(their_minimax)}

    def __minimax3(self, is_x):
        # If someone has won, return 1 or -1 depending on who won
        if is_x:
            if self.__someone_won():
                return {'best': -1, 'avg': -1}
        else:
            if self.__someone_won():
                return {'best': 1, 'avg': 1}
        if self.__stalemate():
            return {'best': 0, 'avg': 0}

        their_minimax = []
        their_avg = []
        # Recursive calls based on whose turn it is
        for i in range(0, 9):
            if self.__id_at(i) == ' ':
                self.__make_move(i, is_x)
                if is_x:
                    move_val = self.__minimax2(False)
                else:
                    move_val = self.__minimax2(True)
                their_minimax.append(move_val['best'])
                their_avg.append(move_val['avg'])
                self.__revert_move(i)
        if is_x:
            return {'best': max(their_minimax), 'avg': sum(their_avg) / len(their_avg)}
        else:
            return {'best': min(their_minimax), 'avg': sum(their_avg) / len(their_avg)}

    def set_test(self, num_in, char_in):
        self.__board[num_in // 3][num_in % 3].id = char_in

    def print_minimax2_x(self):
        best_move = -10
        for i in range(0, 9):
            if self.__id_at(i) == ' ':
                self.__make_move(i, True)
                move_val = self.__minimax2(False)
                best_move = max(best_move, move_val)
                self.__revert_move(i)
        print(best_move)

    def clear_board(self):
        for i in range(0, 9):
            self.__board[i // 3][i % 3].id = ' '
        self.__is_x_turn = True


the_game = Game()
num_players = int(raw_input("How many players?"))
the_game.run_game(num_players)
answer = raw_input("Play again? (y/n/d)")
while answer != "n":
    if answer != "y" and answer != "d":
        answer = raw_input("Please answer with y (yes), n (no), or d (different player number)")
    elif answer == "y":
        the_game.run_game(num_players)
        answer = raw_input("Play again? (y/n/d)")
    else:
        num_players = int(raw_input("How many players?"))
        the_game.run_game(num_players)
        answer = raw_input("Play again? (y/n/d)")
print("Thanks for playing!")
