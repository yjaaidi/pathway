from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class Led:
    red: int
    green: int
    blue: int


class LedController(ABC):

    @staticmethod
    @abstractmethod
    def create() -> LedController:
        pass

    @abstractmethod
    def get_count(self) -> int:
        pass

    @abstractmethod
    def set_leds(self, leds: List[Led]):
        pass
