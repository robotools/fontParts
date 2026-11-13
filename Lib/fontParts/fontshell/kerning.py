from __future__ import annotations
from typing import Any
from collections.abc import ItemsView

import defcon
from fontParts.base.annotations import KerningPairLike
from fontParts.base import BaseKerning
from fontParts.fontshell.base import RBaseObject


class RKerning(RBaseObject, BaseKerning):
    wrapClass = defcon.Kerning

    def _items(self) -> ItemsView[str, int]:
        return self.naked().items()

    def _contains(self, key: str) -> bool:
        return key in self.naked()

    def _setItem(self, key: str, value: int) -> None:
        self.naked()[key] = value

    def _getItem(self, key: str) -> Any:
        return self.naked()[key]

    def _delItem(self, key: str) -> None:
        del self.naked()[key]

    def _round(self, multiple: int) -> None:
        super()._round(multiple)
        # defcon skips item assignments that are numerically equal, even if the
        # types differ. Keep out-of-range floats serializable as plist reals.
        rounded = {
            pair: int(value)
            for pair, value in self.items()
            if isinstance(value, float) and -(1 << 63) <= value < (1 << 64)
        }
        if rounded:
            self.naked().update(rounded)

    def _find(self, pair: KerningPairLike, default: int | float | None = 0) -> int:
        return self.naked().find(pair, default)
