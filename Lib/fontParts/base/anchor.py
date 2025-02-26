from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, Optional, Union, List, Tuple

from fontTools.misc import transform
from fontParts.base import normalizers
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
from fontParts.base.compatibility import AnchorCompatibilityReporter
from fontParts.base.color import Color
from fontParts.base.deprecated import DeprecatedAnchor, RemovedAnchor
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


class BaseAnchor(
    BaseObject,
    TransformationMixin,
    DeprecatedAnchor,
    RemovedAnchor,
    PointPositionMixin,
    InterpolationMixin,
    SelectionMixin,
    IdentifierMixin,
):
    """Represent the basis for an anchor object.

    This object is almost always created with :meth:`BaseGlyph.appendAnchor`.
    An orphan anchor can be created like this::

        >>> anchor = RAnchor()

    """

    def _reprContents(self) -> List[str]:
        contents = [
            f"({self.x}, {self.y})",
        ]
        if self.name is not None:
            contents.append(f"name='{self.name}'")
        if self.color:
            contents.append(f"color={self.color!r}")
        return contents

    # ----
    # Copy
    # ----

    copyAttributes: Tuple[str, ...] = ("x", "y", "name", "color")

    # -------
    # Parents
    # -------

    # Glyph

    _glyph: Optional[Callable[[], BaseGlyph]] = None

    glyph: dynamicProperty = dynamicProperty(
        "glyph", "The anchor's parent :class:`BaseGlyph`."
    )

    def _get_glyph(self) -> Optional[BaseGlyph]:
        if self._glyph is None:
            return None
        return self._glyph()

    def _set_glyph(
        self, glyph: Optional[Union[BaseGlyph, Callable[[], BaseGlyph]]]
    ) -> None:
        if self._glyph is not None:
            raise AssertionError("glyph for anchor already set")
        if glyph is not None:
            glyph = reference(glyph)
        self._glyph = glyph

    # Layer

    layer: dynamicProperty = dynamicProperty(
        "layer", "The anchor's parent :class:`BaseLayer`."
    )

    def _get_layer(self) -> Optional[BaseLayer]:
        if self._glyph is None:
            return None
        return self.glyph.layer

    # Font

    font: dynamicProperty = dynamicProperty(
        "font", "The anchor's parent :class:`BaseFont`."
    )

    def _get_font(self) -> Optional[BaseFont]:
        if self._glyph is None:
            return None
        return self.glyph.font

    # --------
    # Position
    # --------

    # x

    x = dynamicProperty(
        "base_x",
        """Get or set the anchor's x-coordinate.

        The value must be an :class:`int` or a :class:`float`.

        :return: An :class:`int` or a :class:`float` representing the
            x-coordinate of the anchor.

        Example::

            >>> anchor.x
            100
            >>> anchor.x = 101

        """,
    )

    def _get_base_x(self) -> IntFloatType:
        value = self._get_x()
        value = normalizers.normalizeX(value)
        return value

    def _set_base_x(self, value: IntFloatType) -> None:
        value = normalizers.normalizeX(value)
        self._set_x(value)

    def _get_x(self) -> IntFloatType:
        """Get the native anchor's x-coordinate.

        This is the environment implementation of the :attr:`BaseAnchor.x` property
        getter.

        :return: An :class:`int` or a :class:`float` representing the
            x-coordinate of the anchor. The value will be normalized
            with :func:`normalizers.normalizeX`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_x(self, value: IntFloatType) -> None:
        """Set the native anchor's x-coordinate.

        This is the environment implementation of the :attr:`BaseAnchor.x` property
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
        """Get or set the anchor's y-coordinate.

        The value must be an :class:`int` or a :class:`float`.

        :return: An :class:`int` or a :class:`float` representing the
            y-coordinate of the anchor.

        Example::

            >>> anchor.y
            100
            >>> anchor.y = 101

        """,
    )

    def _get_base_y(self) -> IntFloatType:
        value = self._get_y()
        value = normalizers.normalizeY(value)
        return value

    def _set_base_y(self, value: IntFloatType) -> None:
        value = normalizers.normalizeY(value)
        self._set_y(value)

    def _get_y(self) -> IntFloatType:
        """Get the native anchor's y-coordinate.

        This is the environment implementation of the :attr:`BaseAnchor.y` property
        getter.

        :return: An :class:`int` or a :class:`float` representing the
            x-coordinate of the anchor. The value will be normalized
            with :func:`normalizers.normalizeY`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_y(self, value: IntFloatType) -> None:
        """Set the native anchor's y-coordinate.

        This is the environment implementation of the :attr:`BaseAnchor.y` property
        setter.

        :param value: The y-coordinate to set as an :class:`int` or a :class:`float`.
            The value will have been normalized with :func:`normalizers.normalizeY`.
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
        """Get the anchor's index.

        This property is read-only.

        :return: An :class:`int` representing the index of the anchor within
            the ordered list of the parent glyph's anchors.

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
        """Get the native anchor's index.

        This is the environment implementation of the :attr:`BaseAnchor.index`
        property getter.

        :return: An :class:`int` representing the index of the anchor within
            the ordered list of the parent glyph's anchors. The value will be
            normalized with :func:`normalizers.normalizeIndex`.

        .. note::

            Subclasses may override this method.

        """
        glyph = self.glyph
        if glyph is None:
            return None
        return glyph.anchors.index(self)

    # name

    name: dynamicProperty = dynamicProperty(
        "base_name",
        """Get or set the anchor's name.

        The value must be a :class:`str` or :obj: `None`.

        :return: A :class:`str` representing the name of the anchor, or :obj:`None`.

            >>> anchor.name
            'my anchor'
            >>> anchor.name = None

        """,
    )

    def _get_base_name(self) -> Optional[str]:
        value = self._get_name()
        if value is not None:
            value = normalizers.normalizeAnchorName(value)
        return value

    def _set_base_name(self, value: Optional[str]) -> None:
        if value is not None:
            value = normalizers.normalizeAnchorName(value)
        self._set_name(value)

    def _get_name(self) -> Optional[str]:
        """Get the native anchor's name.

        This is the environment implementation of the :attr:`BaseAnchor.name`
        property getter.

        :return: A :class:`str` representing the name of the anchor,
            or :obj:`None`. The value will have been normalized
            with :func:`normalizers.normalizeAnchorName`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_name(self, value: Optional[str]) -> None:
        """Set the native anchor's name.

        This is the environment implementation of the :attr:`BaseAnchor.name`
        property setter.

        :param value: The name to set as a :class:`str` or :obj:`None`. The
            value will have been normalized
            with :func:`normalizers.normalizeAnchorName`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # color

    color: dynamicProperty = dynamicProperty(
        "base_color",
        """Get or set the anchor's color.

        The value must be a :ref:`type-color` or :obj:`None`.

        :return: A :ref:`type-color` representing the color of the anchor,
            or :obj:`None`.

        Example::

            >>> anchor.color
            None
            >>> anchor.color = (1, 0, 0, 0.5)

        """,
    )

    def _get_base_color(self) -> Optional[Color]:
        value = self._get_color()
        if value is not None:
            value = normalizers.normalizeColor(value)
            value = Color(value)
        return value

    def _set_base_color(self, value: QuadrupleCollectionType[IntFloatType]) -> None:
        if value is not None:
            value = normalizers.normalizeColor(value)
        self._set_color(value)

    def _get_color(self) -> Optional[QuadrupleCollectionType[IntFloatType]]:
        """Get the native anchor's color.

        This is the environment implementation of the :attr:`BaseAnchor.color`
        property getter.

        :return: A :ref:`type-color` representing the color of the anchor,
            or :obj:`None`. The value will be normalized
         with :func:`normalizers.normalizeColor`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_color(self, value: Optional[QuadrupleType[float]]) -> None:
        """Set the native anchor's color.

        Description

        This is the environment implementation of the :attr:`BaseAnchor.color`
        property setter.

        :param value: The :ref:`type-color` to set for the anchor or :obj:`None`.
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
        r"""Transform the native anchor according to the given matrix.

        This is the environment implementation of :meth:`BaseAnchor.transformBy`.

        :param matrix: The :ref:`type-transformation` to apply. The value will
             be normalized with :func:`normalizers.normalizeTransformationMatrix`.
        :param \**kwargs: Additional keyword arguments.

        .. note::

            Subclasses may override this method.

        """
        t = transform.Transform(*matrix)
        x, y = t.transformPoint((self.x, self.y))
        self.x = x
        self.y = y

    # -------------
    # Interpolation
    # -------------

    compatibilityReporterClass = AnchorCompatibilityReporter

    def isCompatible(
        self, other: BaseAnchor, cls=None
    ) -> Tuple[bool, AnchorCompatibilityReporter]:
        """Evaluate interpolation compatibility with another anchor.

        :param other: The other :class:`BaseAnchor` instance to check
            compatibility with.
        :return: A :class:`tuple` where the first element is a :class:`bool`
            indicating compatibility, and the second element is
            a :class:`fontParts.base.compatibility.AnchorCompatibilityReporter`
            instance.

        Example::

            >>> compatible, report = self.isCompatible(otherAnchor)
            >>> compatible
            True
            >>> compatible
            [Warning] Anchor: "left" + "right"
            [Warning] Anchor: "left" has name left | "right" has name right

        """
        return super(BaseAnchor, self).isCompatible(other, BaseAnchor)

    def _isCompatible(
        self, other: BaseAnchor, reporter: AnchorCompatibilityReporter
    ) -> None:
        """Evaluate interpolation compatibility with another native anchor.

        This is the environment implementation of :meth:`BaseAnchor.isCompatible`.

        :param other: The other :class:`BaseAnchor` instance to check
            compatibility with.
        :param reporter: An object used to report compatibility issues.

        .. note::

            Subclasses may override this method.

        """
        anchor1 = self
        anchor2 = other
        # base names
        if anchor1.name != anchor2.name:
            reporter.nameDifference = True
            reporter.warning = True

    # -------------
    # Normalization
    # -------------

    def round(self) -> None:
        """Round the anchor's coordinate.

        This applies to:

        - :attr:`x`
        - :attr:`y

        Example::`

            >>> guideline.round()

        """
        self._round()

    def _round(self) -> None:
        """Round the native anchor's coordinate.

        This is the environment implementation of :meth:`BaseGuideline.round`.

        .. note::

            Subclasses may override this method.

        """
        self.x = normalizers.normalizeVisualRounding(self.x)
        self.y = normalizers.normalizeVisualRounding(self.y)
