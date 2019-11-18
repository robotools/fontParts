from fontParts.fontshell.ttf.font import TTFont,TTLayer
from fontParts.fontshell.otf.glyph import OTGlyph

class OTLayer(TTLayer):
    glyphClass = OTGlyph

class OTFont(TTFont):
    layerClass = OTLayer
