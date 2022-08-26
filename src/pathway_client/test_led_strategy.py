

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
    set_objs, leds_spy, tear_down, advance_by = set_up()

    set_objs("-----------------------------------aaaaaaaaaa-----------------------------------aaaaaaaaaaaaaaaaaaaa")

    # Wait 500ms for things to stabilize.
    advance_by(.5)

    # Get last call.
    leds_ascii = leds_to_ascii(leds_spy.call_args[0][0])
    assert leds_ascii == "-----------------------------------6cefffffec-----------------------------------6acdeefffffffffeedca"

    tear_down()


def test_change_led_progressively():
    set_objs, leds_spy, tear_down, advance_by = set_up()

    set_objs("-----------------------------------aaaaaaaaaa-------------------------------------------------------")

    # Wait 500ms and see light fading in
    advance_by(.5)

    # First call is the seed (initial leds value) which is triggered before even detected_objects start emitting,
    # then we have an event triggered by detected_changes_obs when we call "set_objs",
    # and finally, we have a call every 50ms during 500ms, meaning there are 10 additional calls.
    assert leds_spy.call_count == 12

    leds = leds_to_ascii(leds_spy.call_args_list[0][0][0])
    assert leds == "----------------------------------------------------------------------------------------------------"
    leds = leds_to_ascii(leds_spy.call_args_list[1][0][0])
    assert leds == "-----------------------------------1111111111-------------------------------------------------------"
    leds = leds_to_ascii(leds_spy.call_args_list[2][0][0])
    assert leds == "-----------------------------------3333333333-------------------------------------------------------"
    leds = leds_to_ascii(leds_spy.call_args_list[3][0][0])
    assert leds == "-----------------------------------4444444444-------------------------------------------------------"
    leds = leds_to_ascii(leds_spy.call_args_list[4][0][0])
    assert leds == "-----------------------------------6666666666-------------------------------------------------------"
    leds = leds_to_ascii(leds_spy.call_args_list[5][0][0])
    assert leds == "-----------------------------------6777777777-------------------------------------------------------"
    leds = leds_to_ascii(leds_spy.call_args_list[6][0][0])
    assert leds == "-----------------------------------6999999999-------------------------------------------------------"
    leds = leds_to_ascii(leds_spy.call_args_list[7][0][0])
    assert leds == "-----------------------------------6aaaaaaaaa-------------------------------------------------------"
    leds = leds_to_ascii(leds_spy.call_args_list[8][0][0])
    assert leds == "-----------------------------------6ccccccccc-------------------------------------------------------"
    leds = leds_to_ascii(leds_spy.call_args_list[9][0][0])
    assert leds == "-----------------------------------6cdddddddc-------------------------------------------------------"
    leds = leds_to_ascii(leds_spy.call_args_list[10][0][0])
    assert leds == "-----------------------------------6cefffffec-------------------------------------------------------"
    # We are stable and additional calls produce the same result.
    leds = leds_to_ascii(leds_spy.call_args_list[11][0][0])
    assert leds == "-----------------------------------6cefffffec-------------------------------------------------------"

    tear_down()


def set_up():

    scheduler = TestScheduler()

    strategy = LedStrategy(led_count=100, scheduler=scheduler)

    detected_objects_obs: SubjectType[List[DetectedObject]] = Subject()

    leds_spy = Mock()

    subscription = strategy.get_leds_obs(
        detected_objects_obs).subscribe(on_next=leds_spy)

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
