from src.random_provider import Random
from time import time
from src.algos.util_random import handle_seed
from itertools import cycle


class CollatzConjectureRandom(Random):
    """ Experimental generator based on the collatz conjecture """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max = 0xFFFF
        self.__seq = None
        self.__origin = None
        s = kwargs.get('seed')
        if s is None:
            s = time()
        self.seed(s)

    def random(self, *args, **kwargs):
        x = next(self.__seq) & self.max
        return x / self.max

    def seed(self, a, *args, **kwargs):
        val = handle_seed(a)
        self.__origin = val
        self.__seq = cycle(CollatzConjectureRandom.__collatz(val))

    @staticmethod
    def __collatz(n):
        """ Recursively iterate over the given collatz sequence,
            Finally, return a tuple of the resulting sequence """
        result = tuple()
        while n != 1:
            if n % 2 != 0:
                n = 3 * n + 1
            else:
                n = n // 2
            result += (n,)
        return result

