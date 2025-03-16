from __future__ import annotations
from typing import Optional

import defcon

from fontParts.base.annotations import IntFloatType
from fontParts.base import BasePoint, FontPartsError
from fontParts.fontshell.base import RBaseObject


class RPoint(RBaseObject, BasePoint):
    wrapClass = defcon.Point

    def _init(self, pathOrObject: Optional[defcon.Point] = None) -> None:
        if pathOrObject is None and self.wrapClass is not None:
            pathOrObject = self.wrapClass((0, 0))
        super(RPoint, self)._init(pathOrObject=pathOrObject)

    def _postChangeNotification(self) -> None:
        contour = self.contour
        if contour is None:
            return
        contour.naked().postNotification("Contour.PointsChanged")
        self.changed()

    def changed(self) -> None:
        self.contour.naked().dirty = True

    def _getNaked(self) -> defcon.Point:
        point = self.naked()
        if point is None:
            raise ValueError("Point cannot be None.")
        return point

    # ----------
    # Attributes
    # ----------

    # type

    def _get_type(self) -> str:
        value = self._getNaked().segmentType
        if value is None:
            value = "offcurve"
        return value

    def _set_type(self, value: str) -> None:
        self._getNaked().segmentType = None if value == "offcurve" else value
        self._postChangeNotification()

    # smooth

    def _get_smooth(self) -> bool:
        return self._getNaked().smooth

    def _set_smooth(self, value: bool) -> None:
        self._getNaked().smooth = value
        self._postChangeNotification()

    # x

    def _get_x(self) -> IntFloatType:
        return self._getNaked().x

    def _set_x(self, value: IntFloatType) -> None:
        self._getNaked().x = value
        self._postChangeNotification()

    # y

    def _get_y(self) -> IntFloatType:
        return self._getNaked().y

    def _set_y(self, value: IntFloatType) -> None:
        self._getNaked().y = value
        self._postChangeNotification()

    # --------------
    # Identification
    # --------------

    # name

    def _get_name(self) -> Optional[str]:
        return self._getNaked().name

    def _set_name(self, value: str) -> None:
        self._getNaked().name = value
        self._postChangeNotification()

    # identifier

    def _get_identifier(self) -> Optional[str]:
        return self._getNaked().identifier

    def _getIdentifier(self) -> str:
        point = self._getNaked()
        value = point.identifier
        if value is not None:
            return value
        if self.contour is not None:
            contour = self.contour.naked()
            contour.generateIdentifierForPoint(point)
            value = point.identifier
        else:
            raise FontPartsError(
                (
                    "An identifier can not be generated "
                    "for this point because it does not "
                    "belong to a contour."
                )
            )
        return value
