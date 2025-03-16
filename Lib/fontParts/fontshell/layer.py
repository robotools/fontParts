from __future__ import annotations
from typing import Optional, Tuple, Dict, Any

import defcon
from fontParts.base import BaseLayer
from fontParts.base.annotations import (
    QuadrupleCollectionType,
    IntFloatType,
)
from fontParts.fontshell.base import RBaseObject
from fontParts.fontshell.lib import RLib
from fontParts.fontshell.glyph import RGlyph


class RLayer(RBaseObject, BaseLayer):
    wrapClass = defcon.Layer
    libClass = RLib
    glyphClass = RGlyph

    def _getNaked(self) -> defcon.Layer:
        layer = self.naked()
        if layer is None:
            raise ValueError("Layer cannot be None.")
        return layer

    # -----------
    # Sub-Objects
    # -----------

    # lib

    def _get_lib(self) -> RLib:
        return self.libClass(wrap=self._getNaked().lib)

    # tempLib

    def _get_tempLib(self) -> RLib:
        return self.libClass(wrap=self._getNaked().tempLib)

    # --------------
    # Identification
    # --------------

    # name

    def _get_name(self) -> str:
        return self._getNaked().name

    def _set_name(self, value: str, **kwargs: Any) -> None:
        self._getNaked().name = value

    # color

    def _get_color(self) -> Optional[QuadrupleCollectionType[IntFloatType]]:
        value = self._getNaked().color
        if value is not None:
            value = tuple(value)
        return value

    def _set_color(
            self,
            value: Optional[QuadrupleCollectionType[IntFloatType]],
            **kwargs: Any
    ) -> None:
        self._getNaked().color = value

    # -----------------
    # Glyph Interaction
    # -----------------

    def _getItem(self, name: str, **kwargs: Any) -> RGlyph:
        layer = self._getNaked()
        glyph = layer[name]
        return self.glyphClass(glyph)

    def _keys(self, **kwargs: Any) -> Tuple[str, ...]:
        return tuple(self._getNaked().keys())

    def _newGlyph(self, name: str, **kwargs: Any) -> RGlyph:
        layer = self._getNaked()
        layer.newGlyph(name)
        return self[name]

    def _removeGlyph(self, name: str, **kwargs: Any) -> None:
        layer = self._getNaked()
        del layer[name]

    # -------
    # mapping
    # -------

    def _getReverseComponentMapping(self) -> Dict[str, Tuple[str, ...]]:
        mapping = self._getNaked().componentReferences
        return {k: tuple(v) for k, v in mapping.items()}

    def _getCharacterMapping(self) -> Dict[int, Tuple[str, ...]]:
        mapping = self._getNaked().unicodeData
        return {k: tuple(v) for k, v in mapping.items()}
