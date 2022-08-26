
import math
from sched import scheduler
from typing import List
from rx.operators import map
from rx.core import Observable
from rx.core.typing import Scheduler
from pathway_client.leds.led_controller import Led
from pathway_client.leds.terminal_controller import leds_to_ascii
from pathway_shared.detected_object import DetectedObject
import rx
import rx.operators as ops


class LedStrategy:

    _led_count: int
    _scheduler: Scheduler | None

    def __init__(self, led_count: int, scheduler: Scheduler | None = None):
        """
        :param scheduler: overrides the timer's scheduler. This is useful for testing.
        """
        self._led_count = led_count
        self._scheduler = scheduler

    def get_leds_obs(self, detected_objects_obs: Observable):

        # Initial state.
        leds_seed = [Led(0, 0, 0) for _ in range(self._led_count)]

        # Trigger led computation every 50ms or if we recieve a new detected objects event.
        return rx.combine_latest(detected_objects_obs, rx.timer(0, .05, scheduler=self._scheduler)) \
            .pipe(
                ops.map(lambda args: args[0]),
                ops.scan(self._compute_next_leds, seed=leds_seed),
                ops.start_with(leds_seed),
        )

    def _compute_next_leds(self, current_leds: List[Led], detected_objects: List[DetectedObject]):
        """
        Computes the next leds state depending on previous state.
        """
        target_leds = self._compute_target_leds(
            detected_objects=detected_objects)

        return [self._compute_next_led(current_leds[i], target_leds[i]) for i in range(self._led_count)]

    def _compute_target_leds(self, detected_objects: List[DetectedObject]):
        """
        Computes the targeted state depending on detected objects.
        """
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

    def _compute_next_led(self, current_led: Led, target_led: Led):
        return Led(
            red=self._compute_next_color(current_led.red, target_led.red),
            green=self._compute_next_color(
                current_led.green, target_led.green),
            blue=self._compute_next_color(current_led.blue, target_led.blue)
        )

    def _compute_next_color(self, current_color: int, target_color: int):
        if current_color == target_color:
            return target_color

        # Increment if current color is inferior, otherwise decrement.
        direction = 1 if current_color < target_color else -1

        # Step by 25 in order to switch from 0 to 255 in around 500ms
        # consdering we are triggering this around once each 50ms
        step = 25

        return current_color + direction * min(step, abs(target_color - current_color))
