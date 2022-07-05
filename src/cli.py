import argparse
import collections.abc
import time
import uuid

import src.random_provider
from src.algos.hammi_xorshift import XorRandom
from src.algos.native_random import NativeRandom
from src.algos.collatz_conjecture import CollatzConjectureRandom
from src.artworks import art, DummyPlot
from pathlib import Path
from src.logger import get_logger
from src.argument_randomizer import create_random_argument_map
from typing import Union, Optional


LOGGER = get_logger(__name__)


class Arguments(object):
    def __init__(self):
        """ Generate an image """
        self.generate = None
        """ Generate a gallery of images """
        self.gallery = None
        """ Run the BigCrush Test Suite """
        self.crush = None
        """ Run the DieHard Test Suite """
        self.test = None
        """ Random generator used """
        self.generator = None
        """ The random seed """
        self.seed = None
        """ Indicates if the generated images should be displayed """
        self.show = None
        """ All the artwork classes to be used for the gallery  """
        self.artworks = None
        """ Path for the image to be stored at """
        self.output = None

        # those are lists, but we want to handle those as single values, so properties are created
        """ The artwork class to be used """
        self._artwork = None
        """ Count of artworks to be generated """
        self._count = None

    @property
    def count(self) -> int:
        return self._count[0]

    @count.setter
    def count(self, value: int):
        self._count = value

    @property
    def artwork(self) -> str:
        return self._artwork[0]

    @artwork.setter
    def artwork(self, value: str):
        self._artwork = value


class CommandlineRunner(object):
    """ Pass sys.argv into this"""

    def __init__(self, *args):
        parser = argparse.ArgumentParser(description='Random Images CLI', exit_on_error=False)

        subparsers = parser.add_subparsers()

        generate_parser = Generator.add_arguments(subparsers.add_parser('generate', help='Generate some artwork'))
        generate_parser.set_defaults(generate=self.generate)

        gallery_parser = Gallery.add_arguments(
            subparsers.add_parser('gallery', help='Generate a whole gallery of artworks'))
        gallery_parser.set_defaults(gallery=self.gallery)

        test_parser = subparsers.add_parser('test', help='Run the die hard test suite')
        test_parser.set_defaults(test=self.test)

        crush_parser = subparsers.add_parser('crush', help='Run the Big Crush test')
        crush_parser.set_defaults(crush=self.crush)

        self.arguments = Arguments()
        parser.parse_args(args, namespace=self.arguments)

        self.parser = parser

    def run(self):
        if self.arguments.generate:
            self.generate()
        elif self.arguments.gallery:
            self.gallery()
        elif self.arguments.test:
            self.test()
        elif self.arguments.crush:
            self.crush()
        else:
            self.help()

    def generate(self):
        return Generator(self.arguments).execute()

    def help(self):
        self.parser.print_help()

    def gallery(self):
        return Gallery(self.arguments).execute()

    def test(self):
        raise NotImplementedError('Tests are not implemented yet')

    def crush(self):
        raise NotImplementedError('Tests are not implemented yet')


