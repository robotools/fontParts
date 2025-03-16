from __future__ import annotations
from typing import Optional

import defcon
from fontParts.base import BaseFeatures
from fontParts.fontshell.base import RBaseObject


class RFeatures(RBaseObject, BaseFeatures):
    wrapClass = defcon.Features

    def _getNaked(self) -> defcon.Features:
        freatures = self.naked()
        if freatures is None:
            raise ValueError("Features cannot be None.")
        return freatures

    def _get_text(self) -> Optional[str]:
        features = self._getNaked()
        return features.text

    def _set_text(self, value: str) -> None:
        features = self._getNaked()
        features.text = value
