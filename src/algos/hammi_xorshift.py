from time import time

from .util_random import handle_seed
from ..util.random_provider import Random


class XorRandom(Random):
    _max = 0xFFFFFFFF

    def __init__(self, seed=None) -> None:
        self.x = 123456789
        self.y = 362436069
        self.z = 521288629
        self.w = 88675123

        if seed is None:
            seed = 88675123 + int(time())

        # AND this so that a really huge seed value is being compressed to the fitting size
        val = handle_seed(seed) & XorRandom._max

        super().__init__()
        self.seed(val)

    def seed(self, a, *args, **kwargs)  -> None:
        val = handle_seed(a) & XorRandom._max

        self.x = 123456789
        self.y = 362436069
        self.z = 521288629
        self.w = val

    def random(self, *args, **kwargs) -> float:
        t = self.x ^ ((self.x << 11) & 0xFFFFFFFF)  # 32bit
        self.x, self.y, self.z = self.y, self.z, self.w
        self.w = self.w ^ (self.w >> 19) ^ (t ^ (t >> 8))

        # xor with the max value and right shift to 2
        # the xor again with y rshifted on the max of (x, z), which then again is lshifted on on the min of (x, z)
        self.w = (self.w ^ 0xFFFFFFFF >> 2) ^ (
            self.y >> max(self.z, self.x) << min(self.z, self.x)
        )
        return self.w / XorRandom._max
