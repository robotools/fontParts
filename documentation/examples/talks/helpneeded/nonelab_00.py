# robothon06
# demo of executing python in FontLab, MacOS only
 
# this script runs in the Python IDE
# it will send some python code to FontLab
# FontLab will execute the python code:
# it will find the current glyph and send it to our other script.
 
from fontParts.tools.remote import runFontLabRemote, receiveGlyph
from fontParts.world import RFont
 
# this is what we want FontLab to do:
pythonCode = """
from fontParts.world import CurrentGlyph
from fontParts.tools.remote import transmitGlyph
g = CurrentGlyph()
transmitGlyph(g)
"""
 
# this the font where we'll store the glyph from FontLab
destFont = RFont()
 
result = runFontLabRemote(pythonCode)
receiveGlyph(result, destFont)
print(list(destFont.keys()))
