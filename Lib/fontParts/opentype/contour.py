from fontParts.base import BaseContour
from fontParts.fontshell.base import RBaseObject
from fontParts.fontshell.point import RPoint
from fontParts.fontshell.segment import RSegment
from fontParts.fontshell.bPoint import RBPoint

class OTPoint(RPoint):
    def _postChangeNotification(self):
        contour = self.contour
        if contour is None:
            return
        contour._pointsChanged()

class OTContour(RBaseObject, BaseContour):
    pointClass = OTPoint
    segmentClass = RSegment
    bPointClass = RBPoint

    def _init(self, *args, **kwargs):
        self._wrapped = kwargs["wrap"]
        self._index = kwargs["index"]

    def _pointsChanged(self):
        self.glyph._setContour(self._index,self)

    # --------------
    # Identification
    # --------------

    # index

    def _set_index(self, value):
        self._index = value

    # identifier - OT fonts don't do this.

    def _get_identifier(self):
        return None

    def _getIdentifier(self):
        return None

    def _getIdentifierforPoint(self, point):
        return None

    # ----
    # Open
    # ----

    def _get_open(self):
        return self.naked().open

    # ------
    # Bounds
    # ------

    def _get_bounds(self):
        return self.naked().bounds

    # ----
    # Area
    # ----

    def _get_area(self):
        return self.naked().area

    # ---------
    # Direction
    # ---------

    def _get_clockwise(self):
        return self.naked().clockwise

    def _reverseContour(self, **kwargs):
        self.naked().reverse()

    # ------------------------
    # Point and Contour Inside
    # ------------------------

    def _pointInside(self, point):
        return self.naked().pointInside(point)

    def _contourInside(self, otherContour):
        return self.naked().contourInside(otherContour.naked(), segmentLength=5)

    # ------
    # Points
    # ------

    def _lenPoints(self, **kwargs):
        return len(self.naked())

    def _getPoint(self, index, **kwargs):
        contour = self.naked()
        point = contour[index]
        return self.pointClass(point)

    def _insertPoint(self, index, position, type=None, smooth=None,
                     name=None, identifier=None, **kwargs):
        point = self.pointClass()
        point.x = position[0]
        point.y = position[1]
        point.type = type
        point.smooth = smooth
        point.name = name
        point = point.naked()
        point.identifier = identifier
        self.naked().insertPoint(index, point)

    def _removePoint(self, index, preserveCurve, **kwargs):
        contour = self.naked()
        point = contour[index]
        contour.removePoint(point)
