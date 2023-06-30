import seaborn as sns

from PIL import ImageDraw
from math import sqrt

from .art_utils import hex_to_rgb
from .artwork import Artwork

from ..util.random_colors import RandomColors


class CirclePacking(Artwork):
    """Sourced from https://generativeartistry.com/tutorials/circle-packing/
    The code shown there was improved in some ways"""

    class Circle(object):
        def __init__(self, x, y, r) -> None:
            self.x = x
            self.y = y
            self.radius = r

    def __init__(
        self,
        create_circle_attempts: int = 500,
        total_circles: int = 500,
        min_radius: int = 4,
        max_radius: int = 100,
        overlap_borders: bool = False,
        line_width: int = 2,
        *args,
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        self.line_width = line_width
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.total_circles = total_circles
        self.create_circle_attempts = create_circle_attempts

        self.random_colors = RandomColors(self.rng)
        self.palette = sns.color_palette(
            self.random_colors.random_palette(), 32
        ).as_hex()
        self.random_color = lambda: hex_to_rgb(
            self.random_colors.random_color_from_palette(self.palette)
        )
        self.theme = hex_to_rgb(
            self.random_colors.pop_random_color_from_palette(self.palette)
        )
        self.canvas.image = self.canvas.new(
            Artwork.DEFAULT_MODE, Artwork.DEFAULT_SIZE, self.theme
        )

        self.circles = list()

        self.width = self.canvas.size[0]
        self.height = self.canvas.size[1]

        self.total_fails = 10

        if overlap_borders:
            self.__has_collision = lambda circle: self.__overlap(circle)
        else:
            self.__has_collision = lambda circle: self.__border_check(
                circle
            ) or self.__overlap(circle)

    def draw(self) -> None:
        draw = ImageDraw.Draw(self.canvas.image)
        fails = 0
        while True:
            if not self.__create_and_draw_circle(draw):
                fails += 1
            if fails > self.total_fails:
                break

    def __create_and_draw_circle(self, draw: ImageDraw.ImageDraw) -> bool:
        new_circle = None
        can_draw = False
        for tries in range(self.create_circle_attempts):
            new_circle = CirclePacking.Circle(
                self.rng.random() * self.width,
                self.rng.random() * self.width,
                self.min_radius,
            )
            if self.__has_collision(new_circle):
                continue
            else:
                can_draw = True
                break

        if not can_draw:
            return False

        for radius_size in range(self.min_radius, self.max_radius, 1):
            new_circle.radius = radius_size
            if self.__has_collision(new_circle):
                new_circle.radius -= 1
                break

        self.circles.append(new_circle)
        coordinates = (new_circle.x, new_circle.y)
        box = self.__bounding_box(coordinates, new_circle.radius)
        draw.ellipse(
            box,
            outline=self.random_color(),
            fill=self.random_color(),
            width=self.line_width,
        )
        return True

    def __border_check(self, circle: Circle) -> bool:
        return not (
            0 <= circle.x - circle.radius < circle.x + circle.radius < self.width
            and 0 <= circle.y - circle.radius < circle.y + circle.radius < self.height
        )

    def __overlap(self, circle: Circle) -> bool:
        for other_circle in self.circles:
            a = circle.radius + other_circle.radius
            x = circle.x - other_circle.x
            y = circle.y - other_circle.y

            if a >= sqrt((x * x) + (y * y)):
                return True
        return False

    @staticmethod
    def __bounding_box(point, radius) -> list[tuple]:
        return [
            (point[0] - radius, point[1] - radius),
            (point[0] + radius, point[1] + radius),
        ]
