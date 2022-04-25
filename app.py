import itertools
from typing import NamedTuple
import random
from PIL import Image
from Crypto.Hash import keccak
from coincurve import PublicKey
from hashlib import md5
from src.algos.hammi_xorshift import XorRandom
from src.model import RandomImage


# TODO: find out how to seed that shit / a general way of how to seed RNGs
# -> Looks like we did it
# TODO: setup file(s) for random number generators
# TODO: create interface for random number generator with the default Mersenne twister from native python as default
# -> How can we assure that the Mersenne Twister is actually used?
# TODO: push the RNG part of your project to Github, maybe even make a separate project?
# TODO: Create a UnitTest-Suite based around the RandomProvider class and find a way to test all algos with that class
# TODO: Accept command line args here and start doing stuff
# Options to consider:
"""
- Generate Test Data (length, algo_used)
- Run Diehard Tests (WSL->dieharder->extract report to this project)
- Run tests (there are no tests.. yet. but no srsly, we need some tests for the random provider, to assure, that
 all the algos we are going to implement are actually correct)
- Generate Image (seed)
-
"""

IMAGE_SIZE = (256, 256)


#IMAGE_SIZE = (1920, 1280)


class Address:
    _gen = None
    _address = NamedTuple("Address", [("private_key", bytes), ("public_key", bytes), ("address", bytes)])
    _start = 32

    def __init__(self, start=0):
        Address._start = start

    @staticmethod
    def address_generator():
        for index in range(0x0, 0xffffffffffffffffffffffffffffffffffffffff, 1):
            kek = keccak.new(digest_bits=256)
            seed = bytes(Address._start + index)
            private_key = kek.update(seed).digest()
            public_key = PublicKey.from_valid_secret(private_key).format(compressed=False)[1:]
            address_kek = keccak.new(digest_bits=256)
            print(private_key.hex())
            # print(public_key.hex())

            addr = address_kek.update(public_key).digest()[-20:]
            print(addr.hex())
            yield Address._address(private_key=private_key, public_key=public_key, address=addr)

    def __call__(self, *args, **kwargs):
        if Address._gen is None:
            Address._gen = Address.address_generator()
        return next(Address._gen)


class ImageView(object):
    def __init__(self, strategy, cycler):
        self.impl = strategy
        self.image = Image.new('RGB', IMAGE_SIZE, "black")
        self.pixels = self.image.load()

        self.cycler = cycler

    def execute(self):
        for i in range(self.image.size[0]):
            [self.impl.execute(self.pixels, self.cycler, i, j) for j in range(self.image.size[1])]

    def show(self):
        self.execute()
        self.image.show()


class IStrategy(object):
    # data: pixel data to manipulate, indexed with data[x, y]
    # c: generator yielding random values, use with next, assume it can't be exhausted
    # x: current x coordinate
    # y: current y coordinate
    def execute(self, data, c, x, y):
        pass


class RandomColorsPercentageBase(IStrategy):
    chance = 0.24
    random_call = random.random
    random_seed_call = random.seed

    red_color_high = 255
    red_color_low = 0
    red_chance = chance

    green_color_high = 255
    green_color_low = 0
    green_chance = chance

    blue_color_high = 255
    blue_color_low = 0
    blue_chance = chance

    def execute(self, data, c, x, y):
        random.seed(next(c))
        r = random.randint(self.red_color_low, self.red_color_high)
        g = random.randint(self.green_color_low, self.green_color_high)
        b = random.randint(self.blue_color_low, self.blue_color_high)

        if self.random_call() > self.red_chance:
            r = self.red_color_high
        elif self.random_call() > self.red_chance:
            r = self.red_color_low

        if self.random_call() > self.green_chance:
            g = self.green_color_high
        elif self.random_call() > self.green_chance:
            g = self.green_color_low

        if self.random_call() > self.blue_chance:
            b = self.blue_color_high
        elif self.random_call() > self.blue_chance:
            b = self.blue_color_low

        data[x, y] = (r, g, b)


xorry = XorRandom()


class RandomColorsPercentagePattern(RandomColorsPercentageBase):
    random_call = xorry.random
    random_seed_call = xorry.seed

    def __init__(self):
        self.theme = None
        self.colors_set = False

    def get_theme(self):
        if self.theme is None:
            r = [xorry.randint(0, 255), xorry.randint(0, 255), xorry.randint(0, 255)]
            xorry.shuffle(r)
            self.theme = tuple(r)
        return self.theme

    def set_colors(self):
        if not self.colors_set:
            self.red_color_low = xorry.randint(0, 255)
            self.red_color_high = xorry.randint(min(256, self.red_color_low + 1), 255)

            self.green_color_low = self.red_color_low
            self.green_color_high = self.red_color_high

            self.blue_color_low = self.red_color_low
            self.blue_color_high = self.red_color_high
            self.colors_set = True


    def execute(self, data, c, x, y):
        #val = x ^ y ^ (x + y)
        val = x ^ y
        self.random_seed_call(val)
        self.set_colors()
        r = xorry.randint(self.red_color_low, self.red_color_high)
        g = xorry.randint(self.green_color_low, self.green_color_high)
        b = xorry.randint(self.blue_color_low, self.blue_color_high)

        if self.random_call() > .5:
            data[x, y] = (r, g, b)
        else:
            data[x, y] = self.get_theme()


"""
Test the generation of an image
"""


def main2():
    # USED_STRATEGY = RandomColorsPercentagePattern()
    strats = [RandomColorsPercentagePattern()]
    address = Address(2)
    rand_bytes = list(address().address)
    random_cycler = itertools.cycle(rand_bytes)

    for strategy in strats:
        view = ImageView(strategy, random_cycler)
        view.show()


"""
Hamm-Xorshift implementation testing
"""

"""
def main1():
    x = XorRandom()
    x.seed(md5(__name__.encode()).digest())
    xx = XorRandom()
    xx.seed(md5("YEEES YEEESE YYYYYYYYYYYYYYYYYEEEEEEEEEEEES".encode()).digest())

    xxx = XorRandom()

    print(x.random())
    print(xx.random())
    print(xxx.random())
"""

"""
Testing the object model and procedural generation
"""

"""
def main3():
    img = RandomImage("XXXQ=§)MMKMFASPMDPASMDPXX")
    seeds = list()
    for pattern in img.patterns:
        print(hex(int.from_bytes(pattern.seed, 'big')))
        seeds.append(pattern.seed)
        for pixel in pattern.pixels:
            seeds.append(pixel.seed)
"""

if __name__ == '__main__':
    main2()
