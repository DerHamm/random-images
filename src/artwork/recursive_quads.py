import seaborn as sns

from PIL import ImageDraw
from itertools import cycle

from .artwork import Artwork
from .art_utils import hex_to_rgb

from ..random_colors import RandomColors

class RecursiveQuads(Artwork):
    DEFAULT_COLOR = None

    def __init__(self, chance=0.5, *args, **kwargs):
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
        self.default_color = self.theme

    def draw(self):
        draw = ImageDraw.Draw(self.canvas.image)
        w = self.canvas.size[0]
        h = self.canvas.size[1]

        size_w = w / 100
        size_h = h / 100

        mid_x = w / 2
        mid_y = h / 2

        x1 = mid_x - size_w
        y1 = mid_y - size_h
        x2 = mid_x + size_w
        y2 = mid_y + size_h

        step_w = size_w
        step_h = size_h

        count = 0

        colors = cycle(self.palette)

        while x1 < w and y1 < h and x2 > 0 and y2 > 0:
            x1 += step_w
            y1 += step_h
            x2 -= step_w
            y2 -= step_h
            rect = (x1, y1, x2, y2)
            if count > 0:
                draw.rectangle(rect, outline=next(colors))
            count += 1
