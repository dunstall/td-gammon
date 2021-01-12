# Copyright 2021 Andrew Dunstall

import game.player


class TDGammonPlayer(game.player.Player):
    def __init__(self, model):
        self._model = model

    async def turn(self, board):
        print("TURN")
        roll = [1, 2]

        while True:  # rolls remaining
            move = self._model.action(board, roll)
            if move is None:
                return

            board.move(*move)
                
            # remove roll used
