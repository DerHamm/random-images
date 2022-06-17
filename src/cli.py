import argparse
from src.algos.hammi_xorshift import XorRandom
from src.algos.native_random import NativeRandom
from src.artworks import art


class CommandlineRunner(object):
    """ Pass sys.argv into this"""

    def __init__(self, *args):
        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-generate', action='store_true')
        group.add_argument('-gallery', action='store_false')
        group.add_argument('-test', action='store_false')
        group.add_argument('-crush', action='store_false')

        generate_group = group.add_argument_group()
        generate_group.add_argument('--artwork', required=True, action='store')
        generate_group.add_argument('--seed', action='store')
        generate_group.add_argument('--generator', action='store')

        arguments = parser.parse_args(args)
        self.arguments = arguments

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
            img = artwork(rng=random)
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
