import defcon
from fontParts.base import BaseGlyph
from fontParts.base.errors import FontPartsError
from fontParts.nonelab.base import RBaseObject
from fontParts.nonelab.contour import RContour
from fontParts.nonelab.component import RComponent
from fontParts.nonelab.anchor import RAnchor
from fontParts.nonelab.guideline import RGuideline
from fontParts.nonelab.image import RImage
from fontParts.nonelab.lib import RLib
from ufoLib.glifLib import readGlyphFromString, writeGlyphToString


class RGlyph(RBaseObject, BaseGlyph):

    wrapClass = defcon.Glyph
    contourClass = RContour
    componentClass = RComponent
    anchorClass = RAnchor
    guidelineClass = RGuideline
    imageClass = RImage
    libClass = RLib

    # --------------
    # Identification
    # --------------

    # Name

    def _get_name(self):
        return self.naked().name

    def _set_name(self, value):
        self.naked().name = value

    # Unicodes

    def _get_unicodes(self):
        return self.naked().unicodes

    def _set_unicodes(self, value):
        self.naked().unicodes = value

    # -------
    # Metrics
    # -------

    # horizontal

    def _get_width(self):
        return self.naked().width

    def _set_width(self, value):
        self.naked().width = value

    # vertical

    def _get_height(self):
        return self.naked().height

    def _set_height(self, value):
        self.naked().height = value

    # ----
    # Pens
    # ----

    def getPen(self):
        return self.naked().getPen()

    def getPointPen(self):
        return self.naked().getPointPen()

    # -----------------------------------------
    # Contour, Component and Anchor Interaction
    # -----------------------------------------

    # Contours

    def _lenContours(self, **kwargs):
        return len(self.naked())

    def _getContour(self, index, **kwargs):
        glyph = self.naked()
        contour = glyph[index]
        return self.contourClass(contour)

    def _removeContour(self, index, **kwargs):
        glyph = self.naked()
        contour = glyph[index]
        glyph.removeContour(contour)

    # Components

    def _lenComponents(self, **kwargs):
        return len(self.naked().components)

    def _getComponent(self, index, **kwargs):
        glyph = self.naked()
        component = glyph.components[index]
        return self.componentClass(component)

    def _removeComponent(self, index, **kwargs):
        glyph = self.naked()
        component = glyph.components[index]
        glyph.removeComponent(component)

    # Anchors

    def _lenAnchors(self, **kwargs):
        return len(self.naked().anchors)

    def _getAnchor(self, index, **kwargs):
        glyph = self.naked()
        anchor = glyph.anchors[index]
        return self.anchorClass(anchor)

    def _appendAnchor(self, name, position=None, color=None, **kwargs):
        glyph = self.naked()
        anchor = self.anchorClass().naked()
        anchor.name = name
        anchor.x = position[0]
        anchor.y = position[1]
        anchor.color = color
        glyph.appendAnchor(anchor)
        return self.anchorClass(anchor)

    def _removeAnchor(self, index, **kwargs):
        glyph = self.naked()
        anchor = glyph.anchors[index]
        glyph.removeAnchor(anchor)

    # Guidelines

    def _lenGuidelines(self, **kwargs):
        return len(self.naked().guidelines)

    def _getGuideline(self, index, **kwargs):
        glyph = self.naked()
        guideline = glyph.guidelines[index]
        return self.guidelineClass(guideline)

    def _appendGuideline(self, position, angle, name=None, color=None, **kwargs):
        glyph = self.naked()
        guideline = self.guidelineClass().naked()
        guideline.x = position[0]
        guideline.y = position[1]
        guideline.angle = angle
        guideline.name = name
        guideline.color = color
        glyph.appendGuideline(guideline)
        return self.guidelineClass(guideline)

    def _removeGuideline(self, index, **kwargs):
        glyph = self.naked()
        guideline = glyph.guidelines[index]
        glyph.removeGuideline(guideline)

    # -----------------
    # Layer Interaction
    # -----------------

    # new

    def _newLayer(self, name, **kwargs):
        layerName = name
        glyphName = self.name
        font = self.font
        if layerName not in font.layerOrder:
            layer = font.newLayer(layerName)
        else:
            layer = font.getLayer(layerName)
        glyph = layer.newGlyph(glyphName)
        return glyph

    # remove

    def _removeLayer(self, name, **kwargs):
        layerName = name
        glyphName = self.name
        font = self.font
        layer = font.getLayer(layerName)
        layer.removeGlyph(glyphName)

    # -----
    # Image
    # -----

    def _get_image(self):
        image = self.naked().image
        if image is None:
            return None
        return self.imageClass(image)

    def _addImage(self, data, transformation=None, color=None):
        image = self.naked().image
        image = self.imageClass(image)
        image.data = data
        image.transformation = transformation
        image.color = color

    def _clearImage(self):
        self.naked().image = None

    # ----
    # Note
    # ----

    # Mark

    def _get_markColor(self):
        value = self.naked().markColor
        if value is not None:
            value = tuple(value)
        return value

    def _set_markColor(self, value):
        self.naked().markColor = value

    # Note

    def _get_note(self):
        return self.naked().note

    def _set_note(self, value):
        self.naked().note = value

    # -----------
    # Sub-Objects
    # -----------

    # lib

    def _get_lib(self):
        return self.libClass(wrap=self.naked().lib)

    # ---
    # API
    # ---

    def _readGlyphFromString(self, glifData):
        try:
            readGlyphFromString(glifData, glyphObject=self.naked(), pointPen=self.getPointPen())
        except:
            raise FontPartsError("Not valid glif data")

    def _writeGlyphToString(self, glyphFormatVersion):
        glyph = self.naked()
        return writeGlyphToString(glyph.name, glyph, glyph.drawPoints, glyphFormatVersion)
