from typing import List, NoReturn

from pieces.field import Field
from color import Color
from pieces.pawn import Pawn
from pieces.piece import Piece


class King(Piece):
    """
    Class representing King.\n
    :param x: Location of piece on vertical axis
    :param y: Location of piece on horizontal axis
    :param color: Color of this piece
    :param possible_moves: List of possible moves
    :param moves: List of anonymous functions changing one location into another representing types of moves of piece.
    :param attacked_fields: List of Fields King attacks
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
        self.attacked_fields = []

    def find_possible_moves(self, chessboard, enemy_pieces: List[Piece]) -> NoReturn:
        """
        Finds empty Fields which aren't attacked by enemy_pieces around the King
        :param chessboard: Chessboard on which King and enemy pieces are.
        :param enemy_pieces: enemy pieces that are threat to the King
        :return:
        """
        self.possible_moves = []
        locations = []
        for move in self.moves:
            location = move()
            if 0 <= location[0] <= 7 \
                    and 0 <= location[1] <= 7:
                field = chessboard.chessboard[location[0]][location[1]]
                if not (isinstance(field, Piece) and field.color == self.color)\
                        and ((isinstance(field, Piece) and field.color == self.enemy_color
                              and not chessboard.is_defended(field, enemy_pieces))
                             or not isinstance(field, Piece)):
                    locations.append(location)

        for location in locations:
            is_attacked = False
            field = chessboard.chessboard[location[0]][location[1]]
            for piece in enemy_pieces:
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
        """
        Finds Empty fields that King attacks.
        :param chessboard: Chessboard on which King is.
        :return: None
        """
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
