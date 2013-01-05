#!/bin/python
import random

# Complete the function below to print 2 integers separated by a single space which will be your next move
def nextMove(player,board):
    print (1, 0)


#If player is X, I'm the first player.
#If player is O, I'm the second player.
player = raw_input()

#Read the board now. The board is a 3x3 array filled with X, O or _.
board = []
for i in xrange(0, 3):
    board.append(raw_input())

nextMove(player,board)