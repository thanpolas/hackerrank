#!/bin/python
import tictactoe
from time import time

# _ _ _
# _ _ _
# _ _ _

# 0 1 2
# 3 4 5
# 6 7 8
#
#
# 1 L3 W1 D2
# 3 L1 W0 D4
# 4 L2 W3 D5
# 6 L0 W0 D9
#

# First submittion, static code results:
# 25% win - 260games played - 65games won / 195 lost (!)


# Positions map
playMap = {
    0: (0,0),
    1: (0,1),
    2: (0,2),
    3: (1,0),
    4: (1,1),
    5: (1,2),
    6: (2,0),
    7: (2,1),
    8: (2,2)
}

game = tictactoe.TicTacToe()

def run():
    i = 0
    while not game.is_finished():
        i += 1
        start_time = time()
        player_one = tictactoe.TicPlayer('X', game.get_board())
        x_move = player_one.get_next_move()

        game.put_item(x_move, 'X')
        x_time = time() - start_time

        o_time = time()
        player_two = tictactoe.TicPlayer('O', game.get_board())
        if not game.is_finished():
            o_move = player_two.get_next_move()
            game.put_item(o_move, 'O')
        print 'Round: %d Player X:%s (%f) -- O:%s (%f) :: Total Time: %f' %(i, x_move, x_time, o_move, time() - o_time, time() - start_time)

        print game.get_board_str()

def scenario(board, player):
    player_one = tictactoe.TicPlayer(player, board)
    x_move = player_one.get_next_move()
    print x_move


board = ['___', '_O_', '__X']

run()
#scenario(board, 'X')
