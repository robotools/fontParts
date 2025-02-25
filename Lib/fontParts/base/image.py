from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, Optional, Union

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

    glyph = dynamicProperty("glyph", "The image's parent :class:`BaseGlyph`.")

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
        "layer", "The image's parent :class:`BaseLayer`."
    )

    def _get_layer(self) -> Optional[BaseLayer]:
        if self._glyph is None:
            return None
        return self.glyph.layer

    # Font

    font: dynamicProperty = dynamicProperty(
        "font", "The image's parent :class:`BaseFont`."
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
        """
        The image's :ref:`type-transformation`.
        This defines the image's position, scale,
        and rotation. ::

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
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_transformation(self, value: SextupleCollectionType[IntFloatType]) -> None:
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    offset: dynamicProperty = dynamicProperty(
        "base_offset",
        """
        The image's offset. This is a shortcut to the offset
        values in :attr:`transformation`. This must be an
        iterable containing two :ref:`type-int-float` values
        defining the x and y values to offset the image by. ::

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
        """
        Subclasses may override this method.
        """
        sx, sxy, syx, sy, ox, oy = self.transformation
        return (ox, oy)

    def _set_offset(self, value: PairType[IntFloatType]) -> None:
        """
        Subclasses may override this method.
        """
        sx, sxy, syx, sy, ox, oy = self.transformation
        ox, oy = value
        self.transformation = (sx, sxy, syx, sy, ox, oy)

    scale: dynamicProperty = dynamicProperty(
        "base_scale",
        """
        The image's scale. This is a shortcut to the scale
        values in :attr:`transformation`. This must be an
        iterable containing two :ref:`type-int-float` values
        defining the x and y values to scale the image by. ::

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
        """
        Subclasses may override this method.
        """
        sx, sxy, syx, sy, ox, oy = self.transformation
        return (sx, sy)

    def _set_scale(self, value: PairType[float]) -> None:
        """
        Subclasses may override this method.
        """
        sx, sxy, syx, sy, ox, oy = self.transformation
        sx, sy = value
        self.transformation = (sx, sxy, syx, sy, ox, oy)

    # Color

    color: dynamicProperty = dynamicProperty(
        "base_color",
        """
        The image's color. This will be a
        :ref:`type-color` or ``None``. ::

            >>> image.color
            None
            >>> image.color = (1, 0, 0, 0.5)
        """,
    )

    def _get_base_color(self) -> Optional[Color]:
        value = self._get_color()
        if value is not None:
            value = normalizers.normalizeColor(value)
            value = Color(value)
        return value

    def _set_base_color(
        self, value: Optional[QuadrupleCollectionType[IntFloatType]]
    ) -> None:
        if value is not None:
            value = normalizers.normalizeColor(value)
        self._set_color(value)

    def _get_color(self) -> Optional[QuadrupleCollectionType[IntFloatType]]:
        """
        Return the color value as a color tuple or None.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_color(self, value: Optional[QuadrupleType[float]]) -> None:
        """
        value will be a color tuple or None.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # Data

    data: dynamicProperty = dynamicProperty(
        "data",
        """
        The image's raw byte data. The possible
        formats are defined by each environment.
        """,
    )

    def _get_base_data(self) -> bytes:
        return self._get_data()

    def _set_base_data(self, value: bytes) -> None:
        self._set_data(value)

    def _get_data(self) -> bytes:
        """
        This must return raw byte data.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_data(self, value: bytes) -> None:
        """
        value will be raw byte data.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # --------------
    # Transformation
    # --------------

    def _transformBy(
        self, matrix: SextupleCollectionType[IntFloatType], **kwargs: Any
    ) -> None:
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
