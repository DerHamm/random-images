from src.random_provider import Random
from string import printable, ascii_lowercase, ascii_uppercase, digits, punctuation
from inspect import signature


class RandomArguments(object):
    """ Pass the application random source into this """

    def __init__(self, random: Random):
        self.random = random

    def int(self):
        return IntArgument(self.random)

    def str(self):
        return StringArgument(self.random)

    def bool(self):
        return BoolArgument(self.random)

    def float(self):
        return FloatArgument(self.random)


class RandomArgument(object):
    """ Pass the application random source into this """

    def __init__(self, random: Random):
        self.random = random

    def build(self):
        raise NotImplementedError


class BoolArgument(RandomArgument):

    def __init__(self, random: Random):
        super().__init__(random)

    def build(self) -> ():
        return lambda: bool(self.random.randint(0, 1))


class FloatArgument(RandomArgument):
    def __init__(self, random: Random):
        super().__init__(random)
        self.__min = None
        self.__min_default = 0xFFFFFFFF
        self.__max = None
        self.__max_default = 0xFFFFFFFF

    def min(self, value):
        self.__min = value
        return self

    def max(self, value):
        self.__max = value
        return self

    def build(self) -> ():
        min_val = self.__min if self.__min is not None else self.__min_default
        max_val = self.__max if self.__max is not None else self.__max_default
        return lambda: self.random.randint(min_val, max_val)


class IntArgument(RandomArgument):
    def __init__(self, random: Random):
        super().__init__(random)
        self.__min = None
        self.__min_default = 0xFFFFFFFF
        self.__max = None
        self.__max_default = 0xFFFFFFFF

    def min(self, value):
        self.__min = value
        return self

    def max(self, value):
        self.__max = value
        return self

    def build(self) -> ():
        min_val = self.__min if self.__min is not None else self.__min_default
        max_val = self.__max if self.__max is not None else self.__max_default
        return lambda: self.random.randint(min_val, max_val)


class StringArgument(RandomArgument):
    def __init__(self, random: Random):
        super().__init__(random)
        self.__length = None
        self.__min = 0
        self.__max = 20
        self.source = {'lower': False,
                       'upper': False,
                       'digits': False,
                       'punctuation': False}
        self.__source = None
        self.__custom_source = None

    def __random_string(self, n, source):
        return ''.join([self.random.choice(source) for _ in range(n)])

    def printable(self):
        return self.lower().upper().punctuation().digits()

    def letters(self):
        return self.lower().upper()

    def lower(self):
        self.source['lower'] = True
        return self

    def upper(self):
        self.source['upper'] = True
        return self

    def punctuation(self):
        self.source['punctuation'] = True
        return self

    def digits(self):
        self.source['digits'] = True
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
            if self.source.get('upper'):
                source += ascii_uppercase
            if self.source.get('lower'):
                source += ascii_lowercase
            if self.source.get('punctuation'):
                source += punctuation
            if self.source.get('digits'):
                source += digits
        self.__source = source

    def build(self) -> ():
        def get(argument: StringArgument) -> str:
            if argument.__length is None:
                argument.__length = argument.random.randint(argument.__min, argument.__max)
            return argument.__random_string(argument.__length, argument.__source)

        self.__handle_source()

        return lambda: get(self)


# create random kwargs
def randomize(class_object, rng):
    sig = signature(class_object.__init__)
    res = dict()
    for param in sig.parameters.values():
        if param.annotation == str:
            res[param.name] = RandomArguments(rng).str().length(12).build()()
        elif param.annotation == int:
            res[param.name] = RandomArguments(rng).int().min(param.default // 2).max(param.default * 2).build()()
        elif param.annotation == float:
            res[param.name] = RandomArguments(rng).float().min(param.default / 2).max(param.default * 2).build()()
        elif param.annotation == bool:
            res[param.name] = RandomArguments(rng).bool().build()()
        else:
            pass
    return res
