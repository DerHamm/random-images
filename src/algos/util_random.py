from time import time
from hashlib import md5

__all__ = ['handle_seed', 'SeedException']


def handle_seed(seed):
    """
    Get a md5 hash of seed values of common simple data types.
    Uses Big endian to convert md5 hashes to integer values afterwards
    """
    if seed is None:
        seed = 88675123 + int(time())

    if isinstance(seed, (int, float)):
        return md5_to_int(md5(str(seed).encode()))
    elif isinstance(seed, str):
        return md5_to_int(md5(seed.encode()))
    elif isinstance(seed, bytes):
        return md5_to_int(md5(seed))
    else:
        raise SeedException("Invalid seed {}".format(seed))


def md5_to_int(h):
    """
    Return the big endian integer version of some md5 hash
    """
    return abs(int.from_bytes(h.digest(), 'big'))


class SeedException(Exception):
    """ Used for any errors in the seed handling """
    pass
