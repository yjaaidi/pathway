

import re
from typing import List
from unittest.mock import Mock
from pathway_client.leds.terminal_controller import leds_to_ascii

from pathway_shared.detected_object import DetectedObject
from pathway_shared.position import Position
from rx.core.typing import Subject as SubjectType
from rx.subject import Subject
from rx.testing import TestScheduler

from pathway_client.led_strategy import LedStrategy
import pytest


def test_turn_on_leds_around_detected_objects():
    set_objs, leds_spy, tear_down, _ = set_up()

    set_objs("-----------------------------------aaaaaaaaaa-----------------------------------aaaaaaaaaaaaaaaaaaaa")

    assert leds_spy.call_count == 1
    leds = leds_spy.call_args[0][0]

    assert leds_to_ascii(
        leds
    ) == "-----------------------------------6cefffffec-----------------------------------6acdeefffffffffeedca"

    tear_down()


@pytest.mark.skip("🚧 work in progress")
def test_change_led_progressively():
    set_objs, leds_spy, tear_down, advance_by = set_up()

    set_objs("-----------------------------------aaaaaaaaaa-------------------------------------------------------")

    # Wait 500ms and see light fading in
    advance_by(.5)

    assert leds_spy.call_count == 11
    assert leds_to_ascii(
        leds_spy.call_args[0][0]) == "----------------------------------------------------------------------------------------------------"
    assert leds_to_ascii(
        leds_spy.call_args[1][0]) == "-----------------------------------1111111111-------------------------------------------------------"
    assert leds_to_ascii(
        leds_spy.call_args[2][0]) == "-----------------------------------2222222222-------------------------------------------------------"
    # @todo the progress here...
    assert leds_to_ascii(
        leds_spy.call_args[10][0]) == "-----------------------------------6cefffffec-------------------------------------------------------"

    tear_down()


def set_up():

    scheduler = TestScheduler()

    strategy = LedStrategy(led_count=100, scheduler=scheduler)

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
            type="person",
            probability=int(match.group()[0], 16),
            position=Position(
                x=(match.start() + match.end()) / 2,
                width=match.end() - match.start(),
                height=10
            )
        ) for match in matches]
        detected_objects_obs.on_next(detected_objects)

    def teardown(): subscription.dispose()

    return update_detected_objects, leds_spy, teardown, scheduler.advance_by
