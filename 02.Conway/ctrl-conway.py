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
