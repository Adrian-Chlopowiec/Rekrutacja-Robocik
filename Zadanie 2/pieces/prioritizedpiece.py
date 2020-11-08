from dataclasses import dataclass, field
from pieces.piece import Piece


@dataclass(order=True)
class PrioritizedPiece:
    priority: int
    piece: Piece = field(compare=False)
