from src.pixel_iterator_strategies.strategies import XorRandom

# TODO: Implement a PCG instead of XorShift for further experimentation
# TODO: Update the project's README
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

IMAGE_SIZE = (1280, 720)
random = XorRandom()
random.seed("http¯\_(ツ)_/¯¯\_(ツ)_/¯¯\_(ツ)_/¯YEET_8¯\_(ツ)_/¯¯\_(ツ)_/¯¯\_(ツ)_/¯¯\_(ツ)_/¯¯\_(ツ)_/¯//wwwyw")

# IMAGE_SIZE = (1920, 1280)

"""
Test the generation of an image
"""

def main():

    from src.artworks import art
    b = list()
    for artwork in art:
        img = artwork(rng=random)
        print("created {}".format(artwork.__name__))
        img.draw()
        print("drawn")
        img.show()
        print("shown")

        if input("bad?") == "y":
            b.append(artwork.__name__)
    print(b)




if __name__ == '__main__':


    main()
