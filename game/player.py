# Copyright 2021 Andrew Dunstall

import abc
import random

import game.board


class Player(abc.ABC):
    @abc.abstractmethod
    def turn(self, board):
        pass


class RandomPlayer(Player):
    def turn(self, board):
        roll1 = random.randint(1, 6)
        roll2 = random.randint(1, 6)
        if roll1 == roll2:
            # Doubles.
            rolls = [roll1] * 4
        else:
            rolls = [roll1, roll2]

        print("OPPONENT ROLL", rolls)
        while len(rolls) > 0:
            permitted = board.permitted_moves(rolls, game.board.PLAYER_BLACK)
            if len(permitted) == 0:
                return

            move = random.choice(permitted)
            print("opponent move", move)

            position, steps = move

            del rolls[rolls.index(steps)]

            board.move(position, steps, game.board.PLAYER_BLACK)
