# Copyright 2021 Andrew Dunstall

import random

from game.board import Board
from game.player import Player


class Backgammon:
    def __init__(self, player1, player2):
        self._player1 = player1
        self._player2 = player2

        self._board = Board()

    async def play(self):
        while True:
            await self._player1.turn(self._board)
            await self._player2.turn(self._board)


class BackgammonOld:
    def __init__(self, opponent):
        self._opponent = opponent

        self._board = Board()
        # TODO maintain both players rolls and send to client
        self._rolls = []

    def board(self):
        return self._board

    def move(self, position, steps) -> bool:
        print("player move", position, steps)
        if steps not in self._rolls:
            return False

        if not self._board.move(position, steps):
            return False

        del self._rolls[self._rolls.index(steps)]

        # If player is out of rolls play the opponents turn.
        if len(self._rolls) == 0:

            if self._board.white_won():
                print("WHITE WON")
                raise ValueError("WHITE WON")
            if self._board.black_won():
                print("BLACK WON")
                raise ValueError("BLACK WON")


            self._opponent.turn(self._board)

            #  self._wait_for_roll = True



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

    def permitted_moves(self):
        return self._board.permitted_moves(self._rolls)

    def skip(self):
        print("SKIP")
        self._rolls = []
        # TODO(AD)
        #  self._opponent.turn(self._board)
