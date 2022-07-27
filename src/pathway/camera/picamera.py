from __future__ import annotations

from dataclasses import dataclass

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
    self._picam2 = __import__("picamera2").Picamera2()
  
  def read_image(self):
    return self._picam2.capture_array()
  
  def start(self):
    config = self._picam2.create_still_configuration({'size': [self.width, self.height]})
    self._picam2.configure(config)
    self._picam2.start()
  
  def stop(self):
    self._picam2.stop()
