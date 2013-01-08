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

mock = []

mock.append('---------w-------------------')
mock.append('-----w-----------------------')
mock.append('-----------------------------')
mock.append('---------w-------------------')
mock.append('----w------------------------')
mock.append('--w----w---------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-w---w-----------------------')
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
mock.append('-------------------bbb-------')
mock.append('------------------b--b-------')
mock.append('-----------------b-----------')
mock.append('----------------b------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')



def scenario(mock_scenario):
    start_time = time()
    i = 40
    game = conway.GolRules(mock_scenario)
    player_one = conway.Player('b', game.get_board())
    # 21, 13
    w_play = player_one.get_next_move()
    game.put_cell(w_play, 'w')
    b_play = (16,14)
    game.put_cell(b_play, 'b')
    print 'Round: %d Player A:%s -- B:%s time: %f' %(i, w_play, b_play, time() - start_time)
    print game.get_board_str()

    #run_scenario(game)

def run_scenario(game, generations=500):
    init_time = time()
    for i in xrange(generations):
        start_time = time()
        game.generate()
        if game.game_ended():
            break
        print "Gen %d W:%d B:%d :: Time:%f" % (i, game.get_count('w'), game.get_count('b'), time() - start_time)
        #print game.get_board_str()

    print "Winner:%s Gen %d W:%d B:%d :: Total Time:%f" % (game.get_winner(), i, game.get_count('w'), game.get_count('b'), time() - init_time)
    #print game.get_board_str()

run()
#scenario(mock)

