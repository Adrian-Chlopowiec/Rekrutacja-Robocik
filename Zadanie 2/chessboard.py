from copy import copy
from queue import PriorityQueue
from typing import List, Optional, Tuple, NoReturn, Any

from color import Color
from pieces.bishop import Bishop
from pieces.field import Field
from pieces.king import King
from pieces.knight import Knight
from pieces.pawn import Pawn
from pieces.piece import Piece
from pieces.prioritizedpiece import PrioritizedPiece
from pieces.queen import Queen
from pieces.rook import Rook


def parse(matrix: List[List[str]]) -> List[List[Field]]:
    """
    Parses matrix of strings to matrix of fields and pieces on chessboard.
    :param matrix: matrix of strings containing string representations of pieces and fields.
    :return: matrix of fields and chess pieces representing chessboard.
    """
    chessboard = list()

    for i in range(len(matrix)):
        chessboard.append(list())
        for j in range(len(matrix[i])):
            chessboard[i].append(
                {
                    '--': Field(i, j),
                    'wW': King(i, j, Color.WHITE),
                    'bW': King(i, j, Color.BLACK),
                    'wq': Queen(i, j, Color.WHITE),
                    'bq': Queen(i, j, Color.BLACK),
                    'wb': Bishop(i, j, Color.WHITE),
                    'bb': Bishop(i, j, Color.BLACK),
                    'wk': Knight(i, j, Color.WHITE),
                    'bk': Knight(i, j, Color.BLACK),
                    'wr': Rook(i, j, Color.WHITE),
                    'br': Rook(i, j, Color.BLACK),
                    'wp': Pawn(i, j, Color.WHITE),
                    'bp': Pawn(i, j, Color.BLACK)
                }[matrix[i][j]]
            )
    return chessboard


def queue_to_list(queue: PriorityQueue) -> List[Piece]:
    """
    Copies elements of PriorityQueue to List in unchanged order.
    :param queue: PriorityQueue to copy.
    :return: List containing elements of PriorityQueue in unchanged order.
    """
    elements = []
    queue_elems = []
    while queue.qsize() > 0:
        elem = queue.get_nowait()
        queue_elems.append(elem)
        elements.append(elem.piece)
    for elem in queue_elems:
        queue.put(elem)
    return elements


