from fontParts.base import BaseGlyph
from fontParts.base.errors import FontPartsError
from fontParts.fontshell.base import RBaseObject
from fontParts.opentype.contour import OTContour
from fontParts.opentype.component import OTComponent
# from fontParts.fontshell.point import RPoint
import defcon
from fontTools.pens.areaPen import AreaPen
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
        return list(self.font.naked()["cmap"].buildReversed()[self._name])

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
        oldLSB = self.font.naked()["hmtx"][self._name][1]
        delta = value - oldLSB
        oldWidth = self.width
        self.font.naked()["hmtx"][self._name] = (self.font.naked()["hmtx"][self._name][0], value)
        self.move((delta,0))
        self.width = oldWidth + delta

    def _get_rightMargin(self):
        return self.width - self.bounds[2]

    def _set_rightMargin(self, value):
        newWidth = self.bounds[2] + value
        self._set_width(newWidth)

    # vertical
    def _get_height(self):
        return self.font.naked()["hhea"].ascent
        # Or maybe self.font.naked()["OS/2"].usWinAscent

    def _set_height(self, value):
        self.font.naked()["hhea"].ascent = value

    # ------
    # Bounds
    # ------

    def _get_bounds(self):
        naked = self.naked()
        return (naked.xMin, naked.yMin, naked.xMax, naked.yMax)

    # ----
    # Area
    # ----
    def _get_area(self):
        pen = AreaPen()
        self.naked().draw(pen, self.font.naked()["glyf"])
        return abs(pen.value)

    # ----
    # Pens
    # ----

    def getPen(self):
        from fontTools.pens.pointPen import SegmentToPointPen
        return SegmentToPointPen(self.getPointPen())

    def getPointPen(self):
        from fontTools.pens.pointPen import BasePointToSegmentPen
        return BasePointToSegmentPen()
        # return self.naked().getPointPen()

    # -----------------------------------------
    # Contour, Component and Anchor Interaction
    # -----------------------------------------

    # Contours

    def _contourStartAndEnd(self,index):
        glyph = self.naked()
        endPt = glyph.endPtsOfContours[index]
        if index > 0:
            startPt = glyph.endPtsOfContours[index-1]
        else:
            startPt = 0
        return startPt, endPt

    def _lenContours(self, **kwargs):
        return max(self.naked().numberOfContours,0)

    def _getContour(self, index, **kwargs):
        glyph = self.naked()
        startPt, endPt = self._contourStartAndEnd(index)
        contour = []
        for j in range(startPt, endPt+1):
            coords = (glyph.coordinates[j][0], glyph.coordinates[j][1])
            flags = glyph.flags[j] == 1
            t = "offcurve"
            if flags == 1:
                if (j == startPt and glyph.flags[endPt] == 1) or (j != startPt and contour[-1].segmentType != "offcurve"):
                    t = "line"
                else:
                    t = "curve"
            contour.append(defcon.Point(coords,segmentType = t))
        return self.contourClass(wrap=contour, index=index)

    def _setContour(self,index,contour):
        old = self._getContour(index)
        clist = contour.naked()
        if len(old.naked()) != len(clist):
            self.raiseNotImplementedError()
        glyph = self.naked()
        startPt, endPt = self._contourStartAndEnd(index)
        for j in range(0,len(clist)):
            glyph.coordinates[j+startPt] = (clist[j].x,clist[j].y)
            glyph.flags[j+startPt] = int(clist[j].segmentType != "offcurve")
        glyph.recalcBounds(self.font.naked()["glyf"])

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

    def _removeComponent(self, index, **kwargs): # XXX
        glyph = self.naked()
        component = glyph.components[index]
        glyph.removeComponent(component)

    # Guidelines
    def _lenGuidelines(self, **kwargs):
        return 0 # len(self.naked().anchors)

    # Anchors

    def _lenAnchors(self, **kwargs):
        return 0 # len(self.naked().anchors)

    def _getAnchor(self, index, **kwargs):
        return None
        # glyph = self.naked()
        # anchor = glyph.anchors[index]
        # return self.anchorClass(anchor)

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
