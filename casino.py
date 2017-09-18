from game import Game
from player import Player
from randomplayer import RandomPlayer
from student import StudentPlayer


if __name__ == '__main__':

    players = [StudentPlayer("Fabio",100)]

    for i in range(10):
        print(players)
        g = Game(players, min_bet=1, max_bet=5, verbose=True, debug=True)
        g.run()

    print("OVERALL: ", players)
    print('Win rate', (players[0].wins/players[0].ngames)*100)
    print('win profit', players[0].win_profit)
    print('lose', players[0].lose_jf)
    print('win overall', players[0].pocket - players[0].initmoney)
    print(players[0].wins)
