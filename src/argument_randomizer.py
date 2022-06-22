from src.random_provider import Random
from string import printable, ascii_lowercase, ascii_uppercase, digits, punctuation


class RandomArguments(object):
    """ Pass the application random source into this """

    def __init__(self, random: Random):
        self.random = random

    def int(self):
        return IntArgument(self.random)

    def str(self):
        return StringArgument(self.random)


class RandomArgument(object):
    """ Pass the application random source into this """

    def __init__(self, random: Random):
        self.random = random


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

    def build(self):
        result = self.random.randint(self.__min if self.__min is not None else self.__min_default,
                                     self.__max if self.__max is not None else self.__max_default)
        return result


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

    def build(self):
        def get(argument: StringArgument):
            if argument.__length is None:
                argument.__length = argument.random.randint(argument.__min, argument.__max)
            return argument.__random_string(argument.__length, argument.__source)

        self.__handle_source()

        return lambda: get(self)
