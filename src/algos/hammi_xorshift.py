from ..random_provider import Random
from time import time
from hashlib import md5


class XorRandom(Random):
    _max = 0xFFFFFFFF

    @staticmethod
    def _handle_seed(seed):
        # make *anything* to md5 seed and then convert that seed to int
        def md5_to_int(h):
            return abs(int.from_bytes(h.digest(), 'big'))

        class SeedException(Exception):
            pass

        if isinstance(seed, (int, float)):
            return md5_to_int(md5(str(seed).encode()))
        elif isinstance(seed, str):
            return md5_to_int(md5(seed.encode()))
        elif isinstance(seed, bytes):
            return md5_to_int(md5(seed))
        else:
            raise SeedException("Invalid seed {}".format(seed))

    def __init__(self, seed=None):
        self.x = 123456789
        self.y = 362436069
        self.z = 521288629
        self.w = 88675123

        if seed is None:
            seed = 88675123 + int(time())

        val = (self._handle_seed(seed) & XorRandom._max)

        super().__init__()
        self.seed(val)


    def seed(self, a, *args, **kwargs):
        val = (self._handle_seed(a) & XorRandom._max)

        self.x = 123456789
        self.y = 362436069
        self.z = 521288629
        self.w = val

    def random(self, *args, **kwargs):
        t = self.x ^ ((self.x << 11) & 0xFFFFFFFF)  # 32bit
        self.x, self.y, self.z = self.y, self.z, self.w
        self.w = (self.w ^ (self.w >> 19) ^ (t ^ (t >> 8)))

        # xor with the max value and right shift to 2
        # the xor again with y rshifted on the max of (x, z), which then again is lshifted on on the min of (x, z)
        self.w = (self.w ^ 0xFFFFFFFF >> 2) ^ (self.y >> max(self.z, self.x) << min(self.z, self.x))

        return self.w / XorRandom._max


# example of basic xorshift 128-bit
def xorshift128():
    """xorshift
    https://ja.wikipedia.org/wiki/Xorshift
    """

    x = 123456789
    y = 362436069
    z = 521288629
    w = 88675123

    def _random():
        nonlocal x, y, z, w
        t = x ^ ((x << 11) & 0xFFFFFFFF)  # 32bit
        x, y, z = y, z, w
        w = (w ^ (w >> 19)) ^ (t ^ (t >> 8))
        return w

    return _random


"""
OLD IMPLS

class XorRandom(Random):
    _max = 0xFFFFFFFF

    def __init__(self):
        super().__init__()
        self._random = xorshift()

    def seed(self, a, *args, **kwargs):
        val = (abs(int.from_bytes(a, 'big')) & XorRandom._max)
        _random = xorshift(val)

    def random(self, *args, **kwargs):
        return self._random() / XorRandom._max


def xorshift(seed=None):
    '''xorshift
    https://en.wikipedia.org/wiki/Xorshift
    '''

    if seed is None:
        seed = 88675123
    x = 123456789
    y = 362436069
    z = 521288629
    # w = 88675123
    w = seed

    def _random():
        nonlocal x, y, z, w
        t = x ^ ((x << 11) & 0xFFFFFFFF)  # 32bit
        x, y, z = y, z, w
        w = (w ^ (w >> 19) ^ (t ^ (t >> 8)))

        # xor with the max value and right shift to 2
        # the xor again with y rshifted on the max of (x, z), which then again is lshifted on on the min of (x, z)
        w = (w ^ 0xFFFFFFFF >> 2) ^ (y >> max(z, x) << min(z, x))
        return w

    return _random

"""
