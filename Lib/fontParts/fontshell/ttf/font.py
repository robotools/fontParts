from fontTools.misc.py23 import basestring
from fontParts.base import BaseFont
import fontTools
from fontParts.fontshell.base import RBaseObject
from fontParts.fontshell.ttf.glyph import TTGlyph
from fontParts.fontshell.ttf.info import TTInfo
from fontParts.fontshell.ttf.kerning import TTKerning_kernTable
from fontParts.fontshell.ttf.kerning import TTKerning_GPOSTable
from fontTools.ttLib.tables._g_l_y_f import Glyph

from fontParts.base import BaseLayer

class TTLayer(RBaseObject, BaseLayer):
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
        glyph = self.naked().getGlyphSet()[name]
        return self.glyphClass(wrap=glyph,name=name)

    def _keys(self, **kwargs):
        return self.naked().getGlyphSet().keys()

class TTFont(RBaseObject, BaseFont):
    wrapClass = fontTools.ttLib.TTFont

    infoClass = TTInfo
    # groupsClass = TTGroups
    # kerningClass = TTKerning
    # featuresClass = TTFeatures
    # libClass = TTLib
    layerClass = TTLayer

    # ---------------
    # File Operations
    # ---------------

    # Initialize

    def _init(self, pathOrObject=None, showInterface=True, **kwargs):
        if isinstance(pathOrObject, basestring):
            font = self.wrapClass(pathOrObject)
        elif pathOrObject is None:
            font = self.wrapClass()
        else:
            font = pathOrObject
        self._wrapped = font

    # path

    def _get_path(self, **kwargs):
        return self.naked().reader.file.name

    # save

    def _save(self, path=None, showProgress=False,
              formatVersion=None, fileStructure=None, **kwargs):
        self.naked().save(path)

    # close

    def _close(self, **kwargs):
        del self._wrapped

    # -----------
    # Sub-Objects
    # -----------

    # info

    def _get_info(self):
        return self.infoClass(wrap=self.naked())

    # groups

    def _get_groups(self):
        return self.groupsClass(wrap=self.naked().groups)

    # kerning

    def _get_kerning(self):
        if "kern" in self.naked():
            return TTKerning_kernTable(wrap=self.naked()['kern'].getkern(0))
        else:
            if not hasattr(self, "_kernCache"):
                self._kernCache = TTKerning_GPOSTable(wrap=self.naked())
            return self._kernCache

    # features

    def _get_features(self):
        return self.raiseNotImplementedError()

    # lib

    def _get_lib(self):
        return None
    def _get_base_lib(self):
        return None

    # ------
    # Layers
    # ------

    def _get_layers(self, **kwargs):
        return [self.layerClass(wrap=self.naked())]

    # order
    def _get_layerOrder(self, **kwargs):
        return ["self"]

    # default layer
    def _get_defaultLayerName(self):
        return "self"

    # ------
    # Glyphs
    # ------

    def _get_glyphOrder(self):
        return self.naked().getGlyphOrder()

    def _set_glyphOrder(self, value):
        self.naked().glyphOrder = value

    def _lenGuidelines(self, **kwargs):
        return 0

    def _getGuideline(self, index, **kwargs):
        return None


    def _newGlyph(self, name, **kwargs):
        layer = self.naked()
        layer["hmtx"][name] = (0,0)
        layer.glyphOrder.append(name)
        # newId = layer["maxp"].numGlyphs
        # layer["maxp"].numGlyphs = newId + 1
        layer["glyf"][name] = Glyph() # XXX Only TTF
        layer["glyf"][name].numberOfContours = -1 # Only components right now
        return self[name]
