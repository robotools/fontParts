from __future__ import annotations
from typing import Optional

import defcon
from fontParts.base import BaseGuideline
from fontParts.base.annotations import (
    QuadrupleType,
    QuadrupleCollectionType,
    IntFloatType,
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

    # --------
    # Position
    # --------

    # x

    def _get_x(self) -> float:
        return self.naked().x

    def _set_x(self, value: float) -> None:
        self.naked().x = value

    # y

    def _get_y(self) -> float:
        return self.naked().y

    def _set_y(self, value: float) -> None:
        self.naked().y = value

    # angle

    def _get_angle(self) -> float:
        return self.naked().angle

    def _set_angle(self, value: Optional[IntFloatType]) -> None:
        self.naked().angle = value

    # --------------
    # Identification
    # --------------

    # identifier

    def _get_identifier(self) -> Optional[str]:
        return self.naked().identifier

    def _getIdentifier(self) -> str:
        return self.naked().generateIdentifier()

    def _setIdentifier(self, value: str) -> None:
        self.naked().identifier = value

    # name

    def _get_name(self) -> Optional[str]:
        return self.naked().name

    def _set_name(self, value: Optional[str]) -> None:
        self.naked().name = value

    # color

    def _get_color(self) -> Optional[QuadrupleType[float]]:
        value = self.naked().color
        if value is not None:
            value = tuple(value)
        return value

    def _set_color(
        self, value: Optional[QuadrupleCollectionType[IntFloatType]]
    ) -> None:
        self.naked().color = value
