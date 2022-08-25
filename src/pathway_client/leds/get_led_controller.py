import logging
from pathway_client.leds.neopixel_controller import NeopixelController
from pathway_client.leds.terminal_controller import TerminalController


def get_led_controller():
    try:
        return NeopixelController.create()
    except Exception as error:
        logging.warn("Neopixel not available: reason {message}".format(
            message=str(error)))
        return TerminalController.create()
