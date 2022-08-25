
from typing import List
from rx.core.typing import Observable
from pathway_shared.detected_object import DetectedObject


class LedStrategy:

    _led_count: int

    def __init__(self, led_count: int):
        self._led_count = led_count

    def get_leds_obs(self, detected_objects_obs: Observable[List[DetectedObject]]):
        raise NotImplementedError()
