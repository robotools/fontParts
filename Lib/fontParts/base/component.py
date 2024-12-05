from __future__ import annotations
from typing import TYPE_CHECKING, cast, Any, Iterator, List, Optional, Tuple, Union

from fontTools.misc import transform
from fontParts.base import normalizers
from fontParts.base.errors import FontPartsError
from fontParts.base.base import (
    BaseObject,
    TransformationMixin,
    InterpolationMixin,
    PointPositionMixin,
    SelectionMixin,
    IdentifierMixin,
    dynamicProperty,
    reference,
)
from fontParts.base.compatibility import ComponentCompatibilityReporter
from fontParts.base.deprecated import DeprecatedComponent, RemovedComponent
from fontParts.base.annotations import (
    PairType,
    PairCollectionType,
    QuadrupleType,
    SextupleType,
    SextupleCollectionType,
    IntFloatType,
    PenType,
    PointPenType,
)

if TYPE_CHECKING:
    from fontParts.base.point import BasePoint
    from fontParts.base.bPoint import BaseBPoint
    from fontParts.base.segment import BaseSegment
    from fontParts.base.glyph import BaseGlyph
    from fontParts.base.layer import BaseLayer
    from fontParts.base.font import BaseFont


class BaseComponent(
    BaseObject,
    TransformationMixin,
    InterpolationMixin,
    SelectionMixin,
    IdentifierMixin,
    DeprecatedComponent,
    RemovedComponent,
):
    copyAttributes: Tuple[str, str] = ("baseGlyph", "transformation")

    def _reprContents(self) -> List[str]:
        contents = [
            f"baseGlyph='{self.baseGlyph}'",
            f"offset='({self.offset[0]}, {self.offset[1]})'",
        ]
        if self.glyph is not None:
            contents.append("in glyph")
            contents += self.glyph._reprContents()
        return contents

    # -------
    # Parents
    # -------

    # Glyph

    _glyph = None

    glyph: dynamicProperty = dynamicProperty("glyph", "The component's parent glyph.")

    def _get_glyph(self) -> Optional[BaseGlyph]:
        if self._glyph is None:
            return None
        return self._glyph()

    def _set_glyph(self, glyph: Optional[BaseGlyph]) -> None:
        if self._glyph is not None:
            raise AssertionError("glyph for component already set")
        if glyph is not None:
            glyph = reference(glyph)
        self._glyph = glyph

    # Layer

    layer: dynamicProperty = dynamicProperty("layer", "The component's parent layer.")

    def _get_layer(self) -> Optional[BaseLayer]:
        if self._glyph is None:
            return None
        return self.glyph.layer

    # Font

    font: dynamicProperty = dynamicProperty("font", "The component's parent font.")

    def _get_font(self) -> Optional[BaseFont]:
        if self._glyph is None:
            return None
        return self.glyph.font

    # ----------
    # Attributes
    # ----------

    # baseGlyph

    baseGlyph: dynamicProperty = dynamicProperty(
        "base_baseGlyph", "The name of the glyph the component references."
    )

    def _get_base_baseGlyph(self) -> Optional[str]:
        value = self._get_baseGlyph()
        # if the component does not belong to a layer,
        # it is allowed to have None as its baseGlyph
        if value is None or self.layer is None:
            return value
        return normalizers.normalizeGlyphName(value)

    def _set_base_baseGlyph(self, value: str) -> None:
        value = normalizers.normalizeGlyphName(value)
        self._set_baseGlyph(value)

    def _get_baseGlyph(self) -> Optional[str]:
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_baseGlyph(self, value: str) -> None:
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # transformation

    transformation: dynamicProperty = dynamicProperty(
        "base_transformation", "The component's transformation matrix."
    )

    def _get_base_transformation(self) -> SextupleType[float]:
        value = self._get_transformation()
        value = normalizers.normalizeTransformationMatrix(value)
        return value

    def _set_base_transformation(self, value: SextupleCollectionType[IntFloatType]) -> None:
        value = normalizers.normalizeTransformationMatrix(value)
        self._set_transformation(value)

    def _get_transformation(self) -> SextupleType[float]:
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_transformation(self, value: SextupleCollectionType[IntFloatType]) -> None:
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # offset

    offset: dynamicProperty = dynamicProperty("base_offset", "The component's offset.")

    def _get_base_offset(self) -> PairType[IntFloatType]:
        value = self._get_offset()
        value = normalizers.normalizeTransformationOffset(value)
        return value

    def _set_base_offset(self, value: PairCollectionType[IntFloatType]) -> None:
        value = normalizers.normalizeTransformationOffset(value)
        self._set_offset(value)

    def _get_offset(self) -> PairType[IntFloatType]:
        """
        Subclasses may override this method.
        """
        sx, sxy, syx, sy, ox, oy = self.transformation
        return ox, oy

    def _set_offset(self, value: PairCollectionType[IntFloatType]) -> None:
        """
        Subclasses may override this method.
        """
        sx, sxy, syx, sy, ox, oy = self.transformation
        ox, oy = value
        self.transformation = sx, sxy, syx, sy, ox, oy

    # scale

    scale: dynamicProperty = dynamicProperty("base_scale", "The component's scale.")

    def _get_base_scale(self) -> PairType[float]:
        value = self._get_scale()
        value = normalizers.normalizeComponentScale(value)
        return value

    def _set_base_scale(self, value: PairCollectionType[IntFloatType]) -> None:
        value = normalizers.normalizeComponentScale(value)
        self._set_scale(value)

    def _get_scale(self) -> PairType[float]:
        """
        Subclasses may override this method.
        """
        sx, sxy, syx, sy, ox, oy = self.transformation
        return sx, sy

    def _set_scale(self, value: PairCollectionType[IntFloatType]) -> None:
        """
        Subclasses may override this method.
        """
        sx, sxy, syx, sy, ox, oy = self.transformation
        sx, sy = value
        self.transformation = sx, sxy, syx, sy, ox, oy

    # --------------
    # Identification
    # --------------

    # index

    index: dynamicProperty = dynamicProperty(
        "base_index",
        (
            "The index of the component within the "
            "ordered list of the parent glyph's components."
        ),
    )

    def _get_base_index(self) -> Optional[int]:
        glyph = self.glyph
        if glyph is None:
            return None
        value = self._get_index()
        value = normalizers.normalizeIndex(value)
        return value

    def _set_base_index(self, value: int) -> None:
        glyph = self.glyph
        if glyph is None:
            raise FontPartsError("The component does not belong to a glyph.")
        value = normalizers.normalizeIndex(value)
        if value is None:
            raise ValueError("Value cannot be None.")
        componentCount = len(glyph.components)
        if value < 0:
            value = -(value % componentCount)
        if value >= componentCount:
            value = componentCount
        self._set_index(value)

    def _get_index(self) -> Optional[int]:
        """
        Subclasses may override this method.
        """
        glyph = self.glyph
        return glyph.components.index(self)

    def _set_index(self, value: int) -> None:
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # ----
    # Pens
    # ----

    def draw(self, pen: PenType) -> None:
        """
        Draw the component with the given Pen.
        """
        self._draw(pen)

    def _draw(self, pen: PenType, **kwargs: Any) -> None:
        """
        Subclasses may override this method.
        """
        from fontTools.ufoLib.pointPen import PointToSegmentPen

        adapter = PointToSegmentPen(pen)
        self.drawPoints(adapter)

    def drawPoints(self, pen: PointPenType) -> None:
        """
        Draw the contour with the given PointPen.
        """
        self._drawPoints(pen)

    def _drawPoints(self, pen: PointPenType, **kwargs: Any) -> None:
        """
        Subclasses may override this method.
        """
        # The try: ... except TypeError: ...
        # handles backwards compatibility with
        # point pens that have not been upgraded
        # to point pen protocol 2.
        try:
            pen.addComponent(
                self.baseGlyph,
                self.transformation,
                identifier=self.identifier,
                **kwargs,
            )
        except TypeError:
            pen.addComponent(self.baseGlyph, self.transformation, **kwargs)

    # --------------
    # Transformation
    # --------------

    def _transformBy(self, matrix: SextupleCollectionType[IntFloatType], **kwargs: Any) -> None:
        """
        Subclasses may override this method.
        """
        t = transform.Transform(*matrix)
        transformation = t.transform(self.transformation)
        self.transformation = tuple(transformation)

    # -------------
    # Normalization
    # -------------

    def round(self) -> None:
        """
        Round offset coordinates.
        """
        self._round()

    def _round(self) -> None:
        """
        Subclasses may override this method.
        """
        x, y = self.offset
        x = normalizers.normalizeVisualRounding(x)
        y = normalizers.normalizeVisualRounding(y)
        self.offset = (x, y)

    def decompose(self) -> None:
        """
        Decompose the component.
        """
        glyph = self.glyph
        if glyph is None:
            raise FontPartsError("The component does not belong to a glyph.")
        self._decompose()

    def _decompose(self) -> None:
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # -------------
    # Interpolation
    # -------------

    compatibilityReporterClass = ComponentCompatibilityReporter

    def isCompatible(self, other: BaseComponent) -> Tuple[bool, ComponentCompatibilityReporter]:
        """
        Evaluate interpolation compatibility with **other**. ::

            >>> compatible, report = self.isCompatible(otherComponent)
            >>> compatible
            True
            >>> compatible
            [Warning] Component: "A" + "B"
            [Warning] Component: "A" has name A | "B" has name B

        This will return a ``bool`` indicating if the component is
        compatible for interpolation with **other** and a
        :ref:`type-string` of compatibility notes.
        """
        return super(BaseComponent, self).isCompatible(other, BaseComponent)

    def _isCompatible(self, other: BaseComponent, reporter: ComponentCompatibilityReporter) -> None:
        """
        This is the environment implementation of
        :meth:`BaseComponent.isCompatible`.

        Subclasses may override this method.
        """
        component1 = self
        component2 = other
        # base glyphs
        if component1.baseGlyph != component2.baseGlyph:
            reporter.baseDifference = True
            reporter.warning = True

    # ------------
    # Data Queries
    # ------------

    def pointInside(self, point: PairCollectionType[IntFloatType]) -> bool:
        """
        Determine if point is in the black or white of the component.

        point must be an (x, y) tuple.
        """
        point = normalizers.normalizeCoordinateTuple(point)
        return self._pointInside(point)

    def _pointInside(self, point: PairCollectionType[IntFloatType]) -> bool:
        """
        Subclasses may override this method.
        """
        from fontTools.pens.pointInsidePen import PointInsidePen

        pen = PointInsidePen(glyphSet=self.layer, testPoint=point, evenOdd=False)
        self.draw(pen)
        return pen.getResult()

    bounds: dynamicProperty = dynamicProperty(
        "base_bounds",
        ("The bounds of the component: " "(xMin, yMin, xMax, yMax) or None."),
    )

    def _get_base_bounds(self) -> QuadrupleType[float]:
        value = self._get_bounds()
        if value is not None:
            value = normalizers.normalizeBoundingBox(value)
        return value

    def _get_bounds(self) -> QuadrupleType[float]:
        """
        Subclasses may override this method.
        """
        from fontTools.pens.boundsPen import BoundsPen

        pen = BoundsPen(self.layer)
        self.draw(pen)
        return pen.bounds
