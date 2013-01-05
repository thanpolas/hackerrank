#!/bin/python
import tictactoe

#Read the board now. The board is a 3x3 array filled with X, O or _.

def make_play(pos_string, player, board):
    print pos_string + " player:" + player
    pos = pos_string.split(' ')
    pos[0] = int(pos[0])
    pos[1] = int(pos[1])
    play_row = board[pos[0]]
    colOne = player if pos[1] == 0 else play_row[0]
    colTwo = player if pos[1] == 1 else play_row[1]
    colThree = player if pos[1] == 2 else play_row[2]
    board[pos[0]] = ( colOne + colTwo + colThree )
    return board

#board = [('___'), ('___'), ('___')]
# board = [('__X'),
#          ('_O_'),
#          ('___')]
# playerInst = tictactoe.TicPlayer('O', board)
# print playerInst.get_next_move()

# for i in xrange(0, 9):
#     player = 'X' if i % 2 == 0 else 'O'
#     playerInst = tictactoe.TicPlayer(player, board)
#     board = make_play(playerInst.get_next_move(), player, board)
#     print 'Round ' + str(i + 1) + ' Player: ' + player
#     print board

# _ _ _
# _ _ _
# _ _ _

# 0 1 2
# 3 4 5
# 6 7 8

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


fiveTiles = [('100'), ('111'), ('010')]


