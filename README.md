# PyDroste

Small python project to generate movies with a droste effect.

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

