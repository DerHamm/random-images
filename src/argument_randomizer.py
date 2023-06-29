import typing

from string import printable, ascii_lowercase, ascii_uppercase, digits, punctuation
from inspect import signature, Parameter

from .random_provider import Random


class RandomArgument(object):
    """Pass the application random source into this"""

    def __init__(self, random: Random):
        self.random = random

    def build(self):
        raise NotImplementedError


class BoolArgument(RandomArgument):
    def __init__(self, random: Random):
        super().__init__(random)

    def build(self) -> typing.Callable:
        return lambda: self.random.random() > 0.5


class BytesArgument(RandomArgument):
    def __init__(self, random: Random):
        super().__init__(random)

        self.__min = None
        self.__min_default = 0
        self.__max = None
        self.__max_default = 0xFFFFFFFF

    def min(self, value):
        self.__min = value
        return self

    def max(self, value):
        self.__max = value
        return self

    def build(self) -> typing.Callable:
        min_val = self.__min if self.__min is not None else self.__min_default
        max_val = self.__max if self.__max is not None else self.__max_default

        def get():
            return bytes(self.random.randint(min_val, max_val))

        return get


class FloatArgument(RandomArgument):
    def __init__(self, random: Random):
        super().__init__(random)
        self.__min = None
        self.__min_default = 0
        self.__max = None
        self.__max_default = 0xFFFFFFFF

    def min(self, value):
        self.__min = value
        return self

    def max(self, value):
        self.__max = value
        return self

    def build(self) -> typing.Callable:
        min_val = self.__min if self.__min is not None else self.__min_default
        max_val = self.__max if self.__max is not None else self.__max_default

        def get():
            return min_val + self.random.random() * (max_val - min_val)

        return get


class IntArgument(RandomArgument):
    def __init__(self, random: Random):
        super().__init__(random)
        self.__min = None
        self.__min_default = 0
        self.__max = None
        self.__max_default = 0xFFFFFFFF

    def min(self, value):
        self.__min = value
        return self

    def max(self, value):
        self.__max = value
        return self

    def build(self) -> typing.Callable:
        min_val = self.__min if self.__min is not None else self.__min_default
        max_val = self.__max if self.__max is not None else self.__max_default

        def get():
            return self.random.randint(min_val, max_val)

        return get


class StringArgument(RandomArgument):
    def __init__(self, random: Random):
        super().__init__(random)
        self.__length = None
        self.__min = 0
        self.__max = 20
        self.source = {
            "lower": False,
            "upper": False,
            "digits": False,
            "punctuation": False,
        }
        self.__source = None
        self.__custom_source = None

    def __random_string(self, n, source):
        return "".join([self.random.choice(source) for _ in range(n)])

    def printable(self):
        return self.lower().upper().punctuation().digits()

    def letters(self):
        return self.lower().upper()

    def lower(self):
        self.source["lower"] = True
        return self

    def upper(self):
        self.source["upper"] = True
        return self

    def punctuation(self):
        self.source["punctuation"] = True
        return self

    def digits(self):
        self.source["digits"] = True
        return self

    def custom_source(self, value):
        self.__custom_source = value
        return self

    def length(self, value):
        self.__length = value
        return self

    def min(self, value):
        self.__min = value
        return self

    def max(self, value):
        self.__max = value
        return self

    def __handle_source(self):
        source = str()

        if self.__custom_source is not None:
            source = self.__custom_source
        elif sum(self.source.values()) not in [4, 0]:
            source = printable
        else:
            if self.source.get("upper"):
                source += ascii_uppercase
            if self.source.get("lower"):
                source += ascii_lowercase
            if self.source.get("punctuation"):
                source += punctuation
            if self.source.get("digits"):
                source += digits
        if not source:
            source = ascii_lowercase + digits
        self.__source = source

    def build(self) -> typing.Callable:
        def get() -> str:
            if self.__length is None:
                self.__length = self.random.randint(self.__min, self.__max)
            return self.__random_string(self.__length, self.__source)

        self.__handle_source()

        return get


# wip, just an experiment rn
def find_argument(t):
    return {
        str: StringArgument,
        int: IntArgument,
        float: FloatArgument,
        bytes: BytesArgument,
        bool: BoolArgument,
        list: ListArgument,
    }.get(t)


class CollectionArgument(RandomArgument):
    DEFAULT_TYPE = int

    def __init__(self, random: Random, collection_type):
        super().__init__(random)
        self.__collection_type = collection_type
        self._len = 5
        self._types = {}

    def len(self, n):
        self._len = n
        return self

    def type(self, t):
        self._types[t] = find_argument(t)
        return self

    def add_to_collection(self, collection, param):
        raise NotImplementedError

    def _build_with_comprehension(self, param):
        raise NotImplementedError

    def build(self) -> typing.Callable:
        if len(self._types) == 0:
            self._types[CollectionArgument.DEFAULT_TYPE] = find_argument(
                CollectionArgument.DEFAULT_TYPE
            )

        def get() -> typing.Any:
            args = {
                t: function(self.random).build() for t, function in self._types.items()
            }
            return self._build_with_comprehension(list(args.values()))

        return get


