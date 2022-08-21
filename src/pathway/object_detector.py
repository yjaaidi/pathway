import io
from dataclasses import dataclass
from os import getcwd
from os.path import join
from typing import List, Literal

import numpy
from PIL import Image

from pathway.imageai.detection import ObjectDetection as ImageAiObjectDetection
from pathway.main import DetectedItem
from pathway.position_calculator import Position, PositionCalculator

@dataclass
class DetectedObject:
  type: str
  position: Position

class ObjectDetector:
  _width = 640
  _height = 480


  def detect_objects(self, picture_data: bytes) -> List[DetectedObject]:
    """
    Detect objects in the given picture.

    @deprecated work in progress
    
    :param picture_data: 640x480 JPEG raw data
    
    :return: List of detected objects"""

    detector = ImageAiObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(join(getcwd(), "models", "yolo.h5"))
    detector.loadModel(detection_speed="flash")
    picture = Image.open(io.BytesIO(picture_data))
    picture_array = numpy.asarray(picture)

    detected_items: List[DetectedItem] = detector.detectObjectsFromImage(
      input_image=picture_array,
      input_type="array",
      output_type="array",
      minimum_percentage_probability=40,
    )[1]

    return list(map(lambda item: self._to_object(detected_item=item), detected_items))

  def _to_object(self, detected_item: DetectedItem) -> DetectedObject:
    position_calculator = PositionCalculator(width=self._width, height=self._height)
    return DetectedObject(
      type=detected_item['name'],
      position=position_calculator.compute_position(box_points=detected_item['box_points'])
    )
