from dataclasses import dataclass, field
from pieces.piece import Piece


@dataclass(order=True)
class PrioritizedPiece:
    """
    Class created for PriorityQueue.\n
    :param priority: priority level of pieces. 0 - the highest.
    :param piece: Piece
    """
    priority: int
    piece: Piece = field(compare=False)
