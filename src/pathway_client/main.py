#!/usr/bin/env python

import io
import os
import sys
from os import getcwd
from os.path import join
from typing import List, TypedDict

import cv2  # type: ignore
import requests
from numpy import ndarray
from PIL import Image
from rx.core.typing import Observable
from rx.core.typing import Subject as SubjectType
from rx.operators import buffer_with_time
from rx.operators import map as rx_map
from rx.operators import share
from rx.subject import Subject

from pathway_client.camera.get_camera import get_camera


def start():
    DetectionProcessor().start()


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

    def start(self):

        self._fps_obs.subscribe(lambda fps: print(fps), lambda err: print(err))
        self._detected_objects_obs.subscribe(
            lambda positions: print(positions))

        api_base_url = os.environ.get('API_BASE_URL', 'http://localhost:8000')

        with get_camera(width=640, height=480) as camera:
            while True:
                frame = camera.read_image()

                cv2.imwrite("dist/last-image.jpg", frame)

                image_bytes = self._frame_to_jpg(frame)
                response = requests.post(
                    '{api_base_url}/images'.format(api_base_url=api_base_url), files={'image': image_bytes})
                detected_items = response.json()['items']

                self._detected_objects_subject.on_next(detected_items)

    def _frame_to_jpg(self, frame: ndarray) -> bytes:
        image = Image.fromarray(frame.astype('uint8'), 'RGB')
        image_buffer = io.BytesIO()
        image.save(image_buffer, format='JPEG')
        return image_buffer.getvalue()


if __name__ == '__main__':
    start()

# +import board
# +import neopixel
# +        poss= list(positions)
# +        l = 150
# +        pixels = neopixel.NeoPixel(board.D18, l, auto_write=False)
# +        for i in range(l): pixels[i] = (255,0,0)
# +        pixels.show()
# +        for pos in poss:
# +            pixels = neopixel.NeoPixel(board.D18, l, auto_write=False)
# +            for i in range(l): pixels[i] = (255,255,255)
# +            pixels.show()
# +        return poss