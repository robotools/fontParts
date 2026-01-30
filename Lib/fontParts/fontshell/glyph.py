from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Any, Union

import defcon
import booleanOperations
from fontParts.base import BaseGlyph
from fontParts.base.annotations import (
    CollectionType,
    PairCollectionType,
    QuadrupleType,
    QuadrupleCollectionType,
    SextupleCollectionType,
    IntFloatType,
)
from fontParts.base.errors import FontPartsError
from fontParts.fontshell.base import RBaseObject
from fontParts.fontshell.contour import RContour
from fontParts.fontshell.component import RComponent
from fontParts.fontshell.anchor import RAnchor
from fontParts.fontshell.guideline import RGuideline
from fontParts.fontshell.image import RImage
from fontParts.fontshell.lib import RLib
from fontTools.ufoLib.glifLib import (
    GlifLibError,
    readGlyphFromString,
    writeGlyphToString,
)

if TYPE_CHECKING:
    from fontParts.base.image import BaseImage
    from fontTools.pens.pointPen import SegmentToPointPen
    from defcon.pens.glyphObjectPointPen import (
        GlyphObjectPointPen,
        GlyphObjectLoadingPointPen,
    )


class RGlyph(RBaseObject, BaseGlyph):
    wrapClass = defcon.Glyph
    contourClass = RContour
    componentClass = RComponent
    anchorClass = RAnchor
    guidelineClass = RGuideline
    imageClass = RImage
    libClass = RLib

    # --------------
    # Identification
    # --------------

    # Name

    def _get_name(self) -> str:
        return self.naked().name

    def _set_name(self, value: str) -> None:
        self.naked().name = value

    # Unicodes

    def _get_unicodes(self) -> CollectionType[int]:
        return self.naked().unicodes

    def _set_unicodes(self, value: CollectionType[int]) -> None:
        self.naked().unicodes = value

    # -------
    # Metrics
    # -------

    # horizontal

    def _get_width(self) -> IntFloatType:
        return self.naked().width

    def _set_width(self, value: IntFloatType) -> None:
        self.naked().width = value

    def _get_leftMargin(self) -> Optional[IntFloatType]:
        return self.naked().leftMargin

    def _set_leftMargin(self, value: IntFloatType) -> None:
        self.naked().leftMargin = value

    def _get_rightMargin(self) -> Optional[IntFloatType]:
        return self.naked().rightMargin

    def _set_rightMargin(self, value: IntFloatType) -> None:
        self.naked().rightMargin = value

    # vertical

    def _get_height(self) -> IntFloatType:
        return self.naked().height

    def _set_height(self, value: IntFloatType) -> None:
        self.naked().height = value

    def _get_bottomMargin(self) -> Optional[IntFloatType]:
        return self.naked().bottomMargin

    def _set_bottomMargin(self, value: IntFloatType) -> None:
        self.naked().bottomMargin = value

    def _get_topMargin(self) -> Optional[IntFloatType]:
        return self.naked().topMargin

    def _set_topMargin(self, value: IntFloatType) -> None:
        self.naked().topMargin = value

    # ------
    # Bounds
    # ------

    def _get_bounds(self) -> Optional[QuadrupleType[IntFloatType]]:
        return self.naked().bounds

    # ----
    # Area
    # ----

    def _get_area(self) -> Optional[float]:
        return self.naked().area

    # ----
    # Pens
    # ----

    def getPen(self) -> SegmentToPointPen:
        return self.naked().getPen()

    def getPointPen(self) -> Union[GlyphObjectPointPen, GlyphObjectLoadingPointPen]:
        return self.naked().getPointPen()

    # -----------------------------------------
    # Contour, Component and Anchor Interaction
    # -----------------------------------------

    # Contours

    def _lenContours(self, **kwargs: Any) -> int:
        return len(self.naked())

    def _getContour(self, index: int, **kwargs: Any) -> RContour:
        contour = self.naked()[index]
        return self.contourClass(contour)

    def _removeContour(self, index: int, **kwargs: Any) -> None:
        glyph = self.naked()
        contour = glyph[index]
        glyph.removeContour(contour)

    def _removeOverlap(self, **kwargs: Any) -> None:
        if len(self):
            contours = list(self)
            for contour in contours:
                for point in contour.points:
                    if point.type == "qcurve":
                        raise TypeError("fontshell can't removeOverlap for quadratics")
            self.clear(
                contours=True,
                components=False,
                anchors=False,
                guidelines=False,
                image=False,
            )
            booleanOperations.union(contours, self.getPointPen())

    def _correctDirection(self, trueType: bool = False, **kwargs: Any) -> None:
        self.naked().correctContourDirection(trueType=trueType)

    # Components

    def _lenComponents(self, **kwargs: Any) -> int:
        return len(self.naked().components)

    def _getComponent(self, index: int, **kwargs: Any) -> RComponent:
        component = self.naked().components[index]
        return self.componentClass(component)

    def _removeComponent(self, index: int, **kwargs: Any) -> None:
        glyph = self.naked()
        component = glyph.components[index]
        glyph.removeComponent(component)

    # Anchors

    def _lenAnchors(self, **kwargs: Any) -> int:
        return len(self.naked().anchors)

    def _getAnchor(self, index: int, **kwargs: Any) -> RAnchor:
        anchor = self.naked().anchors[index]
        return self.anchorClass(anchor)

    def _appendAnchor(
        self,
        name: str,
        position: Optional[PairCollectionType[IntFloatType]] = None,
        color: Optional[QuadrupleCollectionType[IntFloatType]] = None,
        identifier: Optional[str] = None,
        **kwargs: Any,
    ) -> RAnchor:
        glyph = self.naked()
        anchor = self.anchorClass().naked()
        if anchor is None:
            raise ValueError("Anchor cannot be None")
        anchor.name = name
        if position is not None:
            anchor.x = position[0]
            anchor.y = position[1]
        anchor.color = color
        anchor.identifier = identifier
        glyph.appendAnchor(anchor)
        wrapped = self.anchorClass(anchor)
        wrapped.glyph = self
        return wrapped

    def _removeAnchor(self, index: int, **kwargs: Any) -> None:
        glyph = self.naked()
        anchor = glyph.anchors[index]
        glyph.removeAnchor(anchor)

    # Guidelines

    def _lenGuidelines(self, **kwargs: Any) -> int:
        return len(self.naked().guidelines)

    def _getGuideline(self, index: int, **kwargs: Any) -> RGuideline:
        guideline = self.naked().guidelines[index]
        return self.guidelineClass(guideline)

    def _appendGuideline(
        self,
        position: Optional[PairCollectionType[IntFloatType]],
        angle: float,
        name: Optional[str] = None,
        color: Optional[QuadrupleCollectionType[IntFloatType]] = None,
        identifier: Optional[str] = None,
        **kwargs: Any,
    ) -> RGuideline:
        glyph = self.naked()
        guideline = self.guidelineClass().naked()
        if guideline is None:
            raise ValueError("Guideline cannot be None")
        if position is not None:
            guideline.x = position[0]
            guideline.y = position[1]
        guideline.angle = angle
        guideline.name = name
        guideline.color = color
        guideline.identifier = identifier
        glyph.appendGuideline(guideline)
        return self.guidelineClass(guideline)

    def _removeGuideline(self, index: int, **kwargs: Any) -> None:
        glyph = self.naked()
        guideline = glyph.guidelines[index]
        glyph.removeGuideline(guideline)

    # -----------------
    # Layer Interaction
    # -----------------

    # new

    def _newLayer(self, name: str, **kwargs: Any) -> RGlyph:
        layerName = name
        glyphName = self.name
        font = self.font
        if layerName not in font.layerOrder:
            layer = font.newLayer(layerName)
        else:
            layer = font.getLayer(layerName)
        glyph = layer.newGlyph(glyphName)
        return glyph

    # remove

    def _removeLayer(self, name: str, **kwargs: Any) -> None:
        layerName = name
        glyphName = self.name
        font = self.font
        layer = font.getLayer(layerName)
        layer.removeGlyph(glyphName)

    # -----
    # Image
    # -----

    def _get_image(self) -> Optional[RImage]:
        image = self.naked().image
        if image is None:
            return None
        return self.imageClass(image)

    def _addImage(
        self,
        data: bytes,
        transformation: Optional[SextupleCollectionType[IntFloatType]] = None,
        color: Optional[QuadrupleCollectionType[IntFloatType]] = None,
    ) -> RImage:
        image = self.naked().image
        image = self.imageClass(image)
        image.glyph = self
        image.data = data
        image.transformation = transformation
        image.color = color
        return image

    def _clearImage(self, **kwargs: Any) -> None:
        self.naked().image = None

    # ----
    # Note
    # ----

    # Mark

    def _get_markColor(self) -> Optional[QuadrupleType[float]]:
        value = self.naked().markColor
        if value is not None:
            value = tuple(value)
        return value

    def _set_markColor(
        self, value: Optional[QuadrupleCollectionType[IntFloatType]]
    ) -> None:
        self.naked().markColor = value

    # Note

    def _get_note(self) -> Optional[str]:
        return self.naked().note

    def _set_note(self, value: Optional[str]) -> None:
        self.naked().note = value

    # -----------
    # Sub-Objects
    # -----------

    # lib

    def _get_lib(self) -> RLib:
        return self.libClass(pathOrObject=self.naked().lib)

    # tempLib

    def _get_tempLib(self) -> RLib:
        return self.libClass(pathOrObject=self.naked().tempLib)

    # ---
    # API
    # ---

    def _loadFromGLIF(self, glifData: str, validate: bool = True) -> None:
        try:
            readGlyphFromString(
                aString=glifData,
                glyphObject=self.naked(),
                pointPen=self.getPointPen(),
                validate=validate,
            )
        except GlifLibError as e:
            raise FontPartsError("Not valid glif data") from e

    def _dumpToGLIF(self, glyphFormatVersion: int) -> str:
        glyph = self.naked()
        return writeGlyphToString(
            glyphName=glyph.name,
            glyphObject=glyph,
            drawPointsFunc=glyph.drawPoints,
            formatVersion=glyphFormatVersion,
        )
