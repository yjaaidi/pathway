from pathway.camera.opencv_camera import OpencvCamera
from pathway.camera.picamera import Picamera


def get_camera(width: int, height: int):
  try:
      return Picamera.create(width=width, height=height)
  except:
      return OpencvCamera.create(width=width, height=height)
