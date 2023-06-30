from PIL import Image, PyAccess
from pathlib import Path
from os import system
from threading import Thread
from uuid import uuid4
from hashlib import md5

from .canvas import Canvas
from .pillow_canvas import PillowCanvas
from ..util.random_provider import Random

from ..util.config_loader import Config


class Artwork(object):
    _canvas: Image
    _pixels: PyAccess
    rng: Random

    CANVAS_CLASS = PillowCanvas
    DEFAULT_MODE = "RGBA"
    DEFAULT_COLOR = (255, 255, 255, 255)
    DEFAULT_SIZE = (640, 480)

    def __init__(self, rng, canvas: Canvas = None, default_color=None)  -> None:
        self._canvas = canvas
        self._pixels = None
        self._default_color = default_color
        self.rng = rng
        self.hash = abs(
            int.from_bytes(md5(str(self.rng.random()).encode()).digest(), "big")
        )

    @property
    def default_color(self) -> tuple:
        return (
            self.__class__.DEFAULT_COLOR
            if self._default_color is None
            else self._default_color
        )

    @default_color.setter
    def default_color(self, value) -> None:
        self._default_color = value

    @property
    def canvas(self) -> Image:
        if self._canvas is None:
            self._canvas = Artwork.CANVAS_CLASS(
                Artwork.DEFAULT_MODE, Artwork.DEFAULT_SIZE, self.default_color
            )
        return self._canvas

    @property
    def pixels(self) -> PyAccess:
        if self._pixels is None:
            self._pixels = self.canvas.load()
        return self._pixels

    def save(self, path: str = None) -> None:
        if path is None:
            path = Path("img/{}.png".format(str(uuid4()))).absolute()
        if Path(path).is_dir():
            path = Path(path) / (str(uuid4()) + ".png")
        return self.canvas.save(path, "PNG")

    def show(self, path: str = None) -> None:
        if path is None:
            path = Path("img/{}.png".format(str(uuid4()))).absolute()
        if Path(path).is_dir():
            path = Path(path) / (str(uuid4()) + ".png")
        self.canvas.save(path)
        Thread(
            target=lambda: system(
                'start {app} "{path}"'.format(app=Config.get_image_view_application(), path=path)
            ),
            daemon=True,
        ).start()

    def draw(self) -> None:
        raise NotImplementedError("Each pattern has to implement it's own unique image")
