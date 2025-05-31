from __future__ import annotations
from typing import Any

import defcon
from fontParts.base import BaseInfo
from fontParts.fontshell.base import RBaseObject


class RInfo(RBaseObject, BaseInfo):
    wrapClass = defcon.Info

    def _getAttr(self, attr: str) -> Any:
        return getattr(self.naked(), attr)

    def _setAttr(self, attr: str, value: Any) -> None:
        setattr(self.naked(), attr, value)
