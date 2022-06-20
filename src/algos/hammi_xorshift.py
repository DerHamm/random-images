from ..random_provider import Random
from time import time
from hashlib import md5


class XorRandom(Random):
    _max = 0xFFFFFFFF

    @staticmethod
    def _handle_seed(seed):
        if seed is None:
            seed = 88675123 + int(time())

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

        # AND this so that a really huge seed value is being compressed to the fitting size
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
