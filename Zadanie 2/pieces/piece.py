from typing import List, Tuple, Callable, Optional, NoReturn
from abc import abstractmethod
from pieces.field import Field
from color import Color


class Piece(Field):
    """
    Abstract class representing all pieces.\n
    :param x: Location of piece on vertical axis
    :param y: Location of piece on horizontal axis
    :param color: Color of this piece
    :param possible_moves: List of possible moves
    :param moves: List of anonymous functions changing one location into another representing types of moves of piece.
    """
    def __init__(self, x: int, y: int, color: Color):
        super().__init__(x, y)
        self.color: Color = color
        if color == Color.WHITE:
            self.enemy_color = Color.BLACK
        else:
            self.enemy_color = Color.WHITE
        self.possible_moves: List[Tuple] = []
        self.moves: List[Callable[[], Tuple[int]]] = []

    @abstractmethod
    def find_possible_moves(self, chessboard) -> NoReturn:
        """
        Finds every field onto which this piece can move.\n
        :param chessboard: Chessboard on which the piece looks for its moves.
        :return: None
        """
        pass

    @abstractmethod
    def attacks(self, attacked: Field, chessboard) -> bool:
        """
        Checks if this piece attacks given field on given chessboard. Ignores King.\n
        :param attacked: Field to check if it is attacked
        :param chessboard: Chessboard on which the Piece and Field are.
        :return: True if piece attacks field, False otherwise.
        """
        pass

    @abstractmethod
    def find_mate(self, active_pieces: List, chessboard) -> Optional[Tuple[Field]]:
        """
        Looks for a checkmate for this piece\n
        :param active_pieces: Assisting pieces of the same color
        :param chessboard: Chessboard on which the pieces are.
        :return: Piece which gives checkmate and field to which piece must be moved if such exist. Otherwise None.
        """
        pass

    @abstractmethod
    def to_string(self):
        pass
