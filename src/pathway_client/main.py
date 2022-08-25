#!/usr/bin/env python

import io
import os
from typing import List, TypedDict

import cv2  # type: ignore
import requests
from numpy import ndarray
from pathway_service.object_detector import DetectedObject
from PIL import Image
from rx.core.typing import Observable
from rx.core.typing import Subject
from rx.operators import buffer_with_time
from rx.operators import map as rx_map
from rx.operators import share
from rx.subject import Subject

from pathway_client.camera.get_camera import get_camera


def start():
    DetectionProcessor().start()


class DetectionProcessor:
    _fps_obs: Observable[float]
    _detected_objects_subject = Subject()
    _detected_objects_obs: Observable[List[DetectedObject]]

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
            lambda detected_objects: print(detected_objects)
        )

        self._detected_objects_obs.subscribe(
            lambda detected_objects: self._update_lights(detected_objects)
        )

        api_base_url = os.environ.get('API_BASE_URL', 'http://localhost:8000')

        with get_camera(width=640, height=480) as camera:
            while True:
                frame = camera.read_image()

                cv2.imwrite("dist/last-image.jpg", frame)

                image_bytes = self._frame_to_jpg(frame)
                response = requests.post(
                    '{api_base_url}/images'.format(api_base_url=api_base_url), files={'image': image_bytes})
                detected_objects = [DetectedObject(
                    **item) for item in response.json()['items']]

                self._detected_objects_subject.on_next(detected_objects)

    def _frame_to_jpg(self, frame: ndarray) -> bytes:
        image = Image.fromarray(frame.astype('uint8'), 'RGB')
        image_buffer = io.BytesIO()
        image.save(image_buffer, format='JPEG')
        return image_buffer.getvalue()

    def _update_lights(self, detected_objects: List[DetectedObject]):
        import board
        from neopixel import NeoPixel

        leds = NeoPixel(board.D18, 150, auto_write=False)
        led_count = len(leds)
        for i in range(led_count):
            leds[i] = (0, 0, 0)

        for object in detected_objects:
            index = led_count + round(object.position.x * led_count / 2)
            for i in range(max(0, index - 10), min(index + 10, led_count)):
                leds[i] = (255, 255, 255)

        leds.show()


if __name__ == '__main__':
    start()
