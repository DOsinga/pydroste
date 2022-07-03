# PyDroste

Small python project to generate movies with a droste effect or to create
zoomable movies using DALLE

## Installation

To setup a virtual environment with python3 and the dependencies installed,
execute in a shell:

    python3 -m venv venv3
    source venv3/bin/activate
    pip install -r requirements.txt

You can now run the main script:

    python pydroste.py --input=beach.jpg \
                       --output=beach.mp4 \
                       --center=1904,1940 \
                       --scale=125

And it should create a zooming in movie:

![Beach Movie](beach.gif)

Beside the input and output parameters, the important flags are
`center` and `scale`. `center` determines the point in the input picture
to zoom in on. `Scale` is the scale of the sub-image compared to the main
image. In other words, this is how far you need to zoom in to have the
main image be replaced by the sub-image completely and which would
complete one loop.

The two other flags you can pass are `frames`, which determines how
many frames the output image will have and `fps`, which determines
how many frames per seconds the output movie will play with.

The `pydroste_multiple.py` script can render loops with multiple zoom
points. The basic pattern is the same, except that a parameter `zoom_points`
needs to be supplied that contains a list of `;` separated tuples
specifying the various zoom point as `center_x,center_y,scale`

![Manhattanhenge](manhattanhenge.gif)

## DALLE use

This repository also contains some scripts that can be used to create
zoomable movies using DALLE.

Put your images say in the vangogh directory, create a first frame
and put it in the say vangogh directory. You can then use:

    python zoom_transparent.py \
        --input=vangogh/frame1.png \
        --output=vangogh/zoomed.png

To create a zoomed out version of frame1. Use that as a basis for your
next image and repeat this until you have a longish list of zoomed
out frames. You can put them together into a movie using:


    python animate_frames.py \
        --frame_count=6 --frames=60 \
        --input_dir=vangogh

This will produce a movie with 6 frames and with 60 frames per step
valled vangogh.mp4 in the root directory.