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

    def _init(self, pathOrObject: Optional[defcon.Anchor] = None) -> None:
        if self.wrapClass is not None:
            if pathOrObject is None:
                pathOrObject = self.wrapClass()
                pathOrObject.x = 0
                pathOrObject.y = 0
            super(RAnchor, self)._init(pathOrObject=pathOrObject)

    def _getNaked(self) -> defcon.Anchor:
        anchor = self.naked()
        if anchor is None:
            raise ValueError("Anchor cannot be None.")
        return anchor

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

    def _set_name(self, value: str) -> None:
        self._getNaked().name = value

    # color

    def _get_color(self) -> Optional[QuadrupleType[float]]:
        return self._getNaked().color

    def _set_color(
        self, value: Optional[QuadrupleCollectionType[IntFloatType]]
    ) -> None:
        self._getNaked().color = value
