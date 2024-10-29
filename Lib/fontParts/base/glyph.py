# pylint: disable=C0103, C0302, C0114, W0613
from __future__ import annotations
<<<<<<< HEAD
from typing import TYPE_CHECKING, Any, Iterator, Optional, Union, List, Tuple
=======
from typing import TYPE_CHECKING, Any, Iterator, Optional, Union, List, Tuple, TypeVar
>>>>>>> v1
from itertools import zip_longest
from collections import Counter
import os
from copy import deepcopy

from fontMath import MathGlyph
from fontMath.mathFunctions import setRoundIntegerFunction
from fontTools.pens.pointInsidePen import PointInsidePen
from fontTools.pens.areaPen import AreaPen
from fontTools.pens.boundsPen import BoundsPen

from fontParts.base.errors import FontPartsError
from fontParts.base.base import (
    BaseObject,
    TransformationMixin,
    InterpolationMixin,
    SelectionMixin,
    dynamicProperty,
    interpolate,
    FuzzyNumber
)
from fontParts.base import normalizers
from fontParts.base.compatibility import GlyphCompatibilityReporter
from fontParts.base.color import Color
from fontParts.base.deprecated import DeprecatedGlyph, RemovedGlyph
from fontParts.base.annotations import (
    BoundsType,
    CollectionType,
    CoordinateType,
    ColorType,
    FactorType,
    IntFloatType,
    PenType,
    PointPenType,
    TransformationMatrixType,
    ScaleType
)
if TYPE_CHECKING:
    from fontParts.base.font import BaseFont
    from fontParts.base.lib import BaseLib
    from fontParts.base.layer import BaseLayer
    from fontParts.base.guideline import BaseGuideline
    from fontParts.base.contour import BaseContour
    from fontParts.base.component import BaseComponent
    from fontParts.base.anchor import BaseAnchor
    from fontParts.base.image import BaseImage


class BaseGlyph(BaseObject,
                TransformationMixin,
                InterpolationMixin,
                SelectionMixin,
                DeprecatedGlyph,
                RemovedGlyph):
    """Represent the basis for a glyph object.

    This object will almost always be created by retrieving it from a
    font object.

    """

    copyAttributes: Tuple[str, ...] = (
        "name",
        "unicodes",
        "width",
        "height",
        "note",
        "markColor",
        "lib"
    )

    def _reprContents(self) -> List[str]:
        contents: List[str] = [
            "'%s'" % self.name,
        ]
        if self.layer is not None:
            contents.append("('%s')" % self.layer.name)
        return contents

<<<<<<< HEAD
    def copy(self) -> BaseGlyph:
=======
    def copy(self: BaseGlyph) -> BaseGlyph:
>>>>>>> v1
        """Copy data from the current glyph into a new glyph.

        This new glyph object will not belong to a font.

        This will copy:

        - :attr:`name`
        - :attr:`unicodes`
        - :attr:`width`
        - :attr:`height`
        - :attr:`note`
        - :attr:`markColor`
        - :attr:`lib`
        - :attr:`contours`
        - :attr:`components`
        - :attr:`anchors`
        - :attr:`guidelines`
        - :attr:`image`

        :return: A new :class:`BaseGlyph` instance with the same attributes.

        Example::

            >>> copiedGlyph = glyph.copy()

        """
        return super(BaseGlyph, self).copy()

<<<<<<< HEAD
    def copyData(self, source: BaseGlyph) -> None:
        """Copy data from `source` into the current glyph.
=======
    def copyData(self: BaseGlyph, source: BaseGlyph) -> None:
        """Copy data from another glyph instance.
>>>>>>> v1

        Refer to :meth:`BaseGlyph.copy` for a list of values that will
        be copied.

        :param source: The source :class:`BaseGlyph` instance from which
            to copy data.

        Example::

            >>> glyph.copyData(sourceGlyph)

        """
        super(BaseGlyph, self).copyData(source)
        for contour in source.contours:
            self.appendContour(contour)
        for component in source.components:
            self.appendComponent(component=component)
        for anchor in source.anchors:
            self.appendAnchor(anchor=anchor)
        for guideline in source.guidelines:
            self.appendGuideline(guideline=guideline)
        sourceImage = source.image
        if sourceImage.data is not None:
            selfImage = self.addImage(data=sourceImage.data)
            selfImage.transformation = sourceImage.transformation
            selfImage.color = sourceImage.color

    # -------
    # Parents
    # -------

    # Layer

    _layer: Optional[BaseLayer] = None

    layer: dynamicProperty = dynamicProperty(
        "layer",
<<<<<<< HEAD
        """Get the glyph's parent layer object.

        :return: An instance of the :class:`BaseLayer` class.
=======
        """Get or set the glyph's parent layer object.

        The value must be a  :class:`BaseLayer` instance or :obj:`None`.

        :return: The :class:`BaseLayer` instance containing the glyph
            or :obj:`None`.
>>>>>>> v1

        Example::

            >>> layer = glyph.layer

        """
    )

    def _get_layer(self) -> Optional[BaseLayer]:
        if self._layer is None:
            return None
        return self._layer

<<<<<<< HEAD
    def _set_layer(self, layer: BaseLayer) -> None:
=======
    def _set_layer(self, layer: Optional[BaseLayer]) -> None:
>>>>>>> v1
        self._layer = layer

    # Font

    font: dynamicProperty = dynamicProperty(
        "font",
        """Get the glyph's parent font object.

<<<<<<< HEAD
        :return: An instance of the :class:`BaseFont` class.
=======
        This property is read-only.

        :return: The :class:`BaseFont` instance containing the glyph
            or :obj:`None`.
>>>>>>> v1

        Example::

            >>> font = glyph.font

        """
    )

    def _get_font(self) -> Optional[BaseFont]:
        if self._layer is None:
            return None
        return self.layer.font

    # --------------
    # Identification
    # --------------

    # Name

    name: dynamicProperty = dynamicProperty(
        "base_name",
        """Get or set the name of the glyph.

        The value must be a :class:`str`.

        :return: A :class:`str` defining the name of the glyph.
        :raises ValueError: If attempting to set the name to one that
            already exists in the layer.

        Example::

            >>> glyph.name
            "A"
            >>> glyph.name = "A.alt"

        """
    )

<<<<<<< HEAD
    def _get_base_name(self) -> Optional[str]:
=======
    def _get_base_name(self) -> str:
>>>>>>> v1
        value = self._get_name()
        if value is not None:
            value = normalizers.normalizeGlyphName(value)
        return value

<<<<<<< HEAD
    def _set_base_name(self, value: Optional[str]) -> None:
=======
    def _set_base_name(self, value: str) -> None:
>>>>>>> v1
        if value == self.name:
            return
        value = normalizers.normalizeGlyphName(value)
        layer = self.layer
        if layer is not None and value in layer:
            raise ValueError(f"A glyph with the name '{value}' already exists.")
        self._set_name(value)

<<<<<<< HEAD
    def _get_name(self) -> str:
=======
    def _get_name(self) -> str:  # type: ignore[return]
>>>>>>> v1
        """Get the name of the native glyph.

        This is the environment implementation of the :attr:`BaseGlyph.name`
        property getter.

        :return A :class:`str` defining the name of the glyph. The value
<<<<<<< HEAD
            will benormalized with :func:`normalizers.normalizeLayerName`.
=======
            will be normalized with :func:`normalizers.normalizeLayerName`.
>>>>>>> v1

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_name(self, value: str) -> None:
        """Set the name of the native glyph.

        This is the environment implementation of the :attr:`BaseGlyph.name`
        property setter.

<<<<<<< HEAD
        :param value: The name to assign to the glyph as a :class:`str`. The
            value will be normalized with :func:`normalizers.normalizeGlyphName`
            and must be unique to the layer.
=======
        :param value: The name to assign to the glyph as a :class:`str`. The value
             will have been normalized with :func:`normalizers.normalizeGlyphName`
             and must be unique to the layer.
>>>>>>> v1
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # Unicodes

    unicodes: dynamicProperty = dynamicProperty(
        "base_unicodes",
        """Get or set the glyph's Unicode values.

<<<<<<< HEAD
        The value must be a :class:`list` or :class:`tuple` of :class:`int`
        values in order from most to least important.
=======
        The value must be a :class:`list` or :class:`tuple` of :class:`int` or
        hexadecimal :class:`str` values, ordered from most to least important.
>>>>>>> v1

        :return: A :class:`tuple` of :class:`int` values representing the
            glyphs Unicode values in order from most to least important.

        Example::

            >>> glyph.unicodes
            (65,)
            >>> glyph.unicodes = [65, 66]
            >>> glyph.unicodes = []

        """
    )

    def _get_base_unicodes(self) -> Tuple[int, ...]:
        value = self._get_unicodes()
        value = normalizers.normalizeGlyphUnicodes(value)
        return value

    def _set_base_unicodes(self, value: CollectionType[int]) -> None:
        value = tuple(value)
        value = normalizers.normalizeGlyphUnicodes(value)
        self._set_unicodes(value)

<<<<<<< HEAD
    def _get_unicodes(self) -> Tuple[int, ...]:
=======
    def _get_unicodes(self) -> Tuple[int, ...]:  # type: ignore[return]
>>>>>>> v1
        """Get the Unicode values assigned to the glyph.

        This is the environment implementation of
        the :attr:`BaseGlyph.unicodes` property getter.

        :return: A :class:`tuple` of :class:`int` values representing
            the glyphs Unicode values in order from most to least important.
            The value will be normalized
            with :func:`normalizers.normalizeGlyphUnicodes(value)`.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_unicodes(self, value: CollectionType[int]) -> None:
        """Assign Unicode values to the glyph.

        This is the environment implementation of
        the :attr:`BaseGlyph.unicodes` property setter.

        :param value: A :class:`list` or :class:`tuple` of :class:`int`
<<<<<<< HEAD
            values in order from most to least important. The value will be
            normalized with :func:`normalizers.normalizeGlyphUnicodes(value)`.
=======
            values in order from most to least important. The value will have
            been normalized with :func:`normalizers.normalizeGlyphUnicodes(value)`.
>>>>>>> v1
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    unicode: dynamicProperty = dynamicProperty(
        "base_unicode",
        """Get or set the glyph's primary Unicode value.

        This property is equivalent to ``glyph.unicodes[0]`` and will reset
        :attr:`BaseGlyph.unicodes` to a :class:`tuple` containing that value,
        or to an empty :class:`tuple` if value is :obj:`None`.

<<<<<<< HEAD
        The value must be an :class:`int` or :obj:`None`.
=======
        The value must be an :class:`int`, a hexadecimal :class:`str` or :obj:`None`.
>>>>>>> v1

        :return: An :class:`int` representing the glyphs primary Unicode
            value or :obj:`None`.

        Example::

            >>> glyph.unicode
            65
            >>> glyph.unicode = None
            None

        Interaction with the :attr:`BaseGlyph.unicodes` property::

            >>> glyph.unicodes
            (65, 67)
            >>> glyph.unicode = 65
            >>> glyph.unicodes
            (65,)
            >>> glyph.unicode = None
            >>> glyph.unicodes
            ()

        """
    )

    def _get_base_unicode(self) -> Optional[int]:
        value = self._get_unicode()
        if value is not None:
            value = normalizers.normalizeGlyphUnicode(value)
        return value

    def _set_base_unicode(self, value: Optional[int]) -> None:
        if value is not None:
            value = normalizers.normalizeGlyphUnicode(value)
            self._set_unicode(value)
        else:
            self._set_unicodes(())

    def _get_unicode(self) -> Optional[int]:
        """Get the primary Unicode value assigned to the native glyph.

        This is the environment implementation of
        the :attr:`BaseGlyph.unicode` property getter.

        :return: An :class:`int` representing the glyphs primary Unicode
            value or :obj:`None`.

        .. note::

            Subclasses may override this method.

        """
        values = self.unicodes
        if values:
            return values[0]
        return None

    def _set_unicode(self, value: Optional[int]) -> None:
        """Assign the primary Unicode value to the native glyph.

        This is the environment implementation of
        the :attr:`BaseGlyph.unicode` property setter.

        :param value: The primary Unicode value to assign as an :class:`int`
            or :obj:`None`.

        .. note::

            Subclasses may override this method.

        """
        if value is None:
            self.unicodes = []
        else:
            self.unicodes = [value]

    def autoUnicodes(self) -> None:
        """Use heuristics to set the Unicode values in the glyph.

        Environments will define their own heuristics for
        automatically determining values.

        Example::

            >>> glyph.autoUnicodes()

        """
        self._autoUnicodes()

    def _autoUnicodes(self) -> None:
        """Use heuristics to set the Unicode values in the native glyph.

        This is the environment implementation of :meth:`BaseGlyph.autoUnicodes`.

        :return: Description of :obj:`None`.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # -------
    # Metrics
    # -------

    # horizontal

    width: dynamicProperty = dynamicProperty(
        "base_width",
        """Get or set the width of the glyph.

        The value must be an :class:`int` or a :class:`float`.

        :return: An :class:`int` or a :class:`float` representing
            the width of the glyph.

        Example::

            >>> glyph.width
            500
            >>> glyph.width = 200

        """
    )

    def _get_base_width(self) -> IntFloatType:
        value = self._get_width()
        value = normalizers.normalizeGlyphWidth(value)
        return value

    def _set_base_width(self, value: IntFloatType) -> None:
        value = normalizers.normalizeGlyphWidth(value)
        self._set_width(value)

<<<<<<< HEAD
    def _get_width(self) -> IntFloatType:
=======
    def _get_width(self) -> IntFloatType:  # type: ignore[return]
>>>>>>> v1
        """Get the width of the native glyph.

        This is the environment implementation of
        the :attr:`BaseGlyph.width` property getter.

        :return: An :class:`int` or a :class:`float` representing
            the width of the glyph.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.


        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_width(self, value: IntFloatType) -> None:
        """Set the width of the native glyph.

        This is the environment implementation of
        the :attr:`BaseGlyph.width` property setter.

        :param value: The glyph width as an :class:`int` or
            a :class:`float`.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.


        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    leftMargin: dynamicProperty = dynamicProperty(
        "base_leftMargin",
        """Get or set the glyph's left margin.

<<<<<<< HEAD
        The value must be either an :class:`int` or a :class:`float`,
        or :obj:`None` to indicate that the glyph has no outlines.
=======
        The value must be either an :class:`int` or a :class:`float`.
>>>>>>> v1

        :return: The left glyph margin as an :class:`int` or a :class:`float`,
            or :obj:`None` if the glyph has no outlines.

        Example::

            >>> glyph.leftMargin
            35
            >>> glyph.leftMargin = 45

        """
    )

    def _get_base_leftMargin(self) -> Optional[IntFloatType]:
        value = self._get_leftMargin()
        value = normalizers.normalizeGlyphLeftMargin(value)
        return value

<<<<<<< HEAD
    def _set_base_leftMargin(self, value: Optional[IntFloatType]) -> None:
        value = normalizers.normalizeGlyphLeftMargin(value)
        self._set_leftMargin(value)

    def _get_leftMargin(self) -> Optional[float]:
=======
    def _set_base_leftMargin(self, value: IntFloatType) -> None:
        value = normalizers.normalizeGlyphLeftMargin(value)
        self._set_leftMargin(value)

    def _get_leftMargin(self) -> Optional[IntFloatType]:
>>>>>>> v1
        """Get the native glyph's left margin.

        This is the environment implementation of
        the :attr:`BaseGlyph.leftMargin` property getter.

        :return: The left glyph margin as an :class:`int` or a :class:`float`,
            or :obj:`None` if the glyph has no outlines.

        .. note::

            Subclasses may override this method.

        """
        bounds = self.bounds
        if bounds is None:
            return None
        xMin, yMin, xMax, yMax = bounds
        return xMin

    def _set_leftMargin(self, value: IntFloatType) -> None:
        """Set the native glyph's left margin.

        This is the environment implementation of
        the :attr:`BaseGlyph.leftMargin` property setter.

        :param value: The left glyph margin to set as an :class:`int` or
