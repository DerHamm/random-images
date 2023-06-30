# Command Line Arguments

## Generate
Generate an image

### Parameters

### seed 

- optional
- A string for the seed used

Example:

`python app.py generate Artwork --seed=someSeed`

### artwork
- required
- Class name of the artwork to be generated

Example:

`python app.py generate Artwork`


### generator
- optional
- Random Number generator to be used

Example:

`python app.py generate Artwork --generator=NativeRandom`

### show
- optional
- Display the image


Example:

`python app.py generate Artwork --show`

### output
- optional
- Save the image to the given path


Example:

`python app.py generate Artwork --outupt /home/img.png`


### *args/**kwargs

WIP


## Gallery
Generate a gallery of images

### artwork
- required
- Class name of the artworks to be generated

Example:

`python app.py gallery PietMondrian XorCoords 1`

### count
- required
- Amount of artworks to be generated

Example:

`python app.py gallery PietMondrian 12`

### seed 

- optional
- A string for the seed used

Example:

`python app.py gallery Artwork --seed=someSeed 1`

### generator
- optional
- Random Number generator to be used

Example:

`python app.py gallery Artwork --generator=NativeRandom 1`

### show
- optional
- Display the image


Example:

`python app.py gallery Artwork 1 --show`




## Test

Run the unit test suite

WIP

## Crush

Run the BigCrush/Diehard test suite

WIP
