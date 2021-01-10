# Copyright 2021 Andrew Dunstall

from game.board import Board


class Backgammon:
    def __init__(self):
        self._board = Board()

    def board(self):
        return self._board

    def move(self):
        pass
