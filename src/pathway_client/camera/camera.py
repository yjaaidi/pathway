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

    @abstractmethod
    def start(self):
        """Start the camera.

        This will be called automatically when used with contextmanager."""
        pass

    @abstractmethod
    def stop(self):
        """Stop the camera.

        This will be called automatically when used with contextmanager."""
        pass

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_traceback):
        self.stop()
