from __future__ import annotations

from abc import ABC, abstractmethod

from numpy.typing import NDArray


class Camera(ABC):

  @staticmethod
  @abstractmethod
  def create(width: int, height: int) -> Camera:
    pass

  @abstractmethod
  def read_image(self) -> NDArray:
    pass
