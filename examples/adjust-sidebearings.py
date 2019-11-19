#!/usr/bin/python
import argparse

parser = argparse.ArgumentParser(description = "Adjust sidebearings of a glyph")
parser.add_argument("input", metavar="INPUT", help = "font file (OTF/TTF/UFO)")
parser.add_argument("glyph", metavar="GLYPH", help = "glyph name to adjust")
parser.add_argument("-l", "--lsb", type=int, help = "new left sidebearing")
parser.add_argument("-r", "--rsb", type=int, help = "new right sidebearing")
parser.add_argument("--output", type=str,help = "output file (if not given, overwrites input)")
options = parser.parse_args()

if not options.output:
    options.output = options.input

from fontParts.world import *

font = OpenFont(options.input)
glyph = font.layers[0][options.glyph]

if options.rsb:
    glyph.rightMargin = options.rsb
if options.lsb:
    glyph.leftMargin = options.lsb

font.save(options.output)