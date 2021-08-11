.. highlight:: python

###############
Getting Started
###############

These need to be ported and updated from RoboFab's documentation.

For a quick start, here's the sample code from the introduction ported to fontparts::

   from fontParts.world import OpenFont

   font = OpenFont("/path/to/my/font.ufo")

   for glyph in font:
      glyph.leftMargin = glyph.leftMargin + 10
      glyph.rightMargin = glyph.rightMargin + 10

Find more of the original samples at https://github.com/robotools/robofab/tree/master/Docs/Examples
