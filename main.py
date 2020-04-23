from easyAI import TwoPlayersGame
from copy import deepcopy, copy
import random

# Convert D7 to (3,6) and back...
to_string = lambda move: " ".join(["ABCDEFGHIJ"[move[i][0]] + str(move[i][1] + 1)
                                   for i in (0, 1)])
to_tuple = lambda s: ("ABCDEFGHIJ".index(s[0]), int(s[1:]) - 1)

class Hexapawn(TwoPlayersGame):
    """
    A nice game whose rules are explained here:
    http://fr.wikipedia.org/wiki/Hexapawn
    """

    def __init__(self, players, size=(4, 4)):
        self.size = M, N = size
        p = [[(i, j) for j in range(N)] for i in [0, M - 1]]

        for i, d, goal, pawns in [(0, 1, M - 1, p[0]), (1, -1, 0, p[1])]:
            players[i].direction = d
            players[i].goal_line = goal
            players[i].pawns = pawns
            players[i].starting_spaws = copy(pawns)
            players[i].respawn_places = []

        self.players = players #Define the players
        self.nplayer = 1 #player 1 starts



    def possible_moves(self):
        moves = []
        opponent_pawns = self.opponent.pawns
        d = self.player.direction
        for i, j in self.player.pawns:
            if (i + d, j) not in opponent_pawns:
                moves.append(((i, j), (i + d, j)))
            if (i + d, j + 1) in opponent_pawns:
                moves.append(((i, j), (i + d, j + 1)))
            if (i + d, j - 1) in opponent_pawns:
                moves.append(((i, j), (i + d, j - 1)))

        return list(map(to_string, [(i, j) for i, j in moves]))


    def make_move(self, move):
        move = list(map(to_tuple, move.split(' ')))
        ind = self.player.pawns.index(move[0])
        self.player.pawns[ind] = move[1]

        if move[1] in self.opponent.pawns:
            self.opponent.respawn_places.append(self.opponent.starting_spaws[self.opponent.pawns.index(move[1])])
            del self.opponent.starting_spaws[self.opponent.pawns.index(move[1])]
            self.opponent.pawns.remove(move[1])

        if random.randrange(10) == 0 and len(self.player.respawn_places) > 0:
            idx = random.randrange(len(self.player.respawn_places))
            self.player.pawns.append(self.player.respawn_places[idx])
            self.player.starting_spaws.append(copy(self.player.respawn_places[idx]))
            del self.player.respawn_places[idx]


    def lose(self):
        return (any([i == self.opponent.goal_line
                     for i, j in self.opponent.pawns])
                or (self.possible_moves() == []))

    def is_over(self):
        return self.lose()

    def show(self):
        f = lambda x: '1' if x in self.players[0].pawns else (
            '2' if x in self.players[1].pawns else '.')
        print("\n".join([" ".join([f((i, j))
                                   for j in range(self.size[1])])
                         for i in range(self.size[0])]))

if __name__ == "__main__":
    from easyAI import AI_Player, Human_Player, Negamax

    countingwin = [];
    times = [];

    for i in range(random.randint(1,10)):
            print("############### NEW TURN ############### %d" % (i + 1))
            scoring = lambda game: -100 if game.lose() else 0
            ai = Negamax(10, scoring)
            game = Hexapawn([AI_Player(ai), AI_Player(ai)])
            game.play()
            print("player %d wins after %d turns " % (game.nopponent, game.nmove))
            if i % 2 == 0:
                game.nplayer = 1
            else:
                game.nplayer = 2

            if game.nopponent == 1:
                countingwin.append(1)
            else:
                countingwin.append(2)

    #print("Wins table: ", countingwin)

    print("Player 1 won %d games." % countingwin.count(1))
    print("Player 2 won %d games." % countingwin.count(2))