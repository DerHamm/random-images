from src.algos.hammi_xorshift import XorRandom
from src.pixel_iterator_strategies.interface import PixelIteratorStrategy
import random


class RandomColorsPercentageBase(PixelIteratorStrategy):
    chance = 0.5
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


class RandomColorsPercentagePattern(RandomColorsPercentageBase):
    xor_random = XorRandom()
    random_call = xor_random.random
    random_seed_call = xor_random.seed

    def __init__(self):
        self.theme = None
        self.colors_set = False

    def get_theme(self):
        if self.theme is None:
            r = [self.xor_random.randint(0, 255), self.xor_random.randint(0, 255), self.xor_random.randint(0, 255)]
            self.xor_random.shuffle(r)
            self.theme = tuple(r)
        return self.theme

    def set_colors(self):
        if not self.colors_set:
            self.red_color_low = self.xor_random.randint(0, 255)
            self.red_color_high = self.xor_random.randint(min(256, self.red_color_low + 1), 255)

            self.green_color_low = self.red_color_low
            self.green_color_high = self.red_color_high

            self.blue_color_low = self.red_color_low
            self.blue_color_high = self.red_color_high
            self.colors_set = True

    def execute(self, data, c, x, y):

        val = x ^ y

        self.random_seed_call(val)
        self.set_colors()
        r = self.xor_random.randint(self.red_color_low, self.red_color_high)
        g = self.xor_random.randint(self.green_color_low, self.green_color_high)
        b = self.xor_random.randint(self.blue_color_low, self.blue_color_high)

        if self.random_call() > .5:
            data[x, y] = (r, g, b)
        else:
            data[x, y] = self.get_theme()
