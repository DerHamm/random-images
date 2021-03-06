# Random-Images

Playground project for exploring possibilities within the concept of generative art and random number generators.

## Project Goals

One of the first goals of this project was to implement a custom random generator.

This was done by implementing my own version `XorShift`, that adds an extra step to the calculation. I also created a 
`Random` interface similar to the native Python interface, so that other generated can be added easily. A plan for the
future is to implement a derivative of [pcg-random](https://www.pcg-random.org/) in Python this project.

Another goal was to fully understand seeding of PRNGs. For this, a class `Address` was created, which can generate
Ethereum Addresses. Furthermore, I explored different techniques of seeding. For now, I'm deriving  a `md5`-Hash of the
user provided value to generate a seed. With this approach, any data can be transformed into a seed easily, which comes
in handy, if you are doing procedural generation.

Another topic explored here are colors and color palettes in combination with random generation. To be more specific:
How to choose harmonic random colors within a piece of generative art?

The huge end goal of this project is to provide something like an 'endless generative art collection', which essentially
just produces random artworks based on the initial seed given by the used.
'Your very own museum of art', if you will.

The project will probably never reach another stage of development as I exhausted all the available Python technologies
for image processing. I came to the conclusion, that libraries like PIL/Pillow lack support for certain Features I want.
Because of this, the development of this project will soon move to another language and tech stack.

Two possible technologies are [processing](https://processing.org/) and [nannou](https://nannou.cc/). 

Another possibility is to use [PyScript](https://pyscript.net/) to draw the images onto HTML-Canvasses.

## Artworks

Within the file `artworks.py` you will find a collection of images, that can be generated by this project.
My proudest work so far is the `PietMondrian`-Artwork.

If you cloned this project, and you want to create your own `Artwork`, you can simply inherit from the `Artwork`-class
and implement your own logic. Those artworks are loosely coupled to PIL, but you can easily switch the implementation
for something else.

You can even change the implementation of the `Image` class used by providing your own interface for that.

Some really simple example on how to implement your own artwork:

```python
from src.artworks import Artwork
from PIL import ImageDraw


class DemoArtwork(Artwork):
    """ Just some demo artwork for the docs """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def draw(self):
        # draw something here
        draw = ImageDraw.Draw(self.canvas)
        if self.rng.random() > 0.5:
            draw.line((self.rng.randint(0, 600), 0, 40, 60))
        else:
            draw.line((120, 80, self.rng.randint(40, 400), 60))
```

You can also iterate over the pixel array, manipulating each pixel by itself. See the artwork `XorCoords` for examples.


## Running from command line

You can generate images from the command line. Refer to the [command line guide](./arguments.md) for more detailed
information on this.

A general example:

```shell
python app.py generate --artwork PietMondrian --seed 1234556 --generator XorRandom
```

Only `--artwork` is required for the `-generate` command.

## Tips

The dependencies needed for the Ethereum Address Generator are somewhat tedious to set up (at least on Windows).
So if you just care for the artworks and not the crypto/random-generation stuff, you can just delete `address.py` and go
on with your life.

If you want to save the images you generate, just save the `seed`. I plan to add a small utility, which can display your
whole gallery, if you just provide a .json-file, that maps Artwork-Names with seeds like so:

```json
{
  "PietMondrian": ["reallyCoolSeed", "weirdSeed"],
  "MyArtwork": ["someOtherSeed"]
}
```

## Generators

The projects also features some experimental random number generators. The newest addition is the `CollatzConjecture`-
Generator, which is based on the (you name it!) Collatz-Conjecture.

I'm planning on adding a PI-based generator, a prime-number based generator as well as some more serious stuff, like
the PCG-Generator.

## Random arguments

I spent a lot of time implementing `argument_randomizer` to be able to randomize all the parameters for the different
artworks.

The function `create_random_argument_map` can be used to get a map of functions corresponding to the parameters of the
classes `__init__` method.

You need to place proper type hints into your artworks for this to work with the randomizer.

