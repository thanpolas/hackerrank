import conway

game = conway.GolRules()

def run():
    for i in xrange(8):
        print 'Round:', i
        player_one = conway.Player('w', game.get_board())
        play = player_one.get_next_move()
        print 'Player w play:', play
        game.put_cell(play, 'w')

        player_two = conway.Player('b', game.get_board())
        play = player_two.get_next_move()
        print 'Player b play:', play
        game.put_cell(play, 'b')

    print game.get_board_str()

run()

# class Beta():
#     def __init__(self, cells):
#         self.cells = cells
#     def go(self):
#         for i in xrange(3):
#             gamma = Gamma(self.cells[:])
#             gamma.set_cell(i, 'x')
#             print "Iter #", i, self.cells
#     def get_cells(self):
#         return self.cells

# class Gamma():
#     def __init__(self, cells):
#         self.cells = cells
#     def set_cell(self, pos, cell):
#         self.cells[pos][0] = cell

# beta = Beta([['_', '_', '_'], ['_', '_', 'O'], ['_', 'X', '_']])

# beta.go()
# cells = beta.get_cells()
# cells[0][2] = 'Z'
# print beta.get_cells()

# results = [((4, 4), 85, 'w', 232, 0), ((4, 5), 53, 'w', 87, 0), ((4, 6), 85, 'w', 232, 0), ((5, 4), 85, 'w', 232, 0), ((6, 5), 85, 'w', 232, 0), ((6, 6), 85, 'w', 232, 0), ((4, 5), 53, 'w', 87, 0), ((4, 6), 85, 'w', 232, 0), ((4, 7), 499, 'b', 58, 87), ((6, 5), 85, 'w', 232, 0), ((6, 6), 85, 'w', 232, 0), ((4, 6), 85, 'w', 232, 0), ((4, 7), 499, 'b', 58, 87), ((4, 8), 499, 'b', 58, 87), ((5, 8), 499, 'b', 58, 87), ((6, 6), 85, 'w', 232, 0), ((6, 8), 499, 'b', 58, 87), ((5, 8), 499, 'b', 58, 87), ((6, 6), 85, 'w', 232, 0), ((6, 8), 499, 'b', 58, 87), ((7, 6), 1, 'w', 29, 0)]

# win_cases = filter(lambda score: score[2] == 'w', results)
# print len(results), len(win_cases)

# win_cases.sort(key=lambda tup:(tup[1], tup[3]*-1))
# print win_cases

