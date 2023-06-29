import seaborn as sns

from PIL import ImageDraw

from .art_utils import hex_to_rgb
from .artwork import Artwork

from ..random_colors import RandomColors

class PietMondrian(Artwork):
    def __init__(
        self,
        chance_for_background_color: float = 5 / 8,
        subdivisions: int = 40000,
        min_diff: float = 16,
        sep: float = 1,
        splits: list[float] = None,
        edge: float = 10,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        # iterations for the splitting loop
        self.subdivisions = int(subdivisions)

        # minimum size for a single rectangle
        # if this is too small, weird stuff happens
        self.min_diff = int(min_diff)

        # spacing between rectangles
        self.sep = float(sep)

        # Piet Mondrian Color Palette = (38, 71, 124), (240, 217, 92), (162, 45, 40) + (223, 224, 236)
        # Subdivision adjustment
        # Determines the ratio of the split on a rectangle.
        # Using other split values might result in funny/unexpected stuff
        if splits is None:
            self.splits = [0.5, 1, 1.5]
        else:
            self.splits = splits
        # splits = [i / 10 for i in range(1, 15, 1)]

        # Border thiccness
        self.edge = float(edge)

        self.random_colors = RandomColors(self.rng)
        self.palette = sns.color_palette(
            self.random_colors.random_palette(), 16
        ).as_hex()
        self.random_color = lambda: hex_to_rgb(
            self.random_colors.random_color_from_palette(self.palette)
        )
        self.theme = self.random_color()
        self.chance = chance_for_background_color

    def draw(self):
        edge = self.edge
        splits = self.splits
        sep = self.sep
        subdivisions = self.subdivisions
        min_diff = self.min_diff

        random = self.rng
        w = self.canvas.size[0]
        h = self.canvas.size[1]

        draw = ImageDraw.Draw(self.canvas.image)

        rectangles = [
            [(edge, edge), (w - edge, edge), (w - edge, h - edge), (edge, h - edge)]
        ]

        # Start splitting things up
        for _ in range(subdivisions):
            index = random.randint(0, len(rectangles))
            rect = rectangles[index]
            lx = rect[0][0]
            rx = rect[1][0]
            ly = rect[0][1]
            ry = rect[2][1]

            split = splits[random.randint(0, len(splits))]
            if random.random() < 0.5:
                if min_diff < (rx - lx):
                    # Get new shapes x value (y is same)
                    x_split = (rx - lx) / 2 * split + lx

                    rectangles.pop(index)

                    rectangles.append(
                        [(lx, ly), (x_split - sep, ly), (x_split - sep, ry), (lx, ry)]
                    )

                    rectangles.append(
                        [(x_split + sep, ly), (rx, ly), (rx, ry), (x_split + sep, ry)]
                    )

            else:
                if min_diff < (ry - ly):
                    y_split = (ry - ly) / 2 * split + ly

                    rectangles.pop(index)
                    rectangles.append(
                        [(lx, ly), (rx, ly), (rx, y_split - sep), (lx, y_split - sep)]
                    )
                    rectangles.append(
                        [(lx, y_split + sep), (rx, y_split + sep), (rx, ry), (lx, ry)]
                    )

        for rect in rectangles:
            # we only need 2 points for the draw
            rect = rect[0] + rect[2]
            color = self.theme if random.random() > self.chance else self.random_color()
            draw.rectangle(rect, fill=color, width=1)