<<<<<<< HEAD
            a :class:`float`, or :obj:`None` to indicate that the glyph has no
            outlines.
=======
            a :class:`float`.
>>>>>>> v1

        .. note::

            Subclasses may override this method.

        """
        diff = value - self.leftMargin
        self.moveBy((diff, 0))
        self.width += diff

    rightMargin: dynamicProperty = dynamicProperty(
        "base_rightMargin",
        """Get or set the glyph's right margin.

<<<<<<< HEAD
        The value must be either an :class:`int` or a :class:`float`,
        or :obj:`None` to indicate that the glyph has no outlines.
=======
        The value must be either an :class:`int` or a :class:`float`.
>>>>>>> v1

        :return: The right glyph margin as an :class:`int` or a :class:`float`,
            or :obj:`None` if the glyph has no outlines.

        Example::

            >>> glyph.rightMargin
            35
            >>> glyph.rightMargin = 45

        """
    )

    def _get_base_rightMargin(self) -> Optional[IntFloatType]:
        value = self._get_rightMargin()
        value = normalizers.normalizeGlyphRightMargin(value)
        return value

<<<<<<< HEAD
    def _set_base_rightMargin(self, value: Optional[IntFloatType]) -> None:
=======
    def _set_base_rightMargin(self, value: IntFloatType) -> None:
>>>>>>> v1
        value = normalizers.normalizeGlyphRightMargin(value)
        self._set_rightMargin(value)

    def _get_rightMargin(self) -> Optional[IntFloatType]:
        """Get the native glyph's right margin.

        This is the environment implementation of
        the :attr:`BaseGlyph.rightMargin` property getter.

        :return: The right glyph margin as an :class:`int` or a :class:`float`,
            or :obj:`None` if the glyph has no outlines.

        .. note::

            Subclasses may override this method.

        """
        bounds = self.bounds
        if bounds is None:
            return None
        xMin, yMin, xMax, yMax = bounds
        return self.width - xMax

    def _set_rightMargin(self, value: IntFloatType) -> None:
        """Set the native glyph's right margin.

        This is the environment implementation of
        the :attr:`BaseGlyph.rightMargin` property setter.

        :param value: The right glyph margin to set as an :class:`int` or
<<<<<<< HEAD
            a :class:`float`, or :obj:`None` to indicate that the glyph has no
            outlines.
=======
            a :class:`float`.
>>>>>>> v1

        .. note::

            Subclasses may override this method.

        """
        bounds = self.bounds
        if bounds is None:
            self.width = value
        else:
            xMin, yMin, xMax, yMax = bounds
            self.width = xMax + value

    # vertical

    height: dynamicProperty = dynamicProperty(
        "base_height",
        """Get or set the glyph's height.

        The value must be :class:`int` or :class:`float`.

        :return: The glyph height as an :class:`int` or a :class:`float`.

        Example::

            >>> glyph.height
            500
            >>> glyph.height = 200

        """
    )

    def _get_base_height(self) -> IntFloatType:
        value = self._get_height()
        value = normalizers.normalizeGlyphHeight(value)
        return value

    def _set_base_height(self, value: IntFloatType) -> None:
        value = normalizers.normalizeGlyphHeight(value)
        self._set_height(value)

<<<<<<< HEAD
    def _get_height(self) -> IntFloatType:
=======
    def _get_height(self) -> IntFloatType:  # type: ignore[return]
>>>>>>> v1
        """Get the native glyph's height.

        This is the environment implementation of
        the :attr:`BaseGlyph.height` property getter.

        :return: The glyph height as an :class:`int` or :class:`float`.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_height(self, value: IntFloatType) -> None:
        """Set the native glyph's height.

        This is the environment implementation of the :attr:`BaseGlyph.height`
        property setter.

        :param value: The glyph height as an :class:`int` or :class:`float`.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    bottomMargin: dynamicProperty = dynamicProperty(
        "base_bottomMargin",
        """Get or set the glyph's bottom margin.

<<<<<<< HEAD
        The value must be either an :class:`int` or a :class:`float`,
        or :obj:`None` to indicate that the glyph has no outlines.
=======
        The value must be either an :class:`int` or a :class:`float`.
>>>>>>> v1

        :return: The bottom glyph margin as an :class:`int` or a :class:`float`,
            or :obj:`None` to indicate that the glyph has no outlines.

        Example::

            >>> glyph.bottomMargin
            35
            >>> glyph.bottomMargin = 45

        """
    )

    def _get_base_bottomMargin(self) -> Optional[IntFloatType]:
        value = self._get_bottomMargin()
        value = normalizers.normalizeGlyphBottomMargin(value)
        return value

<<<<<<< HEAD
    def _set_base_bottomMargin(self, value: Optional[IntFloatType]) -> None:
=======
    def _set_base_bottomMargin(self, value: IntFloatType) -> None:
>>>>>>> v1
        value = normalizers.normalizeGlyphBottomMargin(value)
        self._set_bottomMargin(value)

    def _get_bottomMargin(self) -> Optional[IntFloatType]:
        """Get the native glyph's bottom margin.

        This is the environment implementation of
        the :attr:`BaseGlyph.bottomMargin` property getter.

        :return: The bottom glyph margin as an :class:`int` or a :class:`float`,
            or :obj:`None` to indicate that the glyph has no outlines.

        .. note::

            Subclasses may override this method.

        """
        bounds = self.bounds
        if bounds is None:
            return None
        xMin, yMin, xMax, yMax = bounds
        return yMin

    def _set_bottomMargin(self, value: IntFloatType) -> None:
        """Set the native glyph's bottom margin.

        This is the environment implementation of
        the :attr:`BaseGlyph.bottomMargin` property setter.

        :param value: The bottom glyph margin to set as an :class:`int` or
<<<<<<< HEAD
            a :class:`float`, or :obj:`None` to indicate that the glyph has no
            outlines.
=======
            a :class:`float`.
>>>>>>> v1

        .. note::

            Subclasses may override this method.

        """
        diff = value - self.bottomMargin
        self.moveBy((0, diff))
        self.height += diff

    topMargin: dynamicProperty = dynamicProperty(
        "base_topMargin",
        """Get or set the glyph's top margin.

<<<<<<< HEAD
        The value must be either an :class:`int` or a :class:`float`,
        or :obj:`None` to indicate that the glyph has no outlines.
=======
        The value must be either an :class:`int` or a :class:`float`.
>>>>>>> v1

        :return: The top glyph margin as an :class:`int` or a :class:`float`,
            or :obj:`None` to indicate that the glyph has no outlines.

        Example::

            >>> glyph.topMargin
            35
            >>> glyph.topMargin = 45
        """
    )

    def _get_base_topMargin(self) -> Optional[IntFloatType]:
        value = self._get_topMargin()
        value = normalizers.normalizeGlyphTopMargin(value)
        return value

<<<<<<< HEAD
    def _set_base_topMargin(self, value: Optional[IntFloatType]) -> None:
=======
    def _set_base_topMargin(self, value: IntFloatType) -> None:
>>>>>>> v1
        value = normalizers.normalizeGlyphTopMargin(value)
        self._set_topMargin(value)

    def _get_topMargin(self) -> Optional[IntFloatType]:
        """Get the native glyph's top margin.

        This is the environment implementation of
        the :attr:`BaseGlyph.topMargin` property getter.

        :return: The top glyph margin as an :class:`int` or a :class:`float`,
            or :obj:`None` to indicate that the glyph has no outlines.

        .. note::

            Subclasses may override this method.

        """
        bounds = self.bounds
        if bounds is None:
            return None
        xMin, yMin, xMax, yMax = bounds
        return self.height - yMax

    def _set_topMargin(self, value: IntFloatType) -> None:
        """Set the native glyph's top margin.

        This is the environment implementation of
        the :attr:`BaseGlyph.topMargin` property setter.

        :param value: The top glyph margin to set as an :class:`int` or
<<<<<<< HEAD
            a :class:`float`, or :obj:`None` to indicate that the glyph has no
            outlines.
=======
            a :class:`float`.
>>>>>>> v1

        .. note::

            Subclasses may override this method.

        """
        bounds = self.bounds
        if bounds is None:
            self.height = value
        else:
            xMin, yMin, xMax, yMax = bounds
            self.height = yMax + value

    # ----
    # Pens
    # ----

    def getPen(self) -> PenType:
        """Return a pen object for adding outline data  to the glyph.

        :return: An instance of an :class:`~fontTools.pens.basePen.AbstractPen`
            subclass.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        Example::

            >>> pen = glyph.getPen()

        """
        self.raiseNotImplementedError()

    def getPointPen(self) -> PointPenType:
        """Return a point pen object for adding outline data to the glyph.

        :return: An instance of
            an :class:`~fontTools.pens.pointPen.AbstractPointPen` subclass.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        Example::

            >>> pointPen = glyph.getPointPen()

        """
        self.raiseNotImplementedError()

    def draw(self,
             pen: PenType,
             contours: bool = True,
             components: bool = True) -> None:
        """Draw the glyph's outline data to the given pen object.

        :param pen: The :class:`~fontTools.pens.basePen.AbstractPen` subclass
            instance to which the data should be drawn.
        :param contours: Whether to draw data from the glyph's contours.
            Defaults to :obj:`True`
        :param components: Whether to draw data from the glyph's contours.
            Defaults to :obj:`True`

        Example::

            >>> glyph.draw(pen)
            >>> glyph.draw(pen, contours=False)
            >>> glyph.draw(pen, components=False)

        """
        if contours:
            for contour in self:
                contour.draw(pen)
        if components:
            for component in self.components:
                component.draw(pen)

    def drawPoints(self,
                   pen: PointPenType,
                   contours: bool = True,
                   components: bool = True) -> None:
        """Draw the glyph's outline data to the given point pen object.

        :param pen: The :class:`~fontTools.pens.pointPen.AbstractPointPen`
            subclass instance to which the data should be drawn.
        :param contours: Whether to draw data from the glyph's contours.
            Defaults to :obj:`True`
        :param components: Whether to draw data from the glyph's contours.
            Defaults to :obj:`True`.

        Example::

            >>> glyph.drawPoints(pointPen)
            >>> glyph.drawPoints(pointPen, contours=False)
            >>> glyph.drawPoints(pointPen, components=False)

        """
        if contours:
            for contour in self:
                contour.drawPoints(pen)
        if components:
            for component in self.components:
                component.drawPoints(pen)

    # -----------------------------------------
    # Contour, Component and Anchor Interaction
    # -----------------------------------------

    def clear(self,
              contours: bool = True,
              components: bool = True,
              anchors: bool = True,
              guidelines: bool = True,
              image: bool = True) -> None:
        """Clear the glyph data.

        This will clear:

        - :attr:`contours`
        - :attr:`components`
        - :attr:`anchors`
        - :attr:`guidelines`
        - :attr:`image`

<<<<<<< HEAD
=======
        The clearing of portions of the glyph may be turned off with the listed
        parameters.

>>>>>>> v1
        :param contours: Whether to clear the glyph's contour data.
            Defaults to :obj:`True`
        :param components: Whether to clear the glyph's component data.
            Defaults to :obj:`True`
        :param anchors: Whether to clear the glyph's anchor data.
            Defaults to :obj:`True`
        :param guidelines: Whether to clear the glyph's guideline data.
            Defaults to :obj:`True`
        :param image: Whether to clear the glyph's image data.
            Defaults to :obj:`True`

        Example::

            >>> glyph.clear()
            >>> glyph.clear(guidelines=False)

        """
        self._clear(contours=contours, components=components,
                    anchors=anchors, guidelines=guidelines, image=image)

    def _clear(self,
<<<<<<< HEAD
               contours: bool = True,
               components: bool = True,
               anchors: bool = True,
               guidelines: bool = True,
               image: bool = True) -> None:
=======
               contours: bool,
               components: bool,
               anchors: bool,
               guidelines: bool,
               image: bool) -> None:
>>>>>>> v1
        """Clear the native glyph data.

        This is the environment implementation of :meth:`BaseGlyph.clear`.

        :param contours: Whether to clear the glyph's contour data.
<<<<<<< HEAD
            Defaults to :obj:`True`
        :param components: Whether to clear the glyph's component data.
            Defaults to :obj:`True`
        :param anchors: Whether to clear the glyph's anchor data.
            Defaults to :obj:`True`
        :param guidelines: Whether to clear the glyph's guideline data.
            Defaults to :obj:`True`
        :param image: Whether to clear the glyph's image data.
            Defaults to :obj:`True`
=======
        :param components: Whether to clear the glyph's component data.
        :param anchors: Whether to clear the glyph's anchor data.
        :param guidelines: Whether to clear the glyph's guideline data.
        :param image: Whether to clear the glyph's image data.
>>>>>>> v1

        .. note::

            Subclasses may override this method.

        """
        if contours:
            self.clearContours()
        if components:
            self.clearComponents()
        if anchors:
            self.clearAnchors()
        if guidelines:
            self.clearGuidelines()
        if image:
            self.clearImage()

    def appendGlyph(self,
                    other: BaseGlyph,
                    offset: Optional[CoordinateType] = None) -> None:
        """Append data from `other` to new objects in the glyph.

        This will append:

        - :attr:`contours`
        - :attr:`components`
        - :attr:`anchors`
        - :attr:`guidelines`
<<<<<<< HEAD

        :param other: The :class:`BaseGlyph` instace containing the source
            data to append.
        :param offset: The x and y shift values to be applied to the
            appended data as a :ref:`type-coordinate`, or :obj:`None`
            representing an offset of ``(0, 0)``.

        Example::

=======

        :param other: The :class:`BaseGlyph` instace containing the source
            data to append.
        :param offset: The x and y shift values to be applied to the
            appended data as a :ref:`type-coordinate`, or :obj:`None`
            representing an offset of ``(0, 0)``.

        Example::

>>>>>>> v1
            >>> glyph.appendGlyph(otherGlyph)
            >>> glyph.appendGlyph(otherGlyph, (100, 0))

        """
        if offset is None:
            offset = (0, 0)
        normalizedOffset = normalizers.normalizeTransformationOffset(offset)
        self._appendGlyph(other, normalizedOffset)

    def _appendGlyph(self,
                     other: BaseGlyph,
                     offset: CoordinateType) -> None:
        """Append data from `other` to new objects in the native glyph.

        This is the environment implementation of :meth:`BaseGlyph.appendGlyph`.

        :param other: The :class:`BaseGlyph` instace containing the source
            data to append.
        :param offset: The x and y shift values to be applied to the
            appended data as a :ref:`type-coordinate`.

        .. note::

            Subclasses may override this method.

<<<<<<< HEAD
    def _appendGlyph(self,
                     other: BaseGlyph,
                     offset: CoordinateType = None) -> None:
        """Append data from `other` to new objects in the native glyph.

        This is the environment implementation of :meth:`BaseGlyph.appendGlyph`.

        :param other: The :class:`BaseGlyph` instace containing the source
            data to append.
        :param offset: The x and y shift values to be applied to the
            appended data as a :ref:`type-coordinate`,
            or :obj:`None` representing an offset of ``(0, 0)``.

        .. note::

            Subclasses may override this method.

=======
>>>>>>> v1
        """
        other = other.copy()
        if offset != (0, 0):
            other.moveBy(offset)
        for contour in other.contours:
            self.appendContour(contour)
        for component in other.components:
            self.appendComponent(component=component)
        for anchor in other.anchors:
            self.appendAnchor(anchor=anchor)
        for guideline in other.guidelines:
            self.appendGuideline(guideline=guideline)

    def _setGlyphInContour(self, contour: BaseContour) -> None:
        if contour.glyph is None:
            contour.glyph = self

    contours: dynamicProperty = dynamicProperty(
        "contours",
        """Get all contours in the glyph.

<<<<<<< HEAD
=======
        This property is read-only.

>>>>>>> v1
        :return: A :class:`tuple` of :class:`BaseContour` objects.

        Example::

            >>> contours = glyph.contours

        """
    )

    def _get_contours(self) -> Tuple[BaseContour, ...]:
        """Get all contours in the native glyph.

        This is the environment implementation of the :attr:`BaseGlyph.contours`
        property getter.

        :return: A :class:`tuple` of :class:`BaseContour` subclass instances.

        .. note::

            Subclasses may override this method.
<<<<<<< HEAD

        """
        return tuple([self[i] for i in range(len(self))])

