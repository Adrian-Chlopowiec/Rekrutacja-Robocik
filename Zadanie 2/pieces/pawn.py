from copy import copy
from typing import List, NoReturn, Tuple

from color import Color
from pieces.field import Field
from pieces.piece import Piece


class Pawn(Piece):
    """
    Class representing Pawn.\n
    :param x: Location of piece on vertical axis
    :param y: Location of piece on horizontal axis
    :param color: Color of this piece
    :param possible_moves: List of possible moves
    :param moves: List of anonymous functions changing one location into another representing types of moves of piece.
    :param possible_attacks: List of fields Pawn attacks
    """
    def __init__(self, x: int, y: int, color: Color):
        super().__init__(x, y, color)
        self.possible_attacks = []
        if color == Color.WHITE:
            if self.location[0] == 6:
                self.moves = [lambda: (self.location[0] - 1, self.location[1]),
                              lambda: (self.location[0] - 1, self.location[1] - 1),
                              lambda: (self.location[0] - 1, self.location[1] + 1),
                              lambda: (self.location[0] - 2, self.location[1])]
            else:
                self.moves = [lambda: (self.location[0] - 1, self.location[1]),
                              lambda: (self.location[0] - 1, self.location[1] - 1),
                              lambda: (self.location[0] - 1, self.location[1] + 1)]
        else:
            if self.location[0] == 1:
                self.moves = [lambda: (self.location[0] + 1, self.location[1]),
                              lambda: (self.location[0] + 1, self.location[1] - 1),
                              lambda: (self.location[0] + 1, self.location[1] + 1),
                              lambda: (self.location[0] + 2, self.location[1])]
            else:
                self.moves = [lambda: (self.location[0] + 1, self.location[1]),
                              lambda: (self.location[0] + 1, self.location[1] - 1),
                              lambda: (self.location[0] + 1, self.location[1] + 1)]

    def find_possible_attacks(self) -> NoReturn:
        """
        Checks which fields does this Pawn attack.
        :return: None
        """
        if self.location[0] == 0:
            self.possible_attacks = []
        elif self.location[1] == 0:
            self.possible_attacks = [self.moves[2]()]
        elif self.location[1] == 7:
            self.possible_attacks = [self.moves[1]()]
        else:
            self.possible_attacks = [self.moves[1](), self.moves[2]()]

    def find_possible_moves(self, chessboard) -> NoReturn:
        self.possible_moves = []
        locations = []
        is_square_infront_empty = False
        for move in self.moves:
            locations.append(move())

        if self.color == Color.WHITE and self.location[0] == 0:
            return
        elif self.color == Color.BLACK and self.location[0] == 7:
            return

        if 0 <= locations[0][0] <= 7 and 0 <= locations[0][1] <= 7:
            field = chessboard.chessboard[locations[0][0]][locations[0][1]]
            if not isinstance(field, Piece):
                is_square_infront_empty = True
                self.possible_moves.append(field)

        if 0 <= locations[1][0] <= 7 and 0 <= locations[1][1] <= 7:
            field = chessboard.chessboard[locations[1][0]][locations[1][1]]
            if isinstance(field, Piece) and field.color == self.enemy_color:
                self.possible_moves.append(field)

        if 0 <= locations[2][0] <= 7 and 0 <= locations[2][1] <= 7:
            field = chessboard.chessboard[locations[2][0]][locations[2][1]]
            if isinstance(field, Piece) and field.color == self.enemy_color:
                self.possible_moves.append(field)

        if len(locations) == 4 and is_square_infront_empty:
            if 0 <= locations[3][0] <= 7 and 0 <= locations[3][1] <= 7:
                field = chessboard.chessboard[locations[3][0]][locations[3][1]]
                if not isinstance(field, Piece):
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
                    if enemy_king.attacks(field, imaginary_board):
                        if imaginary_board.is_defended(self, active_pieces_copy):
                            if imaginary_board.is_attacked(self, enemy_pieces) is not None:
                                field_is_mating = False
                            else:
                                field_is_mating = True
                        else:
                            field_is_mating = False
                    else:
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

    def attacks(self, attacked: Field, chessboard):
        if attacked is self:
            return False
        self.find_possible_attacks()
        for square in self.possible_attacks:
            field = chessboard.chessboard[square[0]][square[1]]
            if isinstance(field, Piece):
                if field.location == attacked.location:
                    return True

        return False

    def attacks_king_field(self, attacked: Field, chessboard) -> bool:
        """
        Checks if this Pawn attacks fields onto which King can move.
        :param attacked: field to check if it is attacked
        :param chessboard: Chessboard on which Pawn and Field are.
        :return: True if pawn attacks field, False otherwise.
        """
        if attacked is self:
            return False
        self.find_possible_attacks()
        for square in self.possible_attacks:
            field = chessboard.chessboard[square[0]][square[1]]
            if field.location == attacked.location:
                return True

        return False

    def to_string(self):
        return "Pawn " + {
            0: 'a',
            1: 'b',
            2: 'c',
            3: 'd',
            4: 'e',
            5: 'f',
            6: 'g',
            7: 'h',
        }[self.location[1]] + str(8 - self.location[0])
