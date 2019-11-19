#!/usr/bin/python
import argparse
import string

parser = argparse.ArgumentParser(description = "Dump kern pairs as CSV")
parser.add_argument("input", metavar="INPUT", help = "font file (OTF/TTF/UFO)")
options = parser.parse_args()

from fontParts.world import *
f = OpenFont(options.input)

for l in string.ascii_letters:
    for r in string.ascii_letters:
        if (l,r) in f.kerning:
            print("%s,%s,%i" % (l,r,f.kerning[(l,r)]))