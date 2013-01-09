#!/bin/python
import random
import copy

X = 'X'
O = 'O'
_ = '_'
DRAW = 'DRAW'


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

WIN_CONDITIONS = [[0,1,2], [0,3,6], [0,4,8],
                  [1,4,7], [2,4,6], [2,5,8],
                  [3,4,5], [6,7,8]]


def nextMove(player,board):
    player = TicPlayer(player, board)
    print player.get_next_move()

class TicPlayer():

    def __init__(self, player, board):

        self.starting_pos_index = [0, 2, 6, 8]

        # board translated into 'playMap' indexes
        self.boardMap = {}
        # board reverse translated into 'playMap'
        self.board_items = {
            'X': [],
            'O': [],
            '_': []
        }

        self.outcomes = {}
        self.ar_outcomes = []

        self.nextMove = (0, 0)

        self.player = player
        self.opponent = X if self.player == O else O
        self.board = []
        item_count = 0
        for row, rows in enumerate(board):
            row_items = []
            for col, item in enumerate(rows):
                row_items.append(item)
                self.board_items[item].append(item_count)
                item_count += 1
            self.board.append(row_items)

    # Initial entry point
    def get_next_move(self):

        return self.static_strategy()

        #return self.sim_strategy()

    def sim_strategy(self):
        """Try every possible outcome and determine
            the best course"""

        turn = self._get_turn_no()
        # First move is scripted
        if turn == 0:
            self._first_move()
            return self._get_output()
        # Defence
        if self._has_threat():
            return self._get_output()

        self._run_simulations()

        pos_index = self._find_next_move_win()
        if not pos_index == False:
            return playMap[pos_index]

        self.nextMove = self._find_optimal_move()
        return self._get_output()


    def _find_next_move_win(self):
        for pos_index in self.outcomes:
            if 1 in self.outcomes[pos_index][self.player]:
                return pos_index
        return False

    def _find_optimal_move(self):
        # convert the dict into an array containing tuples
        # the tuples schema is:
        # 0. Position    :: (0,0)
        # 1. Win count   :: 1
        # 2. Loose count :: 1
        # 3. Draw count  :: 1
        # Todo factor in the move_count that is available
        for pos_index in self.outcomes:
            outcome = self.outcomes[pos_index]
            pos = playMap[pos_index]
            wins = len(outcome[self.player])
            looses = len(outcome[self.opponent])
            draws = len(outcome[DRAW])
            self.ar_outcomes.append((pos, wins, looses, draws))

        self.ar_outcomes.sort(key=lambda tup:(tup[2], tup[1]*-1))

        if len(self.ar_outcomes):
            return self.ar_outcomes[0][0]
        else:
            #EOL
            return playMap[self.board_items[_][0]]

    def _run_simulations(self):
        for pos_index in playMap:
            if not self._is_tile_free(playMap[pos_index]):
                continue
            game = TicTacToe(self.board)
            self.outcomes[pos_index] = {
                'X': [],
                'O': [],
                'DRAW': []
            }

            self.recurse_moves(pos_index, self.player, game, self.outcomes[pos_index], 0)

    def recurse_moves(self, pos_index, player, game, outcome, move_count):
        game.put_item(pos_index, player)
        move_count += 1
        if game.has_winner():
            outcome[game.get_winner()].append(move_count)
            return
        next_player = X if player is O else O
        for pos_index_next in playMap:
            new_game = TicTacToe(game.get_board())
            if not game.is_pos_free(pos_index_next):
                continue
            self.recurse_moves(pos_index_next, next_player, new_game, outcome, move_count)

        if game.is_draw() and not game.has_winner():
            outcome[DRAW].append(1)

    def static_strategy(self):

        if not self._has_win() and not self._has_threat():
            self._next_move()

        return self._get_output()

    def _iter(self, boardItem):
        for rowCount, row in enumerate(self.board):
            for colCount, item in enumerate(row):
                yield (rowCount, colCount, item)


    def _has_threat(self):
        if self._check_all(self.opponent):
            return True

        # Check for case where we are O, on step 2 and
        # opponent has diagonal corners. In that case
        # We need to play on the cross and not diagonal
        if self.player == O and 1 == self._get_turn_no():
            if (0 in self.board_items[self.opponent]
             and 8 in self.board_items[self.opponent]
             or
             2 in self.board_items[self.opponent]
             and 6 in self.board_items[self.opponent]):
                self.nextMove = (0,1)
                return True

        # Check for possible traps
        trap_pos = self._find_traps(self.opponent)
        if len(trap_pos) == 0:
            return False
        # There are possible traps, force play out of them
        win_chance_pos = self._find_traps(self.player, 0)
        #print "traps:", trap_pos
        #print "our win:", win_chance_pos
        for pos_index in win_chance_pos:
            force_play = self._get_winning_pos(pos_index, self.player)
            #print "For:", pos, " force:", force_play
            if force_play not in trap_pos:
                #print pos, " is not in trap"
                self.nextMove = pos_index
                return True

        # This is a bogus outcome
        return False

    def _has_win(self):
        return self._check_all(self.player)

    def _next_move(self):
        turn = self._get_turn_no()

        if turn == 0: self._first_move()
        elif turn == 1: self._second_move()
        elif turn == 2: self._third_move()
        else: self._any_move()

    def _first_move(self):
        if self.player == O:
            # First move for O is center
            self.nextMove = (1,1)
            if self._is_tile_free(self.nextMove):
                return True
            else:
                #play on the cross
                self.nextMove = (0,1)
                return True

        while True:
            next_pos_index = self.starting_pos_index[random.randint(0, 3)]
            # Do not use middle tile on first move
            next_pos_index = 5 if next_pos_index == 4 else next_pos_index
            self.nextMove = playMap[next_pos_index]
            if self._is_tile_free(self.nextMove):
                return True

    # Set the trap on second move
    def _second_move(self):
        step = 4
        while True:
            firstPos = self.board_items[self.player][0]
            if firstPos > 4:
                next_pos_index = firstPos - step
                next_pos_index = 3 if next_pos_index == 4 else next_pos_index
            else:
                next_pos_index = firstPos + step
                next_pos_index = 5 if next_pos_index == 4 else next_pos_index
            self.nextMove = playMap[next_pos_index]
            if self._is_tile_free(self.nextMove):
                return True
            step -= 1

    # Close the trap
    def _third_move(self):
        trap_pos = self._find_traps(self.player)
        if len(trap_pos) == 0:
            self.nextMove = self._get_open_pos()
        else:
            self.nextMove = trap_pos.pop()
        return True

    def set_board_tile(self, pos, player):
        #print pos_index
        play_row = self.board[pos[0]]
        #pos = playMap[pos_index]
        colOne = player if pos[1] == 0 else play_row[0]
        colTwo = player if pos[1] == 1 else play_row[1]
        colThree = player if pos[1] == 2 else play_row[2]
        self.board[pos[0]] = ( colOne + colTwo + colThree )

    def _find_traps(self, player, win_chances=1):
        """Returns an array with all the possible trap
            positions in the board for the provided player token"""
        trap_positions = []

        for pos_index in self.board_items[_]:
            win_promise = self._win_promise_count(pos_index, player)
            if win_promise > win_chances: # win win
                trap_positions.append(pos_index)

        return trap_positions

    def _win_promise_count(self, pos_index, player):
        """return the winnning chances for the provided tile"""
        pos = playMap[pos_index]
        # temporarily put the selected position in
        # the board
        self.set_board_tile(pos, player)
        # Check for a double promissing win
        win_promise = 0
        if self._check_horizontal(pos[0], pos[1], player):
            win_promise += 1
        if self._check_vertical(pos[0], pos[1], player):
            win_promise += 1
        if self._check_diagonal(pos[0], pos[1], player):
            win_promise += 1

        # Reset the tile
        self.set_board_tile(pos, _)
        return win_promise



    # Any consecutive move (4+)
    def _any_move(self):
        self.nextMove = self._get_open_pos()
        return True

    # Get a random pos from the ones that are free
    def _get_open_pos(self):
        free_tiles_len = len(self.board_items[_])
        rand_index = random.randint(0, free_tiles_len-1)
        posIndex = self.board_items[_][rand_index]
        return playMap[posIndex]

    def _get_turn_no(self):
        turn = 0
        for row, col, item in self._iter(self.board):
            if item == self.player:
                turn += 1
        return turn

    def _is_tile_free(self, pos):
        return self._get_item(pos) == _

    def _get_winning_pos(self, pos_index, player):
        """return the winning position for the position
            provided. We assume there is one more token
            of the same type in a winning axis"""
        self.set_board_tile(playMap[pos_index], player)
        if not self._check_all(player):
            #bogus result
            self.set_board_tile(playMap[pos_index], _)
            return self._get_open_pos()
        self.set_board_tile(playMap[pos_index], _)
        return self.nextMove

    def _check_all(self, item_target):
        for row, col, item in self._iter(self.board):
            #print "examining:", row, col, item, item_target
            if item == item_target:
                if self._check_horizontal(row, col, item):
                    return True
                if self._check_vertical(row, col, item):
                    return True
                if self._check_diagonal(row, col, item):
                    return True
        return False


    def _check_horizontal(self, row, col, item):
        """Check if two of the items exist in the horizontal axis
            Returns boolean true if two are found and the third is
            free to use. Stores open coords in self.nextMove
        """
        tiles = [0, 1, 2]
        tiles.remove(col)
        posOne = (row, tiles[0])
        posTwo = (row, tiles[1])
        return self._find_pair(row, col, item, posOne, posTwo)

    def _check_vertical(self, row, col, item):
        """Check if two of the items exist in the vertical axis
            Returns boolean true if two are found and the third is
            free to use. Stores open coords in self.nextMove
        """
        tiles = [0, 1, 2]
        tiles.remove(row)
        posOne = (tiles[0], col)
        posTwo = (tiles[1], col)
        return self._find_pair(row, col, item, posOne, posTwo)

    def _check_diagonal(self, row, col, item):
        """Check if two of the items exist in the diagonal axis
            Returns boolean true if two are found and the third is
            free to use. Stores open coords in self.nextMove
        """
        # exclude positions with no diagonal option
        pos = (row, col)
        if pos in [(0,1), (1,0), (1,2), (2, 1)]:
            return False
        # handle case where item is in the middle of the matrix
        if pos == (1,1):
            posOne = (0,0)
            posTwo = (2,2)
            if self._find_pair(row, col, item, posOne, posTwo):
                return True
            posOne = (0,2)
            posTwo = (2,0)
            if self._find_pair(row, col, item, posOne, posTwo):
                return True
            return False

        # One of the remaining four corners
        posOne = (1,1)
        if row == 0:
            posTwo = (2,0) if col == 2 else (2,2)
        else:
            posTwo = (0,0) if col == 2 else (0,2)
        return self._find_pair(row, col, item, posOne, posTwo)

    def _find_pair(self, row, col, item, posOne, posTwo):
        if self._get_item(posOne) != _ and self._get_item(posTwo) != _:
            return False
        if self._get_item(posOne) == item:
            self.nextMove = posTwo
            return True
        if self._get_item(posTwo) == item:
            self.nextMove = posOne
            return True
        return False

    def _get_item(self, pos):
        return self.board[pos[0]][pos[1]]

    def _get_output(self):
        if type(self.nextMove) is int:
            self.nextMove = playMap[self.nextMove]
        return str(self.nextMove[0]) + " " + str(self.nextMove[1])




