# Copyright 2021 Andrew Dunstall


import numpy as np

class Board:
    _NUM_POINTS = 24
    _STATE_SIZE = 198

    def __init__(self):
        self._whites = np.array([
            0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0,
            5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2
        ])
        self._blacks = np.array([
            0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0,
            5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2
        ])
        self._white_bar = 0
        self._black_bar = 0
        self._white_removed = 0
        self._black_removed = 0

    def state(self):
        return {
            "white_bar": self._white_bar,
            "black_bar": self._black_bar,
            "white_removed": self._white_removed,
            "black_removed": self._black_removed,
            "white": self._whites,
            "black": self._blacks
        }

    def encode_state(self, turn):
        state = np.zeros(self._STATE_SIZE)

        for point in range(self._NUM_POINTS):
            index = point * 4
            state[index:index+4] = encode_point(self._whites[point])

        for point in range(self._NUM_POINTS):
            index = (point + 24) * 4
            state[index:index+4] = encode_point(self._blacks[point])

        state[192] = self._white_bar / 2
        state[193] = self._black_bar / 2
        state[194] = self._white_removed / 15
        state[195] = self._black_removed / 15
        state[196] = 1 - turn
        state[197] = turn

        return state

    def json_encode(self):
        return """
        {
            "type": "eventMatchStart",
            "match": {
                "currentGame": {
                    "id": 15850181,
                    "isOver": false,
                    "moveSequence": 0,
                    "previousTurnDice": null,
                    "state": {
                        "bar": [
                            [],
                            []
                        ],
                        "blackBar": [],
                        "blackOutside": [],
                        "nextPieceID": 31,
                        "outside": [
                            [],
                            []
                        ],
                        "points": [
                            [
                                {
                                    "type": 1
                                },
                                {
                                    "type": 1
                                }
                            ],
                            [],
                            [],
                            [],
                            [],
                            [
                                {
                                    "type": 0
                                },
                                {
                                    "type": 0
                                },
                                {
                                    "type": 0
                                },
                                {
                                    "type": 0
                                },
                                {
                                    "type": 0
                                }
                            ],
                            [],
                            [
                                {
                                    "type": 0
                                },
                                {
                                    "type": 0
                                },
                                {
                                    "type": 0
                                }
                            ],
                            [],
                            [],
                            [],
                            [
                                {
                                    "type": 1
                                },
                                {
                                    "type": 1
                                },
                                {
                                    "type": 1
                                },
                                {
                                    "type": 1
                                },
                                {
                                    "type": 1
                                }
                            ],
                            [
                                {
                                    "type": 0
                                },
                                {
                                    "type": 0
                                },
                                {
                                    "type": 0
                                },
                                {
                                    "type": 0
                                },
                                {
                                    "type": 0
                                }
                            ],
                            [],
                            [],
                            [],
                            [
                                {
                                    "type": 1
                                },
                                {
                                    "type": 1
                                },
                                {
                                    "type": 1
                                }
                            ],
                            [],
                            [
                                {
                                    "type": 1
                                },
                                {
                                    "type": 1
                                },
                                {
                                    "type": 1
                                },
                                {
                                    "type": 1
                                },
                                {
                                    "type": 1
                                }
                            ],
                            [],
                            [],
                            [],
                            [],
                            [
                                {
                                    "type": 0
                                },
                                {
                                    "type": 0
                                }
                            ]
                        ],
                        "whiteBar": [],
                        "whiteOutside": []
                    },
                    "turnConfirmed": false,
                    "turnDice": null,
                    "turnNumber": 1,
                    "turnPlayer": "human"
                },
                "guest": {
                    "currentMatch": 95796029,
                    "currentPieceType": 1,
                    "currentRule": null,
                    "id": 39443361,
                    "name": "Player 39443361",
                    "socketID": "4qcFSHWyx4ovxE-yAAAD",
                    "stats": {
                        "doubles": 0,
                        "loses": 0,
                        "wins": 0
                    }
                },
                "host": {
                    "currentMatch": 95796029,
                    "currentPieceType": 0,
                    "currentRule": null,
                    "id": 95794238,
                    "name": "Player 95794238",
                    "socketID": "ime5vIJ-yuNRmfP3AAAC",
                    "stats": {
                        "doubles": 0,
                        "loses": 0,
                        "wins": 0
                    }
                },
                "id": 95796029,
                "isOver": false,
                "length": 5,
                "players": [
                    95794238,
                    39443361
                ],
                "ruleName": "RuleBgCasual",
                "score": [
                    0,
                    0
                ]
            }
        }
        """

    def json_encode_roll(self):
        return """
{
    "type": "rollDice",
    "clientMsgSeq": 4,
    "dice": {
        "moves": [
            5,
            1
        ],
        "movesLeft": [
            5,
            1
        ],
        "movesPlayed": [],
        "values": [
            5,
            1
        ]
    },
    "match": {
        "currentGame": {
            "id": 52725543,
            "isOver": false,
            "moveSequence": 0,
            "previousTurnDice": {
                "moves": [
                    5,
                    1
                ],
                "movesLeft": [
                    5,
                    1
                ],
                "movesPlayed": [],
                "values": [
                    5,
                    1
                ]
            },
            "state": {
                "bar": [
                    [],
                    []
                ],
                "blackBar": [],
                "blackOutside": [],
                "nextPieceID": 31,
                "outside": [
                    [],
                    []
                ],
                "points": [
                    [
                        {
                            "type": 1
                        },
                        {
                            "type": 1
                        }
                    ],
                    [],
                    [],
                    [],
                    [],
                    [
                        {
                            "type": 0
                        },
                        {
                            "type": 0
                        },
                        {
                            "type": 0
                        },
                        {
                            "type": 0
                        },
                        {
                            "type": 0
                        }
                    ],
                    [],
                    [
                        {
                            "type": 0
                        },
                        {
                            "type": 0
                        },
                        {
                            "type": 0
                        }
                    ],
                    [],
                    [],
                    [],
                    [
                        {
                            "type": 1
                        },
                        {
                            "type": 1
                        },
                        {
                            "type": 1
                        },
                        {
                            "type": 1
                        },
                        {
                            "type": 1
                        }
                    ],
                    [
                        {
                            "type": 0
                        },
                        {
                            "type": 0
                        },
                        {
                            "type": 0
                        },
                        {
                            "type": 0
                        },
                        {
                            "type": 0
                        }
                    ],
                    [],
                    [],
                    [],
                    [
                        {
                            "type": 1
                        },
                        {
                            "type": 1
                        },
                        {
                            "type": 1
                        }
                    ],
                    [],
                    [
                        {
                            "type": 1
                        },
                        {
                            "type": 1
                        },
                        {
                            "type": 1
                        },
                        {
                            "type": 1
                        },
                        {
                            "type": 1
                        }
                    ],
                    [],
                    [],
                    [],
                    [],
                    [
                        {
                            "type": 0
                        },
                        {
                            "type": 0
                        }
                    ]
                ],
                "whiteBar": [],
                "whiteOutside": []
            },
            "turnConfirmed": false,
            "turnDice": {
                "moves": [
                    5,
                    1
                ],
                "movesLeft": [
                    5,
                    1
                ],
                "movesPlayed": [],
                "values": [
                    5,
                    1
                ]
            },
            "turnNumber": 1,
            "turnPlayer": {
                "currentMatch": 30194974,
                "currentPieceType": 0,
                "currentRule": null,
                "id": 45491459,
                "name": "Player 45491459",
                "socketID": "rQ8nL84sbLa5J-slAAAB",
                "stats": {
                    "doubles": 0,
                    "loses": 0,
                    "wins": 0
                }
            }
        },
        "guest": {
            "currentMatch": 30194974,
            "currentPieceType": 1,
            "currentRule": null,
            "id": 93442854,
            "name": "Player 93442854",
            "socketID": "DVgk1MfgUmcCWWRfAAAC",
            "stats": {
                "doubles": 0,
                "loses": 0,
                "wins": 0
            }
        },
        "host": {
            "currentMatch": 30194974,
            "currentPieceType": 0,
            "currentRule": null,
            "id": 45491459,
            "name": "Player 45491459",
            "socketID": "rQ8nL84sbLa5J-slAAAB",
            "stats": {
                "doubles": 0,
                "loses": 0,
                "wins": 0
            }
        },
        "id": 30194974,
        "isOver": false,
        "length": 5,
        "players": [
            45491459,
            93442854
        ],
        "ruleName": "RuleBgCasual",
        "score": [
            0,
            0
        ]
    },
    "player": {
        "currentMatch": 30194974,
        "currentPieceType": 0,
        "currentRule": null,
        "id": 45491459,
        "name": "Player 45491459",
        "socketID": "rQ8nL84sbLa5J-slAAAB",
        "stats": {
            "doubles": 0,
            "loses": 0,
            "wins": 0
        }
    },
    "result": true
}
"""

    def json_encode2(self):
        return """
{

    "type": "eventPieceMove",
    "clientMsgSeq": 5,
    "match": {
        "currentGame": {
            "id": 81566064,
            "isOver": false,
            "moveSequence": 1,
            "previousTurnDice": {
                "moves": [
                    5,
                    1
                ],
                "movesLeft": [
                    5,
                    1
                ],
                "movesPlayed": [],
                "values": [
                    5,
                    1
                ]
            },
            "state": {
                "bar": [
                    [],
                    []
                ],
                "blackBar": [],
                "blackOutside": [],
                "nextPieceID": 31,
                "outside": [
                    [],
                    []
                ],
                "points": [
                    [
                        {
                            "type": 1
                        },
                        {
                            "type": 1
                        }
                    ],
                    [],
                    [],
                    [],
                    [],
                    [
                        {
                            "type": 0
                        },
                        {
                            "type": 0
                        },
                        {
                            "type": 0
                        },
                        {
                            "type": 0
                        },
                        {
                            "type": 0
                        }
                    ],
                    [],
                    [
                        {
                            "type": 0
                        },
                        {
                            "type": 0
                        },
                        {
                            "type": 0
                        },
                        {
                            "type": 0
                        }
                    ],
                    [],
                    [],
                    [],
                    [
                        {
                            "type": 1
                        },
                        {
                            "type": 1
                        },
                        {
                            "type": 1
                        },
                        {
                            "type": 1
                        },
                        {
                            "type": 1
                        }
                    ],
                    [
                        {
                            "type": 0
                        },
                        {
                            "type": 0
                        },
                        {
                            "type": 0
                        },
                        {
                            "type": 0
                        }
                    ],
                    [],
                    [],
                    [],
                    [
                        {
                            "type": 1
                        },
                        {
                            "type": 1
                        },
                        {
                            "id": 23,
                            "type": 1
                        }
                    ],
                    [],
                    [
                        {
                            "id": 16,
                            "type": 1
                        },
                        {
                            "id": 17,
                            "type": 1
                        },
                        {
                            "id": 18,
                            "type": 1
                        },
                        {
                            "id": 19,
                            "type": 1
                        },
                        {
                            "id": 20,
                            "type": 1
                        }
                    ],
                    [],
                    [],
                    [],
                    [],
                    [
                        {
                            "id": 14,
                            "type": 0
                        },
                        {
                            "id": 15,
                            "type": 0
                        }
                    ]
                ],
                "whiteBar": [],
                "whiteOutside": []
            },
            "turnConfirmed": false,
            "turnDice": {
                "moves": [
                    5,
                    1
                ],
                "movesLeft": [
                    1
                ],
                "movesPlayed": [
                    5
                ],
                "values": [
                    5,
                    1
                ]
            },
            "turnNumber": 1,
            "turnPlayer": {
                "currentMatch": 29469679,
                "currentPieceType": 0,
                "currentRule": null,
                "id": 56905594,
                "name": "Player 56905594",
                "socketID": "gzC-RlKxQqVQndTxAAAB",
                "stats": {
                    "doubles": 0,
                    "loses": 0,
                    "wins": 0
                }
            }
        },
        "guest": {
            "currentMatch": 29469679,
            "currentPieceType": 1,
            "currentRule": null,
            "id": 91282624,
            "name": "Player 91282624",
            "socketID": "XJpCTgXM8strSgNzAAAC",
            "stats": {
                "doubles": 0,
                "loses": 0,
                "wins": 0
            }
        },
        "host": {
            "currentMatch": 29469679,
            "currentPieceType": 0,
            "currentRule": null,
            "id": 56905594,
            "name": "Player 56905594",
            "socketID": "gzC-RlKxQqVQndTxAAAB",
            "stats": {
                "doubles": 0,
                "loses": 0,
                "wins": 0
            }
        },
        "id": 29469679,
        "isOver": false,
        "length": 5,
        "players": [
            56905594,
            91282624
        ],
        "ruleName": "RuleBgCasual",
        "score": [
            0,
            0
        ]
    },
    "moveActionList": [
        {
            "from": 12,
            "piece": {
                "id": 13,
                "type": 0
            },
            "position": 12,
            "to": 7,
            "type": "move"
        }
    ],
    "piece": {
        "id": 13,
        "type": 0
    },
    "result": true,
    "steps": 5
}
    """

    def json_encode_new(self):
        return """
        {
            "type": "eventMatchStart",
            "state": {
                "white_bar": 0,
                "black_bar": 0,
                "white_removed": 0,
                "black_removed": 0,
                "white": [0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                "black": [0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]
            }
        }
        """


def encode_point(n_checkers):
    arr = np.zeros(4)
    if n_checkers == 1:  # Blot
        arr[0] = 1
    if n_checkers >= 2:  # Made point
        arr[1] = 1
    if n_checkers == 3:
        arr[2] = 1
    if n_checkers > 3:
        arr[3] = (n_checkers - 3) / 2
    return arr
