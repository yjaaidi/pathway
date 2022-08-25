
class LedStrategy:

    _led_count: int

    def __init__(self, led_count: int):
        self._led_count = led_count

    def get_leds_obs(detected_objects):
        raise NotImplementedError()