class TicTacToe():
    def __init__(self, board=None):
        # board reverse translated into 'playMap'
        self.board_items = {
            'X': [],
            'O': [],
            '_': []
        }
        self.board = None
        if board is None:
            self.board = self._generate_board()
        else:
            self.set_board(board)

    def _generate_board(self):
        board = []
        for i in xrange(3):
            board.append([_] * 3)
            self.board_items[_].append((i, 0))
            self.board_items[_].append((i, 1))
            self.board_items[_].append((i, 2))
        return board

    def set_board(self, board):
        self.board = []
        self.winner = None
        for row, rows in enumerate(board):
            row_items = []
            for col, item in enumerate(rows):
                row_items.append(item)
                self.board_items[item].append((row, col))
            self.board.append(row_items)

    def put_item(self, pos, item):
        p = self.get_pos_from_mixed(pos)
        self.board[p[0]][p[1]] = item
        self.board_items[item].append(p)
        self.board_items[_].remove(p)

    def has_winner(self):
        x_count = len(self.board_items[X])
        o_count = len(self.board_items[O])

        if x_count <= 2 and o_count <=2: return False

        for cond in WIN_CONDITIONS:
            if (not self.get_item(cond[0]) == _ and self.get_item(cond[0]) == self.get_item(cond[1])
                == self.get_item(cond[2])):
                self.winner = self.get_item(cond[2])
                return True
        return False

    def all_moves_done(self):
        return len(self.board_items[_]) == 0

    def is_draw(self):
        return self.all_moves_done() and not self.has_winner()

    def is_finished(self):
        return self.is_draw() or self.has_winner()

    def get_winner(self):
        return self.winner

    def get_item(self, pos):
        p = self.get_pos_from_mixed(pos)
        return self.board[p[0]][p[1]]

    def is_pos_free(self, pos):
        p = self.get_pos_from_mixed(pos)
        return self.board[p[0]][p[1]] == _

    def get_pos_from_mixed(self, pos):
        if type(pos) is int:
            return playMap[pos]
        elif type(pos) is str:
            p = pos.split(' ')
            return (int(p[0]), int(p[1]))
        else:
            return pos

    def get_board(self):
        return copy.deepcopy(self.board)

    def get_board_str(self):
        board_str = ''
        for row in self.board:
            for item in row:
                board_str += item
            board_str += "\n"

        return board_str



if __name__=="__main__":
    player = raw_input()

    #Read the board now. The board is a 3x3 array filled with X, O or _.
    board = []
    for i in xrange(0, 3):
        board.append(raw_input())

    nextMove(player,board)


