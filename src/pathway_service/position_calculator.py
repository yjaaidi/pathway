from dataclasses import dataclass


@dataclass
class Position:
    x: float
    width: float
    height: float


@dataclass
class PositionCalculator:
    width: int
    height: int

    def compute_position(self, box_points: tuple[int, int, int, int]) -> Position:
        x1, y1, x2, y2 = box_points

        # 1. Compute center (x1 + x2) / 2
        # 2. Translate to the left (-self.width / 2)
        # 3. Make it a percentage
        x = round(((x1 + x2 - self.width) / 2) * 100 / (self.width / 2))

        height = round((y2 - y1)/self.height * 100)
        width = round((x2 - x1)/self.width * 100)
        return Position(x=x, height=height, width=width)
