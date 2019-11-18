from fontParts.base import BaseGlyph
from fontParts.base.errors import FontPartsError
import defcon
from fontTools.pens.areaPen import AreaPen
import fontTools.ttLib.tables._g_l_y_f
from fontTools.ttLib.ttFont import _TTGlyph, _TTGlyphCFF
from fontTools.ttLib.tables._g_l_y_f import GlyphComponent,GlyphCoordinates
from fontTools.pens.recordingPen import RecordingPen
from fontParts.fontshell.ttf.glyph import TTGlyph

class OTGlyph(TTGlyph):
    def _get_bounds(self):
        self._glyphset = self.font.naked().getGlyphSet()
        return self.naked()._glyph.calcBounds(self._glyphset)

    def _lenContours(self, **kwargs):
        self._build_CFF_contour_list()
        return len(self._contourlist)

    def _build_CFF_contour_list(self):
        if self._contourlist is None:
            pen = RecordingPen()
            self.naked().draw(pen)
            contours = pen.value
            lastcontour = []
            self._contourlist = []
            startPt = (0,0)
            lastPt = (0,0)
            index = 0
            for c in contours:
                if c[0] == "moveTo":
                    startPt = c[1][0]
                elif c[0] == "closePath":
                    if startPt != lastPt:
                        lastcontour.append(defcon.Point(startPt,segmentType = "line"))
                    contour = self.contourClass(wrap=lastcontour, index=index)
                    self._contourlist.append(contour)
                    index = index + 1
                    lastcontour = []
                elif c[0] == "curveTo":
                    lastcontour.append(defcon.Point(c[1][0],segmentType = "offcurve"))
                    lastcontour.append(defcon.Point(c[1][1],segmentType = "offcurve"))
                    lastcontour.append(defcon.Point(c[1][2],segmentType = "curve"))
                    lastPt = c[1][2]
                elif c[0] == "lineTo":
                    lastcontour.append(defcon.Point(c[1][0],segmentType = "line"))
                    lastPt = c[1][0]
                elif c[0] == "qCurveTo":
                    self.raiseNotImplementedError()

    def _getContour(self, index, **kwargs):
        self._build_CFF_contour_list()
        return self._contourlist[index]

    def _setContour(self,index,contour):
        self._build_CFF_contour_list()
        self._contourlist[index] = contour
        self._rebuild_CFF_contours()

    def _rebuild_CFF_contours(self):
        cff = self.font.naked()["CFF "].cff
        fontname = cff.keys()[0]
        cffFont = cff[fontname]
        cffFont.decompileAllCharStrings()
        from fontTools.pens.t2CharStringPen import T2CharStringPen
        width = 0 # self.width # Really?
        pen = T2CharStringPen(width, None)
        # ?
        for c in self._contourlist:
            pen.moveTo(c.segments[-1].points[-1])
            for s in c.segments:
                if s.type == "line":
                    pen.lineTo(*s.points)
                elif s.type == "curve" and len(s.points) == 3:
                    pen.curveTo(*s.points)
                elif s.type == "curve" and len(s.points) == 2:
                    pen.qCurveTo(*s.points)
            pen.closePath()
            cs = pen.getCharString()
            # cs.private = self.font.naked()["CFF "].cff.topDictIndex[0].CharStrings[self.name].private
            cs.private = cffFont.Private
            self.font.naked()["CFF "].cff.topDictIndex[0].CharStrings[self.name] = cs

    def _removeContour(self, index, **kwargs):
        self._build_CFF_contour_list()
        self._contourlist.pop(index)
        self._rebuild_CFF_contours()

    def _appendContour(self, contour, offset=None, **kwargs):
        if offset:
            contour = contour.copy()
            contour.moveBy(offset)

        self._build_CFF_contour_list()
        self._contourlist.append(None)
        return self._setContour_CFF(-1,contour)
