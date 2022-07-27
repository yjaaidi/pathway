from __future__ import annotations

from dataclasses import dataclass

import cv2
from pathway.camera.camera import Camera


@dataclass
class OpencvCamera(Camera):

  width: int
  height: int

  @staticmethod
  def create(width: int, height: int) -> Camera:
    return OpencvCamera(width=width, height=height)
  
  def read_image(self):
    if self._capture is None:
      raise Exception("Camera not started")

    ret, frame = self._capture.read()
    if not ret:
      raise Exception("Could not read frame")
    return frame

  def start(self):
    self._capture = cv2.VideoCapture(0)
    self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
    self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
  
  def stop(self):
    self._capture.release()