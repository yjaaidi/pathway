import logging
from typing import List
from pathway_client.leds.led_controller import Led, LedController


class TerminalController(LedController):

    @staticmethod
    def create() -> LedController:
        return TerminalController()

    def get_count(self) -> int:
        return 150

    def set_leds(self, leds: List[Led]):
        print(leds_to_ascii(leds))


def leds_to_ascii(leds: List[Led]):
    grey_scale_list = [round((led.red + led.green + led.blue) / 3)
                       for led in leds]
    ascii_list = [_grey_scale_to_char(grey_scale)
                  for grey_scale in grey_scale_list]
    return "".join(ascii_list)


def _grey_scale_to_char(grey_scale: int):
    if grey_scale == 0:
        return '-'
    # Convert grey scale (values from 1 to 255) into hex (values from 1 to F)
    return '{:x}'.format(round(grey_scale / 17))
