# Command Line Arguments

## Generate
Generate an image

### Parameters

### seed 

- optional
- A string for the seed used

Example:

`python app.py generate Artwork seed=someSeed`

### artwork
- required
- Class name of the artwork to be generated

Example:

`python app.py generate Artwork`


### generator
- optional
- Random Number generator to be used

Example:

`python app.py generate Artwork generator=NativeRandom`


### *args/**kwargs
- required/optional
- All the artwork specific arguments
- We have to manage order of unnamed and naming of named arguments here

`python app.py generate PietMondrian splits=1,2.5,4 min_diff=4`

## Gallery
Generate a gallery of images

## Test

Run the unit test suite

WIP

## Crush

Run the BigCrush/Diehard test suite

WIP
