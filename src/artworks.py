import math
import typing
from PIL import Image, PyAccess, ImageDraw
from src.random_colors import RandomColors
import seaborn as sns
from pathlib import Path
from os import system
from threading import Thread
from itertools import cycle
from uuid import uuid4
from hashlib import md5
from math import sqrt

__all__ = ['AddCoords', 'AndCoords', 'Artwork', 'CoordinateMagics', 'ModCoords', 'OrCoords', 'PietMondrian',
           'SubCoordsYFromX', 'XorCoords', 'art', 'RecursiveQuads', 'DummyPlot', 'CirclePacking']

IMAGE_VIEW_APPLICATION = 'paintdotnet'


def hex_to_rgb(h):
    """ It looks cursed, but it just casts the hex numbers to decimals and wraps them in a tuple """
    return tuple(int(h[1:][i:i + 2], 16) for i in (0, 2, 4))


def rect_size(point1, point2, point3, point4):
    width = math.sqrt(math.pow((point2[0] - point1[0]), 2) + math.pow((point2[1] - point1[1]), 2))
    length = math.sqrt(math.pow((point4[0] - point3[0]), 2) + math.pow((point4[1] - point3[1]), 2))
    return width * length


class Canvas(object):
    """ Canvas needs to implement some image """

    @staticmethod
    def new(*args, **kwargs):
        """ Initialize a new image """
        raise NotImplementedError()

    def load(self):
        """ Return the pixel array """
        raise NotImplementedError()

    def save(self, *args, **kwargs):
        """ Save the image to disk """
        raise NotImplementedError()

    def rotate(self, *args, **kwargs):
        """ Rotate image """
        raise NotImplementedError()


class PillowCanvas(Canvas):

    def __init__(self, mode, size, color=0):
        self.image = PillowCanvas.new(mode, size, color=color)
        self._size = size

    @staticmethod
    def new(mode, size, color: typing.Any = 0):
        return Image.new(mode, size, color=color)

    def load(self):
        return self.image.load()

    def save(self, fp, _format=None, **kwargs):
        self.image.save(fp, format=_format, **kwargs)

    @property
    def size(self):
        return self._size

    def rotate(self, *args, **kwargs):
        self.image.rotate(*args, **kwargs)


class Artwork(object):
    _canvas: Image
    _pixels: PyAccess

    CANVAS_CLASS = PillowCanvas
    DEFAULT_MODE = 'RGBA'
    DEFAULT_COLOR = (255, 255, 255, 255)
    DEFAULT_SIZE = (640, 480)

    def __init__(self, rng, canvas: Canvas = None, default_color=None):
        self._canvas = canvas
        self._pixels = None
        self._default_color = default_color
        self.rng = rng
        self.hash = abs(int.from_bytes(md5(str(self.rng.random()).encode()).digest(), 'big'))

    @property
    def default_color(self):
        return self.__class__.DEFAULT_COLOR if self._default_color is None else self._default_color

    @default_color.setter
    def default_color(self, value):
        self._default_color = value

    @property
    def canvas(self):
        if self._canvas is None:
            self._canvas = Artwork.CANVAS_CLASS(Artwork.DEFAULT_MODE, Artwork.DEFAULT_SIZE, self.default_color)
        return self._canvas

    @property
    def pixels(self):
        if self._pixels is None:
            self._pixels = self.canvas.load()
        return self._pixels

    def save(self, path=None):
        if path is None:
            path = Path('img/{}.png'.format(str(uuid4()))).absolute()
        return self.canvas.save(path, 'PNG')

    def show(self, path=None):
        if path is None:
            path = Path('img/{}.png'.format(str(uuid4()))).absolute()
        self.canvas.save(path)
        Thread(target=lambda: system('{app} {path}'.format(app=IMAGE_VIEW_APPLICATION, path=path)), daemon=True).start()

    def draw(self):
        raise NotImplementedError('Each pattern has to implement it\'s own unique image')


class PietMondrian(Artwork):
    def __init__(self, chance_for_background_color=5 / 8, subdivisions=40000, min_diff=16, sep=1, splits=None, edge=10,
                 *args, **kwargs):

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
            self.splits = [.5, 1, 1.5]
        else:
            self.splits = splits
        # splits = [i / 10 for i in range(1, 15, 1)]

        # Border thiccness
        self.edge = float(edge)

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
        w = self.canvas.size[0]
        h = self.canvas.size[1]

        draw = ImageDraw.Draw(self.canvas.image)

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
        for x in range(self.canvas.size[0]):
            for y in range(self.canvas.size[1]):
                rng.seed(self.operation(x, y))
                pixels[x, y] = self.random_color() if rng.random() > self.chance else self.theme


