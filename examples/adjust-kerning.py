#!/usr/bin/python
import argparse

def chunks(l):
    for i in range(0, len(l), 3):
        yield l[i:i + 3]

parser = argparse.ArgumentParser(description = "Adjust font kerning")
parser.add_argument("input", metavar="INPUT", help = "font file (OTF/TTF/UFO)")
parser.add_argument("left", metavar="LEFT", help = "left glyph name")
parser.add_argument("right", metavar="RIGHT", help = "right glyph name")
parser.add_argument("value", metavar="VALUE", type=int, help = "new kerning value in units")
parser.add_argument("--output", type=str,help = "output file (if not given, overwrites input)")
parser.add_argument('rest', metavar="...", nargs=argparse.REMAINDER, help = "additional left/right/value triplets")

options = parser.parse_args()

if not options.output:
    options.output = options.input

from fontParts.world import *

font = OpenFont(options.input)
font.kerning[(options.left,options.right)] = options.value

for l,r,value in chunks(options.rest):
  font.kerning[(l,r)] = int(value)

font.save(options.output)
