from typing import List, Tuple, Callable, Optional
from abc import abstractmethod
from pieces.field import Field
from color import Color


class Piece(Field):
    def __init__(self, x: int, y: int, color: Color):
        super().__init__(x, y)
        self.color = color
        if color == Color.WHITE:
            self.enemy_color = Color.BLACK
        else:
            self.enemy_color = Color.WHITE
        self.possible_moves = List[Tuple]
        self.mating_fields = List[Tuple]  # TODO: To chyba do usunięcia?
        # types_of_moves jest listą funkcji przekształcających aktualną lokalizację na następne pole
        # z danego "kierunku ruchu"
        self.moves = List[Callable[[], Tuple[int]]]

    @abstractmethod
    def find_possible_moves(self, chessboard):
        pass

    @abstractmethod
    def attacks(self, field: Field, chessboard) -> bool:
        pass

    @abstractmethod
    def select_mating_fields(self, active_white_pieces: List, chessboard) -> Optional[Tuple[Field]]:
        pass

    @abstractmethod
    def to_string(self):
        pass
