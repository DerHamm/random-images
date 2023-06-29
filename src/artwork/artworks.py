from src.artwork.artwork import Artwork
from src.artwork.piet_mondrian import PietMondrian
from src.artwork.coordinate_magics import XorCoords, AddCoords

from .recursive_quads import RecursiveQuads
from .circle_packing import CirclePacking

from ..logger import get_logger

__all__ = [
    "AddCoords",
    "AndCoords",
    "Artwork",
    "CoordinateMagics",
    "ModCoords",
    "OrCoords",
    "PietMondrian",
    "SubCoordsYFromX",
    "XorCoords",
    "art",
    "RecursiveQuads",
    "DummyPlot",
    "CirclePacking",
    "ImageMerge",
]

LOGGER = get_logger(__name__)

IMAGE_VIEW_APPLICATION = "paintdotnet"

art = [PietMondrian, XorCoords, RecursiveQuads, CirclePacking, AddCoords, XorCoords]
