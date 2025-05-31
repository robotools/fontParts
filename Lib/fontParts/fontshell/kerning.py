from __future__ import annotations
from typing import Any
from collections.abc import ItemsView

import defcon
from fontParts.base.annotations import PairCollectionType
from fontParts.base import BaseKerning
from fontParts.fontshell.base import RBaseObject


class RKerning(RBaseObject, BaseKerning):
    wrapClass = defcon.Kerning

    def _getNaked(self) -> defcon.Kerning:
        kerning = self.naked()
        if kerning is None:
            raise ValueError("Kerning cannot be None.")
        return kerning

    def _items(self) -> ItemsView[str, int]:
        return self._getNaked().items()

    def _contains(self, key: str) -> bool:
        return key in self._getNaked()

    def _setItem(self, key: str, value: int) -> None:
        self._getNaked()[key] = value

    def _getItem(self, key: str) -> Any:
        return self._getNaked()[key]

    def _delItem(self, key: str) -> None:
        del self._getNaked()[key]

    def _find(self, pair: PairCollectionType[str], default: int = 0) -> int:
        return self._getNaked().find(pair, default)
