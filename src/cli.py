import argparse
from src.algos.hammi_xorshift import XorRandom
from src.algos.native_random import NativeRandom
from src.artworks import art


class CommandlineRunner(object):
    """ Pass sys.argv into this"""

    def __init__(self, *args):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()

        generate_parser = subparsers.add_parser('generate')

        generate_parser.add_argument('--artwork', required=True, action='store')
        generate_parser.add_argument('--seed', action='store')
        generate_parser.add_argument('--generator', action='store')
        generate_parser.add_argument('remainder', nargs=argparse.REMAINDER)
        generate_parser.set_defaults(generate=self.generate)

        gallery_parser = subparsers.add_parser('gallery')
        gallery_parser.set_defaults(gallery=self.gallery)
        test_parser = subparsers.add_parser('test')
        test_parser.set_defaults(test=self.test)
        crush_parser = subparsers.add_parser('crush')
        crush_parser.set_defaults(crush=self.crush)

        arguments = parser.parse_args(args)

        self.arguments = arguments
        self.artwork_specific_arguments, self.artwork_specific_keyword_arguments = self.parse_artwork_specific_arguments()



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
            raise NotImplementedError("This method is not supported")

    def parse_artwork_specific_arguments(self):
        # TODO: Find another/better way for parsing unspecified arguments
        # TODO: or let the artwork provide those specifications
        kwargs = dict()
        args = list()
        for e in self.arguments.remainder:
            if '=' in e:
                key, value = e.split('=')
                if not key:
                    raise ValueError('Invalid arguments: {}'.format(e))
                kwargs[key] = value
            else:
                args.append(e)
        return args, kwargs

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

    def generate(self):
        """ Run the generate command to output an image """
        # TODO: Add argument 'output' and save the image to the path if present
        # TODO: Add argument 'noshow' (naming?) and don't call show() if present
        random_class = self.find_generator_class_by_name(self.arguments.generator)
        random = random_class(seed=self.arguments.seed)

        artwork = self.find_artwork_class_by_name(self.arguments.artwork)
        if artwork is not None:
            img = artwork(*self.artwork_specific_arguments, **self.artwork_specific_keyword_arguments, rng=random)
            img.draw()
            img.show()
        else:
            print('The artwork you search for cannot be found in artworks.py: {}'.format(self.arguments.artwork))

    def gallery(self):
        raise NotImplementedError('Gallery is not implemented yet')

    def test(self):
        raise NotImplementedError('Tests are not implemented yet')

    def crush(self):
        raise NotImplementedError('Tests are not implemented yet')
