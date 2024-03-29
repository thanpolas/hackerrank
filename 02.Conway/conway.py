#!/bin/python
import random
import copy
from time import time

W = 'w'
B = 'b'
_ = '-'
DRAW = 'draw'
BOUNDS = (29, 29) #row, col
# The number of adjacent cells from which we consider
# the group to be an island
ISLAND_TREASHOLD = 2
# How many good results to find before stopping simulations
GOOD_RESULTS_THREASHOLD = 8
# On the final turns raise the threashold
GOOD_RESULTS_LATE_THREASHOLD = 20
# On how many final turns to raise the threashold
FINAL_TURNS_TRIGGER = 5
# Time to thottle execution of move calculation in secs
TIME_THROTTLE = 12
# Generations to perform before giving up (HR does 500 but requires too much cpu)
HR_GENS = 200
# Total cells we position
HR_CELLS = 40

PATTERNS = {
    # Popular GOL Patterns
    # Numbers separated by commas are:
    # 1. Total Generations
    # 2. Initial Population
    # 3. Final Population
    # 4. Population at 500 turns (hackerrank rules)
    #
    'r_pentonimo': [ #1103, 5, 116, 174
        [1,0,0],
        [1,1,1],
        [0,1,0]],
    'acorn': [ #5206, 7, 633, 276
        [0,1,0,0,0,0,0],
        [0,0,0,1,0,0,0],
        [1,1,0,0,1,1,1]],
    'noahs_ark': [#1344, 16, ~1100, 474
        [0,0,0,0,0,0,0,0,0,0,1,0,1,0,0],
        [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,1,0,0,1,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,0,0,10,0,0,0,0,0,0,0,0,0,0,],
        [0,0,1,1,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0]],
    'math_multum': [ #3933, 7, 633, 485
        [0,0,0,1,1,1],
        [0,0,1,0,0,1],
        [0,1,0,0,0,0],
        [1,0,0,0,0,0]
    ],
    'glider_top_left': [
        [1,1,1],
        [1,0,0],
        [0,1,0]],
    'glider_top_right': [
        [1,1,1],
        [0,0,1],
        [0,1,0]],
    'glider_bottom_right': [
        [0,1,0],
        [0,0,1],
        [1,1,1]],
    'glider_bottom_left': [
        [0,1,0],
        [1,0,0],
        [1,1,1]]
}

def nextMove(player, board):
    player = Player(player, board)
    return player.get_next_move()

