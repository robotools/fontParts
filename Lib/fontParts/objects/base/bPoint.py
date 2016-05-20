import weakref
from fontTools.misc import transform

from .errors import FontPartsError
from .base import BaseObject, TransformationMixin, dynamicProperty
import validators

class BaseBPoint(BaseObject, TransformationMixin):

    def _setPoint(self, point):
        assert not hasattr(self, "_point")
        self._point = point

    def __eq__(self, other):
        if hasattr(other, "_point"):
            return self._point == other._point
        return False

    # -------
    # Parents
    # -------

    def getParent(self):
        """
        This is a backwards compatibility method.
        """
        return self.contour

    # Segment

    _segment = dynamicProperty("base_segment")

    def _get_base_segment(self):
        point = self._point
        for segment in self.contour.segments:
            if segment.onCurve == point:
                return segment

    _nextSegment = dynamicProperty("base_nextSegment")

    def _get_base_nextSegment(self):
        contour = self.contour
        segments = contour.segments
        segment = self._segment
        i = segments.index(segment) + 1
        if i >= len(segments):
            i = i % len(segments)
        nextSegment = segments[i]
        return nextSegment

    # Contour

    _contour = None

    contour = dynamicProperty("contour", "The bPoint's parent contour.")

    def _get_contour(self):
        if self._contour is None:
            return None
        return self._contour()

    def _set_contour(self, contour):
        assert self._contour is None
        if contour is not None:
            contour = weakref.ref(contour)
        self._contour = contour

    # Glyph

    glyph = dynamicProperty("glyph", "The bPoint's parent glyph.")

    def _get_glyph(self):
        if self._glyph is None:
            return None
        return self._glyph()

    # Layer

    layer = dynamicProperty("layer", "The bPoint's parent layer.")

    def _get_layer(self):
        if self._glyph is None:
            return None
        return self.glyph.layer

    # Font

    font = dynamicProperty("font", "The bPoint's parent font.")

    def _get_font(self):
        if self._glyph is None:
            return None
        return self.glyph.font

    # ----------
    # Attributes
    # ----------

    # anchor

    anchor = dynamicProperty("base_anchor", "The anchor point.")

    def _get_base_anchor(self):
        value = self._get_anchor()
        value = validators.validateCoordinateTuple(value)
        return value

    def _set_base_anchor(self, value):
        value = validators.validateCoordinateTuple(value)
        self._set_anchor(value)

    def _get_anchor(self):
        """
        Subclasses may override this method.
        """
        point = self._point
        return (point.x, point.y)

    def _set_anchor(self, value):
        """
        Subclasses may override this method.
        """
        pX, pY = self.anchor
        x, y = value
        dX = x - pX
        dY = y - pY
        self.moveBy((dX, dY))

    # bcp in

    bcpIn = dynamicProperty("base_bcpIn", "The incoming off curve.")

    def _get_base_bcpIn(self):
        value = self._get_bcpIn()
        value = validators.validateCoordinateTuple(value)
        return value

    def _set_base_bcpIn(self, value):
        value = validators.validateCoordinateTuple(value)
        self._set_bcpIn(value)

    def _get_bcpIn(self):
        """
        Subclasses may override this method.
        """
        segment = self._segment
        offCurves = segment.offCurve
        if offCurves:
            bcp = offCurves[-1]
            x, y = relativeBCPIn(self.anchor, (bcp.x, bcp.y))
        else:
            x = y = 0
        return (x, y)

    def _set_bcpIn(self, value):
        """
        Subclasses may override this method.
        """
        x, y = absoluteBCPIn(self.anchor, value)
        segment = self._segment
        if segment.type == "move":
            # the user wants to have a bcp leading into the move.
            if value == (0, 0) and self.bcpOut == (0, 0):
                # we have a straight line between the two anchors.
                pass
            else:
                # we need to insert a new curve segment on top of the move.
                # set the prev segment outgoing bcp to the onCurve.
                contour = self.contour
                prevSegment = contour.segments[-1]
                prevOn = prevSeg.onCurve
                contour.appendSegment(
                    "curve",
                    [(prevOn.x, prevOn.y), (x, y), self.anchor],
                    smooth=False
                )
        else:
            offCurves = segment.offCurve
            if offCurves:
                # if the two off curves are located at the anchor
                # coordinates we can switch to a line segment type.
                if value == (0, 0) and self.bcpOut == (0, 0):
                    segment.type = "line"
                    segment.smooth = False
                else:
                    offCurves[-1].x = x
                    offCurves[-1].y = y
            elif value != (0, 0):
                segment.type = "curve"
                offCurves[-1].x = x
                offCurves[-1].y = y

    # bcp out

    bcpOut = dynamicProperty("base_bcpOut", "The outgoing off curve.")

    def _get_base_bcpOut(self):
        value = self._get_bcpOut()
        value = validators.validateCoordinateTuple(value)
        return value

    def _set_base_bcpOut(self, value):
        value = validators.validateCoordinateTuple(value)
        self._set_bcpOut(value)

    def _get_bcpOut(self):
        """
        Subclasses may override this method.
        """
        nextSegment = self._nextSegment
        offCurves = nextSegment.offCurve
        if offCurves:
            bcp = offCurves[0]
            x, y = relativeBCPOut(self.anchor, (bcp.x, bcp.y))
        else:
            x = y = 0
        return (x, y)

    def _set_bcpOut(self, value):
        """
        Subclasses may override this method.
        """
        x, y = absoluteBCPOut(self.anchor, value)
        segment = self._segment
        nextSegment = self._nextSegment
        if nextSegment.type == "move":
            if value == (0, 0) and self.bcpIn == (0, 0):
                pass
            else:
                # we need to insert a new "curve" segment on top of the move
                contour = self.contour
                nextOn = nextSegment.onCurve
                contour.appendSegment(
                    "curve",
                    [(x, y), (nextOn.x, nextOn.y), (nextOn.x, nextOn.y)],
                    smooth=False
                )
        else:
            offCurves = nextSegment.offCurve
            if offCurves:
                # if the off curves are located at the anchor coordinates
                # we can switch to a "line" segment type
                if value == (0, 0) and self.bcpIn == (0, 0):
                    offCurves.type = "line"
                    offCurves.smooth = False
                else:
                    offCurves[0].x = x
                    offCurves[0].y = y
            elif value != (0, 0):
                nextSegment.type = "curve"
                offCurves[0].x = x
                offCurves[0].y = y

    # type

    type = dynamicProperty("base_type", "The bPoint type.")

    def _get_base_type(self):
        value = self._get_type()
        value = validators.validateBPointType(value)
        return value

    def _set_base_type(self, value):
        value = validators.validateBPointType(value)
        self._set_type(value)

    def _get_type(self):
        """
        Subclasses may override this method.
        """
        point = self._point
        typ = point.type
        if typ == "curve" and point.smooth:
            bType = "curve"
        elif typ in ("move", "line", "curve"):
            bType = "corner"
        else:
            raise FontPartsError("A %s point can not be converted to a bPoint." % typ)
        return bType

    def _set_type(self, value):
        """
        Subclasses may override this method.
        """
        point = self._point
        # convert corner to curve
        if value == "curve" and point.type == "line":
            # This needs to insert off curves without
            # generating unnecessary points in the
            # following segment. The segment object
            # implements this logic, so delegate the
            # change to the corresponding segment.
            segment = self._segment
            segment.type = "curve"
            segment.smooth = True
        # convert curve to corner
        elif value == "corner" and point.type == "curve":
            point.smooth = False

    # --------------
    # Identification
    # --------------

    index = dynamicProperty("index", "The index of the bPoint within the ordered list of the parent contour's bPoints. None if the bPoint does not belong to a contour.")

    def _get_base_index(self):
        if self.contour is None:
            return None
        value = self._get_index()
        value = validators.validateIndex(value)
        return value

    def _get_index(self):
        """
        Subclasses may override this method.
        """
        contour = self.contour
        value = contour.bPoints.index(self)
        return value

    # --------------
    # Transformation
    # --------------

    def _transformBy(self, matrix, origin=None, originOffset=None, **kwargs):
        """
        Subclasses may override this method.
        """
        anchor = self.anchor
        bcpIn = absoluteBCPIn(anchor, self.bcpIn)
        bcpOut = absoluteBCPOut(anchor, self.bcpOut)
        points = [bcpIn, anchor, bcpOut]
        t = transform.Transform(*matrix)
        bcpIn, anchor, bcpOut = t.transformPoints(points)
        x, y = anchor
        self._point.x = x
        self._point.y = y
        self.bcpIn = relativeBCPIn(anchor, bcpIn)
        self.bcpOut = relativeBCPOut(anchor, bcpOut)
        if originOffset != (0, 0):
            self.moveBy(originOffset)

    # ----
    # Misc
    # ----

    def round(self):
        """
        Round coordinates.
        """
        x, y = self.anchor
        self.anchor = (int(round(x)), int(round(y)))
        x, y = self.bcpIn
        self.bcpIn = (int(round(x)), int(round(y)))
        x, y = self.bcpOut
        self.bcpOut = (int(round(x)), int(round(y)))


def relativeBCPIn(anchor, BCPIn):
    """convert absolute incoming bcp value to a relative value"""
    return (BCPIn[0] - anchor[0], BCPIn[1] - anchor[1])

def absoluteBCPIn(anchor, BCPIn):
    """convert relative incoming bcp value to an absolute value"""
    return (BCPIn[0] + anchor[0], BCPIn[1] + anchor[1])

def relativeBCPOut(anchor, BCPOut):
    """convert absolute outgoing bcp value to a relative value"""
    return (BCPOut[0] - anchor[0], BCPOut[1] - anchor[1])

def absoluteBCPOut(anchor, BCPOut):
    """convert relative outgoing bcp value to an absolute value"""
    return (BCPOut[0] + anchor[0], BCPOut[1] + anchor[1])
