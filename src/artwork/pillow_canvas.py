from PIL import Image, PyAccess, ImageDraw
from typing import Union

from .canvas import Canvas


class PillowCanvas(Canvas):
    def __init__(self, mode: str, size: tuple, color: Union[float, str, tuple] = 0):
        self.image = PillowCanvas.new(mode, size, color=color)
        self._size = size

    @staticmethod
    def new(mode, size, color: Union[float, str, tuple] = 0) -> Image:
        return Image.new(mode, size, color=color)

    def load(self) -> PyAccess:
        return self.image.load()

    def save(self, fp: str, _format: str = None, **kwargs):
        self.image.save(fp, format=_format, **kwargs)

    @property
    def size(self) -> tuple:
        return self._size

    def rotate(self, *args, **kwargs):
        self.image.rotate(*args, **kwargs)
