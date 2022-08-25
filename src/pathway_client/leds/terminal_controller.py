from typing import List
from pathway_client.leds.led_controller import Led, LedController


class TerminalController(LedController):

    @staticmethod
    def create() -> LedController:
        return TerminalController()

    def get_count(self) -> int:
        return 150

    def set_leds(self, led_list: List[Led]):
        grey_scale_list = [
            round(sum([led.red, led.green, led.blue]) / 3) for led in led_list]
        ascii_list = [self._grey_scale_to_char(
            grey_scale) for grey_scale in grey_scale_list]
        print("".join(ascii_list))

    def _grey_scale_to_char(self, grey_scale: int):
        if grey_scale == 0:
            return '_'
        if grey_scale < 100:
            return '-'
        return 'X'
