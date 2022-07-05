import collections.abc
import typing
from random import shuffle
from itertools import accumulate
from bisect import bisect
from math import ceil, log, floor
from warnings import warn
from itertools import repeat

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

    def random(self, *args, **kwargs) -> float:
        raise NotImplementedError()

    """
    Seed The random number generator
    """

    def seed(self, a, *args, **kwargs):
        raise NotImplementedError()

    """
    Get a random integer in a range between (min, max)
    """

    def randint(self, low, high) -> int:
        return low + int(self.random() * (high - low))

    """
    Shuffle iterable. Uses the native random.shuffle with a lambda to self.random()
    """

    def shuffle(self, x):
        shuffle(x, random=self.random)

    """
    Taken from native implementation
    """

    def sample(self, population: collections.abc.Sequence, k: int, *, counts: list[int] = None) -> collections.abc.Sequence[typing.Any]:
        """Chooses k unique random elements from a population sequence or set.

        Returns a new list containing elements from the population while
        leaving the original population unchanged.  The resulting list is
        in selection order so that all sub-slices will also be valid random
        samples.  This allows raffle winners (the sample) to be partitioned
        into grand prize and second place winners (the subslices).

        Members of the population need not be hashable or unique.  If the
        population contains repeats, then each occurrence is a possible
        selection in the sample.

        Repeated elements can be specified one at a time or with the optional
        counts parameter.  For example:

            sample(['red', 'blue'], counts=[4, 2], k=5)

        is equivalent to:

            sample(['red', 'red', 'red', 'red', 'blue', 'blue'], k=5)

        To choose a sample from a range of integers, use range() for the
        population argument.  This is especially fast and space efficient
        for sampling from a large population:

            sample(range(10000000), 60)

        """
        if not isinstance(population, collections.abc.Sequence):
            raise TypeError("Population must be a sequence.  For dicts or sets, use sorted(d).")
        n = len(population)
        if counts is not None:
            cum_counts = list(accumulate(counts))
            if len(cum_counts) != n:
                raise ValueError('The number of counts does not match the population')
            total = cum_counts.pop()
            if not isinstance(total, int):
                raise TypeError('Counts must be integers')
            if total <= 0:
                raise ValueError('Total of counts must be greater than zero')
            selections = self.sample(range(total), k=k)

            return [population[bisect(cum_counts, s)] for s in selections]
        randbelow = self._randbelow
        if not 0 <= k <= n:
            raise ValueError("Sample larger than population or is negative")
        result = [None] * k
        setsize = 21  # size of a small set minus size of an empty list
        if k > 5:
            setsize += 4 ** ceil(log(k * 3, 4))  # table size for big sets
        if n <= setsize:
            # An n-length list is smaller than a k-length set.
            # Invariant:  non-selected at pool[0 : n-i]
            pool = list(population)
            for i in range(k):
                j = randbelow(n - i)
                result[i] = pool[j]
                pool[j] = pool[n - i - 1]  # move non-selected item into vacancy
        else:
            selected = set()
            selected_add = selected.add
            for i in range(k):
                j = randbelow(n)
                while j in selected:
                    j = randbelow(n)
                selected_add(j)
                result[i] = population[j]
        return result

    """
    Taken from native implementation
    """
    BPF = 53  # Number of bits in a float

    def _randbelow_without_getrandbits(self, n, maxsize=1 << BPF):
        """Return a random int in the range [0,n).  Returns 0 if n==0.

        The implementation does not use getrandbits, but only random.
        """

        random = self.random
        if n >= maxsize:
            warn("Underlying random() generator does not supply \n"
                 "enough bits to choose from a population range this large.\n"
                 "To remove the range limitation, add a getrandbits() method.")
            return floor(random() * n)
        if n == 0:
            return 0
        rem = maxsize % n
        limit = (maxsize - rem) / maxsize  # int(limit * maxsize) % n == 0
        r = random()
        while r >= limit:
            r = random()
        return floor(r * maxsize) % n

    _randbelow = _randbelow_without_getrandbits

    """
    Taken from native implementation
    """

    def choices(self, population: collections.abc.Sequence, weights=None, *, cum_weights=None, k=1) -> list[typing.Any]:

        """Return a k sized list of population elements chosen with replacement.

        If the relative weights or cumulative weights are not specified,
        the selections are made with equal probability.

        """
        random = self.random
        n = len(population)
        if cum_weights is None:
            if weights is None:
                n += 0.0  # convert to float for a small speed improvement
                return [population[floor(random() * n)] for _ in repeat(None, k)]
            cum_weights = list(accumulate(weights))
        elif weights is not None:
            raise TypeError('Cannot specify both weights and cumulative weights')
        if len(cum_weights) != n:
            raise ValueError('The number of weights does not match the population')
        total = cum_weights[-1] + 0.0  # convert to float
        if total <= 0.0:
            raise ValueError('Total of weights must be greater than zero')
        hi = n - 1
        return [population[bisect(cum_weights, random() * total, 0, hi)]
                for _ in repeat(None, k)]

    """
    Taken from native implementation
    """
    def choice(self, seq: collections.abc.Sequence) -> typing.Any:
        """Choose a random element from a non-empty sequence."""
        # raises IndexError if seq is empty
        return seq[self._randbelow(len(seq))]