class Command(object):
    def __init__(self, arguments: Arguments):
        self.arguments = arguments

    @staticmethod
    def add_arguments(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError


# Executes the generate command
class Generator(Command):

    def execute(self):
        """ Run the generate command to output an image """
        random = GeneratorUtils.get_random_number_generator(self)
        save_path = GeneratorUtils.get_save_path(self) / (str(uuid.uuid4()) + ".png")
        self.arguments.count = [1]
        artworks = GeneratorUtils.create_argument_function_mapping(self, random)
        GeneratorUtils.draw_artworks(artworks, self, random, save_path)

    @staticmethod
    def add_arguments(parser):
        parser.add_argument('artwork', nargs=1, help='(Positional) Name for the artwork')
        parser.add_argument('--seed', action='store', help='The seed used for the randomness')
        parser.add_argument('--generator', action='store', help='The random generator to be used')
        parser.add_argument('--show', action='store_true',
                            help='Display the image using artworks::IMAGE_VIEW_APPLICATION')
        parser.add_argument('--output', action='store',
                            help='Store the image to this path')
        return parser


class Gallery(Command):
    def execute(self):
        random = GeneratorUtils.get_random_number_generator(self)
        artworks = GeneratorUtils.create_argument_function_mapping(self, random)
        save_path = GeneratorUtils.get_save_path(self)
        GeneratorUtils.draw_artworks(artworks, self, random, save_path)

    @staticmethod
    def add_arguments(parser):
        parser.add_argument('artworks', nargs='+', help='(Positional) Name for the artwork')
        parser.add_argument('count', nargs=1, help='Count of artworks to be produced', type=int)
        parser.add_argument('--generator', action='store', help='The random generator to be used')
        parser.add_argument('--show', action='store_true',
                            help='Display the image using artworks::IMAGE_VIEW_APPLICATION')
        parser.add_argument('--seed', action='store',
                            help='Seed to be used')
        parser.add_argument('--output', action='store',
                            help='Store all images to this directory')
        return parser


class GeneratorUtils(object):
    @staticmethod
    def get_random_number_generator(command: Union[Gallery, Generator]) -> src.random_provider.Random:
        random_class = GeneratorUtils.find_generator_class_by_name(command.arguments.generator)
        random = random_class()
        random.seed(command.arguments.seed)
        return random

    @staticmethod
    def find_artwork_class_by_name(searched_artwork: str) -> Optional[str]:
        for artwork in art + [DummyPlot]:
            if artwork.__name__ == searched_artwork:
                return artwork

    @staticmethod
    def find_generator_class_by_name(searched_generator: str) -> type:
        classes = [NativeRandom, XorRandom, CollatzConjectureRandom]
        default = XorRandom
        return {cls.__name__: cls for cls in classes}.get(searched_generator, default)

    @staticmethod
    def get_save_path(command: Union[Gallery, Generator]) -> Union[str, Path]:
        if command.arguments.output is not None:
            return Path(command.arguments.output)
        return Path(__file__).parent.parent / Path('img/')

    @staticmethod
    def draw_artworks(artworks: collections.abc.Collection, command: Union[Gallery, Generator], random: src.random_provider.Random, save_path: str):
        if len(artworks) > 0:
            LOGGER.info('Starting to draw images')
            now = time.time()
            for _ in range(command.arguments.count):
                artwork, random_kwargs_generator = random.choice(list(artworks.items()))
                random_kwargs = {key: get() for key, get in random_kwargs_generator.items()}

                LOGGER.info('Drawing artwork ({}/{}): {}'.format(_, command.arguments.count, artwork))
                img = artwork(rng=random, **random_kwargs)
                img.draw()
                if command.arguments.show:
                    img.show(path=save_path)
                else:
                    img.save(save_path)

                random.seed(img.hash)
            LOGGER.info('Drawing done. Took {}'.format(time.time() - now))
        else:
            LOGGER.error(
                'The artwork(s) you search for cannot be found in artworks.py: {}'.format(command.arguments.artwork)
            )

    @staticmethod
    def create_argument_function_mapping(command: Union[Gallery, Generator],
                                         random: src.random_provider.Random) -> dict:
        # produce a map of artworks, that holds another map with the keyword argument random functions
        # e.g.:
        # {Artwork: {param1: param1_getter}}
        # where artwork is an Artwork class, param1 is the key string for the parameter and param1_getter is a lambda
        artworks = dict()
        artwork_arguments = command.arguments.artworks if command.arguments.artworks is not None else [
            command.arguments.artwork]

        for artwork in artwork_arguments:
            value = GeneratorUtils.find_artwork_class_by_name(artwork)
            if value is not None:
                artworks[value] = create_random_argument_map(artwork, random)
        return artworks
