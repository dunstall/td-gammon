# Copyright 2021 Andrew Dunstall

from game.board import Board


class Backgammon:
    def __init__(self, player1, player2):
        # TODO(AD) Rotate randomly
        self._player1 = player1
        self._player2 = player2

        self._board = Board()

    async def play(self):
        while True:
            await self._player1.turn(self._board)
            # TODO(AD) Rename white/black player1/player1
            if self._board.white_won():
                self._player1.won()
                self._player2.lost()
                return

            await self._player2.turn(self._board)
            if self._board.black_won():
                self._player1.lost()
                self._player2.won()
                return
