import random
from ..util.random_provider import Random

"""
Use the native Python randomness. Note: random.seed has to be called with version=1 to ensure, that
the Mersenne Twister is being used. Otherwise the platform dependant default implementation from the OS will be used
(which in our case, would suck)
"""


class NativeRandom(Random):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        # Seed native PRNG using the native Mersenne Twister implementation rather than SystemDefault
        random.seed(version=1)
        self._seed = random.seed
        self._random = random.random

    def random(self) -> float:
        return self._random()

    def seed(self, *args, **kwargs) -> None:
        self._seed(*args, **kwargs)