class Player():

    def __init__(self, player, board):
        self.player = player
        self.opponent = B if player == W else W
        self.board = []
        for rows in board:
            row_items = []
            for item in rows:
                row_items.append(item)
            self.board.append(row_items)

        self.board_items = {
            'w': [],
            'b': [],
            '-': []
        }

        for pos, item in self.next():
            self.board_items[item].append(pos)

    def get_next_move(self):
        # Main class entry point
        if self._get_player_count() < 7: #multum pattern size
            next_move = self._draw_pattern(PATTERNS['math_multum'])
            if next_move is not None:
                return next_move # otherwise attack

        # Start attacking
        return self._attack()

    def _attack(self):
        """master attack algo entry point. Returns next pos"""

        opponent_islands = self._get_opponent_islands()

        # Get not attacked opponent islands
        clean_opponent_islands = self._get_clean_opponent_islands(opponent_islands)

        if len(clean_opponent_islands):
            prospect_attack_pos = self._get_adjacent_dead_cells(clean_opponent_islands[0])
        else:
            prospect_attack_pos = self._get_adjacent_dead_cells_from_list(opponent_islands)

        return self._get_optimal_attack_pos(prospect_attack_pos)

    def _get_optimal_attack_pos(self, prospect_attack_pos):
        random.shuffle(prospect_attack_pos)
        pos_score = self._run_emulations(prospect_attack_pos)
        win_cases = filter(lambda score: score[2] == self.player, pos_score)
        #print self.player, pos_score

        if not len(win_cases):
            # not good...
            if len(prospect_attack_pos):
                return prospect_attack_pos[0]
            # not good at all, only single cells exist in grid
            empty_cells = self._get_adjacent_dead_cells(self.board_items[self.opponent])
            if len(empty_cells):
                return empty_cells[0]
            # all failed... wtf
            return self._get_random_pos()


        # Define the tuple key our player is on and sort the
        # win cases by generations count asc
        # and by living cells desc
        p = 3 if self.player == W else 4
        win_cases.sort(key=lambda tup:(tup[1], tup[p]*-1))
        return win_cases[0][0] # Best case position

    def _run_emulations(self, prospect_attack_pos):
        pos_score = []
        # pos_score will contain the result of each simulation
        # that is run.
        #
        # The result stored is a tuple with the following values:
        # 0. pos: the row,col tuple
        # 1. generation: the number of generation the sim concluded
        # 2. Winner: W, B or DRAW
        # 3. W Count: White player count
        # 4. B Count: Black player count
        start_time = time()
        good_threashold = GOOD_RESULTS_THREASHOLD
        # Check if on last turn trigger...
        # In that case raise the good_threashold
        if self._get_player_count() == HR_CELLS-FINAL_TURNS_TRIGGER:
            # opponent has the last word
            good_threashold = GOOD_RESULTS_LATE_THREASHOLD

        for index, pos in reversed(list(enumerate(prospect_attack_pos))):
            game_sim = GolRules()
            game_sim.set_board(self.board)
            # make our prospect move
            game_sim.put_cell(pos, self.player)


            for i in xrange(HR_GENS):
                game_sim.generate()
                if game_sim.game_ended():
                    break

            game_score = (pos, i, game_sim.get_winner(), game_sim.get_count(W), game_sim.get_count(B))
            pos_score.append(game_score)
            elapsed = time() - start_time
            # print "Time: %f Iters: %d player: %s " % (elapsed, i, self.player), game_score, game_sim.game_ended()

            #print game_sim.count_history

            # stop sims if we find a satisfactory win case
            good_cases = filter(lambda score: score[1]<(HR_GENS-10) and score[2]==self.player, pos_score)

            if len(good_cases) >= good_threashold:
                return pos_score

            if elapsed > TIME_THROTTLE:
                return pos_score

        return pos_score

    def _get_opponent_islands(self):
        """return an array with arrays of pos representing opponent's
            islands. An island is considered a concentration of at least
            3 opponent adjacent cells"""
        islands = []
        examined_pos = []
        opponent_cells = self.board_items[self.opponent]

        loop_cells = []

        def recurse_pos(pos_exam):
            loop_cells.append(pos_exam)
            examined_pos.append(pos_exam)
            adjacent = self._get_adjacent_cells(pos_exam)
            for pos in adjacent:
                if pos in examined_pos: continue
                if pos in opponent_cells:
                    examined_pos.append(pos)
                    recurse_pos(pos)

        for pos in opponent_cells:
            loop_cells = []
            if pos in examined_pos: continue
            recurse_pos(pos)
            if len(loop_cells) >= ISLAND_TREASHOLD:
                islands.append(loop_cells)

        return islands

    def _get_adjacent_cells(self, pos):
        cells = []
        cells.append((pos[0]-1, pos[1]-1))
        cells.append((pos[0]-1, pos[1]))
        cells.append((pos[0]-1, pos[1]+1))
        cells.append((pos[0], pos[1]-1))
        cells.append((pos[0], pos[1]+1))
        cells.append((pos[0]+1, pos[1]-1))
        cells.append((pos[0]+1, pos[1]))
        cells.append((pos[0]+1, pos[1]+1))
        #eliminate out of bounds cells
        clear_cells = []
        for cell in cells:
            if cell[0] < 0 or cell[0] > BOUNDS[0]: continue
            if cell[1] < 0 or cell[1] > BOUNDS[1]: continue
            clear_cells.append(cell)

        return clear_cells

    def _get_adjacent_dead_cells(self, cells):
        dead_cells = []
        for pos in cells:
            adjacent_cells = self._get_adjacent_cells(pos)
            for cell in adjacent_cells:
                if self._get_pos_item(cell) == _:
                    dead_cells.append(cell)
        return dead_cells

    def _get_adjacent_dead_cells_from_list(self, islands):
        dead_cells = []
        for cells in islands:
            dead_cells += self._get_adjacent_dead_cells(cells)
        return dead_cells

    def _get_clean_opponent_islands(self, opponent_islands):
        """From the islands provided check which ones have not
            been attacked and return them"""

        clean_islands = []
        for island in opponent_islands:
            try:
                for opponent_pos in island:
                    cells = self._get_adjacent_cells(opponent_pos)
                    for pos in cells:
                        if self._get_pos_item(pos) == self.player:
                            raise StopIteration
                clean_islands.append(island)
            except StopIteration:
                pass
        return clean_islands


    def _draw_pattern(self, pattern):
        """return next pos for defined pattern"""
        if self._get_player_count() == 0:
            return self._draw_pattern_first_move()

        start_player_pos = self.board_items[self.player][0]
        pattern_offset_pos = None # Top left corner to apply pattern
        pattern_item_count = 0
        for row, row_list in enumerate(pattern):
            for col, cell in enumerate(row_list):
                if not cell:
                    continue
                pattern_item_count += 1
                if pattern_item_count == 1:
                    pattern_offset_pos = (start_player_pos[0] - row, start_player_pos[1] - col)

                if pattern_item_count > self._get_player_count():
                    pos = (pattern_offset_pos[0] + row, pattern_offset_pos[1] + col)
                    if self._is_pos_free(pos):
                        return pos
                    # cell occupied, move to next one...


    def _draw_pattern_first_move(self):
        # first play, check opponent's move
        if self._get_opponent_count() == 0:
            # We have the initiative, statically select center
            # to bottom-right
            col = 16
            while True:
                pos = (16, col)
                if self._is_pos_free(pos):
                    return pos
                col += 1

        # get opponents quadrant
        op_quad = self._get_pos_quadrant(self.board_items[self.opponent][0])
        # Go to the opposite quad
        player_quad = self._get_opposite_quadrant(op_quad)
        quad_center_pos = self._get_quadrant_center_pos(player_quad)
        # -2, -2 for grace
        return (quad_center_pos[0] - 2, quad_center_pos[1] -2)

    def _get_next_pos(self, posAnc):
        return self._next_pos

    def _get_pos_item(self, pos):
        try:
            return self.board[pos[0]][pos[1]]
        except:
            return -1

    def _is_pos_free(self, pos):
        return pos in self.board_items[_]

    def next(self):
        for rowCount, row in enumerate(self.board):
            for colCount, item in enumerate(row):
                yield ((rowCount, colCount), item)

    def _get_random_pos(self):
        while True:
            row = random.randint(0, BOUNDS[0])
            col = random.randint(0, BOUNDS[1])
            pos = (row, col)
            if self._is_pos_free(pos):
                return pos

    def _get_player_count(self):
        return len(self.board_items[self.player])
    def _get_opponent_count(self):
        return len(self.board_items[self.opponent])
    def _get_pos_quadrant(self, pos):
        # 0, 1
        # 2, 3
        if pos[0] < BOUNDS[0] / 2:
            return 0 if pos[1] < BOUNDS[1] / 2 else 1
        else:
            return 2 if pos[1] < BOUNDS[1] / 2 else 3
    def _get_opposite_quadrant(self, quad):
        if quad == 0:
            return 3
        elif quad == 1:
            return 2
        elif quad == 2:
            return 1
        else:
            return 0
    def _get_quadrant_center_pos(self, quad):
        row_half = BOUNDS[0] / 2
        row_quarter = BOUNDS[0] / 4
        col_half = BOUNDS[1] / 2
        col_quarter = BOUNDS[1] / 4

        if quad == 0:
            return (row_quarter, col_quarter)
        elif quad == 1:
            return (row_quarter, col_half + col_quarter)
        elif quad == 2:
            return (row_half + row_quarter, col_quarter)
        else:
            return (row_half + row_quarter, col_half + col_quarter)


