import math
import time

from PIL import Image
from pathlib import Path
from typing import Union

from .logger import get_logger

LOGGER = get_logger(__name__)


class ImageMerge(object):
    def __init__(self, directory: Union[str, Path]):
        self.directory = Path(directory)

    def merge(self):
        LOGGER.info("Merging image")
        now = time.time()

        images = list()
        for p in self.directory.iterdir():
            image = Image.open(str(p))
            images.append(image)

        images_per_row = round(math.sqrt(len(images)))

        first_image = images[0]
        width = first_image.size[0]
        height = first_image.size[1]

        row_width = images_per_row * width
        row_height = images_per_row * height

        new_image = Image.new("RGBA", (row_width, row_height), (255, 255, 255))

        x = 0
        y = 0
        for image in images:
            new_image.paste(image, (x, y))
            x += width
            if x >= row_width:
                x = 0
                y += height

        LOGGER.info("Image merged. Took {}".format(time.time() - now))
        new_image.save("img/test.png")
