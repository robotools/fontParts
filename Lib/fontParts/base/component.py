from __future__ import annotations
from typing import TYPE_CHECKING, Any, List, Optional, Tuple

from fontTools.misc import transform
from fontTools.pens.pointInsidePen import PointInsidePen
from fontTools.pens.boundsPen import BoundsPen
from fontParts.base import normalizers
from fontParts.base.errors import FontPartsError
from fontParts.base.base import (
    BaseObject,
    TransformationMixin,
    InterpolationMixin,
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
    """Represent the basis for a component object.

    This object provides a reference to another glyph, allowing it to be
    inserted as part of an outline.

    """

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

    glyph: dynamicProperty = dynamicProperty(
        "glyph",
        """Get or set the component's parent glyph object.

        The value must be a :class:`BaseGlyph` instance or :obj:`None`.

        :return: The :class:`BaseGlyph` instance containing the component
            or :obj:`None`.
        :raises AssertionError: If attempting to set the glyph when it
            has already been set.

        Example::

            >>> glyph = component.glyph

        """,
    )

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

    layer: dynamicProperty = dynamicProperty(
        "layer",
        """Get the component's parent layer object.

        This property is read-only.

        :return: The :class:`BaseLayer` instance containing the component
            or :obj:`None`.

        Example::

            >>> layer = component.layer

        """,
    )

    def _get_layer(self) -> Optional[BaseLayer]:
        if self._glyph is None:
            return None
        return self.glyph.layer

    # Font

    font: dynamicProperty = dynamicProperty(
        "font",
        """Get the component's parent font object.

        This property is read-only.

        :return: The :class:`BaseFont` instance containing the component
            or :obj:`None`.

        Example::

            >>> font = component.font

        """,
    )

    def _get_font(self) -> Optional[BaseFont]:
        if self._glyph is None:
            return None
        return self.glyph.font

    # ----------
    # Attributes
    # ----------

    # baseGlyph

    baseGlyph: dynamicProperty = dynamicProperty(
        "base_baseGlyph",
        """Get or set the name of the glyph referenced by the component.

        The value must be a :class:`str`.

        :return: A :class:`str` representing the name of the base glyph,
            or :obj:`None` if the component does not belong to a layer.
        :raise ValueError: If value is None when the component is part of a layer.

        """,
    )

    def _get_base_baseGlyph(self) -> Optional[str]:
        value = self._get_baseGlyph()
        # if the component does not belong to a layer,
        # it is allowed to have None as its baseGlyph
        if value is None and self.layer is None:
            return value
        if value is None:
            raise ValueError(f"Value cannot be None when layer is '{self.layer}'.")
        return normalizers.normalizeGlyphName(value)

    def _set_base_baseGlyph(self, value: str) -> None:
        value = normalizers.normalizeGlyphName(value)
        self._set_baseGlyph(value)

    def _get_baseGlyph(self) -> Optional[str]:
        """Get the name of the glyph referenced by the native component.

        This is the environment implementation of the :attr:`BaseComponent.baseGlyph`
        property getter.

        :return: A :class:`str` representing the name of the base glyph,
            or :obj:`None` if the component does not belong to a layer. The value
            will be normalized with :func:`normalizers.normalizeGlyphName`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_baseGlyph(self, value: str) -> None:
        """Set the name of the glyph referenced by the native component.

        This is the environment implementation of the :attr:`BaseComponent.baseGlyph`
        property setter.

        :param value: The name of the glyph to set as a :class:`str`. The value
            will have been normalized
         with :func:`normalizers.normalizeGlyphName`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # transformation

    transformation: dynamicProperty = dynamicProperty(
        "base_transformation",
        """Get or set the component's transformation matrix.

        The value must be a :ref:`type-transformation`.

        :return: A :ref:`type-transformation` value representing the
            transformation matrix of the component.

        """,
    )

    def _get_base_transformation(self) -> SextupleType[float]:
        value = self._get_transformation()
        value = normalizers.normalizeTransformationMatrix(value)
        return value

    def _set_base_transformation(
        self, value: SextupleCollectionType[IntFloatType]
    ) -> None:
        value = normalizers.normalizeTransformationMatrix(value)
        self._set_transformation(value)

    def _get_transformation(self) -> SextupleType[float]:
        """Get the native component's transformation matrix.

        This is the environment implementation of the
        :attr:`BaseComponent.transformation` property getter.

        :return: A :ref:`type-transformation` value representing the
            transformation matrix of the component. The value will be
            normalized with :func:`normalizers.normalizeTransformationMatrix`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_transformation(self, value: SextupleCollectionType[IntFloatType]) -> None:
        """Set the native component's transformation matrix.

        This is the environment implementation of the
        :attr:`BaseComponent.transformation` property setter.

        :param value: The :ref:`type-transformation` to set. The value will have
            been normalized with :func:`normalizers.normalizeTransformationMatrix`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # offset

    offset: dynamicProperty = dynamicProperty(
        "base_offset",
        """Get or set the component's offset.

        The value must be a :ref:`type-coordinate.`

        :return: A :ref:`type-coordinate.` representing the offset of the component.

        """,
    )

    def _get_base_offset(self) -> PairType[IntFloatType]:
        value = self._get_offset()
        value = normalizers.normalizeTransformationOffset(value)
        return value

    def _set_base_offset(self, value: PairCollectionType[IntFloatType]) -> None:
        value = normalizers.normalizeTransformationOffset(value)
        self._set_offset(value)

    def _get_offset(self) -> PairType[IntFloatType]:
        """Get the native component's offset.

        This is the environment implementation of the :attr:`BaseComponent.offset`
        property getter.

        :return: A :ref:`type-coordinate.` representing the offset of the component.
            The value will be normalized
            with :func:`normalizers.normalizeTransformationOffset`.

        .. note::

            Subclasses may override this method.

        """
        sx, sxy, syx, sy, ox, oy = self.transformation
        return ox, oy

    def _set_offset(self, value: PairCollectionType[IntFloatType]) -> None:
        """Set the native component's offset.

        This is the environment implementation of the :attr:`BaseComponent.offset`
        property setter.

        :param value: The offset to set as a :ref:`type-coordinate.`. The value will
            have been normalized with :func:`normalizers.normalizeTransformationOffset`.

        .. note::

            Subclasses may override this method.

        """
        sx, sxy, syx, sy, ox, oy = self.transformation
        ox, oy = value
        self.transformation = sx, sxy, syx, sy, ox, oy

    # scale

    scale: dynamicProperty = dynamicProperty(
        "base_scale",
        """Get or set the component's scale.

        The value must be a :class:`list` or :class:`tuple` of two :class:`int`
        or :class:`float` items representing the ``(x, y)`` scale of the component.

        :return: A :class:`tuple` of two :class:`float` items representing the
            ``(x, y)`` scale of the component.

        """,
    )

    def _get_base_scale(self) -> PairType[float]:
        value = self._get_scale()
        value = normalizers.normalizeComponentScale(value)
        return value

    def _set_base_scale(self, value: PairCollectionType[IntFloatType]) -> None:
        value = normalizers.normalizeComponentScale(value)
        self._set_scale(value)

    def _get_scale(self) -> PairType[float]:
        """Get the native component's scale.

        This is the environment implementation of the :attr:`BaseComponent.scale`
        property getter.

        :return: A :class:`tuple` of two :class:`float` items representing the
            ``(x, y)`` scale of the component. The value will have been normalized
            with :func:`normalizers.normalizeComponentScale`.

        .. note::

            Subclasses may override this method.

        """
        sx, sxy, syx, sy, ox, oy = self.transformation
        return sx, sy

    def _set_scale(self, value: PairCollectionType[IntFloatType]) -> None:
        """Set the native component's scale.

        This is the environment implementation of the :attr:`BaseComponent.scale`
        property setter.

        :param value: The scale to set as a :class:`list` or :class:`tuple`
            of :class:`int` or :class:`float` items representing the ``(x, y)``
            scale of the component. The value will have been normalized
            with :func:`normalizers.normalizeComponentScale`.

        .. note::

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
        """Get or set the index of the contour.

        The value must be an :class:`int`

        :return: An :class:`int` representing the index of the component within
            the ordered list of parent glyph's components, or :obj:`None` if the
            component does not belong to a glyph.
        :raise FontPartsError: If attempting to set the index while the
            component does not belong to a glyph.

        """,
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
            return
        componentCount = len(glyph.components)
        if value < 0:
            value = -(value % componentCount)
        if value >= componentCount:
            value = componentCount
        self._set_index(value)

    def _get_index(self) -> Optional[int]:
        """Get the index of the native contour.

        This is the environment implementation of the :attr:`BaseComponent.index`
        property getter.

        :return: An :class:`int` representing the index of the component within
            the ordered list of parent glyph's components, or :obj:`None` if the
            component does not belong to a glyph. The value will be normalized
            with :func:`normalizers.normalizeIndex`.

        .. note::

            Subclasses may override this method.

        """
        glyph = self.glyph
        return glyph.components.index(self)

    def _set_index(self, value: int) -> None:
        """Set the index of the native contour.

        This is the environment implementation of the :attr:`BaseComponent.index`
        property setter.

        :param value: The index to set as an :class:`int`. The value will have been
            normalized with :func:`normalizers.normalizeIndex`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # ----
    # Pens
    # ----

    def draw(self, pen: PenType) -> None:
        """Draw the component with the given pen.

        :param pen: The :class:`fontTools.pens.basePen.AbstractPen` with which
            to draw the componnet.

        """
        self._draw(pen)

    def _draw(self, pen: PenType, **kwargs: Any) -> None:
        r"""Draw the native component with the given pen.

        This is the environment implementation of :meth:`BaseComponent.draw`.

        :param pen: The :class:`fontTools.pens.basePen.AbstractPen` with which
            to draw the componnet.
        :param \**kwargs: Additional keyword arguments.

        .. note::

            Subclasses may override this method.

        """
        from fontTools.ufoLib.pointPen import PointToSegmentPen

        adapter = PointToSegmentPen(pen)
        self.drawPoints(adapter)

    def drawPoints(self, pen: PointPenType) -> None:
        """Draw the component with the given point pen.

        :param pen: The :class:`fontTools.pens.pointPen.AbstractPointPen` with
            which to draw the componnet.

        """
        self._drawPoints(pen)

    def _drawPoints(self, pen: PointPenType, **kwargs: Any) -> None:
        r"""Draw the native component with the given point pen.

        This is the environment implementation of :meth:`BaseComponent.draw`.

        :param pen: The :class:`fontTools.pens.pointPen.AbstractPointPen` with
            which to draw the componnet.
        :param \**kwargs: Additional keyword arguments.

        .. note::

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

    def _transformBy(
        self, matrix: SextupleCollectionType[IntFloatType], **kwargs: Any
    ) -> None:
        r"""Transform the component according to the given matrix.

        This is the environment implementation of :meth:`BaseComponent.transformBy`.

        :param matrix: The :ref:`type-transformation` to apply. The value will
             be normalized with :func:`normalizers.normalizeTransformationMatrix`.
        :param \**kwargs: Additional keyword arguments.

        .. note::

            Subclasses may override this method.

        """
        t = transform.Transform(*matrix)
        transformation = t.transform(self.transformation)
        self.transformation = tuple(transformation)

    # -------------
    # Normalization
    # -------------

    def round(self) -> None:
        """Round the compnent's offset coordinates.

        This applies to :attr:`offset`

        """
        self._round()

    def _round(self) -> None:
        """Round the native compnent's offset coordinates.

        This is the environment implementation of :meth:`BaseComponent.round`.

        .. note::

            Subclasses may override this method.

        """
        x, y = self.offset
        x = normalizers.normalizeVisualRounding(x)
        y = normalizers.normalizeVisualRounding(y)
        self.offset = (x, y)

    def decompose(self) -> None:
        """Decompose the component."""
        glyph = self.glyph
        if glyph is None:
            raise FontPartsError("The component does not belong to a glyph.")
        self._decompose()

    def _decompose(self) -> None:
        """Decompose the native component.

        This is the environment implementation of :meth:`BaseComponent.decompose`.

        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # -------------
    # Interpolation
    # -------------

    compatibilityReporterClass = ComponentCompatibilityReporter

    def isCompatible(
        self, other: BaseComponent
    ) -> Tuple[bool, ComponentCompatibilityReporter]:
        """Evaluate interpolation compatibility with another component.

        :param other: The other :class:`BaseComponent` instance to check
            compatibility with.
        :return: A :class:`tuple` where the first element is a :class:`bool`
            indicating compatibility, and the second element is
            a :class:`fontParts.base.compatibility.ComponentCompatibilityReporter`
            instance.

        Example::

            >>> compatible, report = self.isCompatible(otherComponent)
            >>> compatible
            True
            >>> compatible
            [Warning] Component: "A" + "B"
            [Warning] Component: "A" has name A | "B" has name B

        """
        return super(BaseComponent, self).isCompatible(other, BaseComponent)

    def _isCompatible(
        self, other: BaseComponent, reporter: ComponentCompatibilityReporter
    ) -> None:
        """Evaluate interpolation compatibility with another native component.

        This is the environment implementation of :meth:`BaseComponent.isCompatible`.

        :param other: The other :class:`BaseComponent` instance to check
            compatibility with.
        :param reporter: An object used to report compatibility issues.

        .. note::

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
        """Check if `point` lies inside the filled area of the component.

        :param point: The point to check as a :ref:`type-coordinate`.
        :return: :obj:`True` if `point` is inside the filled area of the
            glyph, :obj:`False` otherwise.

        Example::

            >>> glyph.pointInside((40, 65))
            True

        """
        point = normalizers.normalizeCoordinateTuple(point)
        return self._pointInside(point)

    def _pointInside(self, point: PairCollectionType[IntFloatType]) -> bool:
        """Check if `point` lies inside the filled area of the native component.

        This is the environment implementation of :meth:`BaseComponent.pointInside`.

        :param point: The point to check as a :ref:`type-coordinate`. The value will
            have been normalized with :func:`normalizers.normalizeCoordinateTuple`.
        :return: :class:`bool`.

        .. note::

            Subclasses may override this method.

        """
        pen = PointInsidePen(glyphSet=self.layer, testPoint=point, evenOdd=False)
        self.draw(pen)
        return pen.getResult()

    bounds: dynamicProperty = dynamicProperty(
        "base_bounds",
        """Get the bounds of the component.

        This property is read-only.

        :return: A :class:`tuple` of four :class:`int` or :class:`float` values
            in the form ``(x minimum, y minimum, x maximum, y maximum)``
            representing the bounds of the component, or :obj:`None` if the
            component is empty.

        Example::

            >>> component.bounds
            (10, 30, 765, 643)

        """,
    )

    def _get_base_bounds(self) -> QuadrupleType[float]:
        value = self._get_bounds()
        if value is not None:
            value = normalizers.normalizeBoundingBox(value)
        return value

    def _get_bounds(self) -> QuadrupleType[float]:
        """Get the bounds of the component.

         This is the environment implementation of the :attr:`BaseComponent.bounds`
         property getter.

        :return: A :class:`tuple` of four :class:`int` or :class:`float` values
             in the form ``(x minimum, y minimum, x maximum, y maximum)``
             representing the bounds of the component, or :obj:`None` if the
             component is empty. The value will be normalized
             with :func:`normalizers.normalizeBoundingBox`.

         .. note::

             Subclasses may override this method.

        """
        pen = BoundsPen(self.layer)
        self.draw(pen)
        return pen.bounds
