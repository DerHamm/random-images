from src.cli import CommandlineRunner
from os import mkdir
from os.path import isdir
from pathlib import Path

# TODO: Create a project plan or some sort of that kind and (kinda) estimate all those TODOs below


# TODO: Try and see if you can run this project with PyScript
# TODO: Explore alternative image libraries
# TODO: Implement a PCG instead of XorShift for further experimentation
# TODO: Create a UnitTest-Suite based around the RandomProvider class
# TODO: BigCrush and or DieHard testsuite
# TODO: Finish argument_randomizer (lists, maps,  more flexibility, configurability)
# TODO: Refactor the whole project to use type hints where appropriate
# TODO: Restructure the project in a more 'pythonic' way
# TODO: Implement the announced "seeds.json"-feature
# TODO: Update readme/cli guide
# TODO: Clean up the color palettes (redundant names)
# TODO: Fix the `art = classes =` / __all__ dilemma
# TODO: Parallel image generation / split of write and generation
# TODO: More art


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
    gallery_command_line_arguments = ['gallery', 'PietMondrian', 'XorCoords', '3', '--show', '--seed',
                                      '456356325', '--generator', 'CollatzConjectureRandom']
    generate_command_line_arguments = ['generate', 'CirclePacking', '--show', '--generator', 'XorRandom', '--seed', '12xdb567uzrhztg3']
    cli = CommandlineRunner(*generate_command_line_arguments)
    cli.run()


if __name__ == '__main__':
    main()