=======

        """
        return tuple(self[i] for i in range(len(self)))

>>>>>>> v1
    def __len__(self) -> int:
        """Get the number of contours in the glyph.

        :return: An :class:`int` representing the number of contours in the
            glyph.

        Example::

            >>> len(glyph)
            2

        """
        return self._lenContours()

<<<<<<< HEAD
    def _lenContours(self, **kwargs: Any) -> int:
=======
    def _lenContours(self, **kwargs: Any) -> int:  # type: ignore[return]
>>>>>>> v1
        r"""Get the number of contours in the native glyph.

        This is the environment implementation of :meth:`BaseGlyph.__len__`.

        :param \**kwargs: Additional keyword arguments.
        :return: An :class:`int` representing the number of contours in the
            glyph.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def __iter__(self) -> Iterator[BaseContour]:
        """Iterate through all contours in the glyph.

        :return: An iterator of :class:`BaseContour` instances.

        Example::

            >>> for contour in glyph:
            ...     contour.reverse()

        """
        return self._iterContours()

    def _iterContours(self, **kwargs: Any) -> Iterator[BaseContour]:
        r"""Iterate through all contours in the native glyph.

        This is the environment implementation of :meth:`BaseGlyph.__iter__`.

        :param \**kwargs: Additional keyword arguments.
        :return: An iterator of :class:`BaseContour` subclass instances.

        .. note::

            Subclasses may override this method.

        """
        count = len(self)
        index = 0
        while count:
            yield self[index]
            count -= 1
            index += 1

    def __getitem__(self, index: int) -> BaseContour:
        """Get the contour located at the given index from the glyph.

        :param index: The index of the glyph to return as an :class:`int`.
        :return: An instance of the :class:`BaseContour` class.

        Example::

            >>> contour = glyph[0]

        """
        index = normalizers.normalizeIndex(index)
        if index >= len(self):
            raise ValueError(f"No contour located at index {index}.")
        contour = self._getContour(index)
        self._setGlyphInContour(contour)
        return contour

<<<<<<< HEAD
    def _getContour(self, index: int, **kwargs: Any) -> BaseContour:
=======
    def _getContour(self, index: int, **kwargs: Any) -> BaseContour:  # type: ignore[return]
>>>>>>> v1
        r"""Get the contour located at the given index from the native glyph.

        :param index: The index of the contour to return as an :class:`int`.
        :param \**kwargs: Additional keyword arguments.
        :return: An instance of a :class:`BaseContour` subclass.

        Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _getContourIndex(self, contour: BaseContour) -> int:
        for i, other in enumerate(self.contours):
            if contour == other:
                return i
        raise FontPartsError("The contour could not be found.")

    def appendContour(self,
                      contour: BaseContour,
<<<<<<< HEAD
                      offset: CoordinateType = None) -> BaseContour:
=======
                      offset: Optional[CoordinateType] = None) -> BaseContour:
>>>>>>> v1
        """Append the given contour's data to the glyph.

        :param contour: The :class:`BaseContour` instace containing the source
            data to append.
        :param offset: The x and y shift values to be applied to the
            appended data as a :ref:`type-coordinate`,
            or :obj:`None` representing an offset of ``(0, 0)``.
        :return: A :class:`BaseContour` instance containing the appended data.

        Example::

            >>> contour = glyph.appendContour(contour)
            >>> contour = glyph.appendContour(contour, (100, 0))

        """
        normalizedContour = normalizers.normalizeContour(contour)
        if offset is None:
            offset = (0, 0)
        normalizedOffset = normalizers.normalizeTransformationOffset(offset)
        return self._appendContour(normalizedContour, normalizedOffset)

    def _appendContour(self,
                       contour: BaseContour,
<<<<<<< HEAD
                       offset: CoordinateType = None,
=======
                       offset: CoordinateType,
>>>>>>> v1
                       **kwargs: Any) -> BaseContour:
        r"""Append the given contour's data to the native glyph.

        This is the environment implementation of :meth:`BaseGlyph.appendContour`.

        :param contour: The :class:`BaseContour` instace containing the source
            data to append.
<<<<<<< HEAD
        :param offset: The x and y shift values to be applied to the
            appended data as a :ref:`type-coordinate`,
            or :obj:`None` representing an offset of ``(0, 0)``.
=======
        :param offset: The x and y shift values to be applied to the appended
            data as a :ref:`type-coordinate`.
>>>>>>> v1
        :param \**kwargs: Additional keyword arguments.
        :return: A :class:`BaseContour` instance containing the appended data.

        .. note::

            Subclasses may override this method.

        """
        pointPen = self.getPointPen()
        if offset != (0, 0):
            copy = contour.copy()
            copy.moveBy(offset)
            copy.drawPoints(pointPen)
        else:
            contour.drawPoints(pointPen)
        return self[-1]

    def removeContour(self, contour: Union[BaseContour, int]) -> None:
        """Remove the given contour from the glyph.

        :param contour: The contour to remove as a :class:`BaseContour`
            instance or an :class:`int` representing a contour index.
        :raises ValueError: If no contour can be found at the given `index`.

        Example::

            >>> glyph.removeContour(contour)

        """
        if isinstance(contour, int):
            index = contour
        else:
            index = self._getContourIndex(contour)
        index = normalizers.normalizeIndex(index)
        if index >= len(self):
            raise ValueError(f"No contour located at index {index}.")
        self._removeContour(index)

    def _removeContour(self, index: int, **kwargs: Any) -> None:
        r"""Remove the given contour from the native glyph.

        This is the environment implementation
        of :meth:`BaseGlyph.removeContour`.

        :param contour: The contour to remove as a :class:`BaseContour`
            instance or an :class:`int` representing a contour index.
        :param \**kwargs: Additional keyword arguments.

        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def clearContours(self) -> None:
        """Clear all contours in the glyph.

        Example::

            >>> glyph.clearContours()

        """
        self._clearContours()

    def _clearContours(self) -> None:
        """Clear all contours in the native glyph.

        This is the environment implementation
        of :meth:`BaseGlyph.clearContours`.

        .. note::

            Subclasses may override this method.

        """
        for _ in range(len(self)):
            self.removeContour(-1)

    def removeOverlap(self) -> None:
        """Perform a remove overlap operation on the glyph's contours.

        The behavior of this may vary across environments.

        Example::

            >>> glyph.removeOverlap()

        """
        self._removeOverlap()

    def _removeOverlap(self) -> None:
        """Perform a remove overlap operation on the native glyph's contours.

        This is the environment implementation
        of :meth:`BaseGlyph.removeOverlap`.

        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must implement this method.

        """
        self.raiseNotImplementedError()

    # Components

    def _setGlyphInComponent(self, component: BaseComponent) -> None:
        if component.glyph is None:
            component.glyph = self

    components: dynamicProperty = dynamicProperty(
        "components",
        """Get all components in the glyph.

<<<<<<< HEAD
=======
        This property is read-only.

>>>>>>> v1
        :return: A :class:`tuple` of :class:`BaseComponent` instances.

        Example::

            >>> components = glyph.components

        """
    )

    def _get_components(self) -> Tuple[BaseComponent, ...]:
        """Get all components in the native glyph.

        This is the environment implementation of
        the :attr:`BaseGlyph.components` property getter.

        :return: A :class:`tuple` of :class:`BaseComponent` subclass instances.

        .. note::

            Subclasses may override this method.

        """
        return tuple(self._getitem__components(i) for
                      i in range(self._len__components()))

    def _len__components(self) -> int:
        return self._lenComponents()

<<<<<<< HEAD
    def _lenComponents(self, **kwargs: Any) -> int:
        r"""Get the number of components in the ntive glyph.
=======
    def _lenComponents(self, **kwargs: Any) -> int:  # type: ignore[return]
        r"""Get the number of components in the glyph.
>>>>>>> v1

        :param \**kwargs: Additional keyword arguments.
        :return: An :class:`int` indicating the number of components in the
            glyph.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _getitem__components(self, index: int) -> BaseComponent:
        index = normalizers.normalizeIndex(index)
        if index >= self._len__components():
            raise ValueError(f"No component located at index {index}.")
        component = self._getComponent(index)
        self._setGlyphInComponent(component)
        return component

<<<<<<< HEAD
    def _getComponent(self, index: int, **kwargs: Any) -> BaseComponent:
=======
    def _getComponent(self, index: int, **kwargs: Any) -> BaseComponent:  # type: ignore[return]
>>>>>>> v1
        r"""Get the component at the given index from the native glyph.

        :param index: The index of the component to return as an :class:`int`.
        :param \**kwargs: Additional keyword arguments.
        :return: An instance of a :class:`BaseComponent` subclass.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _getComponentIndex(self, component: BaseComponent) -> int:
        for i, other in enumerate(self.components):
            if component == other:
                return i
        raise FontPartsError("The component could not be found.")

    def appendComponent(self,
                        baseGlyph: Optional[str] = None,
                        offset: Optional[CoordinateType] = None,
                        scale: Optional[ScaleType] = None,
                        component: Optional[BaseComponent] = None
                        ) -> BaseComponent:
        """Append a component to the glyph.

        If `baseGlyph`, `offset` or `scale` is specified, those values will be
        used instead of the values in the given `component`.

        :param baseGlyph: An optional glyph name to append as a component.
            Defaults to :obj:`None`.
        :param offset: The x and y shift values to be applied to the
            appended data as a :ref:`type-coordinate`,
            or :obj:`None` representing an offset of ``(0, 0)``.
            Defaults to :obj:`None`
        :param scale: The x and y scale values that should be applied to
            the appended component as a :class:`tuple` of :class:`int`
            or :class:`float` values, or :obj:`None` representing a scale of
            ``(1.0, 1.0)``. Defaults to :obj:`None`
        :param component: An optional :class:`BaseComponent` instance from which
            to copy attribute values. Defaults to :obj:`None`.
        :return: The newly appended :class:`BaseComponent` instance.
        :raises FontPartsError: If the `baseGlyph` refers to the current glyph
            instance, which would result in a component referencing itself. This
            is not permitted.

        Example::

            >>> component = glyph.appendComponent("A")
            >>> component = glyph.appendComponent("A", offset=(10, 20))
            >>> component = glyph.appendComponent("A", scale=(1.0, 2.0))

        """
        identifier = None
        sxy = 0
        syx = 0
        if component is not None:
            normalizedComponent = normalizers.normalizeComponent(component)
            if baseGlyph is None:
                baseGlyph = normalizedComponent.baseGlyph
            sx, sxy, syx, sy, ox, oy = normalizedComponent.transformation
            if offset is None:
                offset = (ox, oy)
            if scale is None:
                scale = (sx, sy)
            if baseGlyph is None:
                baseGlyph = normalizedComponent.baseGlyph
            if normalizedComponent.identifier is not None:
                existing = set([c.identifier for c in self.components
                                if c.identifier is not None])
                if normalizedComponent.identifier not in existing:
                    identifier = normalizedComponent.identifier
<<<<<<< HEAD
        baseGlyph = normalizers.normalizeGlyphName(baseGlyph)
        if self.name == baseGlyph:
=======
        normalizedBaseGlyph = normalizers.normalizeGlyphName(baseGlyph)
        if self.name == normalizedBaseGlyph:
>>>>>>> v1
            raise FontPartsError(
                "A glyph cannot contain a component referencing itself."
            )
        if offset is None:
            offset = (0, 0)
        if scale is None:
            scale = (1, 1)
        normalizedOffset = normalizers.normalizeTransformationOffset(offset)
        normalizedScale = normalizers.normalizeTransformationScale(scale)
        ox, oy = normalizedOffset
        sx, sy = normalizedScale
        transformation = (sx, sxy, syx, sy, ox, oy)
<<<<<<< HEAD
        identifier = normalizers.normalizeIdentifier(identifier)
        return self._appendComponent(
            baseGlyph, transformation=transformation, identifier=identifier
=======
        normalizedIdentifier = normalizers.normalizeIdentifier(identifier)
        return self._appendComponent(
            normalizedBaseGlyph,
            transformation=transformation,
            identifier=normalizedIdentifier
>>>>>>> v1
        )

    def _appendComponent(self,
                         baseGlyph: str,
<<<<<<< HEAD
                         transformation: Optional[TransformationMatrixType] = None,
                         identifier: str = None,
=======
                         transformation: Optional[TransformationMatrixType],
                         identifier: Optional[str],
>>>>>>> v1
                         **kwargs: Any) -> BaseComponent:
        r"""Append a component to the native glyph.

        This is the environment implementation of :meth:`BaseGlyph.appendComponent`.

<<<<<<< HEAD
        :param baseGlyph: An optional glyph name to append as a component.
        :param transformation: The :ref:`type-transformation` values to be applied
            to the appended data. Defaults to :obj:`None`
        :param identifier: A valid, nonconflicting :ref:`type-identifier` as
            a :clss:`str`. Defaults to :obj:`None`
=======
        :param baseGlyph: The glyph name to append as a component.
        :param transformation: The :ref:`type-transformation` values to be applied
            to the appended data or :obj:`None`.
        :param identifier: A valid, nonconflicting :ref:`type-identifier` as
            a :clss:`str` or :obj:`None`.
>>>>>>> v1
        :param \**kwargs: Additional keyword arguments.
        :return: The newly appended :class:`BaseComponent` subclass instance.

        .. note::

            Subclasses may override this method.

        """
        pointPen = self.getPointPen()
        pointPen.addComponent(
            baseGlyph, transformation=transformation, identifier=identifier
        )
        return self.components[-1]

    def removeComponent(self, component: Union[BaseComponent, int]) -> None:
        """Remove the specified component from the glyph.

        :param component: The component to remove as a :class:`BaseComponent`
            instance or an :class:`int` representing the component's index.

        :raises ValueError: If no component can be found at the given `index`.

        Example::

            >>> glyph.removeComponent(component)

        """
        if isinstance(component, int):
            index = component
        else:
            index = self._getComponentIndex(component)
        index = normalizers.normalizeIndex(index)
        if index >= self._len__components():
            raise ValueError(f"No component located at index {index}.")
        self._removeComponent(index)

    def _removeComponent(self, index: int, **kwargs: Any) -> None:
        r"""Remove the specified component from the native glyph.

        This is the environment implementation of :meth:`BaseGlyph.removeComponent`.

        :param index: The index of the component to remove as an :class:`int`.
        :param \**kwargs: Additional keyword arguments.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def clearComponents(self) -> None:
        """Clear all components in the glyph.

        Example::

            >>> glyph.clearComponents()

        """
        self._clearComponents()

    def _clearComponents(self) -> None:
        """Clear all components in the native glyph.

        This is the environment implementation
        of :meth:`BaseGlyph.clearComponents`.

        .. note::

            Subclasses may override this method.

        """
        for _ in range(self._len__components()):
            self.removeComponent(-1)

    def decompose(self) -> None:
        """Decompose all components in the glyph to contours.

        Example::

            >>> glyph.decompose()

        """
        self._decompose()

    def _decompose(self) -> None:
        """Decompose all components in the native glyph to contours.

        .. note::

            Subclasses may override this method.

        """
        for component in self.components:
            component.decompose()

    # Anchors

    def _setGlyphInAnchor(self, anchor: BaseAnchor) -> None:
        if anchor.glyph is None:
            anchor.glyph = self

    anchors: dynamicProperty = dynamicProperty(
        "anchors",
        """Get all anchors in the glyph.

<<<<<<< HEAD
=======
        This property is read-only.

>>>>>>> v1
        :return: A :class:`tuple` of :class:`BaseAnthor` instances.

        Example::

            >>> anchors = glyph.anchors

        """
    )

    def _get_anchors(self) -> Tuple[BaseAnchor, ...]:
        """Get all anchors in the native glyph.

        :return: A :class:`tuple` of :class:`BaseAnthor` subclass instances.

        .. note::

            Subclasses may override this method.

        """
