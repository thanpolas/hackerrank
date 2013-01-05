#!/bin/python
import random

W = 'w'
B = 'b'
_ = '-'
bounds = (28, 28) #row, col

fiveTiles = [('100'), ('111'), ('010')]

posAnchors = [
    (1,3),
    (2,16),
    (7, 4),
    (9, 21),
    (11, 16),
    (16, 5),
    (17, 20),
    (21, 3),
    (22, 15),
    (23, 22)
]

def nextMove(player, board):
    player = Conway(player, board)
    return player.get_next_move()

class Conway():

    def __init__(self, player, board):
        self.player = player
        self.opponent = B if player == W else W

        self.board = board
        self.board_items = {
            'w': [],
            'b': [],
            '-': []
        }

        self._next_tile = None

        for pos, item in self.next():
            self.board_items[item].append(pos)

    def get_next_move(self):
        for posAnc in posAnchors:
            if not self._get_tile(posAnc):
                return posAnc

            if not self._is_pattern_complete(posAnc):
                return self._get_next_tile(posAnc)

        return self._get_random_tile()


    def _is_pattern_complete(self, posAnc):
        for row, rowPat in enumerate(fiveTiles):
            for col, colPat in enumerate(rowPat):
                pos = (posAnc[0] + row, posAnc[1] + col)
                if bool(int(colPat)) and self._is_tile_free(pos):
                    self._next_tile = pos
                    return False
        return True

    def _get_next_tile(self, posAnc):
        return self._next_tile

    def _get_tile(self, pos):
        return self.board[pos[0]][pos[1]]

    def _is_tile_free(self, pos):
        return pos in self.board_items[_]

    def next(self):
        for rowCount, row in enumerate(self.board):
            for colCount, item in enumerate(row):
                yield ((rowCount, colCount), item)

    def _get_random_tile(self):
        while True:
            row = random.randint(0, bounds[0])
            col = random.randint(0, bounds[1])
            pos = (row, col)
            if self._is_tile_free(pos):
                return pos

player = raw_input()
board = []
for i in xrange(0, 29):
    board.append(raw_input())

a,b = nextMove(player,board)
print a,b
