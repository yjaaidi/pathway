
import time


class LogTime:
    """
    Logs execution time in ms in a with block.
    Usage:
        with LogTime("f"):
          f()
    """

    def __init__(self, name):
        self._name = name

    def __enter__(self):
        self._start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_traceback):
        print(self._name, (time.time() - self._start) * 1000)
