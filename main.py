#!/usr/bin/env python

from dataclasses import dataclass
from os import environ, getcwd
from os.path import join
from signal import SIGINT, signal
from tempfile import mkdtemp
from typing import List, TypedDict

import cv2
from imageai.Detection import VideoObjectDetection

from position_calculator import PositionCalculator


def main():

    cwd = getcwd()
    camera = cv2.VideoCapture(0)

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    fps = round(camera.get(cv2.CAP_PROP_FPS))
    width = round(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = round(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

    processor = DetectionProcessor(width=width, height=height)

    detector = VideoObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(join(cwd, "models", "yolo.h5"))
    detector.loadModel(detection_speed="flash")

    output_file_path = join(cwd, "dist", "video")

    detector.detectObjectsFromVideo(
        camera_input=camera,
        output_file_path=output_file_path,
        frame_detection_interval=round(fps / 2),
        frames_per_second=fps,
        minimum_percentage_probability=60,
        per_frame_function=lambda frame_number, output_array, output_count: processor.process_frame(
            output_array),
    )


class Item(TypedDict):
    name: str
    percentage_probability: float
    box_points: tuple[int, int, int, int]


@dataclass
class DetectionProcessor:
    _position_calculator: PositionCalculator

    def __init__(self, width: int, height: int):
        self._position_calculator = PositionCalculator(
            width=width, height=height)

    def process_frame(self, items: List[Item]):
        people = filter(lambda item: item['name'] == "person", items)
        positions = map(lambda item: self._position_calculator.compute_position(
            box_points=item['box_points']), people)
        print(list(positions))


if __name__ == '__main__':
    main()
