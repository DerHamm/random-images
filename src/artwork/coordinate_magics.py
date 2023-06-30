import seaborn as sns

from .artwork import Artwork
from .art_utils import hex_to_rgb

from ..util.random_colors import RandomColors


class CoordinateMagics(Artwork):
    def __init__(self, chance: float = 0.5, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.random_colors = RandomColors(self.rng)
        self.chance = chance
        self.palette = sns.color_palette(
            self.random_colors.random_palette(), 16
        ).as_hex()
        self.random_color = lambda: hex_to_rgb(
            self.random_colors.random_color_from_palette(self.palette)
        )
        self.theme = self.random_color()

    def operation(self, x: int, y: int) -> None:
        raise NotImplementedError("Implement this method in a subclass of CoordinateMagics")

    def draw(self) -> None:
        pixels = self.pixels
        rng = self.rng
        for x in range(self.canvas.size[0]):
            for y in range(self.canvas.size[1]):
                rng.seed(self.operation(x, y))
                pixels[x, y] = (
                    self.random_color() if rng.random() > self.chance else self.theme
                )


class XorCoords(CoordinateMagics):
    def operation(self, x, y) -> None:
        return x ^ y


class OrCoords(CoordinateMagics):
    def operation(self, x, y) -> None:
        return x | y


class AndCoords(CoordinateMagics):
    def operation(self, x, y) -> None:
        return x & y


class AddCoords(CoordinateMagics):
    def operation(self, x, y) -> None:
        return x + y


class SubCoordsYFromX(CoordinateMagics):
    def operation(self, x, y) -> None:
        return abs(y - x)


class ModCoords(CoordinateMagics):
    def operation(self, x, y) -> None:
        return x % max(1, y)
