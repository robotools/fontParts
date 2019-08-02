from fontParts.base import BaseLayer
from fontParts.fontshell.base import RBaseObject
from fontParts.opentype.glyph import OTGlyph
import fontParts.opentype.font

class OTLayer(RBaseObject, BaseLayer):
    wrapClass = fontParts.opentype.font.OTFont
    glyphClass = OTGlyph

    # For now only deal with single masters
    def _get_name(self):
        return "self"

    # color
    def _get_color(self):
        return None

    # -----------------
    # Glyph Interaction
    # -----------------

    def _getItem(self, name, **kwargs):
        layer = self.naked()
        glyph = layer[name]
        return self.glyphClass(glyph)

    def _keys(self, **kwargs):
        return self.naked().keys()

    def _newGlyph(self, name, **kwargs):
        layer = self.naked()
        layer.newGlyph(name)
        return self[name]

    def _removeGlyph(self, name, **kwargs):
        layer = self.naked()
        del layer[name]
