from fontTools.misc.py23 import basestring
from fontParts.base import BaseFont
from fontTools.ttLib import TTFont
from fontParts.fontshell.base import RBaseObject
from fontParts.opentype.glyph import OTGlyph
# from fontParts.opentype.groups import OTGroups
# from fontParts.opentype.kerning import OTKerning
# from fontParts.opentype.features import OTFeatures
# from fontParts.opentype.lib import OTLib
# from fontParts.opentype.guideline import OTGuideline

from fontParts.base import BaseLayer

class OTLayer(RBaseObject, BaseLayer):
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
        glyftable = self.naked()["glyf"]
        glyph = glyftable[name]
        return self.glyphClass(wrap=glyph,name=name)

    def _keys(self, **kwargs):
        return self.naked()["glyf"].keys()

    def _newGlyph(self, name, **kwargs):
        layer = self.naked()
        layer.newGlyph(name)
        return self[name]

    def _removeGlyph(self, name, **kwargs):
        layer = self.naked()
        del layer[name]

class OTFont(RBaseObject, BaseFont):
    wrapClass = TTFont
    # infoClass = OTInfo
    # groupsClass = OTGroups
    # kerningClass = OTKerning
    # featuresClass = OTFeatures
    # libClass = OTLib
    layerClass = OTLayer

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
        return self.infoClass(wrap=self.naked().info)

    # groups

    def _get_groups(self):
        return self.groupsClass(wrap=self.naked().groups)

    # kerning

    def _get_kerning(self):
        return self.kerningClass(wrap=self.naked().kerning)

    # features

    def _get_features(self):
        return self.featuresClass(wrap=self.naked().features)

    # lib

    def _get_lib(self):
        return self.libClass(wrap=self.naked().lib)

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
        return self.naked().glyphOrder

    def _set_glyphOrder(self, value):
        self.naked().glyphOrder = value
