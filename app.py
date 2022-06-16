from src.algos.hammi_xorshift import XorRandom
from src.artworks import PietMondrian

# TODO: Try and see if you can run this project with PyScript
# TODO: Implement a PCG instead of XorShift for further experimentation
# TODO: Create a UnitTest-Suite based around the RandomProvider class and find a way to test all algos with that class
# TODO: Accept command line args here and start doing stuff
# Options to consider:
"""
- Run Big Crush / Small Crush / Diehard / Whatever Tests
- Run tests (there are no tests.. yet. but no srsly, we need some tests for the random provider, to assure, that
 all the algos we are going to implement are actually correct)
- Generate Image (w and w/o seed)
- Generate Test Data (length, algo_used) (This is probably obsolete because the test frameworks accept streams)
"""

random = XorRandom()
random.seed("welchen random seed soll ich nehmen?")

# IMAGE_SIZE = (1920, 1280)

"""
Test the generation of an image
"""


def main():
    image = PietMondrian(rng=random, min_diff=4)
    image.draw()
    image.show()


if __name__ == '__main__':
    main()