class GolRules():
    def __init__(self, board=None, bounds=BOUNDS):
        # bounds is a 2 value tuple, rows / cols
        self.bounds = bounds
        # board is an array of arrays representing the board
        if board is None:
            self.board = self._generate_board()
        else:
            self.set_board(board)

        self.board_items = {
            'w': [],
            'b': [],
            '-': []
        }

        # will contain a history of cells count.
        # Items will be tuples: (W,B)
        self.count_history = []

        self.generations = 0

    def _generate_board(self):
        board = []
        for i in xrange(self.bounds[0]):
            board.append([_] * self.bounds[1])
        return board

    def set_board(self, board):
        self.board = []
        for rows in board:
            row_items = []
            for item in rows:
                row_items.append(item)
            self.board.append(row_items)


    def get_board(self):
        return copy.deepcopy(self.board)

    def get_board_str(self, board=None):
        board = board if board is not None else self.board
        board_str = ''
        for row in board:
            for item in row:
                board_str += item
            board_str += "\n"

        return board_str

    def put_cell(self, pos, item):
        self.board[pos[0]][pos[1]] = item


    def generate(self):
        """generate 1 step and returns the new board"""

        next_board = self._generate_board()

        board_items = {
            'w': [],
            'b': [],
            '-': []
        }

        for pos, item in self.next():
            next_state = self._next_state(pos, item)
            next_board[pos[0]][pos[1]] = next_state
            board_items[next_state].append(pos)

        self.board = next_board
        self.board_items = board_items
        self.count_history.append((len(self.board_items[W]), len(self.board_items[B])))
        self.generations += 1

        return self.board

    def game_ended(self):
        w_count = len(self.board_items[W])
        b_count = len(self.board_items[B])
        if not w_count or not b_count:
            return True
        # Check if population has stabilized
        if self.generations > 10:
            last_run = self.count_history[self.generations -2]
            if last_run[0] == w_count and last_run[1] == b_count:
                return True

        return False

    def get_winner(self):
        """returns W, B or DRAW consts"""
        w_count = len(self.board_items[W])
        b_count = len(self.board_items[B])
        if w_count == b_count: return DRAW
        return W if w_count > b_count else B

    def get_count(self, item):
        return len(self.board_items[item])

    def _next_state(self, pos, item):
        """Determine the state of the next step for given pos"""
        neighborhood = {
            'w': 0,
            'b': 0,
            '-': 0,
            'out_of_bounds': 0
        }

        # -1 -1    -1 0    -1 +1
        #  0 -1     ---     0 +1
        # +1 -1    +1 0    +1 +1
        #
        neighborhood[self.get_item(pos, -1, -1)] += 1
        neighborhood[self.get_item(pos, -1)] += 1
        neighborhood[self.get_item(pos, -1, 1)] += 1
        neighborhood[self.get_item(pos, 0, -1)] += 1
        neighborhood[self.get_item(pos, 0, 1)] += 1
        neighborhood[self.get_item(pos, 1, -1)] += 1
        neighborhood[self.get_item(pos, 1)] += 1
        neighborhood[self.get_item(pos, 1, 1)] += 1

        total_near_items = neighborhood[W] + neighborhood[B]

        # certain death rule
        if total_near_items > 3 or total_near_items < 2:
            return _
        # life preservation rule
        if item is not _:
            return item
        # Dead cell becomes alive with 3 and only 3 nearby cells
        if total_near_items == 2:
            return _

        # Cell becomes alive
        return W if neighborhood[W] > neighborhood[B] else B

    def next(self):
        for rowCount, row in enumerate(self.board):
            for colCount, item in enumerate(row):
                yield ((rowCount, colCount), item)

    def get_item(self, pos, offset_row=None, offset_col=None):
        out = 'out_of_bounds'
        row = pos[0] if offset_row is None else pos[0] + offset_row
        col = pos[1] if offset_col is None else pos[1] + offset_col

        # Check for out of bounds
        if row < 0 or row > self.bounds[0]: return out
        if col < 0 or col > self.bounds[1]: return out
        try:
            return self.board[row][col]
        except:
            return out
