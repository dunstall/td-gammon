# Copyright 2021 Andrew Dunstall

import random

from game.board import Board


class Backgammon:
    def __init__(self):
        self._board = Board()

    def board(self):
        return self._board

    def move(self, position, steps) -> bool:
        return self._board.move(position, steps)

    def roll(self):
        roll1 = random.randint(1, 6)
        roll2 = random.randint(1, 6)
        if roll1 == roll2:
            return [roll1] * 4
        return [roll1, roll2]
