class RandomColors(object):

    def __init__(self, rng):
        self.rng = rng

    """
    Color Palettes
    'Perceptually Uniform Sequential'
    ['viridis', 'plasma', 'inferno', 'magma', 'cividis']

    ('Sequential' ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds','YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 
    'RdPu', 'BuPu','GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn'] 

    'Sequential (2)
    ['binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink','spring', 'summer', 'autumn', 'winter', 'cool',
    'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper']

    'Diverging'
    ['PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu','RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']

    'Cyclic'
    ['twilight', 'twilight_shifted', 'hsv'])

    'Qualitative'
    ['Pastel1', 'Pastel2', 'Paired', 'Accent','Dark2', 'Set1', 'Set2', 'Set3','tab10', 'tab20', 'tab20b', 'tab20c']),

    'Miscellaneous'
    ['flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern','gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg'
    'gist_rainbow', 'rainbow', 'turbo', 'nipy_spectral','gist_ncar']
    """

    COLOR_PALETTE_NAMES = ['viridis', 'gnuplot', 'coolwarm', 'Accent', 'tab20c', 'ocean', 'BrBG', 'RdBu', 'Set3',
                           'RdYlGn', 'YlOrRd',
                           'inferno', 'flag', 'afmhot', 'Set2', 'Pastel2', 'cool', 'gist_yarg', 'BuGn', 'RdPu', 'PuRd',
                           'Purples', 'terrain',
                           'YlGnBu', 'brg', 'twilight_shifted', 'PRGn', 'PuBuGn', 'YlOrBr', 'seismic', 'bwr', 'OrRd',
                           'Spectral', 'PuBu',
                           'gist_earth', 'Oranges', 'prism', 'gist_ncar', 'nipy_spectral', 'gist_rainbow', 'twilight',
                           'Pastel1', 'GnBu',
                           'gist_heat', 'Reds', 'hot', 'Paired', 'PuOr', 'cubehelix', 'spring', 'Wistia', 'Greys',
                           'Dark2', 'tab20', 'autumn',
                           'tab10', 'gist_gray', 'bone', 'Set1', 'gray', 'RdYlBu', 'RdGy', 'magma', 'gist_stern',
                           'tab20b', 'Blues', 'hsv',
                           'plasma', 'PiYG', 'copper', 'turbo', 'summer', 'BuPu', 'rainbow', 'CMRmap', 'winter',
                           'Greens', 'gnuplot2', 'pink',
                           'cividis', 'YlGn', 'binary']

    def random_palette(self):
        return self.rng.choice(RandomColors.COLOR_PALETTE_NAMES)

    def random_color(self):
        return self.rng.randint(0, 255), self.rng.randint(0, 255), self.rng.randint(0, 255)

    def random_color_from_palette(self, palette):
        return palette[self.rng.randint(0, len(palette) - 1)]

    def pop_random_color_from_palette(self, palette):
        return palette.pop(self.rng.randint(0, len(palette) - 1))
