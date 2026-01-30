from __future__ import annotations
from typing import Optional, Type

import defcon
from fontParts.base import BaseComponent
from fontParts.base.annotations import (
    SextupleType,
    SextupleCollectionType,
    IntFloatType,
)
from fontParts.fontshell.base import RBaseObject


class RComponent(RBaseObject, BaseComponent):
    wrapClass: Type[defcon.Component] = defcon.Component

    # ----------
    # Attributes
    # ----------

    # baseGlyph

    def _get_baseGlyph(self) -> Optional[str]:
        component = self.naked()
        return component.baseGlyph if component else None

    def _set_baseGlyph(self, value: str) -> None:
        component = self.naked()
        if component is not None:
            component.baseGlyph = value

    # transformation

    def _get_transformation(self) -> SextupleType[float]:
        component = self.naked()
        if component is None:
            raise ValueError("Component cannot be None.")
        return component.transformation

    def _set_transformation(self, value: SextupleCollectionType[IntFloatType]) -> None:
        component = self.naked()
        if component is not None:
            component.transformation = value

    # --------------
    # Identification
    # --------------

    # index

    def _set_index(self, value):
        component = self.naked()
        glyph = component.glyph
        if value > glyph.components.index(component):
            value -= 1
        glyph.removeComponent(component)
        glyph.insertComponent(value, component)

    # identifier

    def _get_identifier(self):
        component = self.naked()
        if component is None:
            return None
        return component.identifier

    def _getIdentifier(self):
        component = self.naked()
        if component is None:
            return None
        return component.generateIdentifier()

    def _setIdentifier(self, value):
        component = self.naked()
        if component is not None:
            component.identifier = value

    # -------------
    # Normalization
    # -------------

    def _decompose(self):
        component = self.naked()
        glyph = component.glyph
        glyph.decomposeComponent(component)
