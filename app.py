from os import mkdir
from os.path import isdir
from pathlib import Path

from src.util.cli import CommandlineRunner
from src.util.logger import get_logger
from src.util.config_loader import ConfigLoader

LOGGER = get_logger(__name__)


def setup() -> None:
    if not isdir("img"):
        try:
            mkdir("img")
        except Exception as e:
            LOGGER.error(e)
            return False
    return True


def cleanup() -> None:
    files = list(Path("img").iterdir())
    if len(files) > 10:
        for path in files:
            path.unlink()


def init_config() -> None:
    ConfigLoader().load_config()

"""
Test the generation of an image
"""


def main() -> None:
    init_config()

    if not setup():
        quit(2)
    cleanup()

    # command_line_arguments = argv[1::]
    gallery_command_line_arguments = [
        "gallery",
        "PietMondrian",
        "5",
        "--seed",
        "6515806815",
        "--generator",
        "XorRandom",
    ]
    generate_command_line_arguments = [
        "generate",
        "CirclePacking",
        "--show",
        "--generator",
        "XorRandom",
        "--seed",
        "546l3e63h",
    ]
    generate_command_line_arguments2 = [
        "gallery",
        "CirclePacking",
        "1",
        "--show",
        "--generator",
        "XorRandom",
        "--seed",
        "546l3e63h",
    ]
    generate_command_line_arguments3 = [
        "generate",
        "PietMondrian",
        "--show",
        "--generator",
        "XorRandom",
        "--seed",
        "r0392hr",
    ]
    cli = CommandlineRunner(*generate_command_line_arguments3)
    cli.run()



if __name__ == "__main__":
    main()
