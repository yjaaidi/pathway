#!/usr/bin/env python

import logging
import os
from time import sleep
from typing import List

import requests
from numpy.typing import NDArray
from pathway_client.led_strategy import LedStrategy
from pathway_client.leds.led_controller import Led, LedController
from pathway_service.object_detector import DetectedObject
from rx.core.typing import Observable
from rx.operators import buffer_with_time
from rx.operators import map as rx_map
from rx.operators import share
from rx.subject import Subject

from pathway_client.camera.frame_to_jpg import frame_to_jpg
from pathway_client.camera.get_camera import get_camera
from pathway_client.leds.get_led_controller import get_led_controller


def start():
    DetectionProcessor().start()


class DetectionProcessor:
    _api_base_url: str
    _fps_obs: Observable[float]
    _detected_objects_subject = Subject()
    _detected_objects_obs: Observable[List[DetectedObject]]
    _led_controller: LedController
    _led_strategy: LedStrategy

    def __init__(self):
        self._detected_objects_obs = self._detected_objects_subject.pipe(
            share()
        )

        self._fps_obs = self._detected_objects_obs.pipe(
            buffer_with_time(timespan=5, timeshift=1),
            rx_map(lambda buffer: len(buffer) / 5),
        )

        self._led_controller = get_led_controller()
        self._led_strategy = LedStrategy(self._led_controller.get_count())

        self._api_base_url = os.environ.get(
            'API_BASE_URL', 'http://localhost:8000')

    def start(self):
        self._fps_obs.subscribe(
            on_next=lambda fps: logging.debug("FPS: {fps}".format(fps=fps)),
            on_error=lambda error: logging.exception(error)
        )

        self._led_strategy.get_leds_obs(self._detected_objects_obs).subscribe(
            on_next=lambda leds: self._led_controller.set_leds(leds),
            on_error=lambda error: logging.exception(error)
        )

        with get_camera(width=640, height=480) as camera:
            while True:
                frame = camera.read_image()

                try:
                    detected_objects = self._detect_objects(frame)
                    self._detected_objects_subject.on_next(detected_objects)
                    continue
                except ConnectionError:
                    logging.warn(
                        "Object detection failed: service unreachable.")
                except Exception as error:
                    logging.warn("Object detection failed: unknown error.")
                    logging.exception(error)

                # Wait a sec before trying again.
                sleep(1)

    def _detect_objects(self, frame: NDArray):
        image_bytes = frame_to_jpg(frame)

        response = requests.post(
            '{api_base_url}/images'.format(api_base_url=self._api_base_url), files={'image': image_bytes})

        detected_objects = [DetectedObject(
            **item) for item in response.json()['items']]

        return detected_objects


if __name__ == '__main__':
    start()
