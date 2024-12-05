from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, Optional, Union, Tuple

from fontTools.misc import transform
from fontParts.base.base import (
    BaseObject,
    TransformationMixin,
    PointPositionMixin,
    SelectionMixin,
    IdentifierMixin,
    dynamicProperty,
    reference,
)
from fontParts.base import normalizers
from fontParts.base.deprecated import DeprecatedPoint, RemovedPoint
from fontParts.base.annotations import (
    QuintupleType,
    SextupleCollectionType,
    IntFloatType,
)

if TYPE_CHECKING:
    from fontParts.base.font import BaseFont
    from fontParts.base.glyph import BaseGlyph
    from fontParts.base.lib import BaseLib
    from fontParts.base.contour import BaseContour


class BasePoint(
    BaseObject,
    TransformationMixin,
    PointPositionMixin,
    SelectionMixin,
    IdentifierMixin,
    DeprecatedPoint,
    RemovedPoint,
):
    """Represent the basis for a point object.

    This object is almost always created with :meth:`BaseContour.appendPoint`,
    the pen returned by :meth:`BaseGlyph.getPen` or the point pen returned
    by :meth:`BaseGlyph.getPointPen`.

    An orphan point can be created like this::

        >>> point = RPoint()

    """

    copyAttributes: QuintupleType[str] = ("type", "smooth", "x", "y", "name")

    def _reprContents(self) -> list[str]:
        contents = [
            f"{self.type}",
            f"({self.x}, {self.y})",
        ]
        if self.name is not None:
            contents.append(f"name='{self.name}'")
        if self.smooth:
            contents.append(f"smooth={self.smooth!r}")
        return contents

    # -------
    # Parents
    # -------

    # Contour

    _contour: Optional[Callable[[], BaseContour]] = None

    contour: dynamicProperty = dynamicProperty(
        "contour",
        """Get or set the point's parent contour object.

        The value must be a :class:`BaseContour` instance or :obj:`None`.

        :return: The :class:`BaseContour` instance containing the point
            or :obj:`None`.
        :raises AssertionError: If attempting to set the contour when it
            has already been set.

        Example::

            >>> contour = point.contour

        """,
    )

    def _get_contour(self) -> Optional[BaseContour]:
        if self._contour is None:
            return None
        return self._contour()

    def _set_contour(self, contour: Optional[Union[BaseContour, Callable[[], BaseContour]]]) -> None:
        if self._contour is not None:
            raise AssertionError("contour for point already set")
        if contour is not None:
            contour = reference(contour)
        self._contour = contour

    # Glyph

    glyph: dynamicProperty = dynamicProperty(
        "glyph",
        """Get the point's parent glyph object.

        This property is read-only.

        The value must be a :class:`BaseGlyph` instance or :obj:`None`.

        :return: The :class:`BaseGlyph` instance containing the point
            or :obj:`None`.

        Example::

            >>> glyph = point.glyph

        """,
    )

    def _get_glyph(self) -> Optional[BaseObject]:
        if self._contour is None:
            return None
        return self.contour.glyph

    # Layer

    layer: dynamicProperty = dynamicProperty(
        "layer",
        """Get the point's parent layer object.

        This property is read-only.

        :return: The :class:`BaseLayer` instance containing the point
            or :obj:`None`.

        Example::

            >>> layer = point.layer

        """,
    )

    def _get_layer(self) -> Optional[BaseObject]:
        if self._contour is None:
            return None
        return self.glyph.layer

    # Font

    font: dynamicProperty = dynamicProperty(
        "font",
        """Get the point's parent font object.

        This property is read-only.

        :return: The :class:`BaseFont` instance containing the point
            or :obj:`None`.

        Example::

            >>> font = point.font

        """,
    )

    def _get_font(self) -> Optional[BaseObject]:
        if self._contour is None:
            return None
        return self.glyph.font

    # ----------
    # Attributes
    # ----------

    # type

    type: dynamicProperty = dynamicProperty(
        "base_type",
        """Get or set the point's type.

        The value must be a :class:`str` containing one of the following
        alternatives:

        +----------------+---------------------------------+
        | Type           | Description                     |
        +----------------+---------------------------------+
        | ``'move'``     | An on-curve move to.            |
        | ``'line'``     | An on-curve line to.            |
        | ``'curve'``    | An on-curve cubic curve to.     |
        | ``'qcurve'``   | An on-curve quadratic curve to. |
        | ``'offcurve'`` | An off-curve.                   |
        +----------------+---------------------------------+

        :return: A :class:`str` representing the type of the point.

        """,
    )

    def _get_base_type(self) -> str:
        value = self._get_type()
        value = normalizers.normalizePointType(value)
        return value

    def _set_base_type(self, value: str) -> None:
        value = normalizers.normalizePointType(value)
        self._set_type(value)

    def _get_type(self) -> str:  # type: ignore[return]
        """Get the native point's type.

        This is the environment implementation of the :attr:`BasePoint.type`
        property getter.

        :return: A :class:`str` representing the type of the point. The value
            will be normalized with :func:`normalizers.normalizePointType`.
        :raises NotImplementedError: If the method has not been overridden by
            a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_type(self, value: str) -> None:
        """Set the native point's type.

        Description

        This is the environment implementation of the :attr:`BasePoint.type`
        property setter.

        :param value: The point type definition as a :class:`str`. The value
            will have been normalized with :func:`normalizers.normalizePointType`.
        :raises NotImplementedError: If the method has not been overridden by
            a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # smooth

    smooth: dynamicProperty = dynamicProperty(
        "base_smooth",
        """Get or set the point's smooth state.

        The value must be a :class:`bool` indicating the point's smooth state.

        :return: :obj:`True` if the point is smooth, :obj:`False` if it is sharp.

        Example::

            >>> point.smooth
            False
            >>> point.smooth = True

        """,
    )

    def _get_base_smooth(self) -> bool:
        value = self._get_smooth()
        value = normalizers.normalizeBoolean(value)
        return value

    def _set_base_smooth(self, value: bool) -> None:
        value = normalizers.normalizeBoolean(value)
        self._set_smooth(value)

    def _get_smooth(self) -> bool:  # type: ignore[return]
        """Get the native point's smooth state.

        This is the environment implementation of the :attr:`BasePoint.smooth`
        property getter.

        :return: A :class:`bool` indicating the point's smooth state. The value
            will be normalized with :func:`normalizers.normalizeBoolean`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_smooth(self, value: bool) -> None:
        """Set the native point's smooth state.

        This is the environment implementation of the :attr:`BasePoint.smooth`
        property setter.

        :param value: The point's smooth state as a :class:`bool`. The value
            will have been normalized with :func:`normalizers.normalizeBoolean`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # x

    x: dynamicProperty = dynamicProperty(
        "base_x",
        """Get or set the x coordinate of the point.

        The value must be an :class:`int` or a :class:`float`.

        :return: An :class:`int` or a :class:`float` representing the point's
            x coordinate.

        Example::

            >>> point.x
            100
            >>> point.x = 101

        """,
    )

    def _get_base_x(self) -> IntFloatType:
        value = self._get_x()
        value = normalizers.normalizeX(value)
        return value

    def _set_base_x(self, value: IntFloatType) -> None:
        value = normalizers.normalizeX(value)
        self._set_x(value)

    def _get_x(self) -> IntFloatType:  # type: ignore[return]
        """Get the x coordinate of the native point.

        Description

        This is the environment implementation of the :attr:`BasePoint.x`
        property getter.

        :return: An :class:`int` or a :class:`float` representing the point's
            x coordinate. The value will be normalized with
            :func:`normalizers.normalizeX`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_x(self, value: IntFloatType) -> None:
        """Set the x coordinate of the native point.

        This is the environment implementation of the :attr:`BasePoint.x`
        property setter.

        :param value: The point's x coodinate to set as an :class:`int`
            or :class:`float`. The value will have been normalized
            with :func:`normalizers.normalizeX`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # y

    y: dynamicProperty = dynamicProperty(
        "base_y",
        """Get or set the y coordinate of the point.

        The value must be an :class:`int` or a :class:`float`.

        :return: An :class:`int` or a :class:`float` representing the point's
            y coordinate.

        Example::

            >>> point.y
            100
            >>> point.y = 101

        """,
    )

    def _get_base_y(self) -> IntFloatType:
        value = self._get_y()
        value = normalizers.normalizeY(value)
        return value

    def _set_base_y(self, value: IntFloatType) -> None:
        value = normalizers.normalizeY(value)
        self._set_y(value)

    def _get_y(self) -> IntFloatType:  # type: ignore[return]
        """Get the y coordinate of the native point.

        This is the environment implementation of the :attr:`BasePoint.y`
        property getter.

        :return: An :class:`int` or a :class:`float` representing the point's
            y coordinate. The value will be normalized
            with :func:`normalizers.normalizeY`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_y(self, value: IntFloatType) -> None:
        """Set the y coordinate of the native point.

        This is the environment implementation of the :attr:`BasePoint.y`
        property setter.

        :param value: The point's y coordinate as an :class:`int`
            or :class:`float`. The value will have been normalized
            with :func:`normalizers.normalizeY`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # --------------
    # Identification
    # --------------

    # index

    index: dynamicProperty = dynamicProperty(
        "base_index",
        """Get the index of the point.

        This property is read-only.

        :return: An :class:`int` representing the point's index within an
            ordered list of the parent contour's points, or :obj:`None` if the
            point does not belong to a contour.

        Example::

            >>> point.index
            0

        """,
    )

    def _get_base_index(self) -> Optional[int]:
        value = self._get_index()
        value = normalizers.normalizeIndex(value)
        return value

    def _get_index(self) -> Optional[int]:
        """Get the index of the native point.

        This is the environment implementation of the :attr:`BasePoint.index`
        property getter.

        :return: An :class:`int` representing the point's index within an
            ordered list of the parent contour's points, or :obj:`None` if the
            point does not belong to a contour. The value will be
            normalized with :func:`normalizers.normalizeIndex`.

        .. note::

            Subclasses may override this method.

        """
        contour = self.contour
        if contour is None:
            return None
        return contour.points.index(self)

    # name

    name: dynamicProperty = dynamicProperty(
        "base_name",
        """Get or set the name of the point.

        The value must be a :class:`str` or :obj:`None`.

        :return: A :class:`str` representing the point's name or :obj:`None`.

        Example::

            >>> point.name
            'my point'
            >>> point.name = None

        """,
    )

    def _get_base_name(self) -> Optional[str]:
        value = self._get_name()
        if value is not None:
            value = normalizers.normalizePointName(value)
        return value

    def _set_base_name(self, value: str) -> None:
        if value is not None:
            value = normalizers.normalizePointName(value)
        self._set_name(value)

    def _get_name(self) -> Optional[str]:  # type: ignore[return]
        """Get the name of the native point.

        This is the environment implementation of the :attr:`BasePoint.name`
        property getter.

        :return: A :class:`str` representing the point's name or :obj:`None`.
            The value will be normalized with :func:`normalizers.normalizePointName`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_name(self, value: str) -> None:
        """Set the name of the native point.

        This is the environment implementation of the :attr:`BasePoint.name`
        property setter.

        :param value: The point name as a :class:`str`. The value
            will have been normalized with :func:`normalizers.normalizePointName`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # --------------
    # Transformation
    # --------------

    def _transformBy(
        self, matrix: SextupleCollectionType[IntFloatType], **kwargs: Any
    ) -> None:
        r"""Transform the native point.

        This is the environment implementation of :meth:`BasePoint.transformBy`.

        :param matrix: The transformation to apply as a :ref:`type-transformation`.
        :param \**kwargs: Additional keyword arguments.

        .. note::

            Subclasses may override this method.

        """
        t = transform.Transform(*matrix)
        x, y = t.transformPoint((self.x, self.y))
        self.x = x
        self.y = y

    # -------------
    # Normalization
    # -------------

    def round(self) -> None:
        """Round the point's coordinates.

        This applies to:

        - :attr:`x`
        - :attr:`y`

        Example::

            >>> point.round()

        """
        self._round()

    def _round(self, **kwargs: Any) -> None:
        r"""Round the native point's coordinates.

        This is the environment implementation of :meth:`BasePoint.round`.

        :param \**kwargs: Additional keyword arguments.

        .. note::

            Subclasses may override this method.

        """
        self.x = normalizers.normalizeVisualRounding(self.x)
        self.y = normalizers.normalizeVisualRounding(self.y)
