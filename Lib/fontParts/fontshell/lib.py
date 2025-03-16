from __future__ import annotations
from typing import TYPE_CHECKING, Any

import defcon
from fontParts.base import BaseLib
from fontParts.fontshell.base import RBaseObject

if TYPE_CHECKING:
    from collections.abc import ItemsView


class RLib(RBaseObject, BaseLib):
    wrapClass = defcon.Lib

    def _getNaked(self) -> defcon.Lib:
        lib = self.naked()
        if lib is None:
            raise ValueError("Lib cannot be None.")
        return lib

    def _items(self) -> ItemsView[str, Any]:
        return self._getNaked().items()

    def _contains(self, key: str) -> bool:
        return key in self._getNaked()

    def _setItem(self, key: str, value: Any) -> None:
        self._getNaked()[key] = value

    def _getItem(self, key: str) -> Any:
        return self._getNaked()[key]

    def _delItem(self, key: str) -> None:
        del self._getNaked()[key]
