from PIL import Image, PyAccess, ImageDraw
from src.random_colors import RandomColors
import seaborn as sns
from pathlib import Path
from os import system

__all__ = ['AddCoords', 'AndCoords', 'Artwork', 'CoordinateMagics', 'ModCoords', 'OrCoords', 'PietMondrian',
           'SubCoordsYFromX', 'XorCoords']


def hex_to_rgb(h):
    return tuple(int(h[1:][i:i + 2], 16) for i in (0, 2, 4))


class Artwork(object):
    _image: Image
    _pixels: PyAccess

    DEFAULT_MODE = 'RGBA'
    DEFAULT_COLOR = (255, 255, 255, 255)
    DEFAULT_SIZE = (640, 480)

    def __init__(self, rng, image: Image = None):
        self._image = image
        self._pixels = None
        self.rng = rng

    @property
    def image(self):
        if self._image is None:
            self._image = Image.new(Artwork.DEFAULT_MODE, Artwork.DEFAULT_SIZE, Artwork.DEFAULT_COLOR)
        return self._image

    @property
    def pixels(self):
        if self._pixels is None:
            self._pixels = self.image.load()
        return self._pixels

    def save(self, path):
        return self.image.save(path, 'PNG')

    def show(self):
        # TODO: Replace this path?
        path = Path('img\\tmp.png').absolute()
        self.image.save(path)
        system(str(path))

    def draw(self):
        raise NotImplementedError('Each pattern has to implement it\'s own unique image')


class PietMondrian(Artwork):
    def __init__(self, chance_for_background_color=5 / 8, subdivisions=40000, min_diff=16, sep=1, splits=None, edge=10,
                 *args, **kwargs):

        super().__init__(*args, **kwargs)

        # iterations for the splitting loop
        self.subdivisions = subdivisions

        # minimum size for a single rectangle
        # if this is too small, weird stuff happens
        self.min_diff = min_diff

        # spacing between rectangles
        self.sep = sep

        # Piet Mondrian Color Palette = (38, 71, 124), (240, 217, 92), (162, 45, 40) + (223, 224, 236)
        # Subdivision adjustment
        # Determines the ratio of the split on a rectangle. Using other split values might result in funny/unexpected stuff
        if splits is None:
            self.splits = [.5, 1, 1.5]
        else:
            self.splits = splits
        # splits = [i / 10 for i in range(1, 15, 1)]

        # Border thiccness
        self.edge = edge

        self.random_colors = RandomColors(self.rng)
        self.palette = sns.color_palette(self.random_colors.random_palette(), 16).as_hex()
        self.random_color = lambda: hex_to_rgb(self.random_colors.random_color_from_palette(self.palette))
        self.theme = self.random_color()
        self.chance = chance_for_background_color

    def draw(self):
        edge = self.edge
        splits = self.splits
        sep = self.sep
        subdivisions = self.subdivisions
        min_diff = self.min_diff

        random = self.rng
        w = self.image.size[0]
        h = self.image.size[1]

        draw = ImageDraw.Draw(self.image)

        rectangles = [[(edge, edge), (w - edge, edge), (w - edge, h - edge), (edge, h - edge)]]

        # Start splitting things up
        for _ in range(subdivisions):
            index = random.randint(0, len(rectangles))
            rect = rectangles[index]
            lx = rect[0][0]
            rx = rect[1][0]
            ly = rect[0][1]
            ry = rect[2][1]

            split = splits[random.randint(0, len(splits))]
            if random.random() < .5:
                if min_diff < (rx - lx):
                    # Get new shapes x value (y is same)
                    x_split = (rx - lx) / 2 * split + lx

                    rectangles.pop(index)
                    rectangles.append([(lx, ly), (x_split - sep, ly), (x_split - sep, ry), (lx, ry)])
                    rectangles.append([(x_split + sep, ly), (rx, ly), (rx, ry), (x_split + sep, ry)])

            else:
                if min_diff < (ry - ly):
                    y_split = (ry - ly) / 2 * split + ly

                    rectangles.pop(index)
                    rectangles.append([(lx, ly), (rx, ly), (rx, y_split - sep), (lx, y_split - sep)])
                    rectangles.append([(lx, y_split + sep), (rx, y_split + sep), (rx, ry), (lx, ry)])

        for rect in rectangles:
            # we only need 2 points for the draw
            rect = rect[0] + rect[2]
            color = self.theme if random.random() > self.chance else self.random_color()
            draw.rectangle(rect, fill=color, width=1)


class CoordinateMagics(Artwork):
    def __init__(self, chance=0.5, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.random_colors = RandomColors(self.rng)
        self.chance = chance
        self.palette = sns.color_palette(self.random_colors.random_palette(), 16).as_hex()
        self.random_color = lambda: hex_to_rgb(self.random_colors.random_color_from_palette(self.palette))
        self.theme = self.random_color()

    def operation(self, x, y):
        raise NotImplementedError()

    def draw(self):
        pixels = self.pixels
        rng = self.rng
        for x in range(self.image.size[0]):
            for y in range(self.image.size[1]):
                rng.seed(self.operation(x, y))
                pixels[x, y] = self.random_color() if rng.random() > self.chance else self.theme


class XorCoords(CoordinateMagics):
    def operation(self, x, y):
        return x ^ y


class OrCoords(CoordinateMagics):
    def operation(self, x, y):
        return x | y


class AndCoords(CoordinateMagics):
    def operation(self, x, y):
        return x & y


class AddCoords(CoordinateMagics):
    def operation(self, x, y):
        return x + y


class SubCoordsYFromX(CoordinateMagics):
    def operation(self, x, y):
        return abs(y - x)


class ModCoords(CoordinateMagics):
    def operation(self, x, y):
        return x % max(1, y)


art = classes = [AddCoords,
                 AndCoords,
                 ModCoords,
                 OrCoords,
                 PietMondrian,
                 SubCoordsYFromX,
                 XorCoords]
