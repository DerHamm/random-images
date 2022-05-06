# Random-Images

You can generate images based on different PRNGs in this project.

The initial seed value for an image is provided by using an Ethereum-Address. But any seed could be used
for this.

To run the demo, run:

```python app.py```

A random image based on the strategy defined in the main-function will be generated. You can define your own strategies
and there are some example strategies as well.

Some PRNGs can be injected into a strategy to alter the results.

You can add instances of a strategy in the list `strats`. For each strategy, one image will be generated for now:

```python
def main():
    from app import RandomColorsPercentagePattern, ImageView
    from src.random_sources.address import Address
    import itertools
    # USED_STRATEGY = RandomColorsPercentagePattern()
    strats = [RandomColorsPercentagePattern()]
    address = Address(2)
    rand_bytes = list(address().address)
    random_cycler = itertools.cycle(rand_bytes)

    for strategy in strats:
        view = ImageView(strategy, random_cycler)
        view.show()
```

The end goal of this project is to generate one image, which consists of multiple other images (called 'patterns').
Each pattern consists of N pixels, while a Pixel has some color properties.

One Ethereum-Address (or some other seed) should generate many colorless patterns and the each pixel of a pattern then
calculates a color. The result will be some kind of collage consisting of multiple patterns.

Those patterns will be either generated via abusing the fact that many PRNGs are not *that* random at 
all and produce patterns. Or they will be generated using some approach where
random shapes (e.g. circles, rectangles, fractals) are being drawn on the canvas. This is still WIP right now.

The cool/nerdy thing about this is, that all those images will be procedurally generated, which means,
they are completely unique (even the patterns and pixels will be unique depending on the PRNG(s) used)

Another goal of this project is to learn more about Random Number Generators in general and to implement and test my own
custom random number generator.

When this project is done, I will make an effort to port the code to the web, so that normal people will be able to
generate images in a GUI in their browser.
