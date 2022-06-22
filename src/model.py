from src.algos.hammi_xorshift import XorRandom as Random
from hashlib import md5

random = Random()

"""
The image we want to generate is actually a container holding multiple images (or "patterns" in the further context).
By defining the SIZE field of image as 16, we tell the class to generate an Image, that is 16x16 patterns large.

A pattern is defined almost the same. It uses the same size field for now. The pattern ist just 16x16 pixels in B/W.

The colors then, are coming from the Pixels. Each pixel has it's own seed and will generate it's own color, but only
if it is black. White pixels will simply be ignored. As a final step, we swap white with a random color based on the
the image seed, which will be the Images 'theme'. 
"""


class RandomImage(object):
    SIZE = 16

    def __init__(self, seed):
        self.seed = md5(seed.encode()).digest()
        random.seed(self.seed, version=1)
        self.theme = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.patterns = [RandomImage.Pattern(self.seed) for _ in range(RandomImage.SIZE)]

    class Pattern(object):
        def __init__(self, parent_seed):
            self.parent_seed = parent_seed

            r = random.random()
            self.seed = md5(str(r).encode()).digest()

            random.seed(self.seed, version=1)
            self.pixels = [RandomImage.Pixel(self.seed) for _ in range(RandomImage.SIZE)]

    class Pixel(object):
        def __init__(self, parent_seed):
            r = str(random.random())
            self.seed = md5(r.encode()).digest()
            self.parent_seed = parent_seed


class Pattern(object):
    def draw(self, *args, **kwargs):
        raise NotImplementedError()



