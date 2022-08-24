#!/usr/bin/env python

import io
from os import getcwd
from os.path import join
from typing import List, TypedDict

import cv2  # type: ignore
from PIL import Image
from rx.core.typing import Observable
from rx.core.typing import Subject as SubjectType
from rx.operators import buffer_with_time
from rx.operators import map as rx_map
from rx.operators import share
from rx.subject import Subject

from pathway_client.camera.get_camera import get_camera
import requests


def main():

    processor = DetectionProcessor()

    processor.init()

    with get_camera(width=640, height=480) as camera:
        while True:
            frame = camera.read_image()

            cv2.imwrite("dist/last-image.jpg", frame)

            image = Image.fromarray(frame.astype('uint8'), 'RGB')
            image_bytes = io.BytesIO()
            image.save(image_bytes, format='JPEG')
            detected_items = requests.post(
                'http://localhost:8000/images', files={'image': image_bytes.getvalue()}
            ).json()['items']

            processor.process_detected_objects(detected_items)


class DetectedItem(TypedDict):
    name: str
    percentage_probability: float
    box_points: tuple[int, int, int, int]


class DetectionProcessor:
    _fps_obs: Observable[float]
    _detected_objects_subject = Subject()
    _detected_objects_obs: Observable[List[dict]]

    def __init__(self):
        self._detected_objects_obs = self._detected_objects_subject.pipe(
            share()
        )

        self._fps_obs = self._detected_objects_obs.pipe(
            buffer_with_time(timespan=5, timeshift=1),
            rx_map(lambda buffer: len(buffer) / 5),
        )

    def init(self):
        self._fps_obs.subscribe(lambda fps: print(fps), lambda err: print(err))
        self._detected_objects_obs.subscribe(
            lambda positions: print(positions))

    def process_detected_objects(self, detected_objects: List[dict]):
        self._detected_objects_subject.on_next(detected_objects)


if __name__ == '__main__':
    main()
