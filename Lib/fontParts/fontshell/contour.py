from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Any

import defcon
from fontParts.base import BaseContour
from fontParts.base.annotations import PairCollectionType, QuadrupleType, IntFloatType
from fontParts.fontshell.base import RBaseObject
from fontParts.fontshell.point import RPoint
from fontParts.fontshell.segment import RSegment
from fontParts.fontshell.bPoint import RBPoint

if TYPE_CHECKING:
    from fontParts.base import BasePoint


class RContour(RBaseObject, BaseContour):
    wrapClass = defcon.Contour
    pointClass = RPoint
    segmentClass = RSegment
    bPointClass = RBPoint

    # --------------
    # Identification
    # --------------

    # index

    def _set_index(self, value: int) -> None:
        contour = self.naked()
        glyph = contour.glyph
        if glyph is not None:
            glyph.removeContour(contour)
            glyph.insertContour(value, contour)

    # identifier

    def _get_identifier(self) -> Optional[str]:
        return self.naked().identifier

    def _getIdentifier(self) -> str:
        return self.naked().generateIdentifier()

    def _getIdentifierForPoint(self, point: BasePoint) -> str:
        contour = self.naked()
        nakedPoint = point.naked()
        return contour.generateIdentifierForPoint(nakedPoint)

    # ----
    # Open
    # ----

    def _get_open(self) -> bool:
        return self.naked().open

    # ------
    # Bounds
    # ------

    def _get_bounds(self) -> Optional[QuadrupleType[float]]:
        return self.naked().bounds

    # ----
    # Area
    # ----

    def _get_area(self) -> Optional[float]:
        return self.naked().area

    # ---------
    # Direction
    # ---------

    def _get_clockwise(self) -> bool:
        return self.naked().clockwise

    def _reverse(self, **kwargs: Any) -> None:
        self.naked().reverse()

    # ------------------------
    # Point and Contour Inside
    # ------------------------

    def _pointInside(self, point: PairCollectionType[IntFloatType]) -> bool:
        return self.naked().pointInside(point)

    def _contourInside(self, otherContour: BaseContour) -> bool:
        return self.naked().contourInside(otherContour.naked(), segmentLength=5)

    # ------
    # Points
    # ------

    def _lenPoints(self, **kwargs: Any) -> int:
        return len(self.naked())

    def _getPoint(self, index: int, **kwargs: Any) -> RPoint:
        contour = self.naked()
        point = contour[index]
        return self.pointClass(point)

    def _insertPoint(
        self,
        index: int,
        position: PairCollectionType[IntFloatType],
        type: Optional[str] = None,
        smooth: Optional[bool] = None,
        name: Optional[str] = None,
        identifier: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        point = self.pointClass()
        point.x = position[0]
        point.y = position[1]
        point.type = type
        point.smooth = smooth
        point.name = name
        nakedPoint = point.naked()
        if nakedPoint is not None:
            point = nakedPoint
        point.identifier = identifier
        contour = self.naked()
        contour.insertPoint(index, point)

    def _removePoint(self, index: int, preserveCurve: bool, **kwargs: Any) -> None:
        contour = self.naked()
        point = contour[index]
        contour.removePoint(point)
