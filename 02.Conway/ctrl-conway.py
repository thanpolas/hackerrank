import conway
from time import time

game = conway.GolRules()

def run():
    for i in xrange(40):
        start_time = time()
        player_one = conway.Player('w', game.get_board())
        w_play = player_one.get_next_move()
        game.put_cell(w_play, 'w')

        player_two = conway.Player('b', game.get_board())
        b_play = player_two.get_next_move()
        game.put_cell(b_play, 'b')
        print 'Round: %d Player A:%s -- B:%s time: %f' %(i, w_play, b_play, time() - start_time)


    print game.get_board_str()

run()


mock = []

mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('----------------www----------')
mock.append('---------------w--w-b--------')
mock.append('--------------w--------------')
mock.append('-------------b---------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('----------------------------b')
mock.append('--------------------------bbb')



# game = conway.GolRules(mock)
# player_one = conway.Player('w', game.get_board())
# play = player_one.get_next_move()
# print 'Player w play:', play

