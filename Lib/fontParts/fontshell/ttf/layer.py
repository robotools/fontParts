from fontParts.base import BaseLayer
from fontParts.fontshell.base import RBaseObject
from fontParts.fontshell.ttf.glyph import TTGlyph
import fontParts.fontshell.ttf.font

class TTLayer(RBaseObject, BaseLayer):
    wrapClass = fontParts.fontshell.ttf.font.TTFont
    glyphClass = TTGlyph

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

    def _removeGlyph(self, name, **kwargs):
        layer = self.naked()
        del layer[name]