<<<<<<< HEAD
        return tuple([self._getitem__anchors(i) for
                      i in range(self._len__anchors())])
=======
        return tuple(self._getitem__anchors(i) for
                      i in range(self._len__anchors()))
>>>>>>> v1

    def _len__anchors(self) -> int:
        return self._lenAnchors()

<<<<<<< HEAD
    def _lenAnchors(self, **kwargs: Any) -> int:
=======
    def _lenAnchors(self, **kwargs: Any) -> int:  # type: ignore[return]
>>>>>>> v1
        r"""Get the number of anchors in the ntive glyph.

        :param \**kwargs: Additional keyword arguments.
        :return: An :class:`int` indicating the number of anchors in the glyph.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _getitem__anchors(self, index: int) -> BaseAnchor:
        index = normalizers.normalizeIndex(index)
        if index >= self._len__anchors():
            raise ValueError(f"No anchor located at index {index}.")
        anchor = self._getAnchor(index)
        self._setGlyphInAnchor(anchor)
        return anchor

<<<<<<< HEAD
    def _getAnchor(self, index: int, **kwargs: Any) -> BaseAnchor:
=======
    def _getAnchor(self, index: int, **kwargs: Any) -> BaseAnchor:  # type: ignore[return]
>>>>>>> v1
        r"""Get the anchor at the given index from the native glyph.

        :param index: The index of the anchor to get as an :class:`int`.
        :param \**kwargs: Additional keyword arguments.
        :return: An instance of a :class:`BaseAnchor` subclass.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _getAnchorIndex(self, anchor: BaseAnchor) -> int:
        for i, other in enumerate(self.anchors):
            if anchor == other:
                return i
        raise FontPartsError("The anchor could not be found.")

    def appendAnchor(self,
                     name: Optional[str] = None,
                     position: Optional[CoordinateType] = None,
                     color: Optional[ColorType] = None,
                     anchor: Optional[BaseAnchor] = None) -> BaseAnchor:
        """Append an anchor to the glyph.

        If `name`, `position` or `color` are specified, those values will be
        used instead of the values in the given anchor object.
<<<<<<< HEAD

        :param name: An optional name to be assigned to the anchor as
            a :class:`str`. Defaults to :obj:`None`.
        :param position: The optional x and y location to be applied to the
         anchor as a :ref:`type-coordinate`. Defaults to :obj:`None`.
        :param color: The optional color to be applied to the anchor as
            a :ref:`type-color`. Defaults to :obj:`None`.
        :param anchor: An optional :class:`BaseAnchor` instance from which
            attribute values will be copied. Defualts to :obj:`None`.
        :return: The newly appended :class:`BaseAnchor` instance.

        Example::

=======

        :param name: An optional name to be assigned to the anchor as
            a :class:`str`. Defaults to :obj:`None`.
        :param position: The optional x and y location to be applied to the
         anchor as a :ref:`type-coordinate`. Defaults to :obj:`None`.
        :param color: The optional color to be applied to the anchor as
            a :ref:`type-color`. Defaults to :obj:`None`.
        :param anchor: An optional :class:`BaseAnchor` instance from which
            attribute values will be copied. Defualts to :obj:`None`.
        :return: The newly appended :class:`BaseAnchor` instance.

        Example::

>>>>>>> v1
            >>> anchor = glyph.appendAnchor("top", (10, 20))
            >>> anchor = glyph.appendAnchor("top", (10, 20), color=(1, 0, 0, 1))

        """
        identifier = None
        if anchor is not None:
            normalizedAnchor = normalizers.normalizeAnchor(anchor)
            if name is None:
                name = normalizedAnchor.name
            if position is None:
                position = normalizedAnchor.position
            if color is None:
                color = normalizedAnchor.color
            if normalizedAnchor.identifier is not None:
<<<<<<< HEAD
                existing = set([a.identifier for a in self.anchors
                                if a.identifier is not None])
                if normalizedAnchor.identifier not in existing:
                    identifier = normalizedAnchor.identifier
        name = normalizers.normalizeAnchorName(name)
        position = normalizers.normalizeCoordinateTuple(position)
        if color is not None:
            color = normalizers.normalizeColor(color)
        identifier = normalizers.normalizeIdentifier(identifier)
        return self._appendAnchor(
            name, position=position, color=color, identifier=identifier
        )

    def _appendAnchor(self,
                      name: str,
                      position: Optional[CoordinateType] = None,
                      color: Optional[ColorType] = None,
                      identifier: Optional[str] = None,
                      **kwargs: Any) -> BaseAnchor:
        r"""Append an anchor to the native glyph.

        This is the environment implementation of :meth:`BaseGlyph.appendAnchor`.

        :param name: The name to be assigned to the anchor as a :class:`str`.
            Defaults to :obj:`None`.
        :param position: The x and y location to be applied to the anchor as
            a :ref:`type-coordinate`. Defaults to :obj:`None`.
        :param color: The color to be applied to the anchor as
         a :ref:`type-color`. Defaults to :obj:`None`.
        :param identifier: A valid, nonconflicting :ref:`type-identifier` as
            a :clss:`str`. Defaults to :obj:`None`
        :param \**kwargs: Additional keyword arguments.
        :return: The newly appended :class:`BaseAnchor` subclass instance.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. note::

=======
                existing = {
                    a.identifier for a in self.anchors if a.identifier is not None
                }
                if normalizedAnchor.identifier not in existing:
                    identifier = normalizedAnchor.identifier
        normalizedName = normalizers.normalizeAnchorName(name)
        normalizedPosition = normalizers.normalizeCoordinateTuple(position)
        if color is not None:
            normalizedColor = normalizers.normalizeColor(color)
        normalizedIdentifier = normalizers.normalizeIdentifier(identifier)
        return self._appendAnchor(
            normalizedName,
            position=normalizedPosition,
            color=normalizedColor,
            identifier=normalizedIdentifier
        )

    def _appendAnchor(self,  # type: ignore[return]
                      name: str,
                      position: Optional[CoordinateType],
                      color: Optional[ColorType],
                      identifier: Optional[str],
                      **kwargs: Any) -> BaseAnchor:
        r"""Append an anchor to the native glyph.

        This is the environment implementation of :meth:`BaseGlyph.appendAnchor`.

        :param name: The name to be assigned to the anchor as a :class:`str`
            or :obj:`None`.
        :param position: The x and y location to be applied to the anchor as
            a :ref:`type-coordinate` or :obj:`None`.
        :param color: The color to be applied to the anchor as
         a :ref:`type-color` or :obj:`None`.
        :param identifier: A valid, nonconflicting :ref:`type-identifier` as
            a :clss:`str` or :obj:`None`.
        :param \**kwargs: Additional keyword arguments.
        :return: The newly appended :class:`BaseAnchor` subclass instance.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. note::

>>>>>>> v1
            Subclasses may override this method.

        """
        self.raiseNotImplementedError()

    def removeAnchor(self, anchor: Union[BaseAnchor, int]) -> None:
        """Remove the given anchor from the glyph.

        :param anchor: The anchor to remove as a :class:`BaseAnchor` intance,
            or an :class:`int` representing the anchor's index.

        :raises ValueError: If no anchor can be found at the given `index`.

        Example::

            >>> glyph.removeAnchor(anchor)

        """
        if isinstance(anchor, int):
            index = anchor
        else:
            index = self._getAnchorIndex(anchor)
        index = normalizers.normalizeIndex(index)
        if index >= self._len__anchors():
            raise ValueError(f"No anchor located at index {index}.")
        self._removeAnchor(index)

    def _removeAnchor(self, index: int, **kwargs: Any) -> None:
        r"""Remove the given anchor from the glyph.

        This is the environment implementation of :meth:`BaseGlyph.removeAnchor`.

        :param index: The index of the anchor to remove as an :class:`int`.
        :param \**kwargs: Additional keyword arguments.

        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def clearAnchors(self) -> None:
        """Clear all anchors in the glyph.

        Example::

            >>> glyph.clearAnchors()

        """
        self._clearAnchors()

    def _clearAnchors(self) -> None:
        """Clear all anchors in the native glyph.

        This is the environment implementation of :meth:`BaseGlyph.clearAnchors`.

        .. note::

            Subclasses may override this method.

        """
        for _ in range(self._len__anchors()):
            self.removeAnchor(-1)

    # ----------
    # Guidelines
    # ----------

    def _setGlyphInGuideline(self, guideline: BaseGuideline) -> None:
        if guideline.glyph is None:
            guideline.glyph = self

    guidelines: dynamicProperty = dynamicProperty(
        "guidelines",
        """Get all guidelines in the glyph.

<<<<<<< HEAD
=======
        This property is read-only.

>>>>>>> v1
        :return: A :class:`tuple` of :class:`BaseGuideline` instances.

        Example::

            >>> guidelines = glyph.guidelines

<<<<<<< HEAD
        The list will contain  objects.

=======
>>>>>>> v1
        """
    )

    def _get_guidelines(self) -> Tuple[BaseGuideline, ...]:
        """Get all guidelines in the glyph.

        This is the environment implementation of
        the :attr:`BaseGlyph.guidelines` property getter.

        :return: A :class:`tuple` of :class:`BaseGuideline` subclass instances.

        .. note::

            Subclasses may override this method.

        """
<<<<<<< HEAD
        return tuple([self._getitem__guidelines(i)
                      for i in range(self._len__guidelines())])
=======
        return tuple(self._getitem__guidelines(i)
                      for i in range(self._len__guidelines()))
>>>>>>> v1

    def _len__guidelines(self) -> int:
        return self._lenGuidelines()

<<<<<<< HEAD
    def _lenGuidelines(self, **kwargs: Any) -> int:
=======
    def _lenGuidelines(self, **kwargs: Any) -> int:  # type: ignore[return]
>>>>>>> v1
        r"""Get the number of guidelines in the ntive glyph.

        :param \**kwargs: Additional keyword arguments.
        :return: An :class:`int` indicating the number of guidelines in the
            glyph.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _getitem__guidelines(self, index: int) -> BaseGuideline:
        index = normalizers.normalizeIndex(index)
        if index >= self._len__guidelines():
            raise ValueError("No guideline located at index %d." % index)
        guideline = self._getGuideline(index)
        self._setGlyphInGuideline(guideline)
        return guideline

<<<<<<< HEAD
    def _getGuideline(self, index: int, **kwargs: Any) -> BaseGuideline:
=======
    def _getGuideline(self, index: int, **kwargs: Any) -> BaseGuideline:  # type: ignore[return]
>>>>>>> v1
        r"""Get the anchor at the given index from the native glyph.

        :param index: The index of the guideline to get as an :class:`int`.
        :param \**kwargs: Additional keyword arguments.
        :return: An instance of a :class:`BaseGuideline` subclass.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _getGuidelineIndex(self, guideline: BaseGuideline) -> int:
        for i, other in enumerate(self.guidelines):
            if guideline == other:
                return i
        raise FontPartsError("The guideline could not be found.")

    def appendGuideline(self,
                        position: Optional[CoordinateType] = None,
                        angle: Optional[IntFloatType] = None,
                        name: Optional[str] = None,
                        color: Optional[ColorType] = None,
                        guideline: Optional[BaseGuideline] = None
                        ) -> BaseGuideline:
        """Append a guideline to the glyph.

        If `name`, `position` or `color` are specified, those values will be
        used instead of the values in the given guideline object.

        :param position: The optional x and y location to be applied to the
            guideline as a :ref:`type-coordinate`. Defaults to :obj:`None`.
        :param angle: The optional angle to be applied to the guideline
            as :class:`int` or :class:`float`. Defaults to :obj:`None`.
        :param name: An optional name to be assigned to the guideline as
            a :class:`str`. Defaults to :obj:`None`.
        :param color: The optional color to be applied to the guideline as
            a :ref:`type-color`. Defaults to :obj:`None`.
        :param guideline: An optional :class:`BaseGuideline` instance from which
            attribute values will be copied. Defualts to :obj:`None`.
        :return: The newly appended :class:`BaseGuideline` instance.

        Example::

            >>> anchor = glyph.appendGuideline("top", (10, 20))
            >>> anchor = glyph.appendGuideline("top", (10, 20), color=(1, 0, 0, 1))

        """
        identifier: Optional[str] = None
        if guideline is not None:
            normalizedGuideline = normalizers.normalizeGuideline(guideline)
            if position is None:
                position = normalizedGuideline.position
            if angle is None:
                angle = normalizedGuideline.angle
            if name is None:
                name = normalizedGuideline.name
            if color is None:
                color = normalizedGuideline.color
            if normalizedGuideline.identifier is not None:
                existing = set([g.identifier for g in self.guidelines
                                if g.identifier is not None])
                if normalizedGuideline.identifier not in existing:
                    identifier = normalizedGuideline.identifier
<<<<<<< HEAD
        position = normalizers.normalizeCoordinateTuple(position)
        angle = normalizers.normalizeRotationAngle(angle)
=======
        normalizedPosition = normalizers.normalizeCoordinateTuple(position)
        normalizedAngle = normalizers.normalizeRotationAngle(angle)
>>>>>>> v1
        if name is not None:
            normalizedName = normalizers.normalizeGuidelineName(name)
        if color is not None:
