

from typing import List
from unittest.mock import Mock

from pathway_shared.detected_object import DetectedObject
from pathway_shared.position import Position
from pytest import mark
from rx.core.typing import Subject as SubjectType
from rx.subject import Subject

from pathway_client.led_strategy import LedStrategy
from pathway_client.leds.led_controller import Led


@mark.skip(reason="🚧 Work in progress!")
def test_turn_on_leds_around_detected_objects():
    detected_objects_obs, leds_spy, tear_down = set_up()

    # @todo emit two detected objects
    detected_objects_obs.on_next(
        [
            DetectedObject(probability=100,
                           position=Position(x=0, width=10)),
            DetectedObject(probability=100,
                           position=Position(x=100, width=10))
        ])
    assert leds_spy.call_count == 1
    assert leds_spy.call_args[0:45] == [Led(0, 0, 0) for _ in range(0, 45)]
    assert leds_spy.call_args[45:55] == [
        Led(255, 255, 255) for _ in range(0, 10)]
    assert leds_spy.call_args[55:95] == [Led(0, 0, 0) for _ in range(0, 45)]
    assert leds_spy.call_args[95:100] == [
        Led(255, 255, 255) for _ in range(0, 45)]

    tear_down()


def set_up():

    strategy = LedStrategy(led_count=100)

    detected_objects_obs: SubjectType[List[DetectedObject]] = Subject()

    leds_obs = strategy.get_leds_obs(detected_objects_obs)

    leds_spy = Mock()

    subscription = leds_obs.subscribe(on_next=leds_spy)

    def teardown(): subscription.unsubscribe()

    return detected_objects_obs, leds_spy, teardown
