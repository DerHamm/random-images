from PIL import ImageDraw

from .artwork import Artwork


class DummyPlot(Artwork):
    """The dummy plot that one generates when testing out
    how 'random' a PRNG is"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def draw(self) -> None:
        draw = ImageDraw.Draw(self.canvas.image)

        b, w = (0, 0, 0), (255, 255, 255)
        for x in range(self.canvas.size[0]):
            for y in range(self.canvas.size[1]):
                draw.point((x, y), fill=b if self.rng.random() > 0.5 else w)
