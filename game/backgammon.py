# Copyright 2021 Andrew Dunstall

from game.board import Board


class Backgammon:
    def __init__(self, player1, player2):
        self._player1 = player1
        self._player2 = player2

        self._board = Board()

    async def play(self):
        while True:
            await self._player1.turn(self._board)
            await self._player2.turn(self._board)
