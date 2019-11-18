import defcon
from fontParts.base import BaseComponent
from fontParts.fontshell.base import RBaseObject
import fontTools.ttLib.tables._g_l_y_f

class TTComponent(RBaseObject, BaseComponent):

    wrapClass = fontTools.ttLib.tables._g_l_y_f.GlyphComponent

    # ----------
    # Attributes
    # ----------

    # baseGlyph

    def _get_baseGlyph(self):
        return self.naked().glyphName

    def _set_baseGlyph(self, value):
        self.naked().glyphName = value

    # transformation

    def _get_transformation(self):
        if hasattr(self.naked(), "transformation"):
            return self.naked().transformation
        else:
            return (1, 0, 0, 1, self.naked().x, self.naked().y)

    def _set_transformation(self, value):
        self.naked().transformation = value

    # --------------
    # Identification
    # --------------

    # index

    def _set_index(self, value):
        component = self.naked()
        glyph = component.glyph
        if value > glyph.components.index(component):
            value -= 1
        glyph.removeComponent(component)
        glyph.insertComponent(value, component)

    # identifier

    def _get_identifier(self):
        component = self.naked()
        return component.identifier

    def _getIdentifier(self):
        component = self.naked()
        return component.generateIdentifier()

    def _setIdentifier(self, value):
        self.naked().identifier = value

    # -------------
    # Normalization
    # -------------

    def _decompose(self):
        component = self.naked()
        glyph = component.glyph
        glyph.decomposeComponent(component)
