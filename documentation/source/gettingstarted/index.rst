.. highlight:: python

###############
Getting Started
###############

These need to be ported and updated from RoboFab's documentation.

For a quick start, here's the sample code from the introduction ported to fontParts::

   from fontParts.world import OpenFont

   font = OpenFont("/path/to/my/font.ufo")

   for glyph in font:
      glyph.leftMargin = glyph.leftMargin + 10
      glyph.rightMargin = glyph.rightMargin + 10

Some of the original examples have been converted to fontParts. Get them at https://github.com/robotools/fontParts/tree/master/documentation/examples. Please note that not all of them print out all results and/or do something useful; you may need to flesh them out. Non-working examples have been moved to a helpneeded directory. Bear in mind that not all functionality of RoboFab made it into fontParts, so some will never work.
