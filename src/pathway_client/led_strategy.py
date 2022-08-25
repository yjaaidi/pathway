
import math
from typing import List
from rx.operators import map as rx_map
from rx.core import Observable
from pathway_client.leds.led_controller import Led
from pathway_shared.detected_object import DetectedObject


class LedStrategy:

    _led_count: int

    def __init__(self, led_count: int):
        self._led_count = led_count

    def get_leds_obs(self, detected_objects_obs: Observable):
        return detected_objects_obs.pipe(
            rx_map(self._get_leds)
        )

    def _get_leds(self, detected_objects: List[DetectedObject]):
        leds = [Led(0, 0, 0) for _ in range(self._led_count)]

        for detected_object in detected_objects:
            central_led_index = round(
                detected_object.position.x * self._led_count / 100)

            width_led_count = round(
                detected_object.position.width * self._led_count / 100
            )

            led_indexes = range(
                max(0, round(central_led_index - width_led_count/2)),
                min(central_led_index + round(width_led_count/2), self._led_count)
            )

            for led_index in led_indexes:
                distance_from_central_led = abs(led_index - central_led_index)
                power = max(
                    0, 255 - round(math.exp(10 * distance_from_central_led / width_led_count)))
                leds[led_index] = Led(power, power, power)

        return leds
