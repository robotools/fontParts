from __future__ import annotations
from typing import Optional

import defcon
from fontParts.base import BaseFeatures
from fontParts.fontshell.base import RBaseObject


class RFeatures(RBaseObject, BaseFeatures):
    wrapClass = defcon.Features

    def _get_text(self) -> Optional[str]:
        features = self.naked()
        return features.text

    def _set_text(self, value: Optional[str]) -> None:
        features = self.naked()
        features.text = value