<<<<<<< HEAD
            color = normalizers.normalizeColor(color)
        identifier = normalizers.normalizeIdentifier(identifier)
        newGuideline = self._appendGuideline(
            position, angle, name=name, color=color, identifier=identifier
=======
            normalizedColor = normalizers.normalizeColor(color)
        normalizedIdentifier = normalizers.normalizeIdentifier(identifier)
        newGuideline = self._appendGuideline(
            normalizedPosition,
            normalizedAngle,
            name=normalizedName,
            color=normalizedColor,
            identifier=normalizedIdentifier
>>>>>>> v1
        )
        newGuideline.glyph = self
        return newGuideline

<<<<<<< HEAD
    def _appendGuideline(self,
                         position: CoordinateType,
                         angle: IntFloatType,
                         name: Optional[str] = None,
                         color: Optional[ColorType] = None,
                         identifier: Optional[str] = None,
=======
    def _appendGuideline(self,  # type: ignore[return]
                         position: CoordinateType,
                         angle: IntFloatType,
                         name: Optional[str],
                         color: Optional[ColorType],
                         identifier: Optional[str],
>>>>>>> v1
                         **kwargs: Any) -> BaseGuideline:
        r"""Append a guideline to the native glyph.

        This is the environment implementation of :meth:`BaseGlyph.appendGuideline`.

<<<<<<< HEAD
        :param position: The optional x and y location to be applied to the
            guideline as a :ref:`type-coordinate`.
        :param angle: The optional angle to be applied to the guideline
            as :class:`int` or :class:`float`.
        :param name: An optional name to be assigned to the guideline as
            a :class:`str`. Defaults to :obj:`None`.
        :param color: The optional color to be applied to the guideline as
            a :ref:`type-color`. Defaults to :obj:`None`.
        :param identifier: An optioanal valid,
            nonconflicting :ref:`type-identifier` as a :clss:`str`. Defaults
            to :obj:`None`.
=======
        :param position: The x and y location to be applied to the
            guideline as a :ref:`type-coordinate`.
        :param angle: The angle to be applied to the guideline
            as :class:`int` or :class:`float`.
        :param name: The name to be assigned to the guideline as a :class:`str`
            or :obj:`None`.
        :param color: The color to be applied to the guideline as
            a :ref:`type-color` or :obj:`None`.
        :param identifier: An optioanal valid, nonconflicting :ref:`type-identifier`
            as a :clss:`str` or :obj:`None`.
>>>>>>> v1
        :param \**kwargs: Additional keyword arguments.
        :return: The newly appended :class:`BaseGuideline` subclass instance.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. note::

            Subclasses may override this method.

        """
        self.raiseNotImplementedError()

    def removeGuideline(self, guideline: Union[BaseGuideline, int]) -> None:
        """Remove the given guideline from the glyph.

        :param guideline: The guideline to remove as a :class:`BaseGuideline`
            intance, or an :class:`int` representing the guideline's index.

        :raises ValueError: If no guideline can be found at the given `index`.

        Example::

            >>> glyph.removeGuideline(guideline)

        """
        if isinstance(guideline, int):
            index = guideline
        else:
            index = self._getGuidelineIndex(guideline)
        index = normalizers.normalizeIndex(index)
        if index >= self._len__guidelines():
            raise ValueError("No guideline located at index %d." % index)
        self._removeGuideline(index)

    def _removeGuideline(self, index: int, **kwargs: Any) -> None:
        r"""Remove the given guideline from the glyph.

        This is the environment implementation of :meth:`BaseGlyph.removeGuideline`.

        :param index: The index of the guideline to remove as an :class:`int`.
        :param \**kwargs: Additional keyword arguments.

        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def clearGuidelines(self) -> None:
        """Clear all guidelines in the glyph.

        Example::

            >>> glyph.clearGuidelines()

        """
        self._clearGuidelines()

    def _clearGuidelines(self) -> None:
        """Clear all guidelines in the native glyph.

        This is the environment implementation of :meth:`BaseGlyph.clearGuidelines`.

        .. note::

            Subclasses may override this method.

        """
        for _ in range(self._len__guidelines()):
            self.removeGuideline(-1)

    # ------------------
    # Data Normalization
    # ------------------

    def round(self) -> None:
        """Round coordinates in the glyph to the nearest integer.

        This applies to:
<<<<<<< HEAD

        - :attr:`width`
        - :attr:`height`
        - :attr:`contours`
        - :attr:`components`
        - :attr:`anchors`
        - :attr:`guidelines`

=======

        - :attr:`width`
        - :attr:`height`
        - :attr:`contours`
        - :attr:`components`
        - :attr:`anchors`
        - :attr:`guidelines`

>>>>>>> v1
        Example::

            >>> glyph.round()

        """
        self._round()

    def _round(self) -> None:
        """Round coordinates in the native glyph to the nearest integer.

        This is the environment implementation of :meth:`BaseGlyph.round`.

        .. note::

            Subclasses may override this method.

        """
        for contour in self.contours:
            contour.round()
        for component in self.components:
            component.round()
        for anchor in self.anchors:
            anchor.round()
        for guideline in self.guidelines:
            guideline.round()
        self.width = normalizers.normalizeVisualRounding(self.width)
        self.height = normalizers.normalizeVisualRounding(self.height)

    def correctDirection(self, trueType: bool = False) -> None:
        """Correct the winding direction of the glyph's contours.

        By default this method follows the PostScript winding
        recommendations.

        :param trueType: Whether to follow TrueType rather than PostScript
            winding recommendations. Defaults to :obj:`False`.

        Example::

            >>> glyph.correctDirection()

        """
        self._correctDirection(trueType=trueType)

    def _correctDirection(self,
                          trueType: bool,
                          **kwargs: Any) -> None:
        r"""Correct the winding direction of the native glyph's contours.

        This is the environment implementation
        of :meth:`BaseGlyph.correctDirection`.

        :param trueType: Whether to follow TrueType rather than PostScript
            winding recommendations.
        :param \**kwargs: Additional keyword arguments.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. note::

            Subclasses may override this method.

        """
        self.raiseNotImplementedError()

    def autoContourOrder(self) -> None:
        """Automatically order the glyph's contours based on heuristics.

        The results of this may vary across environments.

        Example::

            >>> glyph.autoContourOrder()

        """
        self._autoContourOrder()

    def _autoContourOrder(self, **kwargs: Any) -> None:
        r"""Automatically order the native glyph's contours based on heuristics.

        This is the environment implementation of :meth:`BaseGlyph.autoContourOrder`.

        Sorting is based on (in this order):

        - the (negative) point count
        - the (negative) segment count
        - x value of the center of the contour rounded to a threshold
        - y value of the center of the contour rounded to a threshold
          (such threshold is calculated as the smallest contour width
          or height in the glyph divided by two)
        - the (negative) surface of the bounding box of the contour: ``width * height``

<<<<<<< HEAD
        :param \**kwargs: Additional keyword arguments.

        """
        Center = Union[float, 'FuzzyNumber']  # float is used for temporary list
        SortKeys = Tuple[int, int, Center, Center, int]
        ContourListType = List[Tuple[SortKeys, 'BaseContour']]

        tempContourList: ContourListType = []
        contourList: ContourListType = []
        xThreshold: Optional[float] = None
        yThreshold: Optional[float] = None
=======
        The latter is a safety net for for instances like a very thin 'O' where the
        x centers could be close enough to rely on the y for the sort, which could
        very well be the same for both contours. We use the *negative* of the surface
        to ensure that larger contours appear first, which seems more natural.

        :param \**kwargs: Additional keyword arguments.

        """
        TempContourListType = List[
            Tuple[int, int, IntFloatType, IntFloatType, IntFloatType, BaseContour]
        ]
        ContourListType = List[
            Tuple[int, int, FuzzyNumber, FuzzyNumber, IntFloatType, BaseContour]
        ]
        tempContourList: TempContourListType = []
        contourList: ContourListType = []
        xThreshold: Optional[IntFloatType] = None
        yThreshold: Optional[IntFloatType] = None
>>>>>>> v1

        for contour in self:
            bounds = contour.bounds
            if bounds is None:
                continue
            xMin, yMin, xMax, yMax = bounds
            width = xMax - xMin
            height = yMax - yMin
            xC = 0.5 * (xMin + xMax)
            yC = 0.5 * (yMin + yMax)
            xTh = abs(width * 0.5)
            yTh = abs(height * 0.5)
            if xThreshold is None or xThreshold > xTh:
                xThreshold = xTh
            if yThreshold is None or yThreshold > yTh:
                yThreshold = yTh
            tempContourList.append((
                -len(contour.points),
                -len(contour.segments),
                xC,
                yC,
                -(width * height),
                contour
            ))
<<<<<<< HEAD
=======

        xThreshold = xThreshold or 0.0
        yThreshold = yThreshold or 0.0
>>>>>>> v1

        for points, segments, x, y, surface, contour in tempContourList:
            contourList.append((
                points,
                segments,
                FuzzyNumber(x, xThreshold),
                FuzzyNumber(y, yThreshold),
                surface,
                contour
            ))
        contourList.sort()

        self.clearContours()
        for points, segments, xO, yO, surface, contour in contourList:
            self.appendContour(contour)

    # --------------
    # Transformation
    # --------------

    def _transformBy(self,
                     matrix: TransformationMatrixType,
                     **kwargs: Any) -> None:
        r"""Transform the glyph according to the given matrix.

<<<<<<< HEAD
        :param matrix: The :ref:`type-matrix` apply.
=======
        :param matrix: The :ref:`type-transformation` to apply.
>>>>>>> v1
        :param \**kwargs: Additional keyword arguments.

        .. note::

            Subclasses may override this method.

        """
        for contour in self.contours:
            contour.transformBy(matrix)
        for component in self.components:
            component.transformBy(matrix)
        for anchor in self.anchors:
            anchor.transformBy(matrix)
        for guideline in self.guidelines:
            guideline.transformBy(matrix)

    def scaleBy(self,
                value: ScaleType,
<<<<<<< HEAD
                origin: CoordinateType = None,
=======
                origin: Optional[CoordinateType] = None,
>>>>>>> v1
                width: bool = False,
                height: bool = False) -> None:
        """Scale the glyph according to the given values.

        :param value: The x and y values to scale the glyph by as
<<<<<<< HEAD
            a :class:`tuple` of :class:`int` or :class:`float` values.
=======
            a :class:`tuple` of two :class:`int` or :class:`float` values.
>>>>>>> v1
        :param origin: The optional point at which the scale should originate as
            a :ref:`type-coordinate`. This must not be set when scaling the width
            or height. Defaults to :obj:`None`, representing an origin of ``(0, 0)``.
        :param width: Whether the glyph's width should be scaled.
            Defaults to :obj:`False`.
        :param height: Whether the glyph's height should be scaled.
            Defaults to :obj:`False`.
        :raises FontPartsError: If the `origin` is specified while `width` or
            `height` are set to :obj:`True`.

        Example::

            >>> glyph.scaleBy(2.0)
            >>> glyph.scaleBy((0.5, 2.0), origin=(500, 500))

        """
        normalizedValue = normalizers.normalizeTransformationScale(value)
        if origin is None:
            origin = (0, 0)
        normalizedOrigin = normalizers.normalizeCoordinateTuple(origin)
        if normalizedOrigin != (0, 0) and (width or height):
            raise FontPartsError(("The origin must not be set when "
                                  "scaling the width or height."))
        super(BaseGlyph, self).scaleBy(normalizedValue, origin=normalizedOrigin)
        sX, sY = normalizedValue
        if width:
            self._scaleWidthBy(sX)
        if height:
            self._scaleHeightBy(sY)

    def _scaleWidthBy(self, value: IntFloatType) -> None:
        """Scale the glyph's width according to the given value.

        :param value: The value to scale the glyph width by as an :class:`int`
            or :class:`float`.

        .. note::

            Subclasses may override this method.

        """
        self.width *= value

    def _scaleHeightBy(self, value: IntFloatType) -> None:
        """Scale the glyph's height according to the given value.

        :param value: The value to scale the glyph height by as an :class:`int`
            or :class:`float`.

        .. note::

            Subclasses may override this method.

        """
        self.height *= value

    # --------------------
    # Interpolation & Math
    # --------------------

    def toMathGlyph(self,
                    scaleComponentTransform: bool = True,
                    strict: bool = False) -> MathGlyph:
        """Return the glyph as a `fontMath <https://github.com/typesupply/fontMath>`_ :class:`MathGlyph` object.

        This method returns the glyph as an object following the `MathGlyph
        protocol <https://github.com/typesupply/fontMath>`_.

        :param scaleComponentTransform: Whether to enable
            the :attr:`fontMath.MathGlyph.scaleComponentTransform` option.
        :param strict: Whether to enable the :attr:`fontMath.MathGlyph.strict`
            option.
        :return: A :class:`fontMath.MathGlyph` object representing the current
            glyph.

        Example::

            >>> mg = glyph.toMathGlyph()

        """
        return self._toMathGlyph(
            scaleComponentTransform=scaleComponentTransform, strict=strict
        )

    def _toMathGlyph(self,
<<<<<<< HEAD
                     scaleComponentTransform: bool = True,
                     strict: bool = False) -> MathGlyph:
=======
                     scaleComponentTransform: bool,
                     strict: bool) -> MathGlyph:
>>>>>>> v1
        """Return the native glyph as a MathGlyph object.

        This is the environment implementation of :meth:`BaseGlyph.toMathGlyph`.

        :param scaleComponentTransform: Whether to enable
            the :attr:`fontMath.MathGlyph.scaleComponentTransform` option.
<<<<<<< HEAD
            Defaults to :obj:`True`.
        :param strict: Whether to enable the :attr:`fontMath.MathGlyph.strict`
            option. Defaults to :obj:`False`.
=======
        :param strict: Whether to enable the :attr:`fontMath.MathGlyph.strict`
            option.
>>>>>>> v1
        :return: A :class:`fontMath.MathGlyph` object representing the current
            native glyph.

        .. note::

            Subclasses may override this method.

        """
        mathGlyph = MathGlyph(
            None,
            scaleComponentTransform=scaleComponentTransform,
            strict=strict
        )
        pen = mathGlyph.getPointPen()
        self.drawPoints(pen)
        for anchor in self.anchors:
            d = dict(
                x=anchor.x,
                y=anchor.y,
                name=anchor.name,
                identifier=anchor.identifier,
                color=anchor.color
            )
            mathGlyph.anchors.append(d)
        for guideline in self.guidelines:
            d = dict(
                x=guideline.x,
                y=guideline.y,
                angle=guideline.angle,
                name=guideline.name,
                identifier=guideline.identifier,
                color=guideline.color
            )
            mathGlyph.guidelines.append(d)
        mathGlyph.lib = deepcopy(self.lib)
        mathGlyph.name = self.name
        mathGlyph.unicodes = self.unicodes
        mathGlyph.width = self.width
        mathGlyph.height = self.height
        mathGlyph.note = self.note
        return mathGlyph

    def fromMathGlyph(self,
                      mathGlyph: MathGlyph,
                      filterRedundantPoints: bool = True) -> BaseGlyph:
        """Replace the glyph's data with the specified mathGlyph.

        This method returns the glyph as an object following the `MathGlyph
        protocol <https://github.com/typesupply/fontMath>`_.
<<<<<<< HEAD

        :param mathGlyph: The :class:`fontMath.MathGlyph` object containing the
            replacement data.
        :param filterRedundantPoints: Whether to enable the
            `filterRedundantPoints` option of the
            :meth:`fontMath.MathGlyph.dreawPoints` method. Defaults
            to :obj:`True`.

=======

        :param mathGlyph: The :class:`fontMath.MathGlyph` object containing the
            replacement data.
        :param filterRedundantPoints: Whether to enable the
            `filterRedundantPoints` option of the
            :meth:`fontMath.MathGlyph.drawPoints` method. Defaults
            to :obj:`True`.

>>>>>>> v1
        :return: The newly updated :class:`BaseGlyph` instance.

        Example::

            >>> glyph.fromMathGlyph(mg)

        """
        return self._fromMathGlyph(
            mathGlyph,
            toThisGlyph=True,
            filterRedundantPoints=filterRedundantPoints
        )
<<<<<<< HEAD

    def _fromMathGlyph(self,
                       mathGlyph: MathGlyph,
                       toThisGlyph: bool = False,
                       filterRedundantPoints: bool = True) -> BaseGlyph:
        """Replace native glyph data with the specified mathGlyph's data.

        This is the environment implementation of :meth:`BaseGlyph.fromMathGlyph`.

        :param mathGlyph: The object containing the replacement data. This must
            be an object following the `MathGlyph protocol
            <https://github.com/typesupply/fontMath>`_.
        :param toThisGlyph: Whether to apply `mathGlyph` to the current glyph
            instance or to a new glyph copy. Defaults to :obj:`False`.
        :param filterRedundantPoints: Whether to enable the
            `filterRedundantPoints` option of the specified `mathGlyph`
            object's :meth:`dreawPoints` method.

        :return: :return: The newly updated :class:`BaseGlyph` instance.
=======

    def _fromMathGlyph(self,
                       mathGlyph: MathGlyph,
                       toThisGlyph: bool,
                       filterRedundantPoints: bool) -> BaseGlyph:
        """Replace native glyph data with the specified mathGlyph's data.

        This is the environment implementation of :meth:`BaseGlyph.fromMathGlyph`.

        :param mathGlyph: The object containing the replacement data. This must
            be an object following the `MathGlyph protocol
            <https://github.com/typesupply/fontMath>`_.
        :param toThisGlyph: Whether to apply `mathGlyph` to the current glyph
            instance or to a new glyph copy.
        :param filterRedundantPoints: Whether to enable the
            `filterRedundantPoints` option of the specified `mathGlyph`
            object's :meth:`dreawPoints` method.

        :return: The newly updated :class:`BaseGlyph` instance.
>>>>>>> v1

        """
        # make the destination
        if toThisGlyph:
            copied = self
            copied.clear()
        else:
            copyClass = self.copyClass
            if copyClass is None:
                copyClass = self.__class__
            copied = copyClass()
        # populate
        pen = copied.getPointPen()
        mathGlyph.drawPoints(
            pen, filterRedundantPoints=filterRedundantPoints
        )
        for anchor in mathGlyph.anchors:
            a = copied.appendAnchor(
                name=anchor.get("name"),
                position=(anchor["x"], anchor["y"]),
                color=anchor["color"]
            )
            identifier = anchor.get("identifier")
            if identifier is not None:
                a._setIdentifier(identifier)
        for guideline in mathGlyph.guidelines:
            g = copied.appendGuideline(
                position=(guideline["x"], guideline["y"]),
                angle=guideline["angle"],
                name=guideline["name"],
                color=guideline["color"]
            )
            identifier = guideline.get("identifier")
            if identifier is not None:
                g._setIdentifier(identifier)
        copied.lib.update(mathGlyph.lib)
        copied.name = mathGlyph.name
        copied.unicodes = mathGlyph.unicodes
        copied.width = mathGlyph.width
        copied.height = mathGlyph.height
        copied.note = mathGlyph.note
        return copied

    def __mul__(self, factor: FactorType) -> BaseGlyph:
        """Multiply the current glyph by a given factor.

        :param factor: The factor by which to multiply the glyph as a
            single :class:`int` or :class:`float` or a :class:`tuple` of
            two :class:`int` or :class:`float` values representing the
            factors ``(x, y)``.
        :return: The newly multiplied :class:`BaseGlyph` instance.

        .. note::

            Subclasses may override this method.

        """
        mathGlyph = self._toMathGlyph(scaleComponentTransform=True, strict=False)
        result = mathGlyph * factor
        copied = self._fromMathGlyph(result,
            toThisGlyph=False,
            filterRedundantPoints=True)
        return copied

    __rmul__ = __mul__

    def __truediv__(self, factor: FactorType) -> BaseGlyph:
        """Divide the current glyph by a given factor.

        :param factor: The factor by which to divide the glyph as a
            single :class:`int` or :class:`float` or a :class:`tuple` of
            two :class:`int` or :class:`float` values representing the
            factors ``(x, y)``.
        :return: The newly divided :class:`BaseGlyph` instance.

        .. note::

            Subclasses may override this method.

        """
        mathGlyph = self._toMathGlyph(scaleComponentTransform=True, strict=False)
        result = mathGlyph / factor
        copied = self._fromMathGlyph(result,
            toThisGlyph=False,
        filterRedundantPoints=True)
        return copied

    # py2 support
    __div__ = __truediv__

    def __add__(self, other: BaseGlyph) -> BaseGlyph:
        """Add another glyph to the current glyph.

        :param other: The :class:`BaseGLyph` instance to add to the current glyph.
        :return: A new :class:`BaseGlyph` instance representing the added results.

        .. note::

            Subclasses may override this method.

        """
        selfMathGlyph = self._toMathGlyph(scaleComponentTransform=True, strict=False)
        otherMathGlyph = other._toMathGlyph(scaleComponentTransform=True, strict=False)
        result = selfMathGlyph + otherMathGlyph
        copied = self._fromMathGlyph(result,
            toThisGlyph=False,
        filterRedundantPoints=True)
        return copied

    def __sub__(self, other: BaseGlyph) -> BaseGlyph:
        """Subtract another glyph from the current glyph.
<<<<<<< HEAD

        :param other: The :class:`BaseGLyph` instance to subtract
            from the current glyph.
        :return: A new :class:`BaseGlyph` instance representing
            the subtracted results.

        .. note::

            Subclasses may override this method.

        """

        selfMathGlyph = self._toMathGlyph()
        otherMathGlyph = other._toMathGlyph()
        result = selfMathGlyph - otherMathGlyph
        copied = self._fromMathGlyph(result)
        return copied

    def interpolate(self,
                    factor: FactorType,
                    minGlyph: BaseGlyph,
                    maxGlyph: BaseGlyph,
                    round: bool = True,
                    suppressError: bool = True) -> None:
        """Interpolate all possible data in the glyph.

        :param factor: The interpolation value as a single :class:`int`
            or :class:`float` or a :class:`tuple` of two :class:`int`
            or :class:`float` values representing the factors ``(x, y)``.
        :param minGlyph: The :class:`BaseGlyph` instance corresponding to the
            0.0 position in the interpolation.
        :param maxGlyph: The :class:`BaseGlyph` instance corresponding to the
            1.0 position in the interpolation.
        :param round: A :class:`bool` indicating whether the result should
            be rounded to integers. Defaults to :obj:`True`.
        :param suppressError: A :class:`bool` indicating whether to ignore
            incompatible data or raise an error when such
            incompatibilities are found. Defaults to :obj:`True`.
        :raises TypeError: If `minGlyph` or `maxGlyph` are not instances
            of :class:`BaseGlyph`.

        Example::

            >>> glyph.interpolate(0.5, otherGlyph1, otherGlyph2)
            >>> glyph.interpolate((0.5, 2.0), otherGlyph1, otherGlyph2, round=False)

=======

        :param other: The :class:`BaseGLyph` instance to subtract
            from the current glyph.
        :return: A new :class:`BaseGlyph` instance representing
            the subtracted results.

        .. note::

            Subclasses may override this method.

        """

        selfMathGlyph = self._toMathGlyph(scaleComponentTransform=True, strict=False)
        otherMathGlyph = other._toMathGlyph(scaleComponentTransform=True, strict=False)
        result = selfMathGlyph - otherMathGlyph
        copied = self._fromMathGlyph(result,
            toThisGlyph=False,
        filterRedundantPoints=True)
        return copied

    def interpolate(self,
                    factor: FactorType,
                    minGlyph: BaseGlyph,
                    maxGlyph: BaseGlyph,
                    round: bool = True,
                    suppressError: bool = True) -> None:
        """Interpolate all possible data in the glyph.

        :param factor: The interpolation value as a single :class:`int`
            or :class:`float` or a :class:`tuple` of two :class:`int`
            or :class:`float` values representing the factors ``(x, y)``.
        :param minGlyph: The :class:`BaseGlyph` instance corresponding to the
            0.0 position in the interpolation.
        :param maxGlyph: The :class:`BaseGlyph` instance corresponding to the
            1.0 position in the interpolation.
        :param round: A :class:`bool` indicating whether the result should
            be rounded to integers. Defaults to :obj:`True`.
        :param suppressError: A :class:`bool` indicating whether to ignore
            incompatible data or raise an error when such
            incompatibilities are found. Defaults to :obj:`True`.
        :raises TypeError: If `minGlyph` or `maxGlyph` are not instances
            of :class:`BaseGlyph`.

        Example::

            >>> glyph.interpolate(0.5, otherGlyph1, otherGlyph2)
            >>> glyph.interpolate((0.5, 2.0), otherGlyph1, otherGlyph2, round=False)

>>>>>>> v1
        """
        normalizedFactor = normalizers.normalizeInterpolationFactor(factor)
        if not isinstance(minGlyph, BaseGlyph):
            raise TypeError(("Interpolation to an instance of %r can not be "
                             "performed from an instance of %r.")
                            % (self.__class__.__name__,
                               minGlyph.__class__.__name__))
        if not isinstance(maxGlyph, BaseGlyph):
            raise TypeError(("Interpolation to an instance of %r can not be "
                             "performed from an instance of %r.")
                            % (self.__class__.__name__,
                               maxGlyph.__class__.__name__))
        round = normalizers.normalizeBoolean(round)
        suppressError = normalizers.normalizeBoolean(suppressError)
        self._interpolate(normalizedFactor, minGlyph, maxGlyph,
                          round=round, suppressError=suppressError)

    def _interpolate(self,
<<<<<<< HEAD
                     factor: FactorType,
                     minGlyph: BaseGlyph,
                     maxGlyph: BaseGlyph,
                     round: bool = True,
                     suppressError: bool = True) -> None:
=======
                     factor: Tuple[IntFloatType, IntFloatType],
                     minGlyph: BaseGlyph,
                     maxGlyph: BaseGlyph,
                     round: bool,
                     suppressError: bool) -> None:
>>>>>>> v1
        """Interpolate all possible data in the native glyph.

        This is the environment implementation of :meth:`BaseGlyph.interpolate`.

        :param factor: The interpolation value as a single :class:`int`
            or :class:`float` or a :class:`tuple` of two :class:`int`
            or :class:`float` values representing the factors ``(x, y)``.
        :param minLayer: The :class:`BaseLayer` subclass instance
            corresponding to the 0.0 position in the interpolation.
        :param maxLayer: The :class:`BaseLayer` subclass instance
            corresponding to the 1.0 position in the interpolation.
        :param round: A :class:`bool` indicating whether the result should
<<<<<<< HEAD
            be rounded to integers. Defaults to :obj:`True`.
        :param suppressError: A :class:`bool` indicating whether to ignore
            incompatible data or raise an error when such
            incompatibilities are found. Defaults to :obj:`True`.
        :raises FontPartsError: If ``suppressError=False`` and the interpolation
            data is incompatible.

        .. note::

=======
            be rounded to integers.
        :param suppressError: A :class:`bool` indicating whether to ignore
            incompatible data or raise an error when such
            incompatibilities are found.
        :raises FontPartsError: If ``suppressError=False`` and the interpolation
            data is incompatible.

        .. note::

>>>>>>> v1
            Subclasses may override this method.

        """
        setRoundIntegerFunction(normalizers.normalizeVisualRounding)

        minMathGlyph = minGlyph._toMathGlyph(scaleComponentTransform=True, strict=False)
        maxMathGlyph = maxGlyph._toMathGlyph(scaleComponentTransform=True, strict=False)
        try:
            result: MathGlyph = interpolate(minMathGlyph, maxMathGlyph, factor)
        except IndexError:
            result = None
        if result is None and not suppressError:
            raise FontPartsError(("Glyphs '%s' and '%s' could not be "
                                  "interpolated.")
                                 % (minGlyph.name, maxGlyph.name))
        if result is not None:
            if round:
                result = result.round()
            self._fromMathGlyph(result, toThisGlyph=True, filterRedundantPoints=True)

    compatibilityReporterClass = GlyphCompatibilityReporter

    @staticmethod
    def _checkPairs(object1: Any,
                    object2: Any,
                    reporter: Any,
                    reporterObject: List[Any]) -> None:
        compatibility = object1.isCompatible(object2)[1]
        if compatibility.fatal or compatibility.warning:
            if compatibility.fatal:
                reporter.fatal = True
            if compatibility.warning:
                reporter.warning = True
            reporterObject.append(compatibility)

    def isCompatible(self, other: BaseGlyph) -> Tuple[bool, str]:
        """Evaluate interpolation compatibility with another glyph.

        :param other: The other :class:`BaseGlyph` instance to check
            compatibility with.
        :return: A :class:`tuple` where the first element is a :class:`bool`
            indicating compatibility, and the second element is a :class:`str`
            of compatibility notes.

        """
        return super(BaseGlyph, self).isCompatible(other, BaseGlyph)

    def _isCompatible(self,
                      other: BaseGlyph,
                      reporter: GlyphCompatibilityReporter) -> None:
        """Evaluate interpolation compatibility with another native glyph.

        This is the environment implementation of :meth:`BaseGlyph.isCompatible`.

        :param other: The other :class:`BaseGlyph` instance to check
            compatibility with.
        :param reporter: An object used to report compatibility issues.

        .. note::

            Subclasses may override this method.


        """
        GuidelineListType = List[Tuple[Optional[str], int]]
        DiffType = List[Tuple[int, Optional[str], Optional[str]]]

        glyph1 = self
        glyph2 = other
        # contour count
        if len(self.contours) != len(glyph2.contours):
            reporter.fatal = True
            reporter.contourCountDifference = True
        # contour pairs
        for i in range(min(len(glyph1), len(glyph2))):
            contour1 = glyph1[i]
            contour2 = glyph2[i]
            self._checkPairs(contour1, contour2, reporter, reporter.contours)
        # component count
        if len(glyph1.components) != len(glyph2.components):
            reporter.fatal = True
            reporter.componentCountDifference = True
        # component check
        component_diff: DiffType = []
        selfComponents = [component.baseGlyph
        for component in glyph1.components]
        otherComponents = [component.baseGlyph
        for component in glyph2.components]
        for index, (left, right) in enumerate(
            zip_longest(selfComponents, otherComponents)
        ):
            if left != right:
                component_diff.append((index, left, right))

        if component_diff:
            reporter.warning = True
            reporter.componentDifferences = component_diff
            if (not reporter.componentCountDifference
                and set(selfComponents) == set(otherComponents)):
                reporter.componentOrderDifference = True

            selfComponents_counted_set = Counter(selfComponents)
            otherComponents_counted_set = Counter(otherComponents)
            missing_from_glyph1 = (
                otherComponents_counted_set - selfComponents_counted_set
            )
            if missing_from_glyph1:
                reporter.fatal = True
                reporter.componentsMissingFromGlyph1 = sorted(
                    missing_from_glyph1.elements()
                )
            missing_from_glyph2 = (
                selfComponents_counted_set - otherComponents_counted_set
            )
            if missing_from_glyph2:
                reporter.fatal = True
                reporter.componentsMissingFromGlyph2 = sorted(
                    missing_from_glyph2.elements()
                )
        # guideline count
        if len(self.guidelines) != len(glyph2.guidelines):
            reporter.warning = True
            reporter.guidelineCountDifference = True
        # guideline check
        selfGuidelines: GuidelineListType = []
        otherGuidelines: GuidelineListType = []
        for source, names in ((self, selfGuidelines),
                              (other, otherGuidelines)):
            for i, guideline in enumerate(source.guidelines):
                names.append((guideline.name, i))
        guidelines1 = set(selfGuidelines)
        guidelines2 = set(otherGuidelines)
        if len(guidelines1.difference(guidelines2)) != 0:
            reporter.warning = True
            reporter.guidelinesMissingFromGlyph2 = list(
                guidelines1.difference(guidelines2))
        if len(guidelines2.difference(guidelines1)) != 0:
            reporter.warning = True
            reporter.guidelinesMissingFromGlyph1 = list(
                guidelines2.difference(guidelines1))
        # anchor count
        if len(self.anchors) != len(glyph2.anchors):
            reporter.warning = True
            reporter.anchorCountDifference = True
        # anchor check
        anchor_diff: DiffType = []
        selfAnchors = [anchor.name for anchor in glyph1.anchors]
        otherAnchors = [anchor.name for anchor in glyph2.anchors]
        for index, (left, right) in enumerate(
            zip_longest(selfAnchors, otherAnchors)):
            if left != right:
                anchor_diff.append((index, left, right))

        if anchor_diff:
            reporter.warning = True
            reporter.anchorDifferences = anchor_diff
            if (not reporter.anchorCountDifference
                and set(selfAnchors) == set(otherAnchors)):
                reporter.anchorOrderDifference = True

            selfAnchors_counted_set = Counter(selfAnchors)
            otherAnchors_counted_set = Counter(otherAnchors)
            missing_from_glyph1 = (otherAnchors_counted_set
                - selfAnchors_counted_set)
            if missing_from_glyph1:
                reporter.anchorsMissingFromGlyph1 = sorted(
                    missing_from_glyph1.elements()
                )
            missing_from_glyph2 = (selfAnchors_counted_set
                - otherAnchors_counted_set)
            if missing_from_glyph2:
                reporter.anchorsMissingFromGlyph2 = sorted(
                    missing_from_glyph2.elements()
                )

    # ------------
    # Data Queries
    # ------------

    def pointInside(self, point: CoordinateType) -> bool:
        """Check if `point` lies inside the filled area of the glyph.

        :param point: The point to check as a :ref:`type-coordinate`.
        :return: :obj:`True` if `point` is inside the filled area of the
            glyph, :obj:`False` otherwise.

        Example::

            >>> glyph.pointInside((40, 65))
            True

        """
        point = normalizers.normalizeCoordinateTuple(point)
        return self._pointInside(point)

    def _pointInside(self, point: CoordinateType) -> bool:
        """Check if `point` lies inside the filled area of the native glyph.

        This is the environment implementation of :meth:`BaseGlyph.pointInside`.

        :param point: The point to check as a :ref:`type-coordinate`.
        :return: :obj:`True` if `point` is inside the filled area of the
            glyph, :obj:`False` otherwise.

        .. note::

            Subclasses may override this method.

        """
        pen = PointInsidePen(glyphSet=None, testPoint=point, evenOdd=False)
        self.draw(pen)
        return pen.getResult()

    bounds: dynamicProperty = dynamicProperty(
        "bounds",
        """Get the bounds of the glyph.

<<<<<<< HEAD
=======
        This property is read-only.

>>>>>>> v1
        :return: A :class:`tuple` of four :class:`int` or :class:`float` values
            in the form ``(x minimum, y minimum, x maximum, y maximum)``
            representing the bounds of the glyph, or :obj:`None` if the glyph
            is empty.

        Example::

            >>> glyph.bounds
            (10, 30, 765, 643)

        """
    )

    def _get_base_bounds(self) -> Optional[BoundsType]:
        value = self._get_bounds()
        if value is not None:
            value = normalizers.normalizeBoundingBox(value)
        return value

    def _get_bounds(self) -> Optional[BoundsType]:
        """Get the bounds of the native glyph.

        This is the environment implementation of the :attr:`BaseGlyph.bounds`
        property getter.

        :return: A :class:`tuple` of four :class:`int` or :class:`float` values
            in the form ``(x minimum, y minimum, x maximum, y maximum)``
            representing the bounds of the glyph, or :obj:`None` if the glyph
            is empty.

        .. note::

            Subclasses may override this method.

        """
        pen = BoundsPen(self.layer)
        self.draw(pen)
        return pen.bounds

    area: dynamicProperty = dynamicProperty(
        "area",
        """Get the area of the glyph

<<<<<<< HEAD
=======
        This property is read-only.

>>>>>>> v1
        :return: An :class:`int` or a :class:` float value representing the
            area of the glyph, or or :obj:`None` if the glyph is empty.

        Example::

            >>> glyph.area
            583
        """
    )

    def _get_base_area(self) -> Optional[float]:
        value = self._get_area()
        if value is not None:
            value = normalizers.normalizeArea(value)
        return value

    def _get_area(self) -> Optional[float]:
        """Get the area of the native glyph

        This is the environment implementation of the :attr:`BaseGlyph.area`
        property getter.

        :return: An :class:`int` or a :class:` float value representing the
             area of the glyph, or or :obj:`None` if the glyph is empty.

        .. note::

            Subclasses may override this method.

        """
        pen = AreaPen(self.layer)
        self.draw(pen)
        return abs(pen.value)

    # -----------------
    # Layer Interaction
    # -----------------

    layers: dynamicProperty = dynamicProperty(
        "layers",
        """Get the layers of the glyph.

<<<<<<< HEAD
=======
        This property is read-only.

>>>>>>> v1
        :return: A :class:`tuple` of the :class:`BaseLayer` instances belonging
            to the glyph.

        Example::

            >>> glyphLayers = glyph.layers

        """
    )

    def _get_layers(self, **kwargs) -> Tuple[BaseGlyph, ...]:
        r"""Get the layers of the native glyph.

        :param \**kwargs: Additional keyword arguments.
        :return: A :class:`tuple` of the :class:`BaseLayer` subclass instances
            belonging to the glyph.

        """
        font = self.font
        if font is None:
            return tuple()
        glyphs = []
        for layer in font.layers:
            if self.name in layer:
                glyphs.append(layer[self.name])
        return tuple(glyphs)

    # get

    def getLayer(self, name: str) -> BaseGlyph:
        """Get the named layer from the glyph.

        :param name: The name of the :class:`BaseLayer` instance to
            retrieve.
        :return: The specified :class:`Baselayer` instance.
        :raises ValueError: If no layer with the given `name` exists in
            the font.

        Example::

            >>> glyphLayer = glyph.getLayer("foreground")

        """
        name = normalizers.normalizeLayerName(name)
        return self._getLayer(name)

    def _getLayer(self, name: str, **kwargs) -> BaseGlyph:
        r"""Get the named layer from the native glyph.

        :param name: The name of the :class:`BaseLayer` instance to
            retrieve.
        :param \**kwargs: Additional keyword arguments.
        :return: The specified :class:`Baselayer` instance.
        :raises ValueError: If no layer with the given `name` exists in
            the font.

        .. note::

            Subclasses may override this method.

        """
        for glyph in self.layers:
            if glyph.layer.name == name:
                return glyph
        raise ValueError("No layer named '%s' in glyph '%s'."
                         % (name, self.name))

    # new

    def newLayer(self, name: str) -> BaseGlyph:
        """Create a new layer in the glyph.

        If the named layer already exists in the glyph, it
        will be cleared.

        :param name: The name of the new layer to create.
        :return: A newly created :class:`BaseLayer` instance.

        Example::

            >>> glyphLayer = glyph.newLayer("background")

        """
        layerName = name
        glyphName = self.name
        layerName = normalizers.normalizeLayerName(layerName)
        for glyph in self.layers:
            if glyph.layer.name == layerName:
                layer = glyph.layer
                layer.removeGlyph(glyphName)
                break
        glyph = self._newLayer(name=layerName)
        layer = self.font.getLayer(layerName)
        return glyph

<<<<<<< HEAD
    def _newLayer(self, name: str, **kwargs) -> BaseGlyph:
=======
    def _newLayer(self, name: str, **kwargs) -> BaseGlyph:  # type: ignore[return]
>>>>>>> v1
        r"""Create a new layer in the glyph.

        This is the environment implementation of :meth:`BaseGlyph.newLayer`.

<<<<<<< HEAD
        The name of the new layer to create. The value must
            be unique to the font and will be normalized
=======
        :param name: The name of the new layer to create. The value must
            be unique to the font and will have been normalized
>>>>>>> v1
            with :func:`normalizers.normalizeLayerName`.
        :param \**kwargs: Additional keyword arguments.
        :return: A newly created :class:`BaseLayer` subclass instance.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # remove

    def removeLayer(self, layer: Union[BaseGlyph, str]) -> None:
        """Remove the specified layer from the glyph.

        :param name: The layer to remove as a :class:`BaseLayer` instance,
            or a :class:`str` representing the layer name.

        Example::

            >>> glyph.removeLayer("background")

        """
        if isinstance(layer, BaseGlyph):
            layer = layer.layer.name
        layerName = layer
        normalizedLayerName = normalizers.normalizeLayerName(layerName)
        if self._getLayer(normalizedLayerName).layer.name == normalizedLayerName:
            self._removeLayer(normalizedLayerName)

<<<<<<< HEAD
    def _removeLayer(self, name: str, **kwargs) -> None:
=======
    def _removeLayer(self, name: str, **kwargs: Any) -> None:
>>>>>>> v1
        r"""Remove the specified layer from the native glyph.

        This is the environment implementation of :meth:`BaseGlyph.removeLayer`.

<<<<<<< HEAD
        :param name: The name of the layer to remove. The value will be
=======
        :param name: The name of the layer to remove. The value will have been
>>>>>>> v1
            normalized with :func:`normalizers.normalizeLayerName`.
        :param \**kwargs: Additional keyword arguments.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. note::

            Subclasses may override this method.

        """
        self.raiseNotImplementedError()

    # -----
    # Image
    # -----

    image: dynamicProperty = dynamicProperty(
        "base_image",
        """Get the image for the glyph.

<<<<<<< HEAD
=======
        This property is read-only.

>>>>>>> v1
        :return: The :class:`BaseImage` instance belonging to the glyph.

        """
    )

    def _get_base_image(self) -> BaseImage:
        image = self._get_image()
        if image.glyph is None:
            image.glyph = self
        return image

<<<<<<< HEAD
    def _get_image(self) -> BaseImage:
=======
    def _get_image(self) -> BaseImage:  # type: ignore[return]
>>>>>>> v1
        """Get the image for the native glyph.

        :return: The :class:`BaseImage` subclass instance belonging to the glyph.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def addImage(self,
<<<<<<< HEAD
        path: Optional[str] = None,
        data: Optional[bytes] = None,
        scale: ScaleType = None,
                 position: CoordinateType = None,
                 color: ColorType = None) -> BaseImage:
=======
                 path: Optional[str] = None,
                 data: Optional[bytes] = None,
                 scale: Optional[ScaleType] = None,
                 position: Optional[CoordinateType] = None,
                 color: Optional[ColorType] = None) -> BaseImage:
>>>>>>> v1
        """Set the image in the glyph.

        The image data may be provided as either the `path` to an image file or
        directly as raw image `data`. The supported image formats will vary
        across environments. Refer to :class:`BaseImage` for complete details.

        :param path: The optional path to the image file to add to the glyph as
            a :class:`str`. Defaults to :obj:`None`.
        :param data: The optional raw image data to add to the glyph
            as :class:`bytes`. Defaults to :obj:`None`.
        :param scale: The optional x and y values to scale the glyph by as
<<<<<<< HEAD
            a :class:`tuple` of :class:`int` or :class:`float` values.
=======
            a :class:`tuple` of two :class:`int` or :class:`float` values.
>>>>>>> v1
            Defaults to :obj:`None`.
        :param position: The optional location of the lower left point of the
            image as a :ref:`type-coordinate`. Defaults to :obj:`None`.
        :param color: The optional color to be applied to the image as
            a :ref:`type-color`. Defaults to :obj:`None`.
        :return: The :class:`BaseImage` instance added to the glyph.
        :raises IOError: If no valid image file can be found at the given path.
        :raises FontPartsError:  If `path` and `data` are both provided.

        Add the image as a filepath::

            >>> image = glyph.addImage(path="/path/to/my/image.png")

        Add the image as raw data::

            >>> image = glyph.addImage(data=someImageData)

        Add the image with scale::

            >>> image = glyph.addImage(path="/p/t/image.png", scale=(0.5, 1.0))

        Add the image with position::

            >>> image = glyph.addImage(path="/p/t/image.png", position=(10, 20))

        Add the image with color::

            >>> image = glyph.addImage(path="/p/t/image.png", color=(1, 0, 0, 0.5))

        """
        if path is not None and data is not None:
            raise FontPartsError("Only path or data may be defined, not both.")
        if scale is None:
            scale = (1, 1)
        if position is None:
            position = (0, 0)
        normalizedScale = normalizers.normalizeTransformationScale(scale)
        normalizedPosition = normalizers.normalizeTransformationOffset(position)
        if color is not None:
            normalizedColor = normalizers.normalizeColor(color)
        sx, sy = normalizedScale
        ox, oy = normalizedPosition
        transformation = (sx, 0, 0, sy, ox, oy)
        if path is not None:
            if not os.path.exists(path):
                raise IOError("No image located at '%s'." % path)
            with open(path, "rb") as f:
                data = f.read()
<<<<<<< HEAD
        self._addImage(data=data, transformation=transformation, color=color)
        return self.image

    def _addImage(self,
                  data: bytes,
                  transformation: Optional[TransformationMatrixType] = None,
                  color: Optional[ColorType] = None) -> BaseImage:
=======
        if data is not None:
            self._addImage(
                data=data, transformation=transformation, color=normalizedColor
            )
        return self.image

    def _addImage(self,  # type: ignore[return]
                  data: bytes,
                  transformation: Optional[TransformationMatrixType],
                  color: Optional[ColorType]) -> BaseImage:
>>>>>>> v1
        """Set the image in the native glyph.

        Each environment may have different possible
        formats, so this is unspecified. Assigning the image
        to the glyph will be handled by the base class.

<<<<<<< HEAD
        :param data: The optional raw image data to add to the glyph
            as :class:`bytes`. Defaults to :obj:`None`.
        :param transformation: The optional :ref:`type-transformation` values
            to be applied to the image. Defaults to :obj:`None`
        :param color: The optional color to be applied to the image as
            a :ref:`type-color`. Defaults to :obj:`None`.
=======
        :param data: The raw image data to add to the glyph as :class:`bytes`.
        :param transformation: The :ref:`type-transformation` values
            to be applied to the image or :obj:`None`.
        :param color: The color to be applied to the image as
            a :ref:`type-color` or :obj:`None`.
>>>>>>> v1
        :return: The :class:`BaseImage` subclass instance added to the glyph.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def clearImage(self) -> None:
        """Remove the image from the glyph.

        Example::

            >>> glyph.clearImage()

        """
        if self.image is not None:
            self._clearImage()

<<<<<<< HEAD
    def _clearImage(self, **kwargs:Any) -> None:
=======
    def _clearImage(self, **kwargs: Any) -> None:
>>>>>>> v1
        r"""Remove the image from the native glyph.

        :param \**kwargs: Additional keyword arguments.
        :raises NotImplementedError: If the method has not
            been overridden by a subclass.

        """
        self.raiseNotImplementedError()

    # ----------
    # Mark color
    # ----------

    markColor: dynamicProperty = dynamicProperty(
        "base_markColor",
        """Get or set the glyph's mark color.

        The value must be either a :ref:`type-color` or :obj:`None`.
        :return: The color value assigned to the glyph, or:obj:`None` if
            no color has been assigned.

        Example::

            >>> glyph.markColor
            (1, 0, 0, 0.5)
            >>> glyph.markColor = None

        """
    )

    def _get_base_markColor(self) -> Optional[ColorType]:
        value = self._get_markColor()
        if value is None:
            return None
        normalizedValue = normalizers.normalizeColor(value)
        return Color(normalizedValue)

    def _set_base_markColor(self, value: Optional[ColorType]) -> None:
        if value is not None:
            value = normalizers.normalizeColor(value)
        self._set_markColor(value)

<<<<<<< HEAD
    def _get_markColor(self) -> Optional[ColorType]:
=======
    def _get_markColor(self) -> Optional[ColorType]:  # type: ignore[return]
>>>>>>> v1
        """Get the glyph's mark color.

        This is the environment implementation of
        the :attr:`BaseGlyph.markColor` property getter.

        :return: The :ref:`type-color` value assigned to the glyph,
            or:obj:`None` if no color has been assigned.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_markColor(self, value: Optional[ColorType]) -> None:
        """Set the glyph's mark color.

        This is the environment implementation of
        the :attr:`BaseGlyph.markColor` property setter.

        :param value: The :ref:`type-color` value to assign to the glyph,
            or :obj:`None`.
        :raises NotImplementedError: If the method has not been overridden
            by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # ----
    # Note
    # ----

    note: dynamicProperty = dynamicProperty(
        "base_note",
        """Get or set the glyph's note.

        The value must be a :class:`str` or :obj:`None`.

        :return: A :class:`str`, or :obj:`None` representing an empty note.

        Example::

            >>> glyph.note
            "P.B. said this looks 'awesome.'"
            >>> glyph.note = "P.B. said this looks 'AWESOME.'"

        """
    )

    def _get_base_note(self) -> Optional[str]:
        value = self._get_note()
        if value is not None:
            value = normalizers.normalizeGlyphNote(value)
        return value

    def _set_base_note(self, value: Optional[str]) -> None:
        if value is not None:
            value = normalizers.normalizeGlyphNote(value)
        self._set_note(value)

<<<<<<< HEAD
    def _get_note(self) -> Optional[str]:
=======
    def _get_note(self) -> Optional[str]:  # type: ignore[return]
>>>>>>> v1
        """Get the glyph's note.

        This is the environment implementation of the :attr:`BaseGlyph.note`
        property getter.

        :return: A :class:`str`, or :obj:`None` representing an empty note.
        :raises NotImplementedError: If the method has not been overridden
            by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_note(self, value: Optional[str]) -> None:
        """Set the glyph's note.

        This is the environment implementation of the :attr:`BaseGlyph.note`
        property setter.

        :param value: The note to assign to the glyph as a :class:`str`
            or :obj:`None`.
        :raises NotImplementedError: If the method has not been overridden
            by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # ---
    # Lib
    # ---

    lib: dynamicProperty = dynamicProperty(
        "base_lib",
        """Get the font's lib object.

<<<<<<< HEAD
=======
        This property is read-only.

>>>>>>> v1
        :return: An instance of the :class:`BaseLib` class.

        Example::

            >>> lib = glyph.lib

        """
    )

    def _get_base_lib(self) -> BaseLib:
        lib = self._get_lib()
        lib.glyph = self
        return lib

<<<<<<< HEAD
    def _get_lib(self) -> BaseLib:
=======
    def _get_lib(self) -> BaseLib:  # type: ignore[return]
>>>>>>> v1
        """Get the native glyph's lib object.

        This is the environment implementation of :attr:`BaseFont.lib`.

        :return: An instance of a :class:`BaseLib` subclass.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # --------
    # Temp Lib
    # --------

    tempLib: dynamicProperty = dynamicProperty(
        "base_tempLib",
        """Get the glyph's temporary lib object.

        This property provides access to a temporary instance of
        the :class:`BaseLib` class, used for storing data that should
        not be persisted. It is similar to :attr:`BaseGlyph.lib`, except
        that its contents will not be saved when calling
        the :meth:`BaseFont.save` method.

<<<<<<< HEAD
=======
        This property is read-only.

>>>>>>> v1
        :return: A temporary instance of the :class:`BaseLib` class.

        Example::

            >>> tempLib = glyph.tempLib

        """
    )

    def _get_base_tempLib(self) -> BaseLib:
        lib = self._get_tempLib()
        lib.glyph = self
        return lib

<<<<<<< HEAD
    def _get_tempLib(self) -> BaseLib:
=======
    def _get_tempLib(self) -> BaseLib:  # type: ignore[return]
>>>>>>> v1
        """Get the native glyph's temporary lib object.

        This is the environment implementation
        of :attr:`BaseGlyph.tempLib`.

        :return: A temporary instance of a :class:`BaseLib` subclass.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # ---
    # API
    # ---

    def isEmpty(self) -> bool:
        """Check if the glyph is empty.

        :return: :obj:`True` if there are no contours and/or
        components in the glyph, :obj:`False` otherwise.

        Example::

            >>> glyph.isEmpty()

        .. note:: This method only checks for the presence of contours and
           components. Other attributes (guidelines, anchors, a lib, etc.) will
           not affect what this method returns.

        """
        if self.contours:
            return False
        if self.components:
            return False
        return True

    def loadFromGLIF(self, glifData: str) -> None:
        """Read data in `GLIF format <http://unifiedfontobject.org/versions/ufo3/glyphs/glif/>`_ into the glyph.

        :param glifData: The data to read as a :class:`str`.

        Example::

            >>> glyph.readGlyphFromString(xmlData)

        """
        self._loadFromGLIF(glifData)

    def _loadFromGLIF(self, glifData: str) -> None:
        """Read data in `GLIF format <http://unifiedfontobject.org/versions/ufo3/glyphs/glif/>`_ into the native glyph.

        :param glifData: The data to read as a :class:`str`.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def dumpToGLIF(self, glyphFormatVersion: int = 2) -> str:
        """Return the glyph's contents as a string in `GLIF format <http://unifiedfontobject.org/versions/ufo3/glyphs/glif/>`_.

        :param glyphFormatVersion: An :class:`int` defining the preferred GLIF
            format version.

        Example::

            >>> xml = glyph.writeGlyphToString()

        """
        glyphFormatVersion = normalizers.normalizeGlyphFormatVersion(glyphFormatVersion)
        return self._dumpToGLIF(glyphFormatVersion)

<<<<<<< HEAD
    def _dumpToGLIF(self, glyphFormatVersion: int) -> str:
=======
    def _dumpToGLIF(self, glyphFormatVersion: int) -> str:  # type: ignore[return]
>>>>>>> v1
        """Return the native glyph's contents as a string in `GLIF format <http://unifiedfontobject.org/versions/ufo3/glyphs/glif/>`_.

        :param glyphFormatVersion: An :class:`int` defining the preferred GLIF
            format version.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # ---------
    # Selection
    # ---------

    # contours

    selectedContours: dynamicProperty = dynamicProperty(
        "base_selectedContours",
        """Get or set the selected contours in the glyph.

        The value must be a :class:`tuple` or :class:`list` of
        either :class:`BaseContour` instances or :class:`int` values
        representing contour indexes to select.

        :return: A :class:`tuple` of the currently
            selected :class:`BaseContour` instances.

        Example::

<<<<<<< HEAD
            >>> components = glyph.selectedContours
=======
            >>> contours = glyph.selectedContours
>>>>>>> v1
            >>> glyph.selectedContours = otherContours

        Set selection using indexes::

            >>> glyph.selectedContours = [0, 2]

        """
    )

    def _get_base_selectedContours(self) -> Tuple[BaseContour, ...]:
<<<<<<< HEAD
        selected = tuple([normalizers.normalizeContour(contour)
            for contour in self._get_selectedContours()])
=======
        selected = tuple(normalizers.normalizeContour(contour)
            for contour in self._get_selectedContours())
>>>>>>> v1
        return selected

    def _get_selectedContours(self) -> Tuple[BaseContour, ...]:
        """Get the selected contours in the native glyph.

        This is the environment implementation of
        the :attr:`BaseGlyph.selectedContour` property getter.

<<<<<<< HEAD
        :return: A :class:`tuple` of the currently
            selected :class:`BaseContour` instances.
=======
        :return: A :class:`tuple` of the currently selected :class:`BaseContour`
            instances. Each value item will be normalized
            with :func:`normalizers.normalizeContour`.
>>>>>>> v1

        .. note::

            Subclasses may override this method.

        """
        return self._getSelectedSubObjects(self.contours)

    def _set_base_selectedContours(self,
        value: CollectionType[Union[int, BaseContour]]) -> None:
        normalized = []
        for i in value:
            if isinstance(i, int):
                i = normalizers.normalizeIndex(i)
            else:
                i = normalizers.normalizeContour(i)
            normalized.append(i)
        self._set_selectedContours(normalized)

    def _set_selectedContours(self,
        value: CollectionType[Union[int, BaseContour]]) -> None:
        """Set the selected contours in the glyph.

        This is the environment implementation of
        the :attr:`BaseGlyph.selectedContour` property setter.

        :param value: a :class:`tuple` or :class:`list` of
            either :class:`BaseContour` instances or :class:`int` values
<<<<<<< HEAD
            representing contour indexes to select.
=======
            representing contour indexes to select. Each value item will have
            been normalized with :func:`normalizers.normalizeContour`.
            or :func:`normalizers.normalizeIndex`.
>>>>>>> v1

        .. note::

            Subclasses may override this method.

        """
        return self._setSelectedSubObjects(self.contours, value)

    # components

    selectedComponents: dynamicProperty = dynamicProperty(
        "base_selectedComponents",
        """Get or set the selected components in the glyph.

        The value must be a :class:`tuple` or :class:`list` of
        either :class:`BaseComponent` instances or :class:`int` values
        representing component indexes to select.

        :return: A :class:`tuple` of the currently
            selected :class:`BaseComponent` instances.

        Example::

            >>> components = glyph.selectedComponents
            >>> glyph.selectedComponents = otherComponents

        Set selection using indexes::

            >>> glyph.selectedComponents = [0, 2]

        """
    )

    def _get_base_selectedComponents(self) -> Tuple[BaseComponent, ...]:
<<<<<<< HEAD
        selected = tuple([normalizers.normalizeComponent(component)
            for component in self._get_selectedComponents()])
=======
        selected = tuple(normalizers.normalizeComponent(component)
            for component in self._get_selectedComponents())
>>>>>>> v1
        return selected

    def _get_selectedComponents(self) -> Tuple[BaseComponent, ...]:
        """Get the selected components in the native glyph.

        This is the environment implementation of
        the :attr:`BaseGlyph.selectedComponents` property getter.

        :return: A :class:`tuple` of the currently
<<<<<<< HEAD
            selected :class:`BaseComponent` instances.
=======
            selected :class:`BaseComponent` instances. Each value item will be
            normalized with :func:`normalizers.normalizeComponent`.
>>>>>>> v1

        .. note::

            Subclasses may override this method.

        """
        return self._getSelectedSubObjects(self.components)

    def _set_base_selectedComponents(self,
        value: CollectionType[Union[int, BaseComponent]]) -> None:
        normalized = []
        for i in value:
            if isinstance(i, int):
                i = normalizers.normalizeIndex(i)
            else:
                i = normalizers.normalizeComponent(i)
            normalized.append(i)
        self._set_selectedComponents(normalized)

    def _set_selectedComponents(self,
        value: CollectionType[Union[int, BaseComponent]]) -> None:
        """Set the selected components in the glyph.

        This is the environment implementation of
        the :attr:`BaseGlyph.selectedComponents` property setter.

        :param value: a :class:`tuple` or :class:`list` of
            either :class:`BaseComponent` instances or :class:`int` values
<<<<<<< HEAD
            representing component indexes to select.
=======
            representing component indexes to select. Each value item will have
            been normalized with :func:`normalizers.normalizeComponent`
            or :func:`normalizers.normalizeIndex`.
>>>>>>> v1

        .. note::

            Subclasses may override this method.

        """
        return self._setSelectedSubObjects(self.components, value)

    # anchors

    selectedAnchors: dynamicProperty = dynamicProperty(
        "base_selectedAnchors",
        """Get or set the selected anchors in the glyph.

        The value must be a :class:`tuple` or :class:`list` of
        either :class:`BaseAnchor` instances or :class:`int` values
        representing anchor indexes to select.

        :return: A :class:`tuple` of the currently
            selected :class:`BaseAnchor` instances.

        Example::

            >>> anchors = glyph.selectedAnchors:
            >>> glyph.selectedAnchors = otherAnchors

        Set selection using indexes::

            >>> glyph.selectedAnchors = [0, 2]

        """
    )

    def _get_base_selectedAnchors(self) -> Tuple[BaseAnchor, ...]:
<<<<<<< HEAD
        selected = tuple([normalizers.normalizeAnchor(anchor)
            for anchor in self._get_selectedAnchors()])
=======
        selected = tuple(normalizers.normalizeAnchor(anchor)
            for anchor in self._get_selectedAnchors())
>>>>>>> v1
        return selected

    def _get_selectedAnchors(self) -> Tuple[BaseAnchor, ...]:
        """Get the selected anchors in the native glyph.

        This is the environment implementation of
        the :attr:`BaseGlyph.selectedAnchors` property getter.

        :return: A :class:`tuple` of the currently
<<<<<<< HEAD
            selected :class:`BaseAnchor` instances.
=======
            selected :class:`BaseAnchor` instances. Each value item will be
            normalized with :func:`normalizers.normalizeAnchor`.
>>>>>>> v1

        .. note::

            Subclasses may override this method.

        """
        return self._getSelectedSubObjects(self.anchors)

    def _set_base_selectedAnchors(self,
        value: CollectionType[Union[int, BaseAnchor]]) -> None:
        normalized = []
        for i in value:
            if isinstance(i, int):
                i = normalizers.normalizeIndex(i)
            else:
                i = normalizers.normalizeAnchor(i)
            normalized.append(i)
        self._set_selectedAnchors(normalized)

    def _set_selectedAnchors(self,
        value: CollectionType[Union[int, BaseAnchor]]) -> None:
        """Set the selected anchors in the glyph.

        This is the environment implementation of
        the :attr:`BaseGlyph.selectedAnchors` property setter.

        :param value: a :class:`tuple` or :class:`list` of
            either :class:`BaseAnchor` instances or :class:`int` values
<<<<<<< HEAD
            representing anchor indexes to select.
=======
            representing anchor indexes to select. Each value item will have
            been normalized with :func:`normalizers.normalizeAnchor`
            or :func:`normalizers.normalizeIndex`.
>>>>>>> v1

        .. note::

            Subclasses may override this method.

        """
        return self._setSelectedSubObjects(self.anchors, value)

    # guidelines

    selectedGuidelines: dynamicProperty = dynamicProperty(
        "base_selectedGuidelines",
        """Get or set the selected guidelines in the glyph.

        The value must be a :class:`tuple` or :class:`list` of
        either :class:`BaseGuideline` instances or :class:`int` values
        representing component indexes to select.

        :return: A :class:`tuple` of the currently
            selected :class:`BaseGuideline` instances.

        Example::

            >>> guidelines = glyph.selectedGuidelines
            >>> glyph.selectedGuidelines = otherGuidelines

        Set selection using indexes::

            >>> glyph.selectedGuidelines = [0, 2]

        """
    )

    def _get_base_selectedGuidelines(self) -> Tuple[BaseGuideline, ...]:
<<<<<<< HEAD
        selected = tuple([normalizers.normalizeGuideline(guideline)
            for guideline in self._get_selectedGuidelines()])
=======
        selected = tuple(normalizers.normalizeGuideline(guideline)
            for guideline in self._get_selectedGuidelines())
>>>>>>> v1
        return selected

    def _get_selectedGuidelines(self) -> Tuple[BaseGuideline, ...]:
        """Get the selected guidelines in the native glyph.

        This is the environment implementation of
        the :attr:`BaseGlyph.selectedGuideline` property getter.

        :return: A :class:`tuple` of the currently
<<<<<<< HEAD
            selected :class:`BaseGuideline` instances.
=======
            selected :class:`BaseGuideline` instances. Each value item will be
            normalized with :func:`normalizers.normalizeGuideline`.
>>>>>>> v1

        .. note::

            Subclasses may override this method.

        """
        return self._getSelectedSubObjects(self.guidelines)

    def _set_base_selectedGuidelines(self,
        value: CollectionType[Union[int, BaseGuideline]]) -> None:
        normalized = []
        for i in value:
            if isinstance(i, int):
                i = normalizers.normalizeIndex(i)
            else:
                i = normalizers.normalizeGuideline(i)
            normalized.append(i)
        self._set_selectedGuidelines(normalized)

    def _set_selectedGuidelines(self,
        value: CollectionType[Union[int, BaseGuideline]]) -> None:
        """Set the selected guidelines in the glyph.

        This is the environment implementation of
        the :attr:`BaseGlyph.selectedGuideline` property setter.

        :param value: a :class:`tuple` or :class:`list` of
            either :class:`BaseGuideline` instances or :class:`int` values
<<<<<<< HEAD
            representing guideline indexes to select.
=======
            representing guideline indexes to select. Each value item will have
            been normalized with :func:`normalizers.normalizeGuideline`
            or :func:`normalizers.normalizeIndex`.
>>>>>>> v1

        .. note::

            Subclasses may override this method.

        """
        return self._setSelectedSubObjects(self.guidelines, value)
