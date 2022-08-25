from pathway_client.leds.neopixel_controller import NeopixelController
from pathway_client.leds.terminal_controller import TerminalController


def get_led_controller():
    try:
        return NeopixelController.create()
    except:
        return TerminalController.create()
