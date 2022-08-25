import io
from dataclasses import dataclass
from os import getcwd
from os.path import join
from typing import List

import numpy
from PIL import Image

from pathway_service.imageai.detected_item import ImageAiDetectedItem
from pathway_service.imageai.detection import \
    ObjectDetection as ImageAiObjectDetection
from pathway_service.position_calculator import Position, PositionCalculator


@dataclass
class DetectedObject:
    type: str
    probability: float
    position: Position

    def __post_init__(self):
        self.position = Position(**self.position)


class ObjectDetector:
    _detector: ImageAiObjectDetection
    _width = 640
    _height = 480

    def __init__(self):
        self._detector = ImageAiObjectDetection()
        self._detector.setModelTypeAsYOLOv3()
        self._detector.setModelPath(join(getcwd(), "models", "yolo.h5"))
        self._detector.loadModel(detection_speed="flash")

    def detect_objects(self, image_data: bytes, filtered_types: List[str] = None) -> List[DetectedObject]:
        """
        Detect objects in the given picture.

        @deprecated work in progress

        :param image_data: 640x480 JPEG raw data

        :return: List of detected objects"""
        picture = Image.open(io.BytesIO(image_data))
        picture_array = numpy.asarray(picture)

        detected_items: List[ImageAiDetectedItem] = self._detector.detectObjectsFromImage(
            input_image=picture_array,
            input_type="array",
            output_type="array",
            minimum_percentage_probability=10,
        )[1]

        detected_objects = [self._to_object(
            detected_item=item) for item in detected_items]

        if filtered_types is not None:
            detected_objects = [
                detected_object for detected_object in detected_objects if detected_object.type in filtered_types]

        return detected_objects

    def _to_object(self, detected_item: ImageAiDetectedItem) -> DetectedObject:
        position_calculator = PositionCalculator(
            width=self._width, height=self._height)
        return DetectedObject(
            type=detected_item['name'],
            position=position_calculator.compute_position(
                box_points=detected_item['box_points']),
            probability=detected_item['percentage_probability'],
        )
