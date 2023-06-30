from typing import Any

MESSAGE = "Implement this method in a subclass of Canvas"

class Canvas(object):
    """Canvas needs to implement some image"""

    @staticmethod
    def new(*args, **kwargs) -> Any:
        """Initialize a new image"""
        raise NotImplementedError(MESSAGE)

    def load(self) -> None:
        """Return the pixel array"""
        raise NotImplementedError(MESSAGE)

    def save(self, *args, **kwargs) -> None:
        """Save the image to disk"""
        raise NotImplementedError(MESSAGE)

    def rotate(self, *args, **kwargs) -> None:
        """Rotate image"""
        raise NotImplementedError(MESSAGE)
