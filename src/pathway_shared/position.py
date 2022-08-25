
from dataclasses import dataclass


@dataclass
class Position:
    """
    :param x: horizontal position in percentage ranging from -100 to +100.
    :param width: width in percentage relative to the width of the image.
    :param height: height in percentage relative to the width of the image.
    """
    x: float
    width: float
    height: float
