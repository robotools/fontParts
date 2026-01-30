from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Tuple, Dict, Any

import defcon
from fontParts.base import BaseLayer
from fontParts.base.annotations import QuadrupleCollectionType, IntFloatType
from fontParts.fontshell.base import RBaseObject
from fontParts.fontshell.lib import RLib
from fontParts.fontshell.glyph import RGlyph

if TYPE_CHECKING:
    from fontParts.base.glyph import BaseGlyph


class RLayer(RBaseObject, BaseLayer):
    wrapClass = defcon.Layer
    libClass = RLib
    glyphClass = RGlyph

    # -----------
    # Sub-Objects
    # -----------

    # lib

    def _get_lib(self) -> RLib:
        return self.libClass(pathOrObject=self.naked().lib)

    # tempLib

    def _get_tempLib(self) -> RLib:
        return self.libClass(pathOrObject=self.naked().tempLib)

    # --------------
    # Identification
    # --------------

    # name

    def _get_name(self) -> str:
        return self.naked().name

    def _set_name(self, value: str, **kwargs: Any) -> None:
        self.naked().name = value

    # color

    def _get_color(self) -> Optional[QuadrupleCollectionType[IntFloatType]]:
        value = self.naked().color
        if value is not None:
            value = tuple(value)
        return value

    def _set_color(
        self, value: Optional[QuadrupleCollectionType[IntFloatType]], **kwargs: Any
    ) -> None:
        self.naked().color = value

    # -----------------
    # Glyph Interaction
    # -----------------

    def _getItem(self, name: str, **kwargs: Any) -> RGlyph:
        layer = self.naked()
        glyph = layer[name]
        return self.glyphClass(glyph)

    def _keys(self, **kwargs: Any) -> Tuple[str, ...]:
        return tuple(self.naked().keys())

    def _newGlyph(self, name: str, **kwargs: Any) -> BaseGlyph:
        layer = self.naked()
        layer.newGlyph(name)
        return self[name]

    def _removeGlyph(self, name: str, **kwargs: Any) -> None:
        layer = self.naked()
        del layer[name]

    # -------
    # mapping
    # -------

    def _getReverseComponentMapping(self) -> Dict[str, Tuple[str, ...]]:
        mapping = self.naked().componentReferences
        return {k: tuple(v) for k, v in mapping.items()}

    def _getCharacterMapping(self) -> Dict[int, Tuple[str, ...]]:
        mapping = self.naked().unicodeData
        return {k: tuple(v) for k, v in mapping.items()}
