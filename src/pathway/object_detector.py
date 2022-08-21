from dataclasses import dataclass
from enum import Enum
from typing import List, Literal, Union

from pathway.position_calculator import Position

DetectedObjectType = Literal["human"]

@dataclass
class DetectedObject:
  type: DetectedObjectType
  position: Position

class ObjectDetector:

  def detect_objects(self, picture_data: bytes) -> List[DetectedObject]:
    """
    Detect objects in the given picture.

    @deprecated work in progress
    
    :param picture_data: 640x480 JPEG raw data
    
    :return: List of detected objects"""

    return []