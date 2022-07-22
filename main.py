#!/usr/bin/env python

from dataclasses import dataclass
from os import environ, getcwd
from os.path import join
from signal import SIGINT, signal
from tempfile import mkdtemp

import cv2
from imageai.Detection import VideoObjectDetection


def main():
    cwd = getcwd()
    camera = cv2.VideoCapture(0)
    width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print("{} {}".format(width, height))

    detector = VideoObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(join(cwd, "yolo.h5"))
    detector.loadModel(detection_speed="flash")

    output_file_path = join(mkdtemp(), "camera_detected_video.avi")

    detector.detectObjectsFromVideo(
        camera_input=camera,
        output_file_path=output_file_path,
        frame_detection_interval=10,
        frames_per_second=30,
        minimum_percentage_probability=60,
        per_frame_function=frame_callback
    )


def frame_callback(frame_number, output_array, output_count):
    print("Processing frame {}".format(frame_number))
    print(output_count)
    people = filter(lambda item: item['name'] == "person", output_array)
    positions = map(lambda item: get_position(item['box_points']), people)
    print(list(positions))


@dataclass
class Position:
    x: int
    height: int
    width: int


def get_position(box_points: tuple[int, int, int, int]) -> Position:
    x1, y1, x2, y2 = box_points
    return Position(x=(x1 + x2)/2, height=y2 - y1, width=x2 - x1)


if __name__ == '__main__':
    main()
