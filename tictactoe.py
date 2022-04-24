# Inspiration from AIMA,Russell,Novig, Shiffman
import random

# positive infinity
p_inf = float("inf")
# negative infinity
n_inf = float("-inf")

board = [
  ['', '', ''],
  ['', '', ''],
  ['', '', '']

]


scores = {'X': 10,'O': -10,'tie': 0}
ai = 'X'
human = 'O'
currentPlayer = human
chars = ['X', 'O']


def check_for_winner(boardf):
    # test win for each character
    for x in chars:
        # check at for triple at row or col
        for y in range(3):
            if x == boardf[0][y] and x == boardf[1][y] and x == boardf[2][y]:
                return x
            if x == boardf[y][0] and x == boardf[y][1] and x == boardf[y][2]:
                return x
        # check at the diagonals
        if x == boardf[0][0] and x == boardf[1][1] and x == boardf[2][2]:
            return x
        if x == boardf[0][2] and x == boardf[1][1] and x == boardf[2][0]:
            return x

    # checks if board is filled to determine if tie
    tie = True
    for x in range(3):
        for y in range(3):
            if boardf[x][y] != 'X' and boardf[x][y] != 'O':
                tie = False
    if tie:
        return 'tie'

    # returns no if not terminal state
    return 'no'


def minimax(boardf, isMaximizing):
    # returns score at terminal state
    winner = check_for_winner(boardf)
    if winner != 'no':
        return scores[winner], None, None

    if isMaximizing:
        v = n_inf
        for x, y in actions(boardf):
            boardf[x][y] = "X"
            v2, ax, ay = minimax(boardf, False)
            # undoes placing char
            boardf[x][y] = ""
            # maximizes
            if v2 >= v:
                v, movex, movey = v2, x, y

    else:
        v = p_inf
        for x, y in actions(boardf):
            boardf[x][y] = "O"
            v2, ax, ay = minimax(boardf, True)
            # undoes placing char
            boardf[x][y] = ""
            # minimizes
            if v2 <= v:
                v, movex, movey = v2, x, y

    # returns score and coords for move
    return v, movex, movey


def find_best_move():
    temp, movex, movey = minimax(deepcopy(board), True)
    move = movex, movey
    return move


def actions(boardf):
    # checks if space is empty and yields that position
    for x in range(3):
        for y in range(3):
            if boardf[x][y] != 'X' and boardf[x][y] != 'O':
                yield x, y


def utility(boardf):
    # returns score of terminal state
    winner = check_for_winner(boardf)
    return scores[winner]


# displays board
def display():
    print("=============")
    for x in board:
        for y in x:
            if y == '':
                y = " "
            print("| " + y, end=' ')
        print("|")
        print("=============")


# places char at pos
def move(char, pos):
    x, y = pos
    if board[x][y] == '':
        board[x][y] = char
        return True
    else:
        return False


def minimove(boardf, char, posx, posy):
    # used in minimax to move
    boardf[posx][posy] = char
    return boardf



def main():
    print("AI moves first! Please be patient")
    move("X", find_best_move())
    display()

    game_over = False
    while not game_over:
        # ask user for move
        goodinp = False
        while not goodinp:
            inp = input(
                "Which cell would you like to put an 'O' in?  \n"
                "starting from top left:0,0 0,1 0,2 1,0 1,1 1,2 2,0 2,1 2,2\n")
            # makes sure input is comma separated ints
            try:
                inp = tuple(map(int, inp.split(',')))

            except ValueError:
                print("Make sure to type in two integers separated by a comma and nothing else")

            # makes sure there's only 2 inputs and both are in range
            if len(inp) == 2:
                goodinp = True
                for x in inp:
                    if x not in range(3):
                        goodinp = False
                        print("space not in board")
                if goodinp == True and board[inp[0]][inp[1]] != '':
                    goodinp = False
                    print("Choose empty space")

        move("O", inp)
        move("X", find_best_move())
        display()

        # check if game over
        winner = check_for_winner(board)
        if winner != 'no':
            if winner == 'tie':
                print("Tie")
            else:
                print("Winner is", winner)
            game_over = True



#Calls on main
main()