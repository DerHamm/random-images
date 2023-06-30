from PIL import ImageDraw

from .artwork import Artwork


class CubicDisarray(Artwork):
    """WIP"""

    """ Source: https://generativeartistry.com/tutorials/cubic-disarray/"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def draw(self) -> None:
        def _draw(_canvas, width, height) -> None:
            _canvas.rectangle((-width / 2, -height / 2, width, height), fill=(0, 0, 0))

        size = 320
        displacement = 15
        rotation_factor = 20
        offset = 10
        square_size = 30

        canvas = ImageDraw.Draw(self.canvas)

        for i in range(square_size, size - square_size, square_size):
            for j in range(square_size, size - square_size, square_size):
                sign = -1 if self.rng.random() > 0.5 else 1
                rotate_amt = j / size * sign * self.rng.random() * rotation_factor
                sign = -1 if self.rng.random() > 0.5 else 1
                translate_amt = j / size * sign * self.rng.random() * displacement

                # self.image.transform((i + translate_amt + offset, j + offset))
                self.canvas.rotate(
                    rotate_amt, translate=(i + translate_amt + offset, j + offset)
                )
                _draw(canvas, square_size, square_size)
