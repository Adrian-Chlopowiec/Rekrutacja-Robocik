from color import Color
from pieces.linearpiece import LinearPiece


class Queen(LinearPiece):
    """
    Class representing Queen.\n
    :param x: Location of piece on vertical axis
    :param y: Location of piece on horizontal axis
    :param color: Color of this piece
    :param possible_moves: List of possible moves
    :param moves: List of anonymous functions changing one location into another representing types of moves of piece.
    :param king_attack_line: List of Fields on line between this Piece and King.
    """
    def __init__(self, x: int, y: int, color: Color):
        super().__init__(x, y, color)
        self.moves = [lambda: (self.location[0] - 1, self.location[1]),
                      lambda: (self.location[0], self.location[1] + 1),
                      lambda: (self.location[0] + 1, self.location[1]),
                      lambda: (self.location[0], self.location[1] - 1),
                      lambda: (self.location[0] - 1, self.location[1] - 1),
                      lambda: (self.location[0] - 1, self.location[1] + 1),
                      lambda: (self.location[0] + 1, self.location[1] + 1),
                      lambda: (self.location[0] + 1, self.location[1] - 1)
                      ]

    def to_string(self):
        return "Queen " + {
            0: 'a',
            1: 'b',
            2: 'c',
            3: 'd',
            4: 'e',
            5: 'f',
            6: 'g',
            7: 'h',
        }[self.location[1]] + str(8 - self.location[0])
