from PIL import ImageDraw
from PIL import Image
from src.pixel_iterator_strategies.strategies import XorRandom
# instead of learning the whole mathematical concept behind colors and color schemes, let's just use a library for
# my sanity's sake for now
import seaborn as sns

# TODO: Implement a PCG instead of XorShift for further experimentation
# TODO: Update the project's README
# TODO: Create a UnitTest-Suite based around the RandomProvider class and find a way to test all algos with that class
# TODO: Accept command line args here and start doing stuff
# Options to consider:
"""
- Run Big Crush / Small Crush / Diehard / Whatever Tests
- Run tests (there are no tests.. yet. but no srsly, we need some tests for the random provider, to assure, that
 all the algos we are going to implement are actually correct)
- Generate Image (w and w/o seed)
- Generate Test Data (length, algo_used) (This is probably obsolete because the test frameworks accept streams)
"""

IMAGE_SIZE = (1280, 720)
random = XorRandom()
random.seed("piet_mondrian")


# IMAGE_SIZE = (1920, 1280)


# TODO: Approach is trash as we don't have to iterate over every pixel when plotting shapes
# TODO: Alternative: Make the range in execute variable, but with what? Who tells how many iterations?
class ImageView(object):
    def __init__(self, strategy, cycler):
        self.impl = strategy
        self.image = Image.new('RGB', IMAGE_SIZE, "white")
        self.pixels = self.image.load()

        self.cycler = cycler

    def execute(self):
        for i in range(self.image.size[0]):
            [self.impl.execute(self.pixels, self.cycler, i, j, self.image) for j in range(self.image.size[1])]

    def show(self):
        self.execute()
        self.image.show()


def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


"""
Color Palettes 
'Perceptually Uniform Sequential'
['viridis', 'plasma', 'inferno', 'magma', 'cividis']

('Sequential'
['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds','YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu','GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']

'Sequential (2)
['binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink','spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia','hot', 'afmhot', 'gist_heat', 'copper']

'Diverging'
['PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu','RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']

'Cyclic'
['twilight', 'twilight_shifted', 'hsv'])

'Qualitative'
['Pastel1', 'Pastel2', 'Paired', 'Accent','Dark2', 'Set1', 'Set2', 'Set3','tab10', 'tab20', 'tab20b', 'tab20c']),

'Miscellaneous'
['flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern','gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg','gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral','gist_ncar']
"""
COLOR_PALETTE_NAMES = ['viridis', 'plasma', 'inferno', 'magma', 'cividis'] + \
                      ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds', 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd',
                       'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn'] + \
                      ['binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink', 'spring', 'summer', 'autumn',
                       'winter', 'cool', 'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper'] + \
                      ['PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm',
                       'bwr', 'seismic'] + \
                      ['twilight', 'twilight_shifted', 'hsv'] + \
                      ['Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2', 'Set1', 'Set2', 'Set3', 'tab10', 'tab20',
                       'tab20b', 'tab20c'] + \
                      ['flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap',
                       'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral', 'gist_ncar']


def random_palette():
    return COLOR_PALETTE_NAMES[random.randint(0, len(COLOR_PALETTE_NAMES) - 1)]


"""
Test the generation of an image
"""


def main():
    color_palette = sns.color_palette(random_palette(), 16).as_hex()

    # TODO: Find a way to determine what the "white" of this palette is and use it as background
    # Should be more pleasing than just using some "whitey" color
    back_color = (random.randint(240, 255), random.randint(240, 255), random.randint(240, 255))

    # TODO: Stop being too lazy for it and implement choice and samples and choices in the random_provider API so that
    # we can remove this and other "random_" functions
    def random_color_from_palette(palette):
        return palette[random.randint(0, len(palette) - 1)]

    def rand_color():
        return random_color_from_palette(color_palette)

    w, h = IMAGE_SIZE[0], IMAGE_SIZE[1]

    # iterations for the splitting loop
    subdivisions = 50000

    # minimum size for a single rectangle
    # if this is too small, weird stuff happens
    min_diff = 80

    # spacing between rectangles
    sep = 1

    # Piet Mondrian Color Palette = (38, 71, 124), (240, 217, 92), (162, 45, 40) + (223, 224, 236)
    # Subdivision adjustment
    # Determines the ratio of the split on a rectangle. Using other split values might result in funny/unexpected stuff
    splits = [.5, 1, 1.5]

    # Border thiccness
    edge = 10

    img = Image.new('RGB', (w, h), (255 - 223, 255 - 224, 255 - 236))
    draw = ImageDraw.Draw(img)

    rectangles = list()
    # Add the initial rectangle
    rectangles.append([(edge, edge), (w - edge, edge), (w - edge, h - edge), (edge, h - edge)])

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
        # fill_colors = colors[int(random.randint(0, len(colors)))]
        if random.random() > 0.8:
            fill_colors = rand_color()
        else:
            fill_colors = back_color

        # we only need 2 points for the draw
        rect = rect[0] + rect[2]
        draw.rectangle(rect, fill=fill_colors, width=1)

    img.show()

    """
    strats = [RandomColorsPercentagePattern()]
    address = Address(2)
    rand_bytes = list(address().address)
    random_cycler = itertools.cycle(rand_bytes)

    for strategy in strats:
        view = ImageView(strategy, random_cycler)
        view.show()
    """


if __name__ == '__main__':
    main()
