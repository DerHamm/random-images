import math


def hex_to_rgb(h: str) -> tuple:
    """It looks cursed, but it just casts the hex numbers to decimals and wraps them in a tuple"""
    return tuple(int(h[1:][num : num + 2], 16) for num in (0, 2, 4))


def rect_size(point1: list, point2: list, point3: list, point4: list) -> float:
    width = math.sqrt(
        math.pow((point2[0] - point1[0]), 2) + math.pow((point2[1] - point1[1]), 2)
    )
    length = math.sqrt(
        math.pow((point4[0] - point3[0]), 2) + math.pow((point4[1] - point3[1]), 2)
    )
    return width * length
