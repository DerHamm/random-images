from .artwork import Artwork
from .piet_mondrian import PietMondrian
from .coordinate_magics import (
    AddCoords,
    AndCoords,
    CoordinateMagics,
    ModCoords,
    OrCoords,
    SubCoordsYFromX,
    XorCoords,
)
from .recursive_quads import RecursiveQuads
from .circle_packing import CirclePacking
from .cubic_disarray import CubicDisarray
from .dummy_plot import DummyPlot


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

art = [
    AddCoords,
    AndCoords,
    CoordinateMagics,
    ModCoords,
    OrCoords,
    PietMondrian,
    SubCoordsYFromX,
    XorCoords,
    RecursiveQuads,
    DummyPlot,
    CirclePacking,
    CubicDisarray,
]
