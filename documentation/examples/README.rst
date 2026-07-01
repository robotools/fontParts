.. highlight:: python

fontParts examples
==================

FontParts is based on RoboFab. RoboFab had an extensive set of documentation and examples, which almost but not quite get you going in fontParts.

The examples of Robofab have been quick-and-dirty converted to be usable in fontParts. Where the code could not be made to work, the example has been deleted if it doesn't make sense outside of Robofab. Some other examples do not translate to fontParts in an obvious way, yet making them work would be worthwhile to people making the switch. These scripts have, possibly in a half converted state, been put in a directory called "helpneeded".

If you can assist, please fork the repo, fix one of more examples and create a pull request.

Many Robofab example scripts are intended to be run from inside a font editor. These have been converted to operate on a standalone font, called test.ufo. The scripts have been tested against DINish. Here's a quick start to get you going::

    mkdir fontparts-playground; cd fontparts-playground
    virtualenv ~/.venv/fontparts-playground
    . ~/.venv/fontparts-playground/bin/activate
    pip install fontParts
    git clone git@github.com:playbeing/dinish.git
    git clone git@github.com:robotools/fontParts.git
    cd fontParts/documentation/examples/howtos
    cp -pr ../../../../dinish/sources/Dinish/Dinish-Regular.ufo test.ufo
    python otFeatures_00.py


