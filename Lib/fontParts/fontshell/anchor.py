from __future__ import annotations
from typing import Optional

import defcon
from fontParts.base import BaseAnchor
from fontParts.base.annotations import (
    QuadrupleType,
    QuadrupleCollectionType,
    IntFloatType,
)
from fontParts.fontshell.base import RBaseObject


class RAnchor(RBaseObject, BaseAnchor):
    wrapClass = defcon.Anchor

    def _init(self, pathOrObject: defcon.Anchor | None = None) -> None:
        if self.wrapClass is not None:
            if pathOrObject is None:
                pathOrObject = self.wrapClass()
                pathOrObject.x = 0
                pathOrObject.y = 0
            super()._init(pathOrObject=pathOrObject)

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

    # --------------
    # Identification
    # --------------

    # identifier

    def _get_identifier(self) -> str | None:
        return self.naked().identifier

    def _getIdentifier(self) -> str:
        return self.naked().generateIdentifier()

    def _setIdentifier(self, value: str) -> None:
        self.naked().identifier = value

    # name

    def _get_name(self) -> str | None:
        return self.naked().name

    def _set_name(self, value: str | None) -> None:
        self.naked().name = value

    # color

    def _get_color(self) -> QuadrupleType[float] | None:
        value = self.naked().color
        if value is not None:
            value = tuple(value)
        return value

    def _set_color(
        self, value: QuadrupleCollectionType[IntFloatType] | None
    ) -> None:
        self.naked().color = value
