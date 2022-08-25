
from dataclasses import dataclass

from pathway_shared.position import Position


@dataclass
class DetectedObject:
    type: str
    probability: float
    position: Position

    def __post_init__(self):
        self.position = Position(
            **self.position) if type(self.position) is dict else self.position
