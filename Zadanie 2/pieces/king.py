from typing import List, NoReturn

from pieces.field import Field
from color import Color
from pieces.pawn import Pawn
from pieces.piece import Piece


class King(Piece):
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
        self.attacked_fields = []

    def find_possible_moves(self, chessboard, enemy_pieces: List[Piece]):
        # Punkt 1
        self.possible_moves = []
        locations = []
        for move in self.moves:
            location = move()
            if 0 <= location[0] <= 7 \
                    and 0 <= location[1] <= 7:
                field = chessboard.chessboard[location[0]][location[1]]
                if not isinstance(field, Piece):
                    locations.append(location)

        for location in locations:
            is_attacked = False
            field = chessboard.chessboard[location[0]][location[1]]
            for piece in enemy_pieces:
                # TODO: wymyślić lepszy sposób (zoptymalizować użycia find_possible_moves?)
                # Nie optymalne rozwiązanie
                if isinstance(piece, Pawn):
                    if piece.attacks_king_field(field, chessboard):
                        is_attacked = True
                        break
                elif piece.attacks(field, chessboard):
                    is_attacked = True
                    break
            if not is_attacked:
                self.possible_moves.append(field)

    def attacks(self, attacked: Field, chessboard) -> bool:
        for move in self.moves:
            location = move()
            if location[0] >= 0 or location[0] <= 7 \
                    or location[1] >= 0 or location[1] <= 7:
                if location == attacked.location:
                    return True

        return False

    def find_attacked_fields(self, chessboard) -> NoReturn:
        attacked_fields = []
        for move in self.moves:
            location = move()
            if location[0] >= 0 or location[0] <= 7 \
                    or location[1] >= 0 or location[1] <= 7:
                field = chessboard.chessboard[location[0]][location[1]]
                if not isinstance(field, Piece):
                    attacked_fields.append(field)
        self.attacked_fields = attacked_fields

    def to_string(self):
        return "King " + {
            0: 'a',
            1: 'b',
            2: 'c',
            3: 'd',
            4: 'e',
            5: 'f',
            6: 'g',
            7: 'h',
        }[self.location[1]] + str(8 - self.location[0])
