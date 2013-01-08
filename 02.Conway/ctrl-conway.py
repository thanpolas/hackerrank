import conway
from time import time

game = conway.GolRules()

def run():
    for i in xrange(40):
        start_time = time()
        player_one = conway.Player('w', game.get_board())
        w_play = player_one.get_next_move()
        game.put_cell(w_play, 'w')
        w_time = time() - start_time
        b_time = time()
        player_two = conway.Player('b', game.get_board())
        b_play = player_two.get_next_move()
        game.put_cell(b_play, 'b')
        print 'Round: %d Player A:%s (%f) -- B:%s (%f) :: Total Time: %f' %(i, w_play, w_time, b_play, time() - b_time, time() - start_time)


    print game.get_board_str()

mock = []

# 1,4 was next move
mock.append('--bbbb-----------------------')
mock.append('---w-w-w---------------------')
mock.append('-ww---w---------------------w')
mock.append('---bbbbbbb-------------------')
mock.append('--wbwwwwwbww-----------------')
mock.append('w-bbwbbbbb-------------------')
mock.append('bbbwbb-b--w------------------')
mock.append('wbwbb---w--------------------')
mock.append('bwbwbw-w-www-----------------')
mock.append('bbbbw--w---------------------')
mock.append('-w---------------------------')
mock.append('--w--------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('----------------------w------')
mock.append('--------------------wb-------')
mock.append('---------------------bww-----')
mock.append('---------------------ww------')
mock.append('----------------------w------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')
mock.append('-----------------------------')

mock_ryandy = [] #2,7
mock_ryandy.append('wwbwwbwbbbb------------------')
mock_ryandy.append('bbbbbb-bwwbb-w---------------')
mock_ryandy.append('---wwwb-bbww-----------------')
mock_ryandy.append('-----w-wwb-bw----------------')
mock_ryandy.append('----b-bwwb-------------------')
mock_ryandy.append('--wwwbbbwb-------------------')
mock_ryandy.append('----b--bbwb------------------')
mock_ryandy.append('---bwb-w-bbw-----------------')
mock_ryandy.append('--bbw-www--------------------')
mock_ryandy.append('----wb--w-w------------------')
mock_ryandy.append('---------w-------------------')
mock_ryandy.append('---w------w------------------')
mock_ryandy.append('-----------------------------')
mock_ryandy.append('-----------------------------')
mock_ryandy.append('-----------------------------')
mock_ryandy.append('-----------------------------')
mock_ryandy.append('-----------------------------')
mock_ryandy.append('-----------------------------')
mock_ryandy.append('-----------------------------')
mock_ryandy.append('-----------------------------')
mock_ryandy.append('-----------------------------')
mock_ryandy.append('-----------------------------')
mock_ryandy.append('-----------------------------')
mock_ryandy.append('-----------------------------')
mock_ryandy.append('-----------------------------')
mock_ryandy.append('-----------------------------')
mock_ryandy.append('---------------------------b-')
mock_ryandy.append('----------------------------w')
mock_ryandy.append('---------------------------ww')

def scenario(mock_scenario):
    start_time = time()
    i = 40
    game = conway.GolRules(mock_scenario)
    player_one = conway.Player('b', game.get_board())
    # 1,4
    w_play = player_one.get_next_move()
    game.put_cell(w_play, 'b')
    b_play = (16,14)
    # game.put_cell(b_play, 'b')
    print 'Round: %d Player A:%s -- B:%s time: %f' %(i, w_play, b_play, time() - start_time)
    print game.get_board_str()

    run_scenario(game)

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
#scenario(mock_ryandy)

