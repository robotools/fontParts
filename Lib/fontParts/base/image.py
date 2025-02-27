from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, Optional, Tuple, Union

from fontTools.misc import transform
from fontParts.base.base import (
    BaseObject,
    TransformationMixin,
    SelectionMixin,
    dynamicProperty,
    reference,
)
from fontParts.base import normalizers
from fontParts.base.color import Color
from fontParts.base.deprecated import DeprecatedImage, RemovedImage
from fontParts.base.annotations import (
    PairType,
    PairCollectionType,
    QuadrupleType,
    QuadrupleCollectionType,
    SextupleType,
    SextupleCollectionType,
    IntFloatType,
    TransformationType,
)

if TYPE_CHECKING:
    from fontParts.base.glyph import BaseGlyph
    from fontParts.base.layer import BaseLayer
    from fontParts.base.font import BaseFont


class BaseImage(
    BaseObject,
    TransformationMixin,
    SelectionMixin,
    DeprecatedImage,
    RemovedImage,
):
    """Represent the basis for an image object."""

    copyAttributes = ("transformation", "color", "data")

    def _reprContents(self) -> list[str]:
        contents = [
            f"offset='({self.offset[0]}, {self.offset[1]})'",
        ]
        if self.color:
            contents.append(f"color={self.color!r}")
        if self.glyph is not None:
            contents.append("in glyph")
            contents += self.glyph._reprContents()
        return contents

    def __bool__(self) -> bool:
        if self.data is None:
            return False
        elif len(self.data) == 0:
            return False
        else:
            return True

    __nonzero__ = __bool__

    # -------
    # Parents
    # -------

    # Glyph

    _glyph: Optional[Callable[[], BaseGlyph]] = None

    glyph = dynamicProperty(
        "glyph",
        """Get or set the image's parent glyph object.

        The value must be a :class:`BaseGlyph` instance or :obj:`None`.

        :return: The :class:`BaseGlyph` instance containing the image
            or :obj:`None`.
        :raises AssertionError: If attempting to set the glyph when it
            has already been set.

        Example::

            >>> glyph = image.glyph

        """,
    )

    def _get_glyph(self) -> Optional[BaseGlyph]:
        if self._glyph is None:
            return None
        return self._glyph()

    def _set_glyph(
        self, glyph: Optional[Union[BaseGlyph, Callable[[], BaseGlyph]]]
    ) -> None:
        if self._glyph is not None:
            raise AssertionError("glyph for image already set")
        if glyph is not None:
            glyph = reference(glyph)
        self._glyph = glyph

    # Layer

    layer: dynamicProperty = dynamicProperty(
        "layer",
        """Get the image's parent layer object.

        This property is read-only.

        :return: The :class:`BaseLayer` instance containing the image
            or :obj:`None`.

        Example::

            >>> layer = image.layer

        """,
    )

    def _get_layer(self) -> Optional[BaseLayer]:
        if self._glyph is None:
            return None
        return self.glyph.layer

    # Font

    font: dynamicProperty = dynamicProperty(
        "font",
        """Get the image's parent font object.

        This property is read-only.

        :return: The :class:`BaseFont` instance containing the image
            or :obj:`None`.

        Example::

            >>> font = image.font

        """,
    )

    def _get_font(self) -> Optional[BaseFont]:
        if self._glyph is None:
            return None
        return self.glyph.font

    # ----------
    # Attributes
    # ----------

    # Transformation

    transformation: dynamicProperty = dynamicProperty(
        "base_transformation",
        """Get or set the image's transformation matrix.

        The value must be a :ref:`type-transformation`.

        :return: A :ref:`type-transformation` value representing the
            transformation matrix of the image.

        Example::

            >>> image.transformation
            (1, 0, 0, 1, 0, 0)
            >>> image.transformation = (2, 0, 0, 2, 100, -50)
            
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

    def _get_transformation(self) -> SextupleCollectionType[IntFloatType]:
        """Get the native image's transformation matrix.

        This is the environment implementation of the
        :attr:`BaseImage.transformation` property getter.

        :return: A :ref:`type-transformation` value representing the
            transformation matrix of the image. The value will be
            normalized with :func:`normalizers.normalizeTransformationMatrix`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_transformation(self, value: SextupleCollectionType[IntFloatType]) -> None:
        """Set the native image's transformation matrix.

        This is the environment implementation of the
        :attr:`BaseImage.transformation` property setter.

        :param value: The :ref:`type-transformation` to set. The value will have
            been normalized with :func:`normalizers.normalizeTransformationMatrix`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    offset: dynamicProperty = dynamicProperty(
        "base_offset",
        """Get or set the component's offset.

        The value must be a :ref:`type-coordinate.`

        :return: A :ref:`type-coordinate.` representing the offset of the image.

        Example::

            >>> image.offset
            (0, 0)
            >>> image.offset = (100, -50)

        """,
    )

    def _get_base_offset(self) -> PairType[IntFloatType]:
        value = self._get_offset()
        value = normalizers.normalizeTransformationOffset(value)
        return value

    def _set_base_offset(self, value: PairCollectionType[IntFloatType]) -> None:
        value = normalizers.normalizeTransformationOffset(value)
        self._set_offset(value)

    def _get_offset(self) -> PairCollectionType[IntFloatType]:
        """Get the native image's offset.

        This is the environment implementation of the :attr:`BaseImage.offset`
        property getter.

        :return: A :ref:`type-coordinate.` representing the offset of the image.
            The value will be normalized
            with :func:`normalizers.normalizeTransformationOffset`.

        .. note::

            Subclasses may override this method.

        """
        sx, sxy, syx, sy, ox, oy = self.transformation
        return (ox, oy)

    def _set_offset(self, value: PairType[IntFloatType]) -> None:
        """Set the native image's offset.

        This is the environment implementation of the :attr:`BaseImage.offset`
        property setter.

        :param value: The offset to set as a :ref:`type-coordinate.`. The value will
            have been normalized with :func:`normalizers.normalizeTransformationOffset`.

        .. note::

            Subclasses may override this method.

        """
        sx, sxy, syx, sy, ox, oy = self.transformation
        ox, oy = value
        self.transformation = (sx, sxy, syx, sy, ox, oy)

    scale: dynamicProperty = dynamicProperty(
        "base_scale",
        """Get or set the image's scale.

        The value must be a :class:`list` or :class:`tuple` of two :class:`int`
        or :class:`float` items representing the ``(x, y)`` scale of the image.

        :return: A :class:`tuple` of two :class:`float` items representing the
            ``(x, y)`` scale of the image.

        Example::

            >>> image.scale
            (1, 1)
            >>> image.scale = (2, 2)
            
        """,
    )

    def _get_base_scale(self) -> PairType[float]:
        value = self._get_scale()
        value = normalizers.normalizeTransformationScale(value)
        return value

    def _set_base_scale(self, value: TransformationType) -> None:
        value = normalizers.normalizeTransformationScale(value)
        self._set_scale(value)

    def _get_scale(self) -> TransformationType:
        """Get the native image's scale.

        This is the environment implementation of the :attr:`BaseImage.scale`
        property getter.

        :return: A :class:`tuple` of two :class:`float` items representing the
            ``(x, y)`` scale of the image. The value will have been normalized
            with :func:`normalizers.normalizeComponentScale`.

        .. note::

            Subclasses may override this method.

        """
        sx, sxy, syx, sy, ox, oy = self.transformation
        return (sx, sy)

    def _set_scale(self, value: PairType[float]) -> None:
        """Set the native image's scale.

        This is the environment implementation of the :attr:`BaseImage.scale`
        property setter.

        :param value: The scale to set as a :class:`list` or :class:`tuple`
            of :class:`int` or :class:`float` items representing the ``(x, y)``
            scale of the image. The value will have been normalized
            with :func:`normalizers.normalizeComponentScale`.

        .. note::

            Subclasses may override this method.

        """
        sx, sxy, syx, sy, ox, oy = self.transformation
        sx, sy = value
        self.transformation = (sx, sxy, syx, sy, ox, oy)

    # Color

    color: dynamicProperty = dynamicProperty(
        "base_color",
        """Get or set the image's color.

        The value must be a :ref:`type-color` or :obj`None`.

        :return: A :class:`Color` instance representing the color of the image,
            or :obj:`None`.

        Example::

            >>> image.color
            None
            >>> image.color = (1, 0, 0, 0.5)

        """,
    )

    def _get_base_color(self) -> Optional[Color]:
        value = self._get_color()
        if value is not None:
            value = Color(value)
        return value

    def _set_base_color(
        self, value: Optional[QuadrupleCollectionType[IntFloatType]]
    ) -> None:
        if value is not None:
            value = normalizers.normalizeColor(value)
        self._set_color(value)

    def _get_color(self) -> Optional[QuadrupleCollectionType[IntFloatType]]:
        """Get the native image's color.

        This is the environment implementation of the :attr:`BaseImage.color`
        property getter.

        :return: A :ref:`type-color` representing the color of the image,
            or :obj:`None`. The value will be normalized
            with :func:`normalizers.normalizeColor`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_color(self, value: Optional[QuadrupleType[float]]) -> None:
        """Set the native image's color.

        This is the environment implementation of the :attr:`BaseImage.color`
        property setter.

        :param value: The :ref:`type-color` to set for the image or :obj:`None`.
            The value will have been normalized with :func:`normalizers.normalizeColor`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # Data

    data: dynamicProperty = dynamicProperty(
        "data",
        """Get or set the image's raw byte data.
        
        The possible formats are defined by each environment.
        The value must be a :class:`bytes` object.

        :return: A :class:`bytes` object representing the raw byte data of the image.

        """,
    )

    def _get_base_data(self) -> bytes:
        return self._get_data()

    def _set_base_data(self, value: bytes) -> None:
        self._set_data(value)

    def _get_data(self) -> bytes:
        """Get the native image's raw byte data.

        This is the environment implementation of the :attr:`BaseImage.data`
        property getter.

        :return: A :class:`bytes` object representing the data of the image.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_data(self, value: bytes) -> None:
        """Set the native image's color.

        This is the environment implementation of the :attr:`BaseImage.color`
        property setter.

        :param value: The :class:`bytes` object to set for the image.
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
        r"""Transform the native image.

        This is the environment implementation of :meth:`BaseImage.transformBy`.

        :param matrix: The transformation to apply as a :ref:`type-transformation`.
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
        """Round the images's offset coordinates.

        Example::

            >>> image.round()

        """
        self._round()

    def _round(self) -> None:
        """Round the native images's offset coordinates.

        This is the environment implementation of :meth:`BaseImage.round`.

        .. note::

            Subclasses may override this method.

        """
        x, y = self.offset
        x = normalizers.normalizeVisualRounding(x)
        y = normalizers.normalizeVisualRounding(y)
        self.offset = (x, y)
