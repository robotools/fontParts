from fontParts.base import BaseGlyph
from fontParts.base.errors import FontPartsError
from fontParts.fontshell.base import RBaseObject
from fontParts.opentype.contour import OTContour
from fontParts.opentype.component import OTComponent

import fontTools.ttLib.tables._g_l_y_f

class OTGlyph(RBaseObject, BaseGlyph):
    wrapClass = fontTools.ttLib.tables._g_l_y_f.Glyph
    contourClass = OTContour
    componentClass = OTComponent

    def _init(self, *args, **kwargs):
        self._wrapped = kwargs["wrap"]
        self._name = kwargs["name"]

    def changed(self, *args, **kwargs):
        print("Notified of change")
        print(args)
        print(kwargs)

    # --------------
    # Identification
    # --------------

    # Name

    def _get_name(self):
        return self._name

    def _set_name(self, value):
        self._name = value

    # Unicodes

    def _get_unicodes(self):
        return list(self.font.naked()["cmap"].buildReversed()[self._named])

    def _set_unicodes(self, value):
        # XXX
        self.naked().unicodes = value

    # -------
    # Metrics
    # -------

    # horizontal

    def _get_width(self):
        return self.font.naked()["hmtx"][self._name][0]

    def _set_width(self, value):
        self.font.naked()["hmtx"][self._name] = (value, self.font.naked()["hmtx"][self._name][1])

    def _get_leftMargin(self):
        return self.font.naked()["hmtx"][self._name][1]

    def _set_leftMargin(self, value):
        self.font.naked()["hmtx"][self._name] = (self.font.naked()["hmtx"][self._name][0], value)
        # XXX Change points

    def _get_rightMargin(self):
        return self.width - self.bounds[2]

    def _set_rightMargin(self, value):
        newWidth = self.bounds[2] + value
        self._set_width(newWidth)

    # vertical
    def _get_height(self):
        return self.font.naked()["hhea"].ascent
        # Or maybe self.font.naked()["OS/2"].usWinAscent

    # ------
    # Bounds
    # ------

    def _get_bounds(self):
        naked = self.naked()
        return (naked.xMin, naked.yMin, naked.xMax, naked.yMax)

    # ----
    # Area
    # ----
    # XXX
    def _get_area(self):
        return self.naked().area

    # ----
    # Pens
    # ----
    # XXX

    def getPen(self):
        return self.naked().getPen()

    def getPointPen(self):
        return self.naked().getPointPen()

    # -----------------------------------------
    # Contour, Component and Anchor Interaction
    # -----------------------------------------

    # Contours

    def _lenContours(self, **kwargs):
        return max(self.naked().numberOfContours,0)

    def _getContour(self, index, **kwargs):
        glyph = self.naked()
        endPt = glyph.endPtsOfContours[index]
        if index > 0:
            startPt = glyph.endPtsOfContours[index-1]
        else:
            startPt = 0
        contour = [
            {"x": glyph.coordinates[j][0],
             "y": glyph.coordinates[j][1],
             "on": glyph.flags[j]
            } for j in range(startPt, endPt)
        ]
        return self.contourClass(wrap=contour, index=index)

    def _removeContour(self, index, **kwargs):
        glyph = self.naked()
        contour = glyph[index]
        glyph.removeContour(contour)

    def _correctDirection(self, trueType=False, **kwargs):
        self.naked().correctContourDirection(trueType=trueType)

    # Components

    def _lenComponents(self, **kwargs):
        if hasattr(self.naked(),"components"):
            return len(self.naked().components)
        return 0

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

    def _appendAnchor(self, name, position=None, color=None, identifier=None, **kwargs):
        glyph = self.naked()
        anchor = self.anchorClass().naked()
        anchor.name = name
        anchor.x = position[0]
        anchor.y = position[1]
        anchor.color = color
        anchor.identifier = identifier
        glyph.appendAnchor(anchor)
        wrapped = self.anchorClass(anchor)
        wrapped.glyph = self
        return wrapped

    def _removeAnchor(self, index, **kwargs):
        glyph = self.naked()
        anchor = glyph.anchors[index]
        glyph.removeAnchor(anchor)

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

    def _loadFromGLIF(self, glifData):
        try:
            readGlyphFromString(
                aString=glifData,
                glyphObject=self.naked(),
                pointPen=self.getPointPen()
            )
        except GlifLibError:
            raise FontPartsError("Not valid glif data")

    def _dumpToGLIF(self, glyphFormatVersion):
        glyph = self.naked()
        return writeGlyphToString(
            glyphName=glyph.name,
            glyphObject=glyph,
            drawPointsFunc=glyph.drawPoints,
            formatVersion=glyphFormatVersion
        )
