from __future__ import annotations
from typing import Any, Optional, Union
from collections.abc import ItemsView

import defcon
from fontParts.base.annotations import PairCollectionType
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

    def _find(
        self, pair: PairCollectionType[str], default: Optional[Union[int, float]] = 0
    ) -> int:
        return self.naked().find(pair, default)