class Chessboard:
    """
    Class representing chessboard. It is also starting point for the algorithm. Performs operations for groups
    of fields and pieces.

    :param chessboard: matrix of strings containing string representations of pieces and fields
    """
    def __init__(self, chessboard: List[List[str]] = None):
        """
        :param chessboard: matrix of fields and chess pieces representing chessboard. Contains subclasses of Field.
        """
        if chessboard is None:
            chessboard = [[]]
        self.chessboard = parse(chessboard)
        self.possible_mating_whites = PriorityQueue()
        self.possible_mating_blacks = PriorityQueue()

    def find_mate(self) -> NoReturn:
        """
        Prepares white and black pieces and looks for mates. Print appropriate message whether it finds mate or not.\n
        :returns: None
        """
        self.__find_possible_mating_pieces(Color.WHITE)
        self.__find_moves_for(queue_to_list(self.possible_mating_whites))

        self.__find_possible_mating_pieces(Color.BLACK)
        self.__find_moves_for(queue_to_list(self.possible_mating_blacks))

        mates = self.__check_for_mates()
        if len(mates) == 0:
            print("Biały ani czarny nie może wygrać w jednym ruchu")
        elif mates[0][0].color == Color.WHITE:
            for mate in mates:
                print("Biały może wygrać " + mate[0].to_string() + " - " + mate[1].to_string())
        else:
            for mate in mates:
                print("Czarny może wygrać " + mate[0].to_string() + " - " + mate[1].to_string())

    def __check_for_mates(self) -> List[Tuple[Piece, Field]]:
        """
        For every possible mating piece of each color find checkmates if there are any.
        Firstly does it for white pieces and then for black.\n

        :returns: List of tuples of piece giving a checkmate and a field to move it to give the mate.
        """
        active_white_pieces = queue_to_list(self.possible_mating_whites)
        active_white_pieces.append(self.get_king(Color.WHITE))
        mates = []
        for piece in active_white_pieces:
            if not isinstance(piece, King):
                mates.extend(piece.find_mate(active_white_pieces, self))

        if len(mates) != 0:
            return mates

        active_black_pieces = queue_to_list(self.possible_mating_blacks)
        active_black_pieces.append(self.get_king(Color.BLACK))
        for piece in active_black_pieces:
            if not isinstance(piece, King):
                mates.extend(piece.find_mate(active_black_pieces, self))

        return mates

    def __find_possible_mating_pieces(self, ally_color: Color) -> NoReturn:
        """
        Looks for pieces that might be a danger to opposing color King.\n
        :param ally_color: color of pieces that want to mate.
        :returns: None
        """
        if ally_color == Color.WHITE:
            enemy_color = Color.BLACK
        else:
            enemy_color = Color.WHITE

        queue = PriorityQueue()
        enemy_king = self.get_king(enemy_color)
        for x in range(len(self.chessboard)):
            for y in range(len(self.chessboard[x])):
                field = self.chessboard[x][y]
                if isinstance(field, Piece) and field.color == ally_color:
                    if isinstance(field, Pawn):
                        if (abs(y - enemy_king.location[1]) <= 2
                                and 0 <= abs(x - enemy_king.location[0]) <= 3):
                            queue.put(PrioritizedPiece(3, field))
                    else:
                        # Queen, Rook or Bishop
                        if isinstance(field, Bishop):
                            queue.put(PrioritizedPiece(2, field))
                        elif isinstance(field, Knight):
                            queue.put(PrioritizedPiece(2, field))
                        elif isinstance(field, Rook):
                            queue.put(PrioritizedPiece(1, field))
                        elif isinstance(field, Queen):
                            queue.put(PrioritizedPiece(0, field))
        if ally_color == Color.WHITE:
            self.possible_mating_whites = queue
        else:
            self.possible_mating_blacks = queue

    def get_king(self, color: Color) -> Piece:
        """
        Looks for king of given color and returns him.\n
        :param color: Color of King to be looked for.
        :return: king of given color
        """
        for i in range(len(self.chessboard)):
            for j in range(len(self.chessboard)):
                field = self.chessboard[i][j]
                if isinstance(field, King) and field.color == color:
                    return field

    def get_all_pieces(self, color: Color) -> List[Piece]:
        """
        Looks for all pieces of given color and returns them\n
        :param color: Color of pieces to be looked for
        :return: list of pieces of given color
        """
        pieces = []
        for i in range(len(self.chessboard)):
            for j in range(len(self.chessboard)):
                field = self.chessboard[i][j]
                if isinstance(field, Piece) and field.color == color:
                    pieces.append(field)
        return pieces

    def __find_moves_for(self, pieces: List[Piece]) -> NoReturn:
        """
        Finds available moves for every piece from given list. For King checks for field it attacks.\n
        :param pieces: pieces to find moves for
        :returns: None
        """
        for piece in pieces:
            if isinstance(piece, King):
                piece.find_attacked_fields(self)
            else:
                piece.find_possible_moves(self)

    def is_attacked(self, field: Piece, pieces: List[Piece], find_moves=True) -> Optional[Piece]:
        """
        Checks if any piece from given ones attacks given field. If needed, firstly finds available moves for them.\n
        :param field: field to check if it is attacked
        :param pieces: list of pieces proposed to attack the field
        :param find_moves: if True, finds moves for pieces
        :return: if exists, piece that attacks field. Otherwise None.
        """
        if find_moves:
            self.__find_moves_for(pieces)
        for piece in pieces:
            if piece.attacks(field, self):
                return piece
        return None

    def is_defended(self, field: Piece, pieces: List[Piece]) -> bool:
        """
        Checks if any piece from given list defends (which is synonymous for attacks) given field.\n
        :param field: field to check if it is defended
        :param pieces: list of pieces proposed to defend the field
        :return: True if piece is defended, False otherwise.
        """
        is_defended = self.is_attacked(field, pieces, find_moves=False)
        if is_defended is None:
            return False
        else:
            return True

    def create_imaginary_board(self, piece: Piece, field: Field) -> Tuple[Any, Optional[Piece]]:
        """
        Creates imaginary board onto which pieces and fields from original board are copied.\n

        Imaginary board is a chessboard used to move selected piece and check various cases of mates.

        :param piece: piece which changes its location
        :param field: field with which piece changed its location
        :return: Imaginary Chessboard and piece taken on imaginary chessboard or None if no piece was taken.
        """
        imaginary = Chessboard()
        imaginary.chessboard = self.__copy_chessboard()

        imaginary.chessboard[field.location[0]].remove(field)
        imaginary.chessboard[piece.location[0]].remove(piece)

        deleted_piece = None
        if isinstance(field, Piece):
            new_field = Field(field.location[0], field.location[1])
            tmp = copy(new_field.location)
            new_field.location = copy(piece.location)
            piece.location = tmp
            imaginary.chessboard[new_field.location[0]].insert(new_field.location[1], new_field)
            deleted_piece = field
        else:
            tmp = copy(field.location)
            field.location = copy(piece.location)
            piece.location = tmp
            imaginary.chessboard[field.location[0]].insert(field.location[1], field)
        imaginary.chessboard[piece.location[0]].insert(piece.location[1], piece)

        return imaginary, deleted_piece

    def __copy_chessboard(self) -> List[List[Field]]:
        """
        Copies own chessboard.\n
        :return: matrix of fields.
        """
        chessboard = list()
        i = 0
        for row in self.chessboard:
            chessboard.append(list())
            for element in row:
                chessboard[i].append(element)
            i += 1
        return chessboard
