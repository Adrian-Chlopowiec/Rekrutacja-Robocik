from copy import copy
from queue import PriorityQueue
from typing import List, Optional, Tuple, Union

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


def parse(matrix: List[List[str]]) -> List[List]:
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


def queue_to_list(queue: PriorityQueue):
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
    def __init__(self, chessboard: List[List[str]] = [[]]):
        self.chessboard = parse(chessboard)
        self.possible_mating_pieces = PriorityQueue()

    def change_board(self, piece: Piece, field: Field):
        other = Chessboard()
        other.chessboard = self.copy_chessboard()

        other.chessboard[field.location[0]].remove(field)
        other.chessboard[piece.location[0]].remove(piece)

        # other_piece = Piece(field.location[0], field.location[1], piece.color)
        # other_field = Field(piece.location[0], piece.location[1])
        deleted_piece = None
        if isinstance(field, Piece):
            new_field = Field(field.location[0], field.location[1])
            tmp = copy(new_field.location)
            new_field.location = copy(piece.location)
            piece.location = tmp
            other.chessboard[new_field.location[0]].insert(new_field.location[1], new_field)
            deleted_piece = field
        else:
            tmp = copy(field.location)
            field.location = copy(piece.location)
            piece.location = tmp
            other.chessboard[field.location[0]].insert(field.location[1], field)
        other.chessboard[piece.location[0]].insert(piece.location[1], piece)

        return other, deleted_piece

    def find_possible_mating_pieces(self):
        # Punkt 2
        queue = PriorityQueue()
        black_king = self.get_king(Color.BLACK)
        for x in range(len(self.chessboard)):
            for y in range(len(self.chessboard[x])):
                field = self.chessboard[x][y]
                if isinstance(field, Piece) and field.color == Color.WHITE:
                    if isinstance(field, Pawn):
                        if (abs(y - black_king.location[1]) <= 2
                                and (abs(x - black_king.location[0]) == 1
                                     or abs(x - black_king.location[0]) == 2
                                     or abs(x - black_king.location[0]) == 0)):
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
        self.possible_mating_pieces = queue
        return queue

    def find_blocking_figures(self):
        return

    def get_king(self, color: Color) -> Piece:
        for i in range(len(self.chessboard)):
            for j in range(len(self.chessboard)):
                field = self.chessboard[i][j]
                if isinstance(field, King) and field.color == color:
                    return field

    def get_all_pieces(self, color: Color) -> List[Piece]:
        pieces = []
        for i in range(len(self.chessboard)):
            for j in range(len(self.chessboard)):
                field = self.chessboard[i][j]
                if isinstance(field, Piece) and field.color == color:
                    pieces.append(field)
        return pieces

    def check_for_mates(self) -> Optional[Tuple[Union[Piece, Field]]]:
        active_white_pieces = queue_to_list(self.possible_mating_pieces)
        for piece in active_white_pieces:
            mate = piece.select_mating_fields(active_white_pieces, self)
            if mate is not None:
                return mate

        black_pieces = self.get_all_pieces(Color.BLACK)
        black_pieces.remove(self.get_king(Color.BLACK))
        for piece in black_pieces:
            mate = piece.select_mating_fields(black_pieces, self)
            if mate is not None:
                return mate
        return None

    def is_attacked(self, field: Piece, pieces: List[Piece], find_moves=True) -> Optional[Field]:  # Optional[Piece]?
        # Zwraca None jeśli figura nie jest atakowana, w przeciwnym wypadku figurę atakującą
        # Dla każdej figury przeciwnika sprawdzić, czy atakuje ona to pole.
        if find_moves:
            self.find_moves_for(pieces)
        for piece in pieces:
            if piece.attacks(field, self):
                return piece
        return None

    def find_moves_for(self, pieces: List[Piece]):
        for piece in pieces:
            piece.find_possible_moves(self)

    def is_defended(self, field: Field, pieces: List[Piece]) -> bool:
        is_defended = self.is_attacked(field, pieces, find_moves=False)
        if is_defended is None:
            return False
        else:
            return True

    def copy_chessboard(self):
        chessboard = list()
        i = 0
        for row in self.chessboard:
            chessboard.append(list())
            for element in row:
                chessboard[i].append(element)
            i += 1
        return chessboard
