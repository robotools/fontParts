from __future__ import annotations
from typing import Optional

import defcon
from fontTools.ufoLib.validators import pngValidator
from fontParts.base import BaseImage, FontPartsError
from fontParts.base.annotations import (
    QuadrupleType,
    SextupleType,
    QuadrupleCollectionType,
    SextupleCollectionType,
    IntFloatType,
)
from fontParts.fontshell.base import RBaseObject


class RImage(RBaseObject, BaseImage):
    wrapClass = defcon.Image
    _orphanData: Optional[bytes] = None
    _orphanColor: Optional[QuadrupleCollectionType[IntFloatType]] = None

    # ----------
    # Attributes
    # ----------

    # Transformation

    def _get_transformation(self) -> SextupleType[float]:
        return self.naked().transformation

    def _set_transformation(self, value: SextupleCollectionType[float]) -> None:
        self.naked().transformation = value

    # Color

    def _get_color(self) -> Optional[QuadrupleType[float]]:
        if self.font is None and self._orphanColor is not None:
            r, g, b, a = self._orphanColor
            return (r, g, b, a)
        value = self.naked().color
        if value is not None:
            value = tuple(value)
        return value

    def _set_color(
        self, value: Optional[QuadrupleCollectionType[IntFloatType]]
    ) -> None:
        if self.font is None:
            self._orphanColor = value
        else:
            self.naked().color = value

    # Data

    def _get_data(self) -> Optional[bytes]:
        if self.font is None:
            return self._orphanData
        image = self.naked()
        images = self.font.naked().images
        fileName = image.fileName
        if fileName is None:
            return None
        if fileName not in images:
            return None
        return images[fileName]

    def _set_data(self, value: bytes) -> None:
        if not isinstance(value, bytes):
            raise FontPartsError("The image data provided is not valid.")
        if not pngValidator(data=value)[0]:
            raise FontPartsError("The image must be in PNG format.")
        if self.font is None:
            self._orphanData = value
        else:
            image = self.naked()
            images = image.font.images
            fileName = images.findDuplicateImage(value)
            if fileName is None:
                fileName = images.makeFileName("image.png")
                images[fileName] = value
            image.fileName = fileName
