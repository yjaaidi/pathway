

from unittest.mock import Mock
from pathway_client.led_strategy import LedStrategy
from rx.subject import Subject
from pytest import mark


@mark.skip(reason="no way of currently testing this")
def test_turn_on_leds_around_detected_objects():
    detected_objects_obs, leds_spy, tear_down = set_up()

    # @todo emit two detected objects
    assert leds_spy.call_count == 1
    # @todo check leds_spy called with 2 x 10 leds on

    tear_down()


def set_up():

    strategy = LedStrategy(led_count=100)

    detected_objects_obs = Subject()

    leds_obs = strategy.get_leds_obs(detected_objects_obs)

    leds_spy = Mock()

    subscription = leds_obs.subscribe(on_next=leds_spy)

    def teardown():
        subscription.unsubscribe()

    return detected_objects_obs, leds_spy, teardown
