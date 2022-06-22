from src.cli import CommandlineRunner
from os import mkdir
from os.path import isdir
from pathlib import Path

# TODO: Try and see if you can run this project with PyScript
# TODO: Implement a PCG instead of XorShift for further experimentation
# TODO: Create a UnitTest-Suite based around the RandomProvider class and find a way to test all algos with that class
# Options to consider:
"""
- Run Big Crush / Small Crush / Diehard / Whatever Tests
- Run tests (there are no tests.. yet. but no srsly, we need some tests for the random provider, to assure, that
 all the algos we are going to implement are actually correct)
- Generate Image (w and w/o seed)
- Generate Test Data (length, algo_used) (This is probably obsolete because the test frameworks accept streams)
"""


def setup():
    if not isdir('img'):
        try:
            mkdir('img')
        except Exception as e:
            print(e)
            return False
    return True

def cleanup():
    files = list(Path('img').iterdir())
    if len(files) > 10:
        for path in files:
            path.unlink()

"""
Test the generation of an image
"""


def main():
    if not setup():
        quit(2)
    cleanup()

    # command_line_arguments = argv[1::]
    gallery_command_line_arguments = ['gallery', 'PietMondrian', 'XorCoords', '3', '--show', '--seed', '123456']
    generate_command_line_arguments = ['generate', 'PietMondrian', '--show', '--seed', '123456']
    cli = CommandlineRunner(*gallery_command_line_arguments)
    cli.run()


if __name__ == '__main__':
    main()
