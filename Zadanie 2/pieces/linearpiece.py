from abc import ABC
from copy import copy
from typing import NoReturn, List, Optional, Tuple

from color import Color
from pieces.field import Field
from pieces.king import King
from pieces.piece import Piece


class LinearPiece(Piece, ABC):
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
                        if field.color == Color.BLACK:
                            self.possible_moves.append(field)
                            can_move = False
                        else:
                            can_move = False
                    else:
                        self.possible_moves.append(field)

            self.location = copy(original_location)
        return

    def select_mating_fields(self, active_white_pieces: List[Piece], chessboard) -> Optional[Tuple[Field]]:
        # Znajduje pola matujące - czyli takie na których figura atakuje króla i wszyskie pola na które może się
        # on ruszyć. Nie sprawdza czy figura może zostać na nim zbita przez króla lub inną figurę, ani nie sprawdza
        # czy linia ataku figury na króla może zostać zablokowana przez figurę przeciwnika
        self.mating_fields = []
        original_location = copy(self.location)
        black_king = chessboard.get_black_king()  # Może warto by było je przesyłać do metody, albo umieścić jako pole Chessboard?
        black_pieces = chessboard.get_all_black_pieces()  # To samo co wyżej
        black_pieces.remove(black_king)

        for field in self.possible_moves:
            changed_chessboard, deleted_piece = chessboard.change_board(self, field)
            if deleted_piece is not None:
                black_pieces.remove(deleted_piece)
            active_whites_copy = copy(active_white_pieces)
            black_king.find_possible_moves(changed_chessboard, active_whites_copy)
            active_whites_copy.remove(self)

            if len(black_king.possible_moves) == 0:
                # To mogę sprawdzić to co w chessboard.check_mates
                field_is_mating = True
                if self.attacks_king(black_king, changed_chessboard):
                    if black_king.attacks(self, changed_chessboard):
                        if changed_chessboard.is_defended(self, active_whites_copy):
                            is_attacked = changed_chessboard.is_attacked(self, black_pieces)
                            if is_attacked is not None:
                                field_is_mating = False
                            else:
                                field_is_mating = True
                        else:
                            field_is_mating = False
                    elif changed_chessboard.is_attacked(self, black_pieces) is None:
                        for square in self.king_attack_line_:
                            # Jeżeli ten if nie przejdzie to field_is_mating jest True
                            # TODO: Optymalizacja - czy muszę za każdym razem szukać ruchów czarnych figur?
                            figure = changed_chessboard.is_attacked(square, black_pieces)
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
                black_pieces.append(deleted_piece)
        return None

    def attacks(self, attacked: Field, chessboard) -> bool:
        # Ignores Black King if piece is White
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
                    else:
                        if self.color == Color.WHITE:
                            if isinstance(field, Piece) and not (
                                    isinstance(field, King) and field.color == Color.BLACK):
                                can_move = False
                        else:
                            if isinstance(field, Piece):
                                can_move = False
            self.location = copy(original_location)

        return False

    def attacks_king(self, king: Piece, chessboard) -> bool:
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
                        self.king_attack_line_ = attack_line
                        self.location = copy(original_location)
                        return True
                    else:
                        if isinstance(field, Piece):
                            can_move = False
                    attack_line.append(field)

            self.location = copy(original_location)

        return False
