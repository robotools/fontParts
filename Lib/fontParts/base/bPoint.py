from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Tuple

from fontParts.base import normalizers
from fontParts.base.base import (BaseObject, IdentifierMixin, SelectionMixin,
                                 TransformationMixin, dynamicProperty,
                                 reference)
from fontParts.base.deprecated import DeprecatedBPoint, RemovedBPoint
from fontParts.base.errors import FontPartsError
from fontTools.misc import transform

if TYPE_CHECKING:
    from fontParts.base.annotations import (CoordinateType, IntFloatType,
                                            TransformationMatrixType)
    from fontParts.base.contour import BaseContour
    from fontParts.base.font import BaseFont
    from fontParts.base.glyph import BaseGlyph
    from fontParts.base.layer import BaseLayer
    from fontParts.base.point import BasePoint
    from fontParts.base.segment import BaseSegment

class BaseBPoint(
                 BaseObject,
                 TransformationMixin,
                 SelectionMixin,
                 DeprecatedBPoint,
                 IdentifierMixin,
                 RemovedBPoint
                 ):

    def _reprContents(self) -> List[str]:
        contents = [
            "%s" % self.type,
            "anchor='({x}, {y})'".format(x=self.anchor[0], y=self.anchor[1]),
        ]
        return contents

    def _setPoint(self, point: BasePoint) -> None:
        if hasattr(self, "_point"):
            raise AssertionError("point for bPoint already set")
        self._point = point

    def __eq__(self, other):
        if hasattr(other, "_point"):
            return self._point == other._point
        return NotImplemented

    # this class should not be used in hashable
    # collections since it is dynamically generated.

    __hash__ = None

    # -------
    # Parents
    # -------

    # identifier

    def _get_identifier(self):
        """
        Subclasses may override this method.
        """
        return self._point.identifier

    def _getIdentifier(self):
        """
        Subclasses may override this method.
        """
        return self._point.getIdentifier()

    # Segment

    _segment: dynamicProperty = dynamicProperty("base_segment")

    def _get_base_segment(self) -> Optional[BaseSegment]:
        point = self._point
        for segment in self.contour.segments:
            if segment.onCurve == point:
                return segment
        return None

    _nextSegment: dynamicProperty = dynamicProperty("base_nextSegment")

    def _get_base_nextSegment(self) -> Optional[BaseSegment]:
        contour = self.contour
        if contour is None:
            return None
        segments = contour.segments
        segment = self._segment
        i = segments.index(segment) + 1
        if i >= len(segments):
            i = i % len(segments)
        nextSegment = segments[i]
        return nextSegment

    # Contour

    _contour: Optional[BaseContour] = None

    contour = dynamicProperty("contour", "The bPoint's parent contour.")

    def _get_contour(self) -> Optional[BaseContour]:
        if self._contour is None:
            return None
        return self._contour()

    def _set_contour(self, contour: BaseContour) -> None:
        if self._contour is not None:
            raise AssertionError("contour for bPoint already set")
        if contour is not None:
            contour = reference(contour)
        self._contour = contour

    # Glyph

    glyph: dynamicProperty = dynamicProperty("glyph", "The bPoint's parent glyph.")

    def _get_glyph(self) -> Optional[BaseGlyph]:
        if self._contour is None:
            return None
        return self.contour.glyph

    # Layer

    layer: dynamicProperty = dynamicProperty("layer", "The bPoint's parent layer.")

    def _get_layer(self) -> Optional[BaseLayer]:
        if self._contour is None:
            return None
        return self.glyph.layer

    # Font

    font: dynamicProperty = dynamicProperty("font", "The bPoint's parent font.")

    def _get_font(self) -> Optional[BaseFont]:
        if self._contour is None:
            return None
        return self.glyph.font

    # ----------
    # Attributes
    # ----------

    # anchor

    anchor: dynamicProperty = dynamicProperty("base_anchor", "The anchor point.")

    def _get_base_anchor(self):
        value = self._get_anchor()
        value = normalizers.normalizeCoordinateTuple(value)
        return value

    def _set_base_anchor(self, value):
        value = normalizers.normalizeCoordinateTuple(value)
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

    bcpIn: dynamicProperty = dynamicProperty("base_bcpIn", "The incoming off curve.")

    def _get_base_bcpIn(self) -> CoordinateType:
        value = self._get_bcpIn()
        value = normalizers.normalizeCoordinateTuple(value)
        return value

    def _set_base_bcpIn(self, value: CoordinateType) -> None:
        value = normalizers.normalizeCoordinateTuple(value)
        self._set_bcpIn(value)

    def _get_bcpIn(self) -> CoordinateType:
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

    def _set_bcpIn(self, value: CoordinateType) -> None:
        """
        Subclasses may override this method.
        """
        x, y = absoluteBCPIn(self.anchor, value)
        segment = self._segment
        if segment.type == "move" and value != (0, 0):
            raise FontPartsError(("Cannot set the bcpIn for the first "
                                  "point in an open contour.")
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
                offCurves = segment.offCurve
                offCurves[-1].x = x
                offCurves[-1].y = y

    # bcp out

    bcpOut: dynamicProperty = dynamicProperty("base_bcpOut", "The outgoing off curve.")

    def _get_base_bcpOut(self) -> CoordinateType:
        value = self._get_bcpOut()
        value = normalizers.normalizeCoordinateTuple(value)
        return value

    def _set_base_bcpOut(self, value: CoordinateType) -> None:
        value = normalizers.normalizeCoordinateTuple(value)
        self._set_bcpOut(value)

    def _get_bcpOut(self) -> CoordinateType:
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

    def _set_bcpOut(self, value: CoordinateType) -> None:
        """
        Subclasses may override this method.
        """
        x, y = absoluteBCPOut(self.anchor, value)
        segment = self._segment
        nextSegment = self._nextSegment
        if nextSegment.type == "move" and value != (0, 0):
            raise FontPartsError(("Cannot set the bcpOut for the last "
                                  "point in an open contour.")
                                 )
        else:
            offCurves = nextSegment.offCurve
            if offCurves:
                # if the off curves are located at the anchor coordinates
                # we can switch to a "line" segment type
                if value == (0, 0) and self.bcpIn == (0, 0):
                    segment.type = "line"
                    segment.smooth = False
                else:
                    offCurves[0].x = x
                    offCurves[0].y = y
            elif value != (0, 0):
                nextSegment.type = "curve"
                offCurves = nextSegment.offCurve
                offCurves[0].x = x
                offCurves[0].y = y

    # type

    type: dynamicProperty = dynamicProperty("base_type", "The bPoint type.")

    def _get_base_type(self) -> Optional[str]:
        value = self._get_type()
        value = normalizers.normalizeBPointType(value)
        return value

    def _set_base_type(self, value: str) -> None:
        value = normalizers.normalizeBPointType(value)
        self._set_type(value)

    def _get_type(self) -> Optional[str]:
        """
        Subclasses may override this method.
        """
        point = self._point
        typ = point.type
        bType = None
        if point.smooth:
            if typ == "curve":
                bType = "curve"
            elif typ == "line" or typ == "move":
                nextSegment = self._nextSegment
                if nextSegment is not None and nextSegment.type == "curve":
                    bType = "curve"
                else:
                    bType = "corner"
        elif typ in ("move", "line", "curve"):
            bType = "corner"

        if bType is None:
            raise FontPartsError("A %s point can not be converted to a bPoint."
                                         % typ)
        return bType

    def _set_type(self, value: str) -> None:
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

    index: dynamicProperty = dynamicProperty("index",
                            ("The index of the bPoint within the ordered "
                             "list of the parent contour's bPoints. None "
                             "if the bPoint does not belong to a contour.")
                            )

    def _get_base_index(self) -> Optional[int]:
        if self.contour is None:
            return None
        value = self._get_index()
        value = normalizers.normalizeIndex(value)
        return value

    def _get_index(self) -> Optional[int]:
        """
        Subclasses may override this method.
        """
        contour = self.contour
        value = contour.bPoints.index(self)
        return value

    # --------------
    # Transformation
    # --------------
    def _transformBy(self, matrix: TransformationMatrixType, **kwargs: Any) -> None:
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

    # ----
    # Misc
    # ----

    def round(self) -> None:
        """
        Round coordinates.
        """
        x, y = self.anchor
        self.anchor = (normalizers.normalizeVisualRounding(x),
                       normalizers.normalizeVisualRounding(y))
        x, y = self.bcpIn
        self.bcpIn = (normalizers.normalizeVisualRounding(x),
                      normalizers.normalizeVisualRounding(y))
        x, y = self.bcpOut
        self.bcpOut = (normalizers.normalizeVisualRounding(x),
                       normalizers.normalizeVisualRounding(y))


def relativeBCPIn(anchor: CoordinateType, BCPIn: CoordinateType) -> CoordinateType:
    """convert absolute incoming bcp value to a relative value"""
    return (BCPIn[0] - anchor[0], BCPIn[1] - anchor[1])


def absoluteBCPIn(anchor: CoordinateType, BCPIn: CoordinateType) -> CoordinateType:
    """convert relative incoming bcp value to an absolute value"""
    return (BCPIn[0] + anchor[0], BCPIn[1] + anchor[1])


def relativeBCPOut(anchor: CoordinateType, BCPOut: CoordinateType) -> CoordinateType:
    """convert absolute outgoing bcp value to a relative value"""
    return (BCPOut[0] - anchor[0], BCPOut[1] - anchor[1])


def absoluteBCPOut(anchor: CoordinateType, BCPOut: CoordinateType) -> CoordinateType:
    """convert relative outgoing bcp value to an absolute value"""
    return (BCPOut[0] + anchor[0], BCPOut[1] + anchor[1])
