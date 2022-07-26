from __future__ import annotations

from dataclasses import dataclass

import cv2
from pathway.camera.camera import Camera


@dataclass
class OpencvCamera(Camera):

  @staticmethod
  def create(width: int, height: int) -> Camera:
    return OpencvCamera(width=width, height=height)
  
  def __init__(self, width, height):
    self._capture = cv2.VideoCapture(0)
    self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
  
  def read_image(self):
    ret, frame = self._capture.read()
    if not ret:
      raise Exception("Could not read frame")
    return frame
