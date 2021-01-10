# Copyright 2021 Andrew Dunstall

import random

from game.board import Board


# TODO(AD) State machine?
class Backgammon:
    def __init__(self):
        self._board = Board()
        self._rolls = []

    def board(self):
        return self._board

    def move(self, position, steps) -> bool:
        if steps not in self._rolls:
            return False

        if not self._board.move(position, steps):
            return False

        del self._rolls[self._rolls.index(steps)]
        return True

    def roll(self):
        roll1 = random.randint(1, 6)
        roll2 = random.randint(1, 6)
        if roll1 == roll2:
            # Doubles.
            self._rolls = [roll1] * 4
        else:
            self._rolls = [roll1, roll2]

    def state(self):
        return {
            "board": self._board.state(),
            "rolls": self._rolls
        }