class CubicDisarray(Artwork):
    """ WIP """
    """ Source: https://generativeartistry.com/tutorials/cubic-disarray/"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def draw(self):
        def _draw(_canvas, width, height):
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
                self.canvas.rotate(rotate_amt, translate=(i + translate_amt + offset, j + offset))
                _draw(canvas, square_size, square_size)


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


class RecursiveQuads(Artwork):
    DEFAULT_COLOR = None

    def __init__(self, chance=0.5, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.random_colors = RandomColors(self.rng)
        self.chance = chance
        self.palette = sns.color_palette(self.random_colors.random_palette(), 16).as_hex()
        self.random_color = lambda: hex_to_rgb(self.random_colors.random_color_from_palette(self.palette))
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


class DummyPlot(Artwork):
    """ The dummy plot that one generates when testing out
        how 'random' a PRNG is """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def draw(self):
        draw = ImageDraw.Draw(self.canvas.image)

        b, w = (0, 0, 0), (255, 255, 255)
        for x in range(self.canvas.size[0]):
            for y in range(self.canvas.size[1]):
                draw.point((x, y), fill=b if self.rng.random() > 0.5 else w)


class CirclePacking(Artwork):
    """ Sourced from https://generativeartistry.com/tutorials/circle-packing/
        The code shown there was improved in some ways """

    class Circle(object):
        def __init__(self, x, y, r):
            self.x = x
            self.y = y
            self.radius = r

    def __init__(self, create_circle_attempts: int = 500,
                 total_circles: int = 500,
                 min_radius: int = 4, max_radius: int = 100,
                 overlap_borders: bool = False,
                 line_width: int = 2, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.line_width = line_width
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.total_circles = total_circles
        self.create_circle_attempts = create_circle_attempts

        self.random_colors = RandomColors(self.rng)
        self.palette = sns.color_palette(self.random_colors.random_palette(), 32).as_hex()
        self.random_color = lambda: hex_to_rgb(self.random_colors.random_color_from_palette(self.palette))
        self.theme = hex_to_rgb(self.random_colors.pop_random_color_from_palette(self.palette))
        self.canvas.image = self.canvas.new(Artwork.DEFAULT_MODE, Artwork.DEFAULT_SIZE, self.theme)

        self.circles = list()

        self.width = self.canvas.size[0]
        self.height = self.canvas.size[1]

        self.total_fails = 10

        if overlap_borders:
            self.__has_collision = lambda circle: self.__overlap(circle)
        else:
            self.__has_collision = lambda circle: self.__border_check(circle) or self.__overlap(circle)

    def draw(self):

        draw = ImageDraw.Draw(self.canvas.image)
        fails = 0
        while True:
            if not self.__create_and_draw_circle(draw):
                fails += 1
            if fails > self.total_fails:
                break

    def __create_and_draw_circle(self, draw: ImageDraw.ImageDraw):
        new_circle = None
        can_draw = False
        for tries in range(self.create_circle_attempts):
            new_circle = CirclePacking.Circle(self.rng.random() * self.width,
                                              self.rng.random() * self.width, self.min_radius)
            if self.__has_collision(new_circle):
                continue
            else:
                can_draw = True
                break

        if not can_draw:
            return False

        for radius_size in range(self.min_radius, self.max_radius, 1):
            new_circle.radius = radius_size
            if self.__has_collision(new_circle):
                new_circle.radius -= 1
                break

        self.circles.append(new_circle)
        coordinates = (new_circle.x, new_circle.y)
        box = self.__bounding_box(coordinates, new_circle.radius)
        draw.ellipse(box, outline=self.random_color(), fill=self.random_color(), width=self.line_width)
        return True

    def __border_check(self, circle: Circle):
        return not (0 <= circle.x - circle.radius < circle.x + circle.radius < self.width and
                    0 <= circle.y - circle.radius < circle.y + circle.radius < self.height)

    def __overlap(self, circle: Circle):
        for other_circle in self.circles:
            a = circle.radius + other_circle.radius
            x = circle.x - other_circle.x
            y = circle.y - other_circle.y

            if a >= sqrt((x * x) + (y * y)):
                return True
        return False

    @staticmethod
    def __bounding_box(point, radius):
        return [(point[0] - radius, point[1] - radius),
                (point[0] + radius, point[1] + radius)]


art = classes = [AddCoords,
                 AndCoords,
                 ModCoords,
                 OrCoords,
                 PietMondrian,
                 SubCoordsYFromX,
                 XorCoords,
                 RecursiveQuads,
                 CirclePacking]
