from src.algos.hammi_xorshift import XorRandom

random = XorRandom()


"""
Color Palettes 
'Perceptually Uniform Sequential'
['viridis', 'plasma', 'inferno', 'magma', 'cividis']

('Sequential'
['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds','YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu','GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']

'Sequential (2)
['binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink','spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia','hot', 'afmhot', 'gist_heat', 'copper']

'Diverging'
['PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu','RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']

'Cyclic'
['twilight', 'twilight_shifted', 'hsv'])

'Qualitative'
['Pastel1', 'Pastel2', 'Paired', 'Accent','Dark2', 'Set1', 'Set2', 'Set3','tab10', 'tab20', 'tab20b', 'tab20c']),

'Miscellaneous'
['flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern','gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg','gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral','gist_ncar']
"""

COLOR_PALETTE_NAMES = ['viridis', 'plasma', 'inferno', 'magma', 'cividis'] + \
                      ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds', 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd',
                       'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn'] + \
                      ['binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink', 'spring', 'summer', 'autumn',
                       'winter', 'cool', 'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper'] + \
                      ['PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm',
                       'bwr', 'seismic'] + \
                      ['twilight', 'twilight_shifted', 'hsv'] + \
                      ['Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2', 'Set1', 'Set2', 'Set3', 'tab10', 'tab20',
                       'tab20b', 'tab20c'] + \
                      ['flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap',
                       'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral', 'gist_ncar']


def random_palette():
    return random.choice(COLOR_PALETTE_NAMES)

def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

def random_color_from_palette(palette):
    return palette[random.randint(0, len(palette) - 1)]

