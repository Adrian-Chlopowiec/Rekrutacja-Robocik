from color import Color
from pieces.linearpiece import LinearPiece


class Bishop(LinearPiece):
    def __init__(self, x: int, y: int, color: Color):
        super().__init__(x, y, color)
        self.moves = [lambda: (self.location[0] - 1, self.location[1] - 1),
                      lambda: (self.location[0] - 1, self.location[1] + 1),
                      lambda: (self.location[0] + 1, self.location[1] + 1),
                      lambda: (self.location[0] + 1, self.location[1] - 1)
                      ]

    def to_string(self):
        return "Bishop " + {
            0: 'a',
            1: 'b',
            2: 'c',
            3: 'd',
            4: 'e',
            5: 'f',
            6: 'g',
            7: 'h',
        }[self.location[1]] + str(8 - self.location[0])
