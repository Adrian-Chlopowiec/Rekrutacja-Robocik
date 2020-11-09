from copy import copy
from typing import List, NoReturn, Optional, Tuple

from color import Color
from pieces.field import Field
from pieces.piece import Piece


class Pawn(Piece):
    def __init__(self, x: int, y: int, color: Color):
        super().__init__(x, y, color)
        self.possible_attacks = []
        if color == Color.WHITE:
            self.moves = [lambda: (self.location[0] - 1, self.location[1]),
                          lambda: (self.location[0] - 1, self.location[1] - 1),
                          lambda: (self.location[0] - 1, self.location[1] + 1)]
        else:
            self.moves = [lambda: (self.location[0] + 1, self.location[1]),
                          lambda: (self.location[0] + 1, self.location[1] - 1),
                          lambda: (self.location[0] + 1, self.location[1] + 1)]

    def find_possible_attacks(self) -> NoReturn:
        if self.location[0] == 0:
            self.possible_attacks = []
        elif self.location[1] == 0:
            self.possible_attacks = [self.moves[2]()]  # [(self.location[0] - 1, self.location[1] + 1)]
        elif self.location[1] == 7:
            self.possible_attacks = [self.moves[1]()]  # [(self.location[0] - 1, self.location[1] - 1)]
        else:
            self.possible_attacks = [self.moves[1](), self.moves[2]()]
            # [(self.location[0] - 1, self.location[1] - 1),(self.location[0] - 1, self.location[1] + 1)]

    def find_possible_moves(self, chessboard) -> NoReturn:
        self.possible_moves = []
        locations = []
        for move in self.moves:
            locations.append(move())

        if self.color == Color.WHITE and self.location[0] == 0:
            return
        elif self.color == Color.BLACK and self.location[0] == 7:
            return

        if 0 <= locations[0][0] <= 7 and 0 <= locations[0][1] <= 7:
            field = chessboard.chessboard[locations[0][0]][locations[0][1]]
            if not isinstance(field, Piece):
                self.possible_moves.append(field)

        if 0 <= locations[1][0] <= 7 and 0 <= locations[1][1] <= 7:
            field = chessboard.chessboard[locations[1][0]][locations[1][1]]
            if isinstance(field, Piece) and field.color == self.enemy_color:
                self.possible_moves.append(field)

        if 0 <= locations[2][0] <= 7 and 0 <= locations[2][1] <= 7:
            field = chessboard.chessboard[locations[2][0]][locations[2][1]]
            if isinstance(field, Piece) and field.color == self.enemy_color:
                self.possible_moves.append(field)

    def select_mating_fields(self, active_pieces: List[Piece], chessboard) -> Optional[Tuple[Field]]:
        # TODO: Zrobić sprawdzenie z check_mates
        self.mating_fields = []
        original_location = copy(self.location)
        enemy_king = chessboard.get_king(self.enemy_color)
        enemy_pieces = chessboard.get_all_pieces(self.enemy_color)
        enemy_pieces.remove(enemy_king)

        for field in self.possible_moves:
            changed_chessboard, deleted_piece = chessboard.change_board(self, field)
            if deleted_piece is not None:
                enemy_pieces.remove(deleted_piece)
            active_pieces_copy = copy(active_pieces)
            enemy_king.find_possible_moves(changed_chessboard, active_pieces_copy)
            active_pieces_copy.remove(self)

            if len(enemy_king.possible_moves) == 0:
                field_is_mating = True
                if self.attacks(enemy_king, changed_chessboard):
                    if enemy_king.attacks(field, changed_chessboard):
                        if changed_chessboard.is_defended(self, active_pieces_copy):
                            if changed_chessboard.is_attacked(self, enemy_pieces) is not None:
                                field_is_mating = False
                            else:
                                field_is_mating = True
                        else:
                            field_is_mating = False
                    else:
                        if changed_chessboard.is_attacked(self, enemy_pieces) is None:
                            field_is_mating = True
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

    def attacks(self, attacked: Field, chessboard):
        self.find_possible_attacks()
        for square in self.possible_attacks:
            field = chessboard.chessboard[square[0]][square[1]]
            if isinstance(field, Piece):
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
