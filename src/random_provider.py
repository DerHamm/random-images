from random import shuffle

"""
Simple interface for providing random numbers.
Also the concrete implementation of native random and hamm-random

The interface has the following contract: In the __init__, you will have to provide two
things two the PRNG: The random()-function and the seed()-function

How those will be passed and implemented if completely up to the implementation.
The important thing however, is, that the seed has to be corresponding to the randomness.
This will not magically work, when you use the seed of some third-party-xorshift to be used in combination
with the native Marsenne Twister random()-function.

As seed()-functions sometimes take more than one argument, the seed function is declared to accept *args and **kwargs 
"""


class Random(object):
    """
    Use the __init__ to set the PRNG
    """

    def __init__(self, *args, **kwargs):
        _random = None

    """
    Returns a number in the interval [0..1]
    """

    def random(self, *args, **kwargs):
        raise NotImplementedError()

    """
    Seed The random number generator
    """

    def seed(self, a, *args, **kwargs):
        raise NotImplementedError()

    """
    Get a random integer in a range between (max, min)
    """
    def randint(self, low, high):
        return low + int(self.random() * (high - low))

    """
    Shuffle iterable. Uses the native random.shuffle with a lambda to self.random()
    """
    def shuffle(self, x):
        shuffle(x, random=self.random)

