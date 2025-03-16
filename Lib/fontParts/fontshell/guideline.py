from __future__ import annotations
from typing import Optional

import defcon
from fontParts.base import BaseGuideline
from fontParts.base.annotations import (
    QuadrupleType,
    QuadrupleCollectionType,
    IntFloatType
)
from fontParts.fontshell.base import RBaseObject


class RGuideline(RBaseObject, BaseGuideline):
    wrapClass = defcon.Guideline

    def _init(self, pathOrObject: Optional[defcon.Guideline] = None) -> None:
        if self.wrapClass is not None:
            if pathOrObject is None:
                pathOrObject = self.wrapClass()
                if pathOrObject is not None:
                    pathOrObject.x = 0
                    pathOrObject.y = 0
                    pathOrObject.angle = 0
            super(RGuideline, self)._init(pathOrObject=pathOrObject)

    def _getNaked(self) -> defcon.Guideline:
        guideline = self.naked()
        if guideline is None:
            raise ValueError("Guideline cannot be None.")
        return guideline

    # --------
    # Position
    # --------

    # x

    def _get_x(self) -> float:
        return self._getNaked().x

    def _set_x(self, value: float) -> None:
        self._getNaked().x = value

    # y

    def _get_y(self) -> float:
        return self._getNaked().y

    def _set_y(self, value: float) -> None:
        self._getNaked().y = value

    # angle

    def _get_angle(self) -> float:
        return self._getNaked().angle

    def _set_angle(self, value: Optional[IntFloatType]) -> None:
        self._getNaked().angle = value

    # --------------
    # Identification
    # --------------

    # identifier

    def _get_identifier(self) -> Optional[str]:
        return self._getNaked().identifier

    def _getIdentifier(self) -> str:
        return self._getNaked().generateIdentifier()

    def _setIdentifier(self, value: str) -> None:
        self._getNaked().identifier = value

    # name

    def _get_name(self) -> Optional[str]:
        return self._getNaked().name

    def _set_name(self, value: Optional[str]) -> None:
        self._getNaked().name = value

    # color

    def _get_color(self) -> Optional[QuadrupleType[float]]:
        value = self._getNaked().color
        if value is not None:
            value = tuple(value)
        return value

    def _set_color(
            self,
            value: Optional[QuadrupleCollectionType[IntFloatType]]
    ) -> None:
        self._getNaked().color = value
