from __future__ import annotations
from typing import Any, Optional, Tuple, Union
import os

import defcon
from fontParts.base.annotations import (
    CollectionType,
    PairCollectionType,
    QuadrupleCollectionType,
    IntFloatType
)
from fontParts.base import BaseFont
from fontParts.fontshell.base import RBaseObject
from fontParts.fontshell.info import RInfo
from fontParts.fontshell.groups import RGroups
from fontParts.fontshell.kerning import RKerning
from fontParts.fontshell.features import RFeatures
from fontParts.fontshell.lib import RLib
from fontParts.fontshell.layer import RLayer
from fontParts.fontshell.guideline import RGuideline


class RFont(RBaseObject, BaseFont):
    wrapClass = defcon.Font
    infoClass = RInfo
    groupsClass = RGroups
    kerningClass = RKerning
    featuresClass = RFeatures
    libClass = RLib
    layerClass = RLayer
    guidelineClass = RGuideline

    def _getNaked(self) -> defcon.Font:
        font = self.naked()
        if font is None:
            raise ValueError("Font cannot be None.")
        return font

    # ---------------
    # File Operations
    # ---------------

    # Initialize

    def _init(
            self,
            pathOrObject: Optional[Union[str, os.PathLike, defcon.Font]] = None,
            showInterface: bool = True,
            **kwargs: Any
    ) -> None:
        if self.wrapClass is not None:
            if pathOrObject is None:
                font = self.wrapClass()
            elif isinstance(pathOrObject, (str, os.PathLike)):
                font = self.wrapClass(os.fspath(pathOrObject))
            else:
                font = pathOrObject
            self._wrapped = font

    # path

    def _get_path(self, **kwargs: Any) -> Optional[str]:
        return self._getNaked().path

    # save

    def _save(
        self,
        path: Optional[str] = None,
        showProgress: bool = False,
        formatVersion: Optional[int] = None,
        fileStructure: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self._getNaked().save(
            path=path, formatVersion=formatVersion, structure=fileStructure
        )

    # close

    def _close(self, **kwargs: Any) -> None:
        del self._wrapped

    # -----------
    # Sub-Objects
    # -----------

    # info

    def _get_info(self) -> RInfo:
        return self.infoClass(pathOrObject=self._getNaked().info)

    # groups

    def _get_groups(self) -> RGroups:
        return self.groupsClass(pathOrObject=self._getNaked().groups)

    # kerning

    def _get_kerning(self) -> RKerning:
        return self.kerningClass(pathOrObject=self._getNaked().kerning)

    # features

    def _get_features(self) -> RFeatures:
        return self.featuresClass(pathOrObject=self._getNaked().features)

    # lib

    def _get_lib(self) -> RLib:
        return self.libClass(pathOrObject=self._getNaked().lib)

    # tempLib

    def _get_tempLib(self) -> RLib:
        return self.libClass(pathOrObject=self._getNaked().tempLib)

    # ------
    # Layers
    # ------

    def _get_layers(self, **kwargs: Any) -> Tuple[RLayer, ...]:
        return tuple(
            self.layerClass(pathOrObject=layer) for layer in self._getNaked().layers
        )

    # order

    def _get_layerOrder(self, **kwargs: Any) -> Tuple[str, ...]:
        return self._getNaked().layers.layerOrder

    def _set_layerOrder(self, value: CollectionType[str], **kwargs: Any) -> None:
        self._getNaked().layers.layerOrder = value

    # default layer

    def _get_defaultLayerName(self) -> str:
        return self._getNaked().layers.defaultLayer.name

    def _set_defaultLayerName(self, value: str, **kwargs: Any) -> None:
        font = self._getNaked()
        for layer in self.layers:
            if layer.name == value:
                break
        layer = layer.naked()
        font.layers.defaultLayer = layer

    # new

    def _newLayer(
            self,
            name: str,
            color: Optional[QuadrupleCollectionType[IntFloatType]], **kwargs: Any
    ) -> RLayer:
        layers = self._getNaked().layers
        layer = layers.newLayer(name)
        layer.color = color
        return self.layerClass(pathOrObject=layer)

    # remove

    def _removeLayer(self, name: str, **kwargs: Any) -> None:
        layers = self._getNaked().layers
        del layers[name]

    # ------
    # Glyphs
    # ------

    def _get_glyphOrder(self) -> Tuple[str, ...]:
        return self._getNaked().glyphOrder

    def _set_glyphOrder(self, value: CollectionType[str]) -> None:
        self._getNaked().glyphOrder = value

    # ----------
    # Guidelines
    # ----------

    def _lenGuidelines(self, **kwargs: Any) -> int:
        return len(self._getNaked().guidelines)

    def _getGuideline(self, index: int, **kwargs: Any) -> RGuideline:
        guideline = self._getNaked().guidelines[index]
        return self.guidelineClass(guideline)

    def _appendGuideline(
        self,
        position: PairCollectionType[IntFloatType],
        angle: Optional[float],
        name: Optional[str] = None,
        color: Optional[QuadrupleCollectionType[IntFloatType]] = None,
        identifier: Optional[str] = None,
        **kwargs: Any
    ) -> RGuideline:
        font = self._getNaked()
        guideline = self.guidelineClass().naked()
        if guideline is None:
            raise ValueError("Guideline cannot be None.")
        guideline.x = position[0]
        guideline.y = position[1]
        guideline.angle = angle
        guideline.name = name
        guideline.color = color
        guideline.identifier = identifier
        font.appendGuideline(guideline)
        return self.guidelineClass(guideline)

    def _removeGuideline(self, index: int, **kwargs: Any) -> None:
        font = self._getNaked()
        guideline = font.guidelines[index]
        font.removeGuideline(guideline)