class ListArgument(CollectionArgument):
    def __init__(self, random: Random):
        super().__init__(random, list)

    def _build_with_comprehension(self, functions):
        return [self.random.choice(functions)() for _ in range(self._len)]

    def add_to_collection(self, collection, param):
        collection.append(param)


class TupleArgument(CollectionArgument):
    def __init__(self, random: Random):
        super().__init__(random, tuple)

    def _build_with_comprehension(self, functions):
        return (self.random.choice(functions)() for _ in range(self._len))

    def add_to_collection(self, collection, param):
        return collection + (param,)


class SetArgument(CollectionArgument):
    def __init__(self, random: Random):
        super().__init__(random, set)

    def _build_with_comprehension(self, functions):
        return {self.random.choice(functions)() for _ in range(self._len)}

    def add_to_collection(self, collection, param):
        collection.add(param)
        return collection


class DictArgument(CollectionArgument):
    class KeyArgument(RandomArgument):
        def __init__(self, random: Random):
            super().__init__(random)

        def build(self):
            pass

    class ValueArgument(RandomArgument):
        def __init__(self, random: Random):
            super().__init__(random)

        def build(self):
            pass

    def __init__(self, random: Random):
        super().__init__(random, set)
        self.__string_generator = StringArgument(self.random).min(4).max(8).build()
        self.__key_types = dict()
        self.__value_types = dict()

    def build(self) -> typing.Callable:
        if len(self._types) + len(self.__key_types) + len(self.__value_types) == 0:
            raise TypeError("No types were given for the generator")

        def get() -> typing.Any:
            if len(self.__key_types) == 0 or len(self.__value_types) == 0:
                used_key_types = self._types
                used_value_types = self._types
            else:
                used_key_types = self.__key_types
                used_value_types = self.__value_types

            key_args = {
                t: function(self.random).build()
                for t, function in used_key_types.items()
            }
            value_args = {
                t: function(self.random).build()
                for t, function in used_value_types.items()
            }

            result = self._build_with_comprehension(
                [list(key_args.values()), list(value_args.values())]
            )
            return result

        return get

    def _build_with_comprehension(self, functions):
        key_args = functions[0]
        value_args = functions[1]

        return {
            self.random.choice(key_args)(): self.random.choice(value_args)()
            for _ in range(self._len)
        }

    def add_to_collection(self, collection, param):
        collection[self.__string_generator()] = param
        return collection

    def key_type(self, t):
        self.__key_types[t] = find_argument(t)
        return self

    def value_type(self, t):
        self.__value_types[t] = find_argument(t)
        return self


class RandomArguments(object):
    """Pass the application random source into this"""

    def __init__(self, random: Random):
        self.random = random

    def int(self) -> IntArgument:
        return IntArgument(self.random)

    def str(self) -> StringArgument:
        return StringArgument(self.random)

    def bool(self) -> BoolArgument:
        return BoolArgument(self.random)

    def float(self) -> FloatArgument:
        return FloatArgument(self.random)

    def bytes(self) -> BytesArgument:
        return BytesArgument(self.random)

    def list(self) -> ListArgument:
        return ListArgument(self.random)

    def tuple(self) -> TupleArgument:
        return TupleArgument(self.random)

    def set(self) -> SetArgument:
        return SetArgument(self.random)

    def dict(self) -> DictArgument:
        return DictArgument(self.random)


def create_random_argument_map(class_object: type, rng: Random):
    sig = signature(class_object.__init__)
    parameters = sig.parameters
    arguments = {}

    for name, param in parameters.items():
        if param.default != Parameter.empty:
            arguments[name] = param.default

    res = dict()
    random_arguments = RandomArguments(rng)

    for param in sig.parameters.values():
        if param.name not in arguments.keys():
            continue
        if param.annotation == str:
            res[param.name] = random_arguments.str().length(12).build()
        elif param.annotation == int:
            res[param.name] = (
                random_arguments.int()
                .min(param.default // 2)
                .max(param.default * 2)
                .build()
            )
        elif param.annotation == float:
            res[param.name] = (
                random_arguments.float()
                .min(param.default / 2)
                .max(param.default * 2)
                .build()
            )
        elif param.annotation == bool:
            res[param.name] = random_arguments.bool().build()
        elif param.annotation == bytes:
            res[param.name] = random_arguments.bytes().min(0).max(32).build()
        elif param.annotation == list:
            res[param.name] = random_arguments.list().len(32).build()
        elif param.annotation == tuple:
            res[param.name] = random_arguments.tuple().len(32).build()
        elif param.annotation == set:
            res[param.name] = random_arguments.set().len(32).build()
        elif param.annotation == dict:
            res[param.name] = (
                random_arguments.dict().len(16).type(str).type(int).type(float).build()
            )
    return res
