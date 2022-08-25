

from audioop import avg
import re
from typing import List
from unittest.mock import Mock

from pathway_shared.detected_object import DetectedObject
from pathway_shared.position import Position
from pytest import mark
from rx.core.typing import Subject as SubjectType
from rx.subject import Subject

from pathway_client.led_strategy import LedStrategy
from pathway_client.leds.led_controller import Led


def test_turn_on_leds_around_detected_objects():
    update_detected_objects, leds_spy, tear_down = set_up()

    update_detected_objects(
        "-----------------------------------aaaaaaaaaa---------------------------------------------aaaaaaaaaa")

    assert leds_spy.call_count == 1
    leds = leds_spy.call_args[0][0]

    assert leds[0:35] == [Led(0, 0, 0) for _ in range(0, 35)]
    assert leds[35:45] == [Led(255, 255, 255) for _ in range(0, 10)]
    assert leds[45:90] == [Led(0, 0, 0) for _ in range(45)]
    assert leds[90:100] == [Led(255, 255, 255) for _ in range(0, 10)]

    tear_down()


def set_up():

    strategy = LedStrategy(led_count=100)

    detected_objects_obs: SubjectType[List[DetectedObject]] = Subject()

    leds_obs = strategy.get_leds_obs(detected_objects_obs)

    leds_spy = Mock()

    subscription = leds_obs.subscribe(on_next=leds_spy)

    def update_detected_objects(detected_objects_str: str):
        """
        Converts ascii string to detected objects list.
        Probability is hexadecimal and ranges from 1 to a to fit as one character.
        """
        matches = list(re.finditer("[1-9a]+", detected_objects_str))
        detected_objects = [DetectedObject(
            type="human",
            probability=int(match.group()[0], 16),
            position=Position(
                x=(match.start() + match.end()) - len(detected_objects_str),
                width=match.end() - match.start(),
                height=10
            )
        ) for match in matches]
        detected_objects_obs.on_next(detected_objects)

    def teardown(): subscription.dispose()

    return update_detected_objects, leds_spy, teardown


def create_object(x: float, width: float, probability: float = 100) -> DetectedObject:
    return DetectedObject(type="human", probability=probability, position=Position(x=x, width=width, height=10))
