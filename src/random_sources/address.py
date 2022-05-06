from typing import NamedTuple
from Crypto.Hash import keccak
from coincurve import PublicKey


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
