#!/usr/bin/env python

from os import getcwd
from os.path import join
from typing import List, TypedDict

import cv2  # type: ignore
from rx.core.typing import Observable
from rx.core.typing import Subject as SubjectType
from rx.operators import buffer_with_time
from rx.operators import map as rx_map
from rx.operators import share
from rx.subject import Subject
from pathway.camera.opencv_camera import OpencvCamera
from pathway.camera.picamera import Picamera

from pathway.imageai.detection import ObjectDetection
from pathway.position_calculator import Position, PositionCalculator


def main():

    cwd = getcwd()

    width = 640
    height = 480

    try:
        camera = Picamera.create(width=width, height=height)
    except:
        camera = OpencvCamera.create(width=width, height=height)

    processor = DetectionProcessor(width=width, height=height)

    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(join(cwd, "models", "yolo.h5"))
    detector.loadModel(detection_speed="flash")

    processor.init()

    while True:
        frame = camera.read_image()
        
        cv2.imwrite("dist/last-image.jpg", frame)

        _, detected_items = detector.detectObjectsFromImage(
            input_image=frame,
            input_type="array",
            output_type="array",
            minimum_percentage_probability=40,
        )
        processor.process_detected_items(detected_items)


class DetectedItem(TypedDict):
    name: str
    percentage_probability: float
    box_points: tuple[int, int, int, int]


class DetectionProcessor:
    _fps_obs: Observable[float]
    _position_calculator: PositionCalculator
    _detected_items_subject = Subject()
    _positions_obs: Observable[List[Position]]

    def __init__(self, width: int, height: int):
        self._position_calculator = PositionCalculator(
            width=width, height=height)

        self._positions_obs = self._detected_items_subject.pipe(
            rx_map(self._process_detected_items),
            share()
        )

        self._fps_obs = self._positions_obs.pipe(
            buffer_with_time(timespan=5, timeshift=1),
            rx_map(lambda buffer: len(buffer) / 5),
        )

    def init(self):
        self._fps_obs.subscribe(lambda fps: print(fps), lambda err: print(err))
        self._positions_obs.subscribe(lambda positions: print(positions))

    def process_detected_items(self, detections: List[DetectedItem]):
        self._detected_items_subject.on_next(detections)

    def _process_detected_items(self, detections: List[DetectedItem]):
        # people = filter(lambda item: item['name'] == "person", items)
        people = detections
        positions = map(lambda item: self._position_calculator.compute_position(
            box_points=item['box_points']), people)
        return list(positions)


if __name__ == '__main__':
    main()
