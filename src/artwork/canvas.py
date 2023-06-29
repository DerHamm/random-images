class Canvas(object):
    """Canvas needs to implement some image"""

    @staticmethod
    def new(*args, **kwargs):
        """Initialize a new image"""
        raise NotImplementedError()

    def load(self):
        """Return the pixel array"""
        raise NotImplementedError()

    def save(self, *args, **kwargs):
        """Save the image to disk"""
        raise NotImplementedError()

    def rotate(self, *args, **kwargs):
        """Rotate image"""
        raise NotImplementedError()
