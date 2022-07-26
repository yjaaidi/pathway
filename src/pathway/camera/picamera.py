from __future__ import annotations

import sys
from dataclasses import dataclass, field

from pathway.camera.camera import Camera


@dataclass
class Picamera(Camera):

  width: int
  height: int

  @staticmethod
  def create(width: int, height: int) -> Camera:
    return Picamera(width=width, height=height)
  
  def __init__(self, width: int, height: int):
    self.width = width
    self.height = height
    self._picamera_module = __import__("picamera")
  
  def read_image(self):
    with self._picamera_module.PiCamera() as camera:
      with self._picamera_module.array.PiRGBArray(camera) as output:
        camera.resolution = (self.width, self.height)
        camera.capture(output, 'rgb')
        return output.array
