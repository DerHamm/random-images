import argparse
from src.algos.hammi_xorshift import XorRandom
from src.algos.native_random import NativeRandom
from src.artworks import art


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

        # those are lists, but we want to handle those as single values, so properties are created
        """ The artwork class to be used """
        self._artwork = None
        """ Count of artworks to be generated """
        self._count = None

    @property
    def count(self):
        return self._count[0]

    @count.setter
    def count(self, value):
        self._count = value

    @property
    def artwork(self):
        return self._artwork[0]

    @artwork.setter
    def artwork(self, value):
        self._artwork = value


class CommandlineRunner(object):
    """ Pass sys.argv into this"""

    def __init__(self, *args):
        parser = argparse.ArgumentParser(description='Random Images CLI')

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
    def add_arguments(parser: argparse.ArgumentParser):
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError


# Executes the generate command
class Generator(Command):

    def execute(self):
        """ Run the generate command to output an image """
        # TODO: Add argument 'output' and save the image to the path if present
        random_class = self.find_generator_class_by_name(self.arguments.generator)
        random = random_class(seed=self.arguments.seed)

        artwork = self.find_artwork_class_by_name(self.arguments.artwork)
        if artwork is not None:
            img = artwork(rng=random)
            img.draw()
            if self.arguments.show:
                img.show()
        else:
            print('The artwork you search for cannot be found in artworks.py: {}'.format(self.arguments.artwork))

    @staticmethod
    def find_artwork_class_by_name(searched_artwork):
        for artwork in art:
            if artwork.__name__ == searched_artwork:
                return artwork

    @staticmethod
    def find_generator_class_by_name(searched_generator):
        classes = [NativeRandom, XorRandom]
        default = XorRandom
        return {cls.__name__: cls for cls in classes}.get(searched_generator, default)

    @staticmethod
    def add_arguments(parser):
        parser.add_argument('artwork', nargs=1, help='(Positional) Name for the artwork')
        parser.add_argument('--seed', action='store', help='The seed used for the randomness')
        parser.add_argument('--generator', action='store', help='The random generator to be used')
        parser.add_argument('--show', action='store_true',
                            help='Display the image using artworks::IMAGE_VIEW_APPLICATION')
        return parser


class Gallery(Command):
    # TODO: Parallel image generation / split of write and generation
    # TODO: Custom artwork parameters?
    # TODO: Better seeding?
    def execute(self):
        random_class = Generator.find_generator_class_by_name(self.arguments.generator)
        random = random_class(seed=self.arguments.seed)
        artworks = [Generator.find_artwork_class_by_name(artwork) for artwork in self.arguments.artworks]
        if artworks:
            for _ in range(self.arguments.count):
                artwork = random.choice(artworks)
                img = artwork(rng=random)
                img.draw()
                if self.arguments.show:
                    img.show()
                else:
                    img.save()
                random.seed(img.hash)
        else:
            print('The artwork you search for cannot be found in artworks.py: {}'.format(self.arguments.artwork))

    @staticmethod
    def add_arguments(parser):
        parser.add_argument('artworks', nargs='+', help='(Positional) Name for the artwork')
        parser.add_argument('count', nargs=1, help='Count of artworks to be produced', type=int)
        parser.add_argument('--generator', action='store', help='The random generator to be used')
        parser.add_argument('--show', action='store_true',
                            help='Display the image using artworks::IMAGE_VIEW_APPLICATION')
        parser.add_argument('--seed', action='store',
                            help='Seed to be used')
        return parser
