import math

from PIL import Image, PyAccess, ImageDraw
from src.random_colors import RandomColors
import seaborn as sns
from pathlib import Path
from os import system, mkdir
from os.path import isdir
from threading import Thread
from itertools import cycle
from uuid import uuid4

__all__ = ['AddCoords', 'AndCoords', 'Artwork', 'CoordinateMagics', 'ModCoords', 'OrCoords', 'PietMondrian',
           'SubCoordsYFromX', 'XorCoords', 'art', 'RecursiveQuads']

IMAGE_VIEW_APPLICATION = 'paintdotnet'


def hex_to_rgb(h):
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
    def new(mode, size, color=0):
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

from hashlib import md5
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
        if not path:
            path = Path('img/{}.png'.format(str(uuid4()))).absolute()
        return self.canvas.save(path, 'PNG')

    def show(self):
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

        """
        var canvas = document.querySelector('canvas');
        var context = canvas.getContext('2d');
        
        var size = 320;
        var dpr = window.devicePixelRatio;
        canvas.width = size * dpr;
        canvas.height = size * dpr;
        context.scale(dpr, dpr);
        context.lineWidth = 2;
        
        var randomDisplacement = 15;
        var rotateMultiplier = 20;
        var offset = 10;
        var squareSize = 30;
        
        function draw(width, height) {
          context.beginPath();
          context.rect(-width/2, -height/2, width, height);
          context.stroke(); 
        }
        
        for(var i = squareSize; i <= size - squareSize; i += squareSize) {
          for(var j = squareSize; j <= size - squareSize; j+= squareSize) {
            var plusOrMinus = Math.random() < 0.5 ? -1 : 1;
            var rotateAmt = j / size * Math.PI / 180 * plusOrMinus * Math.random() * rotateMultiplier;
        
            plusOrMinus = Math.random() < 0.5 ? -1 : 1;
            var translateAmt = j / size * plusOrMinus * Math.random() * randomDisplacement;
              
            context.save();
            context.translate(i + translateAmt + offset, j + offset);
            context.rotate(rotateAmt);
            draw(squareSize, squareSize);
            context.restore();
          }
        }


        """


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


art = classes = [AddCoords,
                 AndCoords,
                 ModCoords,
                 OrCoords,
                 PietMondrian,
                 SubCoordsYFromX,
                 XorCoords,
                 RecursiveQuads]
