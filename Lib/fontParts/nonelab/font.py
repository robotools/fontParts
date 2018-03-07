import os
import defcon
from fontTools.misc.py23 import basestring
from fontParts.base import BaseFont, FontPartsError
from fontParts.nonelab.base import RBaseObject
from fontParts.nonelab.info import RInfo
from fontParts.nonelab.groups import RGroups
from fontParts.nonelab.kerning import RKerning
from fontParts.nonelab.features import RFeatures
from fontParts.nonelab.lib import RLib
from fontParts.nonelab.layer import RLayer
from fontParts.nonelab.guideline import RGuideline


class RFont(RBaseObject, BaseFont):

    wrapClass = defcon.Font
    infoClass = RInfo
    groupsClass = RGroups
    kerningClass = RKerning
    featuresClass = RFeatures
    libClass = RLib
    layerClass = RLayer
    guidelineClass = RGuideline

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
        self._wrappedInfo = None
        self._wrappedGroups = None
        self._wrappedKerning = None
        self._wrappedFeatures = None
        self._wrappedLib = None

    # path

    def _get_path(self, **kwargs):
        return self.naked().path

    # save

    def _save(self, path=None, showProgress=False, formatVersion=None, **kwargs):
        self.naked().save(path=path, formatVersion=formatVersion)

    # close

    def _close(self, **kwargs):
        del self._wrapped

    # -----------
    # Sub-Objects
    # -----------

    # info

    def _get_info(self):
        if self._wrappedInfo is None:
            self._wrappedInfo = self.infoClass(wrap=self.naked().info)
        return self._wrappedInfo

    # groups

    def _get_groups(self):
        if self._wrappedGroups is None:
            self._wrappedGroups = self.groupsClass(wrap=self.naked().groups)
        return self._wrappedGroups

    # kerning

    def _get_kerning(self):
        if self._wrappedKerning is None:
            self._wrappedKerning = self.kerningClass(wrap=self.naked().kerning)
        return self._wrappedKerning

    # features

    def _get_features(self):
        if self._wrappedFeatures is None:
            self._wrappedFeatures = self.featuresClass(wrap=self.naked().features)
        return self._wrappedFeatures

    # lib

    def _get_lib(self):
        if self._wrappedLib is None:
            self._wrappedLib = self.libClass(wrap=self.naked().lib)
        return self._wrappedLib

    # ------
    # Layers
    # ------

    def _get_layers(self, **kwargs):
        return [self.layerClass(wrap=layer) for layer in self.naked().layers]

    # order

    def _get_layerOrder(self, **kwargs):
        return self.naked().layers.layerOrder

    def _set_layerOrder(self, value, **kwargs):
        self.naked().layers.layerOrder = value

    # default layer

    def _get_defaultLayer(self):
        return self.naked().layers.defaultLayer.name

    def _set_defaultLayer(self, value, **kwargs):
        for layer in self.layers:
            if layer.name == value:
                break
        layer = layer.naked()
        self.naked().layers.defaultLayer = layer

    # new

    def _newLayer(self, name, color, **kwargs):
        layers = self.naked().layers
        layer = layers.newLayer(name)
        layer.color = color
        return self.layerClass(wrap=layer)

    # remove

    def _removeLayer(self, name, **kwargs):
        layers = self.naked().layers
        del layers[name]

    # ------
    # Glyphs
    # ------

    def _get_glyphOrder(self):
        return self.naked().glyphOrder

    def _set_glyphOrder(self, value):
        self.naked().glyphOrder = value

    # ----------
    # Guidelines
    # ----------

    def _lenGuidelines(self, **kwargs):
        return len(self.naked().guidelines)

    def _getGuideline(self, index, **kwargs):
        guideline = self.naked().guidelines[index]
        return self.guidelineClass(guideline)

    def _appendGuideline(self, position, angle, name=None, color=None, **kwargs):
        guideline = self.guidelineClass().naked()
        guideline.x = position[0]
        guideline.y = position[1]
        guideline.name = name
        guideline.color = color
        self.naked().appendGuideline(guideline)
        return self.guidelineClass(guideline)

    def _removeGuideline(self, index, **kwargs):
        guideline = self.naked().guidelines[index]
        self.naked().removeGuideline(guideline)
