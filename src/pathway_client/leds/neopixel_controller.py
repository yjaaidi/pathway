from abc import abstractmethod
import enum
from typing import List
from pathway_client.leds.led_controller import Led, LedController


class NeopixelController(LedController):

    def __init__(self):
        board = __import__("board")
        neopixel = __import__("neopixel")
        self._neopixel_leds = neopixel.NeoPixel(
            board.D18, 150, auto_write=False)

    @staticmethod
    def create() -> LedController:
        return NeopixelController()

    def get_length(self) -> int:
        return 150

    def set_leds(self, led_list: List[Led]):
        for i, led in enumerate(led_list):
            self._neopixel_leds[i] = (led.red, led.green, led.blue)
            self._neopixel_leds.show()
