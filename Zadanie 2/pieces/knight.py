from copy import copy
from typing import NoReturn, List, Optional, Tuple

from pieces.field import Field
from color import Color
from pieces.piece import Piece


class Knight(Piece):
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
                if not (isinstance(field, Piece) and field.color == Color.WHITE):
                    self.possible_moves.append(field)

    def select_mating_fields(self, active_white_pieces: List[Piece], chessboard) -> Optional[Tuple[Field]]:
        # TODO: Tak samo jak w linearpiece, zrobić sprawdzanie z check_mates
        self.mating_fields = []
        original_location = copy(self.location)
        black_king = chessboard.get_black_king()
        black_pieces = chessboard.get_all_black_pieces()
        black_pieces.remove(black_king)

        for field in self.possible_moves:
            # TODO: wydzielić to do funkcji i zwracać odpowiedni stuff z niej
            changed_chessboard, deleted_piece = chessboard.change_board(self, field)
            if deleted_piece is not None:
                black_pieces.remove(deleted_piece)
            active_whites_copy = copy(active_white_pieces)
            black_king.find_possible_moves(changed_chessboard, active_whites_copy)
            active_whites_copy.remove(self)

            if len(black_king.possible_moves) == 0:
                field_is_mating = True
                if self.attacks(black_king, changed_chessboard):
                    if changed_chessboard.is_attacked(self, black_pieces) is None:
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
        return None

    def attacks(self, attacked: Field, chessboard) -> bool:
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
