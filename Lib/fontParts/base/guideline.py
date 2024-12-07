from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, Optional, Union, List, Tuple
import math
from fontTools.misc import transform
from fontParts.base.base import (
    BaseObject,
    TransformationMixin,
    InterpolationMixin,
    SelectionMixin,
    PointPositionMixin,
    IdentifierMixin,
    dynamicProperty,
    reference,
)
from fontParts.base import normalizers
from fontParts.base.compatibility import GuidelineCompatibilityReporter
from fontParts.base.color import Color
from fontParts.base.deprecated import DeprecatedGuideline, RemovedGuideline
from fontParts.base.annotations import (
    QuadrupleType,
    QuadrupleCollectionType,
    SextupleCollectionType,
    IntFloatType,
)

if TYPE_CHECKING:
    from fontParts.base.font import BaseFont
    from fontParts.base.layer import BaseLayer
    from fontParts.base.glyph import BaseGlyph


class BaseGuideline(
    BaseObject,
    TransformationMixin,
    DeprecatedGuideline,
    RemovedGuideline,
    PointPositionMixin,
    InterpolationMixin,
    IdentifierMixin,
    SelectionMixin,
):
    """Represent the basis for a guideline object.

    This object is almost always created with :meth:`BaseGlyph.appendGuideline`.
    An orphan guideline can be created like this::

        >>> guideline = RGuideline()

    """

    copyAttributes: Tuple[str, ...] = ("x", "y", "angle", "name", "color")

    def _reprContents(self) -> List[str]:
        contents = []
        if self.name is not None:
            contents.append(f"'{self.name}'")
        if self.layer is not None:
            contents.append(f"('{self.layer.name}')")
        return contents

    # -------
    # Parents
    # -------

    # Glyph

    _glyph: Optional[Callable[[], BaseGlyph]] = None

    glyph: dynamicProperty = dynamicProperty(
        "glyph",
        """Get or set the guideline's parent glyph object.

        The value must be a :class:`BaseGlyph` instance or :obj:`None`.

        :return: The :class:`BaseGlyph` instance containing the guideline
            or :obj:`None`.
        :raises AssertionError: If attempting to set the glyph when it
            has already been set.

        Example::

            >>> glyph = guideline.glyph

        """,
    )

    def _get_glyph(self) -> Optional[BaseGlyph]:
        if self._glyph is None:
            return None
        return self._glyph()

    def _set_glyph(
        self, glyph: Optional[Union[BaseGlyph, Callable[[], BaseGlyph]]]
    ) -> None:
        if self._font is not None:
            raise AssertionError("font for guideline already set")
        if self._glyph is not None:
            raise AssertionError("glyph for guideline already set")
        if glyph is not None:
            glyph = reference(glyph)
        self._glyph = glyph

    # Layer

    layer: dynamicProperty = dynamicProperty(
        "layer", "The guideline's parent :class:`BaseLayer`."
    )

    def _get_layer(self) -> Optional[BaseLayer]:
        if self._glyph is None:
            return None
        return self.glyph.layer

    # Font

    _font: Optional[Callable[[], BaseFont]] = None

    font: dynamicProperty = dynamicProperty(
        "font",
        """Get the guideline's parent font object.

        This property is read-only.

        :return: The :class:`BaseFont` instance containing the guideline
            or :obj:`None`.

        Example::

            >>> font = guideline.font

        """,
    )

    def _get_font(self) -> Optional[BaseFont]:
        if self._font is not None:
            return self._font()
        elif self._glyph is not None:
            return self.glyph.font
        return None

    def _set_font(
        self, font: Optional[Union[BaseFont, Callable[[], BaseFont]]]
    ) -> None:
        if self._font is not None:
            raise AssertionError("font for guideline already set")
        if self._glyph is not None:
            raise AssertionError("glyph for guideline already set")
        if font is not None:
            font = reference(font)
        self._font = font

    # --------
    # Position
    # --------

    # x

    x: dynamicProperty = dynamicProperty(
        "base_x",
        """Get or set the guideline's x-coordinate.

        The value must be an :class:`int` or a :class:`flat`.

        :return: An :class:`int` or a :class:`flat` representing the
            x-coordinate of the guideline.

        Example::

            >>> guideline.x
            100
            >>> guideline.x = 101

        """,
    )

    def _get_base_x(self) -> IntFloatType:
        value = self._get_x()
        if value is None:
            return 0
        value = normalizers.normalizeX(value)
        return value

    def _set_base_x(self, value: IntFloatType) -> None:
        if value is None:
            value = 0
        else:
            value = normalizers.normalizeX(value)
        self._set_x(value)

    def _get_x(self) -> IntFloatType:
        """Get the native guideline's x-coordinate.

        This is the environment implementation of the :attr:`BaseGuideline.x` property
        getter.

        :return: An :class:`int` or a :class:`flat` representing the
            x-coordinate of the guideline. The value will be normalized
            with :func:`normalizers.normalizeX`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_x(self, value: IntFloatType) -> None:
        """Set the native guideline's x-coordinate.

        This is the environment implementation of the :attr:`BaseGuideline.x` property
        setter.

        :param value: The x-coordinate to set as an :class:`int` or a :class:`float`.
            The value will have been normalized with :func:`normalizers.normalizeX`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # y

    y: dynamicProperty = dynamicProperty(
        "base_y",
        """Get or set the guideline's y-coordinate.

        The value must be an :class:`int` or a :class:`flat`.

        :return: An :class:`int` or a :class:`flat` representing the
            y-coordinate of the guideline.

        Example::

            >>> guideline.y
            100
            >>> guideline.y = 101

        """,
    )

    def _get_base_y(self) -> IntFloatType:
        value = self._get_y()
        if value is None:
            return 0
        value = normalizers.normalizeY(value)
        return value

    def _set_base_y(self, value: IntFloatType) -> None:
        if value is None:
            value = 0
        else:
            value = normalizers.normalizeY(value)
        self._set_y(value)

    def _get_y(self) -> IntFloatType:
        """Get the native guideline's y-coordinate.

        This is the environment implementation of the :attr:`BaseGuideline.y` property
        getter.

        :return: An :class:`int` or a :class:`flat` representing the
            y-coordinate of the guideline. The value will be normalized
            with :func:`normalizers.normalizeY`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_y(self, value: IntFloatType) -> None:
        """Set the native guideline's y-coordinate.

        This is the environment implementation of the :attr:`BaseGuideline.y` property
        setter.

        :param value: The y-coordinate to set as an :class:`int` or a :class:`float`.
            The value will have been normalized with :func:`normalizers.normalizeY`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # angle

    angle: dynamicProperty = dynamicProperty(
        "base_angle",
        """Get or set the guideline's angle.

        The value must be :class:`int`, :class:`float` or :obj:`None`.
        If set to :obj:`None`, the angle is automatically derived based on
        the guideline's :attr:`x` and :attr:`y` values:

        - If both :attr:`x` and :attr:`y` are 0, the angle defaults to ``0.0``.
        - If :attr:`x` is 0 and :attr:`y` is not, the angle is ``90.0``.
        - If :attr:`y` is 0 and :attr:`x` is not, the angle is ``0.0``.

        :return: A :class:`float` representing the angle of the guideline.

        Example::

            >>> guideline.angle
            45.0
            >>> guideline.angle = 90

        """,
    )

    def _get_base_angle(self) -> float:
        value = self._get_angle()
        if value is None:
            if self._get_x() != 0 and self._get_y() != 0:
                value = 0
            elif self._get_x() != 0 and self._get_y() == 0:
                value = 90
            elif self._get_x() == 0 and self._get_y() != 0:
                value = 0
            else:
                value = 0
        value = normalizers.normalizeRotationAngle(value)
        return value

    def _set_base_angle(self, value: Optional[IntFloatType]) -> None:
        if value is None:
            if self._get_x() != 0 and self._get_y() != 0:
                value = 0
            elif self._get_x() != 0 and self._get_y() == 0:
                value = 90
            elif self._get_x() == 0 and self._get_y() != 0:
                value = 0
            else:
                value = 0
        value = normalizers.normalizeRotationAngle(value)
        self._set_angle(value)

    def _get_angle(self) -> Optional[IntFloatType]:
        """Get the native guideline's angle.

        This is the environment implementation of the :attr:`BaseGuideline.angle`
        property getter.

        :return: An :class:`int` or a :class:`float` representing the angle of
            the guideline, or :obj:`None`. The value will be normalized
            with :func:`normalizers.normalizeRotationAngle`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_angle(self, value: Optional[IntFloatType]) -> None:
        """Set the native guideline's angle.

        This is the environment implementation of the :attr:`BaseGuideline.angle`
        property setter.

        :param value: The angle to set as an :class:`int` or a :class:`float`,
            or :obj:`None`. The value will have been normalized
            with :func:`normalizers.normalizeRotationAngle`.
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
        """Get the guideline's index.

        This property is read-only.

        :return: An :class:`int` representing the index of the guideline within
            the ordered list of the parent glyph's guidelines.

        Example::

            >>> guideline.index
            0

        """,
    )

    def _get_base_index(self) -> Optional[int]:
        value = self._get_index()
        value = normalizers.normalizeIndex(value)
        return value

    def _get_index(self) -> Optional[int]:
        """Get the native guideline's index.

        This is the environment implementation of the :attr:`BaseGuideline.index`
        property getter.

        :return: An :class:`int` representing the index of the guideline within
            the ordered list of the parent glyph's guidelines. The value will be
            normalized with :func:`normalizers.normalizeIndex`.

        .. note::

            Subclasses may override this method.

        """
        glyph = self.glyph
        if glyph is not None:
            parent = glyph
        else:
            parent = self.font
        if parent is None:
            return None
        return parent.guidelines.index(self)

    # name

    name: dynamicProperty = dynamicProperty(
        "base_name",
        """Get or set the guideline's name.

        The value must be a :class:`str` or :obj: `None`.

        :return: A :class:`str` representing the name of the guideline, or :obj:`None`.

            >>> guideline.name
            'my guideline'
            >>> guideline.name = None

        """,
    )

    def _get_base_name(self) -> Optional[str]:
        value = self._get_name()
        if value is not None:
            value = normalizers.normalizeGuidelineName(value)
        return value

    def _set_base_name(self, value: Optional[str]) -> None:
        if value is not None:
            value = normalizers.normalizeGuidelineName(value)
        self._set_name(value)

    def _get_name(self) -> Optional[str]:
        """Get the native guideline's name.

        This is the environment implementation of the :attr:`BaseGuideline.name`
        property getter.

        :return: A :class:`str` representing the name of the guideline,
            or :obj:`None`. The value will have been normalized
            with :func:`normalizers.normalizeGuidelineName`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_name(self, value: Optional[str]) -> None:
        """Set the native guideline's name.

        This is the environment implementation of the :attr:`BaseGuideline.name`
        property setter.

        :param value: The name to set as a :class:`str` or :obj:`None`. The
            value will have been normalized
            with :func:`normalizers.normalizeGuidelineName`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # color

    color: dynamicProperty = dynamicProperty(
        "base_color",
        """"Get or set the guideline's color.

        The value must be a :ref:`type-color` or :obj:`None`.

        :return: A :ref:`type-color` representing the color of the guideline,
            or :obj:`None`.

        Example::

            >>> guideline.color
            None
            >>> guideline.color = (1, 0, 0, 0.5)

        """,
    )

    def _get_base_color(self) -> QuadrupleType[float]:
        value = self._get_color()
        if value is not None:
            value = normalizers.normalizeColor(value)
            value = Color(value)
        return value

    def _set_base_color(self, value: QuadrupleCollectionType[IntFloatType]) -> None:
        if value is not None:
            value = normalizers.normalizeColor(value)
        self._set_color(value)

    def _get_color(self) -> QuadrupleType[float]:
        """ "Get the native guideline's color.

        This is the environment implementation of the :attr:`BaseGuideline.color`
        property getter.

        :return: A :ref:`type-color` representing the color of the guideline,
            or :obj:`None`. The value will be normalized
         with :func:`normalizers.normalizeColor`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_color(self, value: QuadrupleCollectionType[IntFloatType]) -> None:
        """ "Set the native guideline's color.

        Description

        This is the environment implementation of the :attr:`BaseGuideline.color`
        property setter.

        :param value: The :ref:`type-color` to set for the guideline or :obj:`None`.
            The value will have been normalized with :func:`normalizers.normalizeColor`.
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
        r"""Transform the native guideline according to the given matrix.

        This is the environment implementation of :meth:`BaseGuideline.transformBy`.

        :param matrix: The :ref:`type-transformation` to apply. The value will
             be normalized with :func:`normalizers.normalizeTransformationMatrix`.
        :param \**kwargs: Additional keyword arguments.

        .. note::

            Subclasses may override this method.

        """
        t = transform.Transform(*matrix)
        # coordinates
        x, y = t.transformPoint((self.x, self.y))
        self.x = x
        self.y = y
        # angle
        angle = math.radians(-self.angle)
        dx = math.cos(angle)
        dy = math.sin(angle)
        tdx, tdy = t.transformPoint((dx, dy))
        ta = math.atan2(tdy - t[5], tdx - t[4])
        self.angle = -math.degrees(ta)

    # -------------
    # Interpolation
    # -------------

    compatibilityReporterClass = GuidelineCompatibilityReporter

    def isCompatible(
        self, other: BaseGuideline, cls=None
    ) -> Tuple[bool, GuidelineCompatibilityReporter]:
        """Evaluate interpolation compatibility with another guideline.

        :param other: The other :class:`BaseGuideline` instance to check
            compatibility with.
        :return: A :class:`tuple` where the first element is a :class:`bool`
            indicating compatibility, and the second element is
            a :class:`fontParts.base.compatibility.GuidelineCompatibilityReporter`
            instance.

        Example::

            >>> compatible, report = self.isCompatible(otherGuideline)
            >>> compatible
            True
            >>> compatible
            [Warning] Guideline: "xheight" + "cap_height"
            [Warning] Guideline: "xheight" has name xheight | "cap_height" has
                                  name cap_height

        """
        return super(BaseGuideline, self).isCompatible(other, BaseGuideline)

    def _isCompatible(
        self, other: BaseGuideline, reporter: GuidelineCompatibilityReporter
    ) -> None:
        """Evaluate interpolation compatibility with another native guideline.

        This is the environment implementation of :meth:`BaseGuideline.isCompatible`.

        :param other: The other :class:`BaseGuideline` instance to check
            compatibility with.
        :param reporter: An object used to report compatibility issues.

        .. note::

            Subclasses may override this method.

        """
        guideline1 = self
        guideline2 = other
        # guideline names
        if guideline1.name != guideline2.name:
            reporter.nameDifference = True
            reporter.warning = True

    # -------------
    # Normalization
    # -------------

    def round(self) -> None:
        """Round the guideline's coordinate.

        This applies to:

        - :attr:`x`
        - :attr:`y

        It does not apply to :attr:`angle`.

        Example::`

            >>> guideline.round()


        """
        self._round()

    def _round(self, **kwargs: Any) -> None:
        r"""Round the native guideline's coordinate.

        This is the environment implementation of :meth:`BaseGuideline.round`.

        :param \**kwargs: Additional keyword arguments.

        .. note::

            Subclasses may override this method.

        """
        self.x = normalizers.normalizeVisualRounding(self.x)
        self.y = normalizers.normalizeVisualRounding(self.y)
