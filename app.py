from src.cli import CommandlineRunner
from os import mkdir
from os.path import isdir
from pathlib import Path


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
    gallery_command_line_arguments = ['gallery', 'CirclePacking', '1', '--show', '--seed',
                                      '546l3e63h', '--generator', 'XorRandom']
    generate_command_line_arguments = ['generate', 'CirclePacking', '--show', '--generator', 'XorRandom', '--seed', '546l3e63h']
    cli = CommandlineRunner(*generate_command_line_arguments)
    cli.run()


if __name__ == '__main__':
    main()
