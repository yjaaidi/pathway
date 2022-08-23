
from typing import TypedDict


class ImageAiDetectedItem(TypedDict):
    name: str
    percentage_probability: float
    box_points: tuple[int, int, int, int]
