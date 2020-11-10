from copy import copy
from typing import NoReturn, List, Optional, Tuple

from pieces.field import Field
from color import Color
from pieces.piece import Piece


class Knight(Piece):
    """
    Class representing Knight.\n
    :param x: Location of piece on vertical axis
    :param y: Location of piece on horizontal axis
    :param color: Color of this piece
    :param possible_moves: List of possible moves
    :param moves: List of anonymous functions changing one location into another representing types of moves of piece.
    """
    def __init__(self, x: int, y: int, color: Color):
        super().__init__(x, y, color)
        self.moves = [lambda: (self.location[0] - 2, self.location[1] - 1),
                      lambda: (self.location[0] - 2, self.location[1] + 1),
                      lambda: (self.location[0] - 1, self.location[1] + 2),
                      lambda: (self.location[0] + 1, self.location[1] + 2),
                      lambda: (self.location[0] + 2, self.location[1] + 1),
                      lambda: (self.location[0] + 2, self.location[1] - 1),
                      lambda: (self.location[0] + 1, self.location[1] - 2),
                      lambda: (self.location[0] - 1, self.location[1] - 2)
                      ]

    def find_possible_moves(self, chessboard) -> NoReturn:
        self.possible_moves = []
        moves = [self.moves[0](), self.moves[1](), self.moves[2](), self.moves[3](), self.moves[4](), self.moves[5](),
                 self.moves[6](), self.moves[7]()]

        for location in moves:
            if not (location[0] < 0 or location[0] > 7 or location[1] < 0 or location[1] > 7):
                field = chessboard.chessboard[location[0]][location[1]]
                if not (isinstance(field, Piece) and field.color == self.color):
                    self.possible_moves.append(field)

    def find_mate(self, active_pieces: List[Piece], chessboard) -> List[Tuple[Piece, Field]]:
        possible_mates: List[Tuple[Piece, Field]] = []
        original_location = copy(self.location)
        enemy_king = chessboard.get_king(self.enemy_color)
        enemy_pieces = chessboard.get_all_pieces(self.enemy_color)
        enemy_pieces.remove(enemy_king)

        for field in self.possible_moves:
            imaginary_board, deleted_piece = chessboard.create_imaginary_board(self, field)
            if deleted_piece is not None:
                enemy_pieces.remove(deleted_piece)
            active_pieces_copy = copy(active_pieces)
            enemy_king.find_possible_moves(imaginary_board, active_pieces_copy)
            active_pieces_copy.remove(self)

            field_is_mating = True
            if len(enemy_king.possible_moves) == 0:
                if self.attacks(enemy_king, imaginary_board):
                    if imaginary_board.is_attacked(self, enemy_pieces) is None:
                        field_is_mating = True
                    else:
                        field_is_mating = False
                else:
                    field_is_mating = False

                if field_is_mating:
                    tmp = copy(self.location)
                    self.location = copy(original_location)
                    field.location = tmp
                    possible_mates.append((self, field))
            else:
                field_is_mating = False
            if not field_is_mating:
                field.location = copy(self.location)
                self.location = copy(original_location)
            if deleted_piece is not None:
                enemy_pieces.append(deleted_piece)
        return possible_mates

    def attacks(self, attacked: Field, chessboard) -> bool:
        """
        Checks if this piece attacks given field on given chessboard.\n
        :param attacked: Field to check if it is attacked
        :param chessboard: Chessboard on which the Piece and Field are.
        :return: True if piece attacks field, False otherwise.
        """
        moves = [self.moves[0](), self.moves[1](), self.moves[2](), self.moves[3](), self.moves[4](), self.moves[5](),
                 self.moves[6](), self.moves[7]()]

        for location in moves:
            if not (location[0] < 0 or location[0] > 7 or location[1] < 0 or location[1] > 7):
                if location == attacked.location:
                    return True

        return False

    def to_string(self):
        return "Knight " + {
            0: 'a',
            1: 'b',
            2: 'c',
            3: 'd',
            4: 'e',
            5: 'f',
            6: 'g',
            7: 'h',
        }[self.location[1]] + str(8 - self.location[0])
