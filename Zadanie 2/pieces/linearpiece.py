from abc import ABC
from copy import copy
from typing import NoReturn, List, Optional, Tuple

from color import Color
from pieces.field import Field
from pieces.king import King
from pieces.piece import Piece


class LinearPiece(Piece, ABC):
    """
    Abstract class representing pieces which can move in linear way: Queen, Bishop and Rook.\n
    :param x: Location of piece on vertical axis
    :param y: Location of piece on horizontal axis
    :param color: Color of this piece
    :param possible_moves: List of possible moves
    :param moves: List of anonymous functions changing one location into another representing types of moves of piece.
    :param king_attack_line: List of Fields on line between this Piece and King.
    """
    def __init__(self, x: int, y: int, color: Color):
        super().__init__(x, y, color)
        self.king_attack_line: List[Field] = []

    def find_possible_moves(self, chessboard) -> NoReturn:
        self.possible_moves = []
        original_location = copy(self.location)
        for move in self.moves:
            can_move = True
            while can_move:
                self.location = move()
                if self.location[0] < 0 or self.location[0] > 7 or self.location[1] < 0 or self.location[1] > 7:
                    can_move = False
                else:
                    field = chessboard.chessboard[self.location[0]][self.location[1]]
                    if isinstance(field, Piece):
                        if field.color == self.enemy_color:
                            self.possible_moves.append(field)
                            can_move = False
                        else:
                            can_move = False
                    else:
                        self.possible_moves.append(field)

            self.location = copy(original_location)
        return

    def find_mate(self, active_pieces: List[Piece], chessboard) -> Optional[Tuple[Piece, Field]]:
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

            if len(enemy_king.possible_moves) == 0:
                field_is_mating = True
                if self.attacks_king(enemy_king, imaginary_board):
                    if enemy_king.attacks(self, imaginary_board):
                        if imaginary_board.is_defended(self, active_pieces_copy):
                            is_attacked = imaginary_board.is_attacked(self, enemy_pieces)
                            if is_attacked is not None:
                                field_is_mating = False
                            else:
                                field_is_mating = True
                        else:
                            field_is_mating = False
                    elif imaginary_board.is_attacked(self, enemy_pieces) is None:
                        for square in self.king_attack_line:
                            figure = imaginary_board.is_attacked(square, enemy_pieces)
                            if figure is not None:
                                field_is_mating = False
                                break
                    else:
                        field_is_mating = False
                else:
                    field_is_mating = False

                if field_is_mating:
                    tmp = copy(self.location)
                    self.location = copy(original_location)
                    field.location = tmp
                    return self, field
            field.location = copy(self.location)
            self.location = copy(original_location)
            if deleted_piece is not None:
                enemy_pieces.append(deleted_piece)
        return None

    def attacks(self, attacked: Field, chessboard) -> bool:
        original_location = copy(self.location)

        for move in self.moves:
            can_move = True
            while can_move:
                self.location = move()
                if self.location[0] < 0 or self.location[0] > 7 \
                        or self.location[1] < 0 or self.location[1] > 7:
                    can_move = False
                else:
                    field = chessboard.chessboard[self.location[0]][self.location[1]]
                    if attacked.location == field.location:
                        self.location = copy(original_location)
                        return True
                    elif isinstance(field, Piece):
                        if not (isinstance(field, King) and field.color == self.enemy_color):
                            can_move = False

            self.location = copy(original_location)

        return False

    def attacks_king(self, king: Piece, chessboard) -> bool:
        """
        Checks if this piece attacks enemy King.
        :param king: Enemy King
        :param chessboard: Chessboard on which Piece and King are.
        :return: True if piece attacks King, False otherwise.
        """
        original_location = copy(self.location)

        for move in self.moves:
            attack_line = []
            can_move = True

            while can_move:
                self.location = move()
                if self.location[0] < 0 or self.location[0] > 7 \
                        or self.location[1] < 0 or self.location[1] > 7:
                    can_move = False
                else:
                    field = chessboard.chessboard[self.location[0]][self.location[1]]
                    if king.location == field.location:
                        self.king_attack_line = attack_line
                        self.location = copy(original_location)
                        return True
                    else:
                        if isinstance(field, Piece):
                            can_move = False
                    attack_line.append(field)

            self.location = copy(original_location)

        return False
