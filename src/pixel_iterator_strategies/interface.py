"""
This interface serves the purpose of iterating over each individual pixel for plotting an Image.
You have to pass the pixel data as well as a random source (used with next(), assuming it can't be exhausted) and the
current X and Y coordinates you want to edit.
ImageView will call this classes execute methode for generating images.

It is *extremely* slow. Images larger than 256*256px may take a while to generate.
"""


class PixelIteratorStrategy(object):
    # data: pixel data to manipulate, indexed with data[x, y]
    # c: generator yielding random values, use with next, assume it can't be exhausted
    # x: current x coordinate
    # y: current y coordinate
    def execute(self, data, c, x, y):
        raise NotImplementedError()
