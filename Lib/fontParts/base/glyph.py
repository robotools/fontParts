<<<<<<< HEAD
# pylint: disable=C0103, C0302, C0114, W0613
from __future__ import annotations
<<<<<<< HEAD
from typing import TYPE_CHECKING, Any, Iterator, Optional, Union, List, Tuple
=======
from typing import TYPE_CHECKING, Any, Iterator, Optional, Union, List, Tuple, TypeVar
>>>>>>> v1
from itertools import zip_longest
from collections import Counter
=======
try:
    from itertools import zip_longest as zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest
import collections
>>>>>>> parent of 3d67a1d (Update documentation (#739))
import os
from copy import deepcopy
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


class BaseGlyph(BaseObject,
                TransformationMixin,
                InterpolationMixin,
                SelectionMixin,
                DeprecatedGlyph,
                RemovedGlyph
                ):

    """
    A glyph object. This object will almost always
    be created by retrieving it from a font object.
    """

    copyAttributes = (
        "name",
        "unicodes",
        "width",
        "height",
        "note",
        "markColor",
        "lib"
    )

    def _reprContents(self):
        contents = [
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

=======
    def copy(self):
        """
        Copy this glyph's data into a new glyph object.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        This new glyph object will not belong to a font.

            >>> copiedGlyph = glyph.copy()

        This will copy:

        - name
        - unicodes
        - width
        - height
        - note
        - markColor
        - lib
        - contours
        - components
        - anchors
        - guidelines
        - image
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
=======
    def copyData(self, source):
>>>>>>> parent of 3d67a1d (Update documentation (#739))
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

    _layer = None

    layer = dynamicProperty(
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
=======
        """
        The glyph's parent layer.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

            >>> layer = glyph.layer
        """
    )

    def _get_layer(self):
        if self._layer is None:
            return None
        return self._layer

<<<<<<< HEAD
    def _set_layer(self, layer: BaseLayer) -> None:
=======
<<<<<<< HEAD
    def _set_layer(self, layer):
>>>>>>> parent of 3d67a1d (Update documentation (#739))
=======
    def _set_layer(self, layer: Optional[BaseLayer]) -> None:
>>>>>>> v1
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
        self._layer = layer

    # Font

    font = dynamicProperty(
        "font",
<<<<<<< HEAD
        """Get the glyph's parent font object.

<<<<<<< HEAD
        :return: An instance of the :class:`BaseFont` class.
=======
        This property is read-only.

        :return: The :class:`BaseFont` instance containing the glyph
            or :obj:`None`.
>>>>>>> v1

        Example::
=======
        """
        The glyph's parent font.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

            >>> font = glyph.font
        """
    )

    def _get_font(self):
        if self._layer is None:
            return None
        return self.layer.font

    # --------------
    # Identification
    # --------------

    # Name

    name = dynamicProperty(
        "base_name",
        """
        The glyph's name. This will be a :ref:`type-string`.

            >>> glyph.name
            "A"
            >>> glyph.name = "A.alt"
        """
    )

<<<<<<< HEAD
    def _get_base_name(self) -> Optional[str]:
=======
<<<<<<< HEAD
    def _get_base_name(self):
>>>>>>> parent of 3d67a1d (Update documentation (#739))
=======
    def _get_base_name(self) -> str:
>>>>>>> v1
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
        value = self._get_name()
        if value is not None:
            value = normalizers.normalizeGlyphName(value)
        return value

<<<<<<< HEAD
    def _set_base_name(self, value: Optional[str]) -> None:
=======
<<<<<<< HEAD
    def _set_base_name(self, value):
>>>>>>> parent of 3d67a1d (Update documentation (#739))
=======
    def _set_base_name(self, value: str) -> None:
>>>>>>> v1
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
        if value == self.name:
            return
        value = normalizers.normalizeGlyphName(value)
        layer = self.layer
        if layer is not None and value in layer:
            raise ValueError("A glyph with the name '%s' already exists."
                             % value)
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
=======
    def _get_name(self):
        """
        Get the name of the glyph.
        This must return a unicode string.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

<<<<<<< HEAD
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
=======
    def _set_name(self, value):
        """
        Set the name of the glyph.
        This will be a unicode string.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # Unicodes

    unicodes = dynamicProperty(
        "base_unicodes",
<<<<<<< HEAD
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
=======
        """
        The glyph's unicode values in order from most to least important.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

            >>> glyph.unicodes
            (65,)
            >>> glyph.unicodes = [65, 66]
            >>> glyph.unicodes = []

        The values in the returned tuple will be :ref:`type-int`.
        When setting you may use a list of :ref:`type-int` or
        :ref:`type-hex` values.
        """
    )

    def _get_base_unicodes(self):
        value = self._get_unicodes()
        value = normalizers.normalizeGlyphUnicodes(value)
        return value

    def _set_base_unicodes(self, value):
        value = list(value)
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
=======
    def _get_unicodes(self):
        """
        Get the unicodes assigned to the glyph.
        This must return a tuple of zero or more integers.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

<<<<<<< HEAD
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
=======
    def _set_unicodes(self, value):
        """
        Assign the unicodes to the glyph.
        This will be a list of zero or more integers.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    unicode = dynamicProperty(
        "base_unicode",
<<<<<<< HEAD
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
=======
        """
        The glyph's primary unicode value.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

            >>> glyph.unicode
            65
            >>> glyph.unicode = None

        This is equivalent to ``glyph.unicodes[0]``. Setting a
        ``glyph.unicode`` value will reset ``glyph.unicodes`` to a tuple
        containing that value or an empty tuple if ``value`` is ``None``.

            >>> glyph.unicodes
            (65, 67)
            >>> glyph.unicode = 65
            >>> glyph.unicodes
            (65,)
            >>> glyph.unicode = None
            >>> glyph.unicodes
            ()

        The returned value will be an :ref:`type-int` or ``None``.
        When setting you may send :ref:`type-int` or :ref:`type-hex`
        values or ``None``.
        """
    )

    def _get_base_unicode(self):
        value = self._get_unicode()
        if value is not None:
            value = normalizers.normalizeGlyphUnicode(value)
        return value

    def _set_base_unicode(self, value):
        if value is not None:
            value = normalizers.normalizeGlyphUnicode(value)
            self._set_unicode(value)
        else:
            self._set_unicodes(())

    def _get_unicode(self):
        """
        Get the primary unicode assigned to the glyph.
        This must return an integer or None.

        Subclasses may override this method.
        """
        values = self.unicodes
        if values:
            return values[0]
        return None

    def _set_unicode(self, value):
        """
        Assign the primary unicode to the glyph.
        This will be an integer or None.

        Subclasses may override this method.
        """
        if value is None:
            self.unicodes = []
        else:
            self.unicodes = [value]

    def autoUnicodes(self):
        """
        Use heuristics to set the Unicode values in the glyph.

            >>> glyph.autoUnicodes()

        Environments will define their own heuristics for
        automatically determining values.
        """
        self._autoUnicodes()

    def _autoUnicodes(self):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # -------
    # Metrics
    # -------

    # horizontal

    width = dynamicProperty(
        "base_width",
        """
        The glyph's width.

            >>> glyph.width
            500
            >>> glyph.width = 200

        The value will be a :ref:`type-int-float`.
        """
    )

    def _get_base_width(self):
        value = self._get_width()
        value = normalizers.normalizeGlyphWidth(value)
        return value

    def _set_base_width(self, value):
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
=======
    def _get_width(self):
        """
        This must return an int or float.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_width(self, value):
        """
        value will be an int or float.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    leftMargin = dynamicProperty(
        "base_leftMargin",
<<<<<<< HEAD
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
=======
        """
        The glyph's left margin.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

            >>> glyph.leftMargin
            35
            >>> glyph.leftMargin = 45

        The value will be a :ref:`type-int-float`
        or `None` if the glyph has no outlines.
        """
    )

    def _get_base_leftMargin(self):
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
=======
    def _set_base_leftMargin(self, value):
        value = normalizers.normalizeGlyphLeftMargin(value)
        self._set_leftMargin(value)

    def _get_leftMargin(self):
        """
        This must return an int or float.
        If the glyph has no outlines, this must return `None`.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        Subclasses may override this method.
        """
        bounds = self.bounds
        if bounds is None:
            return None
        xMin, yMin, xMax, yMax = bounds
        return xMin

<<<<<<< HEAD
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
=======
    def _set_leftMargin(self, value):
        """
        value will be an int or float.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        Subclasses may override this method.
        """
        diff = value - self.leftMargin
        self.moveBy((diff, 0))
        self.width += diff

    rightMargin = dynamicProperty(
        "base_rightMargin",
<<<<<<< HEAD
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
=======
        """
        The glyph's right margin.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

            >>> glyph.rightMargin
            35
            >>> glyph.rightMargin = 45

        The value will be a :ref:`type-int-float`
        or `None` if the glyph has no outlines.
        """
    )

    def _get_base_rightMargin(self):
        value = self._get_rightMargin()
        value = normalizers.normalizeGlyphRightMargin(value)
        return value

<<<<<<< HEAD
    def _set_base_rightMargin(self, value: Optional[IntFloatType]) -> None:
=======
<<<<<<< HEAD
    def _set_base_rightMargin(self, value):
>>>>>>> parent of 3d67a1d (Update documentation (#739))
=======
    def _set_base_rightMargin(self, value: IntFloatType) -> None:
>>>>>>> v1
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
        value = normalizers.normalizeGlyphRightMargin(value)
        self._set_rightMargin(value)

    def _get_rightMargin(self):
        """
        This must return an int or float.
        If the glyph has no outlines, this must return `None`.

        Subclasses may override this method.
        """
        bounds = self.bounds
        if bounds is None:
            return None
        xMin, yMin, xMax, yMax = bounds
        return self.width - xMax

<<<<<<< HEAD
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
=======
    def _set_rightMargin(self, value):
        """
        value will be an int or float.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        Subclasses may override this method.
        """
        bounds = self.bounds
        if bounds is None:
            self.width = value
        else:
            xMin, yMin, xMax, yMax = bounds
            self.width = xMax + value

    # vertical

    height = dynamicProperty(
        "base_height",
        """
        The glyph's height.

            >>> glyph.height
            500
            >>> glyph.height = 200

        The value will be a :ref:`type-int-float`.
        """
    )

    def _get_base_height(self):
        value = self._get_height()
        value = normalizers.normalizeGlyphHeight(value)
        return value

    def _set_base_height(self, value):
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
=======
    def _get_height(self):
        """
        This must return an int or float.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_height(self, value):
        """
        value will be an int or float.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    bottomMargin = dynamicProperty(
        "base_bottomMargin",
<<<<<<< HEAD
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
=======
        """
        The glyph's bottom margin.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

            >>> glyph.bottomMargin
            35
            >>> glyph.bottomMargin = 45

        The value will be a :ref:`type-int-float`
        or `None` if the glyph has no outlines.
        """
    )

    def _get_base_bottomMargin(self):
        value = self._get_bottomMargin()
        value = normalizers.normalizeGlyphBottomMargin(value)
        return value

<<<<<<< HEAD
    def _set_base_bottomMargin(self, value: Optional[IntFloatType]) -> None:
=======
<<<<<<< HEAD
    def _set_base_bottomMargin(self, value):
>>>>>>> parent of 3d67a1d (Update documentation (#739))
=======
    def _set_base_bottomMargin(self, value: IntFloatType) -> None:
>>>>>>> v1
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
        value = normalizers.normalizeGlyphBottomMargin(value)
        self._set_bottomMargin(value)

    def _get_bottomMargin(self):
        """
        This must return an int or float.
        If the glyph has no outlines, this must return `None`.

        Subclasses may override this method.
        """
        bounds = self.bounds
        if bounds is None:
            return None
        xMin, yMin, xMax, yMax = bounds
        return yMin

<<<<<<< HEAD
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
=======
    def _set_bottomMargin(self, value):
        """
        value will be an int or float.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        Subclasses may override this method.
        """
        diff = value - self.bottomMargin
        self.moveBy((0, diff))
        self.height += diff

    topMargin = dynamicProperty(
        "base_topMargin",
<<<<<<< HEAD
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
=======
        """
        The glyph's top margin.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

            >>> glyph.topMargin
            35
            >>> glyph.topMargin = 45

        The value will be a :ref:`type-int-float`
        or `None` if the glyph has no outlines.
        """
    )

    def _get_base_topMargin(self):
        value = self._get_topMargin()
        value = normalizers.normalizeGlyphTopMargin(value)
        return value

<<<<<<< HEAD
    def _set_base_topMargin(self, value: Optional[IntFloatType]) -> None:
=======
<<<<<<< HEAD
    def _set_base_topMargin(self, value):
>>>>>>> parent of 3d67a1d (Update documentation (#739))
=======
    def _set_base_topMargin(self, value: IntFloatType) -> None:
>>>>>>> v1
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
        value = normalizers.normalizeGlyphTopMargin(value)
        self._set_topMargin(value)

    def _get_topMargin(self):
        """
        This must return an int or float.
        If the glyph has no outlines, this must return `None`.

        Subclasses may override this method.
        """
        bounds = self.bounds
        if bounds is None:
            return None
        xMin, yMin, xMax, yMax = bounds
        return self.height - yMax

<<<<<<< HEAD
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
=======
    def _set_topMargin(self, value):
        """
        value will be an int or float.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

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

    def getPen(self):
        """
        Return a :ref:`type-pen` object for adding outline data
        to the glyph.

            >>> pen = glyph.getPen()
        """
        self.raiseNotImplementedError()

    def getPointPen(self):
        """
        Return a :ref:`type-pointpen` object for adding outline data
        to the glyph.

            >>> pointPen = glyph.getPointPen()
        """
        self.raiseNotImplementedError()

    def draw(self, pen, contours=True, components=True):
        """
        Draw the glyph's outline data (contours and components) to
        the given :ref:`type-pen`.

            >>> glyph.draw(pen)

        If ``contours`` is set to ``False``, the glyph's
        contours will not be drawn.

            >>> glyph.draw(pen, contours=False)

        If ``components`` is set to ``False``, the glyph's
        components will not be drawn.

            >>> glyph.draw(pen, components=False)
        """
        if contours:
            for contour in self:
                contour.draw(pen)
        if components:
            for component in self.components:
                component.draw(pen)

    def drawPoints(self, pen, contours=True, components=True):
        """
        Draw the glyph's outline data (contours and components) to
        the given :ref:`type-pointpen`.

            >>> glyph.drawPoints(pointPen)

        If ``contours`` is set to ``False``, the glyph's
        contours will not be drawn.

            >>> glyph.drawPoints(pointPen, contours=False)

        If ``components`` is set to ``False``, the glyph's
        components will not be drawn.

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

<<<<<<< HEAD
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

=======
    def clear(self, contours=True, components=True, anchors=True,
              guidelines=True, image=True):
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        Clear the glyph.

<<<<<<< HEAD
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
=======
            >>> glyph.clear()
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        This clears:

<<<<<<< HEAD
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
<<<<<<< HEAD
        - contours
        - components
        - anchors
        - guidelines
        - image
>>>>>>> parent of 3d67a1d (Update documentation (#739))
=======
        :param components: Whether to clear the glyph's component data.
        :param anchors: Whether to clear the glyph's anchor data.
        :param guidelines: Whether to clear the glyph's guideline data.
        :param image: Whether to clear the glyph's image data.
>>>>>>> v1
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea

        It's possible to turn off the clearing of portions of
        the glyph with the listed arguments.

            >>> glyph.clear(guidelines=False)
        """
        self._clear(contours=contours, components=components,
                    anchors=anchors, guidelines=guidelines, image=image)

    def _clear(self, contours=True, components=True, anchors=True,
               guidelines=True, image=True):
        """
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

    def appendGlyph(self, other, offset=None):
        """
        Append the data from ``other`` to new objects in this glyph.

            >>> glyph.appendGlyph(otherGlyph)

<<<<<<< HEAD
        This will append:
=======
        - :attr:`contours`
        - :attr:`components`
        - :attr:`anchors`
        - :attr:`guidelines`
<<<<<<< HEAD
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea

        - contours
        - components
        - anchors
        - guidelines

        ``offset`` indicates the x and y shift values that should
        be applied to the appended data. It must be a :ref:`type-coordinate`
        value or ``None``. If ``None`` is given, the offset will be ``(0, 0)``.

<<<<<<< HEAD
=======
=======

        :param other: The :class:`BaseGlyph` instace containing the source
            data to append.
        :param offset: The x and y shift values to be applied to the
            appended data as a :ref:`type-coordinate`, or :obj:`None`
            representing an offset of ``(0, 0)``.

        Example::

>>>>>>> v1
            >>> glyph.appendGlyph(otherGlyph)
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
            >>> glyph.appendGlyph(otherGlyph, (100, 0))
        """
        if offset is None:
            offset = (0, 0)
<<<<<<< HEAD
        offset = normalizers.normalizeTransformationOffset(offset)
        self._appendGlyph(other, offset)
<<<<<<< HEAD
=======
        normalizedOffset = normalizers.normalizeTransformationOffset(offset)
        self._appendGlyph(other, normalizedOffset)
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea

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
>>>>>>> parent of 3d67a1d (Update documentation (#739))

<<<<<<< HEAD
    def _appendGlyph(self, other, offset=None):
        """
        Subclasses may override this method.
=======
=======
>>>>>>> v1
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
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

    # Contours

    def _setGlyphInContour(self, contour):
        if contour.glyph is None:
            contour.glyph = self

    contours = dynamicProperty(
        "contours",
<<<<<<< HEAD
        """Get all contours in the glyph.

<<<<<<< HEAD
=======
        This property is read-only.

>>>>>>> v1
        :return: A :class:`tuple` of :class:`BaseContour` objects.

        Example::
=======
        """
        An :ref:`type-immutable-list` of all contours in the glyph.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

            >>> contours = glyph.contours

        The list will contain :class:`BaseContour` objects.
        """
    )

<<<<<<< HEAD
    def _get_contours(self):
=======
    def _get_contours(self) -> Tuple[BaseContour, ...]:
        """Get all contours in the native glyph.

        This is the environment implementation of the :attr:`BaseGlyph.contours`
        property getter.

        :return: A :class:`tuple` of :class:`BaseContour` subclass instances.

        .. note::

            Subclasses may override this method.
<<<<<<< HEAD

>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
        """
<<<<<<< HEAD
        return tuple([self[i] for i in range(len(self))])

=======

        """
        return tuple(self[i] for i in range(len(self)))

>>>>>>> v1
    def __len__(self) -> int:
        """Get the number of contours in the glyph.

        :return: An :class:`int` representing the number of contours in the
            glyph.
=======
        Subclasses may override this method.
        """
        return tuple([self[i] for i in range(len(self))])
>>>>>>> parent of 3d67a1d (Update documentation (#739))

    def __len__(self):
        """
        The number of contours in the glyph.

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
=======
    def _lenContours(self, **kwargs):
        """
        This must return an integer.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def __iter__(self):
        """
        Iterate through all contours in the glyph.

            >>> for contour in glyph:
            ...     contour.reverse()
        """
        return self._iterContours()

    def _iterContours(self, **kwargs):
        """
        This must return an iterator that returns wrapped contours.

        Subclasses may override this method.
        """
        count = len(self)
        index = 0
        while count:
            yield self[index]
            count -= 1
            index += 1

    def __getitem__(self, index):
        """
        Get the contour located at ``index`` from the glyph.

            >>> contour = glyph[0]

        The returned value will be a :class:`BaseContour` object.
        """
        index = normalizers.normalizeIndex(index)
        if index >= len(self):
            raise ValueError("No contour located at index %d." % index)
        contour = self._getContour(index)
        self._setGlyphInContour(contour)
        return contour

<<<<<<< HEAD
    def _getContour(self, index: int, **kwargs: Any) -> BaseContour:
=======
    def _getContour(self, index: int, **kwargs: Any) -> BaseContour:  # type: ignore[return]
>>>>>>> v1
        r"""Get the contour located at the given index from the native glyph.
=======
    def _getContour(self, index, **kwargs):
        """
        This must return a wrapped contour.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        index will be a valid index.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _getContourIndex(self, contour):
        for i, other in enumerate(self.contours):
            if contour == other:
                return i
        raise FontPartsError("The contour could not be found.")

<<<<<<< HEAD
    def appendContour(self,
                      contour: BaseContour,
<<<<<<< HEAD
                      offset: CoordinateType = None) -> BaseContour:
=======
                      offset: Optional[CoordinateType] = None) -> BaseContour:
>>>>>>> v1
        """Append the given contour's data to the glyph.
=======
    def appendContour(self, contour, offset=None):
        """
        Append a contour containing the same data as ``contour``
        to this glyph.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

            >>> contour = glyph.appendContour(contour)

        This will return a :class:`BaseContour` object representing
        the new contour in the glyph. ``offset`` indicates the x and
        y shift values that should be applied to the appended data.
        It must be a :ref:`type-coordinate` value or ``None``. If
        ``None`` is given, the offset will be ``(0, 0)``.

            >>> contour = glyph.appendContour(contour, (100, 0))
        """
        normalizedContour = normalizers.normalizeContour(contour)
        if offset is None:
            offset = (0, 0)
<<<<<<< HEAD
        offset = normalizers.normalizeTransformationOffset(offset)
        return self._appendContour(contour, offset)
<<<<<<< HEAD
=======
        normalizedOffset = normalizers.normalizeTransformationOffset(offset)
        return self._appendContour(normalizedContour, normalizedOffset)
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea

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
=======

    def _appendContour(self, contour, offset=None, **kwargs):
        """
        contour will be an object with a drawPoints method.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        offset will be a valid offset (x, y).

        This must return the new contour.

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

    def removeContour(self, contour):
        """
        Remove ``contour`` from the glyph.

            >>> glyph.removeContour(contour)

        ``contour`` may be a :ref:`BaseContour` or an :ref:`type-int`
        representing a contour index.
        """
        if isinstance(contour, int):
            index = contour
        else:
            index = self._getContourIndex(contour)
        index = normalizers.normalizeIndex(index)
        if index >= len(self):
            raise ValueError("No contour located at index %d." % index)
        self._removeContour(index)

    def _removeContour(self, index, **kwargs):
        """
        index will be a valid index.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def clearContours(self):
        """
        Clear all contours in the glyph.

            >>> glyph.clearContours()
        """
        self._clearContours()

    def _clearContours(self):
        """
        Subclasses may override this method.
        """
        for _ in range(len(self)):
            self.removeContour(-1)

    def removeOverlap(self):
        """
        Perform a remove overlap operation on the contours.

            >>> glyph.removeOverlap()

        The behavior of this may vary across environments.
        """
        self._removeOverlap()

    def _removeOverlap(self):
        """
        Subclasses must implement this method.
        """
        self.raiseNotImplementedError()

    # Components

    def _setGlyphInComponent(self, component):
        if component.glyph is None:
            component.glyph = self

    components = dynamicProperty(
        "components",
<<<<<<< HEAD
        """Get all components in the glyph.

<<<<<<< HEAD
=======
        This property is read-only.

>>>>>>> v1
        :return: A :class:`tuple` of :class:`BaseComponent` instances.

        Example::
=======
        """
        An :ref:`type-immutable-list` of all components in the glyph.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

            >>> components = glyph.components

        The list will contain :class:`BaseComponent` objects.
        """
    )

    def _get_components(self):
        """
        Subclasses may override this method.
        """
        return tuple([self._getitem__components(i) for
                     i in range(self._len__components())])

    def _len__components(self):
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
=======
    def _lenComponents(self, **kwargs):
        """
        This must return an integer indicating
        the number of components in the glyph.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _getitem__components(self, index):
        index = normalizers.normalizeIndex(index)
        if index >= self._len__components():
            raise ValueError("No component located at index %d." % index)
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
=======
    def _getComponent(self, index, **kwargs):
        """
        This must return a wrapped component.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        index will be a valid index.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _getComponentIndex(self, component):
        for i, other in enumerate(self.components):
            if component == other:
                return i
        raise FontPartsError("The component could not be found.")

    def appendComponent(self, baseGlyph=None, offset=None, scale=None, component=None):
        """
        Append a component to this glyph.

            >>> component = glyph.appendComponent("A")

        This will return a :class:`BaseComponent` object representing
        the new component in the glyph. ``offset`` indicates the x and
        y shift values that should be applied to the appended component.
        It must be a :ref:`type-coordinate` value or ``None``. If
        ``None`` is given, the offset will be ``(0, 0)``.

            >>> component = glyph.appendComponent("A", offset=(10, 20))

        ``scale`` indicates the x and y scale values that should be
        applied to the appended component. It must be a
        :ref:`type-scale` value or ``None``. If ``None`` is given,
        the scale will be ``(1.0, 1.0)``.

            >>> component = glyph.appendComponent("A", scale=(1.0, 2.0))

        ``component`` may be a :class:`BaseComponent` object from which
        attribute values will be copied. If ``baseGlyph``, ``offset``
        or ``scale`` are specified as arguments, those values will be used
        instead of the values in the given component object.
        """
        identifier = None
        sxy = 0
        syx = 0
        if component is not None:
            component = normalizers.normalizeComponent(component)
            if baseGlyph is None:
                baseGlyph = component.baseGlyph
            sx, sxy, syx, sy, ox, oy = component.transformation
            if offset is None:
                offset = (ox, oy)
            if scale is None:
                scale = (sx, sy)
            if baseGlyph is None:
<<<<<<< HEAD
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
=======
                baseGlyph = component.baseGlyph
            if component.identifier is not None:
                existing = set([c.identifier for c in self.components if c.identifier is not None])
                if component.identifier not in existing:
                    identifier = component.identifier
        baseGlyph = normalizers.normalizeGlyphName(baseGlyph)
        if self.name == baseGlyph:
            raise FontPartsError(("A glyph cannot contain a component referencing itself."))
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        if offset is None:
            offset = (0, 0)
        if scale is None:
            scale = (1, 1)
        offset = normalizers.normalizeTransformationOffset(offset)
        scale = normalizers.normalizeTransformationScale(scale)
        ox, oy = offset
        sx, sy = scale
        transformation = (sx, sxy, syx, sy, ox, oy)
<<<<<<< HEAD
        identifier = normalizers.normalizeIdentifier(identifier)
<<<<<<< HEAD
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
=======
        return self._appendComponent(baseGlyph, transformation=transformation, identifier=identifier)

    def _appendComponent(self, baseGlyph, transformation=None, identifier=None, **kwargs):
        """
        baseGlyph will be a valid glyph name.
        The baseGlyph may or may not be in the layer.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        offset will be a valid offset (x, y).
        scale will be a valid scale (x, y).
        identifier will be a valid, nonconflicting identifier.

        This must return the new component.

        Subclasses may override this method.
        """
        pointPen = self.getPointPen()
        pointPen.addComponent(baseGlyph, transformation=transformation, identifier=identifier)
        return self.components[-1]

    def removeComponent(self, component):
        """
        Remove ``component`` from the glyph.

            >>> glyph.removeComponent(component)

        ``component`` may be a :ref:`BaseComponent` or an
        :ref:`type-int` representing a component index.
        """
        if isinstance(component, int):
            index = component
        else:
            index = self._getComponentIndex(component)
        index = normalizers.normalizeIndex(index)
        if index >= self._len__components():
            raise ValueError("No component located at index %d." % index)
        self._removeComponent(index)

    def _removeComponent(self, index, **kwargs):
        """
        index will be a valid index.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def clearComponents(self):
        """
        Clear all components in the glyph.

            >>> glyph.clearComponents()
        """
        self._clearComponents()

    def _clearComponents(self):
        """
        Subclasses may override this method.
        """
        for _ in range(self._len__components()):
            self.removeComponent(-1)

    def decompose(self):
        """
        Decompose all components in the glyph to contours.

            >>> glyph.decompose()
        """
        self._decompose()

    def _decompose(self):
        """
        Subclasses may override this method.
        """
        for component in self.components:
            component.decompose()

    # Anchors

    def _setGlyphInAnchor(self, anchor):
        if anchor.glyph is None:
            anchor.glyph = self

    anchors = dynamicProperty(
        "anchors",
<<<<<<< HEAD
        """Get all anchors in the glyph.

<<<<<<< HEAD
=======
        This property is read-only.

>>>>>>> v1
        :return: A :class:`tuple` of :class:`BaseAnthor` instances.

        Example::
=======
        """
        An :ref:`type-immutable-list` of all anchors in the glyph.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

            >>> anchors = glyph.anchors

        The list will contain :class:`BaseAnchor` objects.
        """
    )

    def _get_anchors(self):
        """
        Subclasses may override this method.
        """
<<<<<<< HEAD
        return tuple([self._getitem__anchors(i) for
<<<<<<< HEAD
                      i in range(self._len__anchors())])
=======
<<<<<<< HEAD
                     i in range(self._len__anchors())])
>>>>>>> parent of 3d67a1d (Update documentation (#739))
=======
        return tuple(self._getitem__anchors(i) for
                      i in range(self._len__anchors()))
>>>>>>> v1
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea

    def _len__anchors(self):
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
=======
    def _lenAnchors(self, **kwargs):
        """
        This must return an integer indicating
        the number of anchors in the glyph.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _getitem__anchors(self, index):
        index = normalizers.normalizeIndex(index)
        if index >= self._len__anchors():
            raise ValueError("No anchor located at index %d." % index)
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
=======
    def _getAnchor(self, index, **kwargs):
        """
        This must return a wrapped anchor.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        index will be a valid index.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _getAnchorIndex(self, anchor):
        for i, other in enumerate(self.anchors):
            if anchor == other:
                return i
        raise FontPartsError("The anchor could not be found.")

<<<<<<< HEAD
    def appendAnchor(self, name=None, position=None, color=None, anchor=None):
        """
        Append an anchor to this glyph.
=======
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
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea

            >>> anchor = glyph.appendAnchor("top", (10, 20))

        This will return a :class:`BaseAnchor` object representing
        the new anchor in the glyph. ``name`` indicated the name to
        be assigned to the anchor. It must be a :ref:`type-string`
        or ``None``. ``position`` indicates the x and y location
        to be applied to the anchor. It must be a
        :ref:`type-coordinate` value. ``color`` indicates the color
        to be applied to the anchor. It must be a :ref:`type-color`
        or ``None``.

<<<<<<< HEAD
=======
>>>>>>> v1
            >>> anchor = glyph.appendAnchor("top", (10, 20))
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
            >>> anchor = glyph.appendAnchor("top", (10, 20), color=(1, 0, 0, 1))

        ``anchor`` may be a :class:`BaseAnchor` object from which
        attribute values will be copied. If ``name``, ``position``
        or ``color`` are specified as arguments, those values will
        be used instead of the values in the given anchor object.
        """
        identifier = None
        if anchor is not None:
            anchor = normalizers.normalizeAnchor(anchor)
            if name is None:
                name = anchor.name
            if position is None:
                position = anchor.position
            if color is None:
<<<<<<< HEAD
                color = normalizedAnchor.color
            if normalizedAnchor.identifier is not None:
<<<<<<< HEAD
                existing = set([a.identifier for a in self.anchors
                                if a.identifier is not None])
                if normalizedAnchor.identifier not in existing:
                    identifier = normalizedAnchor.identifier
=======
                color = anchor.color
            if anchor.identifier is not None:
                existing = set([a.identifier for a in self.anchors if a.identifier is not None])
                if anchor.identifier not in existing:
                    identifier = anchor.identifier
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        name = normalizers.normalizeAnchorName(name)
        position = normalizers.normalizeCoordinateTuple(position)
        if color is not None:
            color = normalizers.normalizeColor(color)
        identifier = normalizers.normalizeIdentifier(identifier)
<<<<<<< HEAD
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
        return self._appendAnchor(name, position=position, color=color, identifier=identifier)

<<<<<<< HEAD
    def _appendAnchor(self, name, position=None, color=None, identifier=None, **kwargs):
=======
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

>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
        """
        name will be a valid anchor name.
        position will be a valid position (x, y).
        color will be None or a valid color.
        identifier will be a valid, nonconflicting identifier.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        This must return the new anchor.

        Subclasses may override this method.
        """
        self.raiseNotImplementedError()

    def removeAnchor(self, anchor):
        """
        Remove ``anchor`` from the glyph.

            >>> glyph.removeAnchor(anchor)

        ``anchor`` may be an :ref:`BaseAnchor` or an
        :ref:`type-int` representing an anchor index.
        """
        if isinstance(anchor, int):
            index = anchor
        else:
            index = self._getAnchorIndex(anchor)
        index = normalizers.normalizeIndex(index)
        if index >= self._len__anchors():
            raise ValueError("No anchor located at index %d." % index)
        self._removeAnchor(index)

    def _removeAnchor(self, index, **kwargs):
        """
        index will be a valid index.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def clearAnchors(self):
        """
        Clear all anchors in the glyph.

            >>> glyph.clearAnchors()
        """
        self._clearAnchors()

    def _clearAnchors(self):
        """
        Subclasses may override this method.
        """
        for _ in range(self._len__anchors()):
            self.removeAnchor(-1)

    # ----------
    # Guidelines
    # ----------

    def _setGlyphInGuideline(self, guideline):
        if guideline.glyph is None:
            guideline.glyph = self

    guidelines = dynamicProperty(
        "guidelines",
<<<<<<< HEAD
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
<<<<<<< HEAD
=======
>>>>>>> v1
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
        """
        An :ref:`type-immutable-list` of all guidelines in the glyph.

            >>> guidelines = glyph.guidelines

        The list will contain :class:`BaseGuideline` objects.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
    )

    def _get_guidelines(self):
        """
<<<<<<< HEAD
        Subclasses may override this method.
        """
=======
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
<<<<<<< HEAD
        return tuple([self._getitem__guidelines(i)
                      for i in range(self._len__guidelines())])
=======
<<<<<<< HEAD
        return tuple([self._getitem__guidelines(i) for
                     i in range(self._len__guidelines())])
>>>>>>> parent of 3d67a1d (Update documentation (#739))
=======
        return tuple(self._getitem__guidelines(i)
                      for i in range(self._len__guidelines()))
>>>>>>> v1
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea

    def _len__guidelines(self):
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
=======
    def _lenGuidelines(self, **kwargs):
        """
        This must return an integer indicating
        the number of guidelines in the glyph.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _getitem__guidelines(self, index):
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
=======
    def _getGuideline(self, index, **kwargs):
        """
        This must return a wrapped guideline.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        index will be a valid index.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _getGuidelineIndex(self, guideline):
        for i, other in enumerate(self.guidelines):
            if guideline == other:
                return i
        raise FontPartsError("The guideline could not be found.")

    def appendGuideline(self, position=None, angle=None, name=None, color=None, guideline=None):
        """
        Append a guideline to this glyph.

            >>> guideline = glyph.appendGuideline((100, 0), 90)

        This will return a :class:`BaseGuideline` object representing
        the new guideline in the glyph. ``position`` indicates the
        x and y location to be used as the center point of the anchor.
        It must be a :ref:`type-coordinate` value. ``angle`` indicates
        the angle of the guideline, in degrees. This must be a
        :ref:`type-int-float` between 0 and 360. ``name`` indicates
        an name to be assigned to the guideline. It must be a
        :ref:`type-string` or ``None``.

            >>> guideline = glyph.appendGuideline((100, 0), 90, name="left")

        ``color`` indicates the color to be applied to the guideline.
        It must be a :ref:`type-color` or ``None``.

            >>> guideline = glyph.appendGuideline((100, 0), 90, color=(1, 0, 0, 1))

        ``guideline`` may be a :class:`BaseGuideline` object from which
        attribute values will be copied. If ``position``, ``angle``, ``name``
        or ``color`` are specified as arguments, those values will be used
        instead of the values in the given guideline object.
        """
        identifier = None
        if guideline is not None:
            guideline = normalizers.normalizeGuideline(guideline)
            if position is None:
                position = guideline.position
            if angle is None:
                angle = guideline.angle
            if name is None:
                name = guideline.name
            if color is None:
<<<<<<< HEAD
                color = normalizedGuideline.color
            if normalizedGuideline.identifier is not None:
                existing = set([g.identifier for g in self.guidelines
                                if g.identifier is not None])
                if normalizedGuideline.identifier not in existing:
                    identifier = normalizedGuideline.identifier
<<<<<<< HEAD
=======
                color = guideline.color
            if guideline.identifier is not None:
                existing = set([g.identifier for g in self.guidelines if g.identifier is not None])
                if guideline.identifier not in existing:
                    identifier = guideline.identifier
>>>>>>> parent of 3d67a1d (Update documentation (#739))
=======
<<<<<<< HEAD
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
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
<<<<<<< HEAD
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
=======
        guideline = self._appendGuideline(position, angle, name=name, color=color, identifier=identifier)
        guideline.glyph = self
        return guideline
>>>>>>> parent of 3d67a1d (Update documentation (#739))

    def _appendGuideline(self, position, angle, name=None, color=None, identifier=None, **kwargs):
        """
        position will be a valid position (x, y).
        angle will be a valid angle.
        name will be a valid guideline name or None.
        color will be a valid color or None .
        identifier will be a valid, nonconflicting identifier.

        This must return the new guideline.

        Subclasses may override this method.
        """
        self.raiseNotImplementedError()

    def removeGuideline(self, guideline):
        """
        Remove ``guideline`` from the glyph.

            >>> glyph.removeGuideline(guideline)

        ``guideline`` may be a :ref:`BaseGuideline` or an
        :ref:`type-int` representing an guideline index.
        """
        if isinstance(guideline, int):
            index = guideline
        else:
            index = self._getGuidelineIndex(guideline)
        index = normalizers.normalizeIndex(index)
        if index >= self._len__guidelines():
            raise ValueError("No guideline located at index %d." % index)
        self._removeGuideline(index)

    def _removeGuideline(self, index, **kwargs):
        """
        index will be a valid index.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def clearGuidelines(self):
        """
        Clear all guidelines in the glyph.

            >>> glyph.clearGuidelines()
        """
        self._clearGuidelines()

    def _clearGuidelines(self):
        """
        Subclasses may override this method.
        """
        for _ in range(self._len__guidelines()):
            self.removeGuideline(-1)

    # ------------------
    # Data Normalization
    # ------------------

<<<<<<< HEAD
    def round(self):
        """
        Round coordinates to the nearest integer.
=======
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
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea

            >>> glyph.round()

        This applies to the following:

        - width
        - height
        - contours
        - components
        - anchors
        - guidelines
        """
        self._round()

    def _round(self):
        """
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

    def correctDirection(self, trueType=False):
        """
        Correct the winding direction of the contours following
        the PostScript recommendations.

            >>> glyph.correctDirection()

        If ``trueType`` is ``True`` the TrueType recommendations
        will be followed.
        """
        self._correctDirection(trueType=trueType)

    def _correctDirection(self, trueType=False, **kwargs):
        """
        Subclasses may override this method.
        """
        self.raiseNotImplementedError()

    def autoContourOrder(self):
        """
        Automatically order the contours based on heuristics.

            >>> glyph.autoContourOrder()

        The results of this may vary across environments.
        """
        self._autoContourOrder()

    def _autoContourOrder(self, **kwargs):
        """
        Sorting is based on (in this order):
        - the (negative) point count
        - the (negative) segment count
        - x value of the center of the contour rounded to a threshold
        - y value of the center of the contour rounded to a threshold
          (such threshold is calculated as the smallest contour width
          or height in the glyph divided by two)
<<<<<<< HEAD
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
<<<<<<< HEAD
        - the (negative) surface of the bounding box of the contour: width * height
        the latter is a safety net for for instances like a very thin 'O' where the
        x centers could be close enough to rely on the y for the sort which could
        very well be the same for both contours. We use the _negative_ of the surface
        to ensure that larger contours appear first, which seems more natural.
        """
        tempContourList = []
        contourList = []
        xThreshold = None
        yThreshold = None
>>>>>>> parent of 3d67a1d (Update documentation (#739))
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
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea

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
<<<<<<< HEAD
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
            tempContourList.append((-len(contour.points), -len(contour.segments), xC, yC, -(width * height), contour))
>>>>>>> parent of 3d67a1d (Update documentation (#739))
=======
<<<<<<< HEAD
=======

        xThreshold = xThreshold or 0.0
        yThreshold = yThreshold or 0.0
>>>>>>> v1
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea

        for points, segments, x, y, surface, contour in tempContourList:
            contourList.append((points, segments, FuzzyNumber(x, xThreshold), FuzzyNumber(y, yThreshold), surface, contour))
        contourList.sort()

        self.clearContours()
        for points, segments, xO, yO, surface, contour in contourList:
            self.appendContour(contour)

    # --------------
    # Transformation
    # --------------

<<<<<<< HEAD
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

=======
    def _transformBy(self, matrix, **kwargs):
        """
        Subclasses may override this method.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        for contour in self.contours:
            contour.transformBy(matrix)
        for component in self.components:
            component.transformBy(matrix)
        for anchor in self.anchors:
            anchor.transformBy(matrix)
        for guideline in self.guidelines:
            guideline.transformBy(matrix)

<<<<<<< HEAD
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
=======
    def scaleBy(self, value, origin=None, width=False, height=False):
        """
        %s
        **width** indicates if the glyph's width should be scaled.
        **height** indicates if the glyph's height should be scaled.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        The origin must not be specified when scaling the width or height.
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

    scaleBy.__doc__ %= TransformationMixin.scaleBy.__doc__

    def _scaleWidthBy(self, value):
        """
        Subclasses may override this method.
        """
        self.width *= value

    def _scaleHeightBy(self, value):
        """
        Subclasses may override this method.
        """
        self.height *= value

    # --------------------
    # Interpolation & Math
    # --------------------

    def toMathGlyph(self, scaleComponentTransform=True, strict=False):
        """
        Returns the glyph as an object that follows the
        `MathGlyph protocol <https://github.com/typesupply/fontMath>`_.

            >>> mg = glyph.toMathGlyph()

        **scaleComponentTransform** Enables the MathGlyph
          `scaleComponentTransform` option.
        **strict**  Enables the MathGlyph `strict` option.
        """
<<<<<<< HEAD
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
=======
        return self._toMathGlyph(scaleComponentTransform=scaleComponentTransform, strict=strict)
>>>>>>> parent of 3d67a1d (Update documentation (#739))

    def _toMathGlyph(self, scaleComponentTransform=True, strict=False):
        """
        Subclasses may override this method.
        """
        import fontMath
        mathGlyph = fontMath.MathGlyph(
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

<<<<<<< HEAD
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
<<<<<<< HEAD
    def fromMathGlyph(self, mathGlyph, filterRedundantPoints=True):
        """
        Replaces the contents of this glyph with the contents of ``mathGlyph``.

            >>> glyph.fromMathGlyph(mg)
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
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea

        ``mathGlyph`` must be an object following the
        `MathGlyph protocol <https://github.com/typesupply/fontMath>`_.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        **filterRedundantPoints** enables the MathGlyph `drawPoints`
          `filterRedundantPoints` option.
        """
        return self._fromMathGlyph(mathGlyph, toThisGlyph=True, filterRedundantPoints=filterRedundantPoints)

    def _fromMathGlyph(self, mathGlyph, toThisGlyph=False, filterRedundantPoints=True):
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
        mathGlyph.drawPoints(pen, filterRedundantPoints=filterRedundantPoints)
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

    def __mul__(self, factor):
        """
<<<<<<< HEAD
=======
        Subclasses may override this method.
        """
<<<<<<< HEAD
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        mathGlyph = self._toMathGlyph()
=======
        mathGlyph = self._toMathGlyph(scaleComponentTransform=True, strict=False)
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
        result = mathGlyph * factor
        copied = self._fromMathGlyph(result,
            toThisGlyph=False,
            filterRedundantPoints=True)
        return copied

    __rmul__ = __mul__

    def __truediv__(self, factor):
        """
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

    def __add__(self, other):
        """
<<<<<<< HEAD
<<<<<<< HEAD
=======
        Subclasses may override this method.
        """
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        selfMathGlyph = self._toMathGlyph()
        otherMathGlyph = other._toMathGlyph()
=======
        selfMathGlyph = self._toMathGlyph(scaleComponentTransform=True, strict=False)
        otherMathGlyph = other._toMathGlyph(scaleComponentTransform=True, strict=False)
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
        result = selfMathGlyph + otherMathGlyph
        copied = self._fromMathGlyph(result,
            toThisGlyph=False,
        filterRedundantPoints=True)
        return copied

<<<<<<< HEAD
    def __sub__(self, other):
=======
    def __sub__(self, other: BaseGlyph) -> BaseGlyph:
        """Subtract another glyph from the current glyph.
<<<<<<< HEAD

        :param other: The :class:`BaseGLyph` instance to subtract
            from the current glyph.
        :return: A new :class:`BaseGlyph` instance representing
            the subtracted results.

        .. note::

            Subclasses may override this method.

>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
        """
<<<<<<< HEAD

=======
        Subclasses may override this method.
        """
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        selfMathGlyph = self._toMathGlyph()
        otherMathGlyph = other._toMathGlyph()
        result = selfMathGlyph - otherMathGlyph
        copied = self._fromMathGlyph(result)
        return copied

    def interpolate(self, factor, minGlyph, maxGlyph,
                    round=True, suppressError=True):
        """
        Interpolate the contents of this glyph at location ``factor``
        in a linear interpolation between ``minGlyph`` and ``maxGlyph``.

            >>> glyph.interpolate(0.5, otherGlyph1, otherGlyph2)

        ``factor`` may be a :ref:`type-int-float` or a tuple containing
        two :ref:`type-int-float` values representing x and y factors.

            >>> glyph.interpolate((0.5, 1.0), otherGlyph1, otherGlyph2)

<<<<<<< HEAD
        ``minGlyph`` must be a :class:`BaseGlyph` and will be located at 0.0
        in the interpolation range. ``maxGlyph`` must be a :class:`BaseGlyph`
        and will be located at 1.0 in the interpolation range. If ``round``
        is ``True``, the contents of the glyph will be rounded to integers
        after the interpolation is performed.

            >>> glyph.interpolate(0.5, otherGlyph1, otherGlyph2, round=True)

        This method assumes that ``minGlyph`` and ``maxGlyph`` are completely
        compatible with each other for interpolation. If not, any errors
        encountered will raise a :class:`FontPartsError`. If ``suppressError``
        is ``True``, no exception will be raised and errors will be silently
        ignored.
=======
=======

        :param other: The :class:`BaseGLyph` instance to subtract
            from the current glyph.
        :return: A new :class:`BaseGlyph` instance representing
            the subtracted results.

        .. note::

            Subclasses may override this method.

>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
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

<<<<<<< HEAD
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

=======
    def _interpolate(self, factor, minGlyph, maxGlyph,
                     round=True, suppressError=True):
        """
        Subclasses may override this method.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        from fontMath.mathFunctions import setRoundIntegerFunction

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
    def _checkPairs(object1, object2, reporter, reporterObject):
        compatibility = object1.isCompatible(object2)[1]
        if compatibility.fatal or compatibility.warning:
            if compatibility.fatal:
                reporter.fatal = True
            if compatibility.warning:
                reporter.warning = True
            reporterObject.append(compatibility)

    def isCompatible(self, other):
        """
        Evaluate the interpolation compatibility of this glyph
        and ``other``.

            >>> compatible, report = self.isCompatible(otherGlyph)
            >>> compatible
            False

        This will return a :ref:`type-bool` indicating if this glyph is
        compatible with ``other`` and a :class:`GlyphCompatibilityReporter`
        containing a detailed report about compatibility errors.
        """
        return super(BaseGlyph, self).isCompatible(other, BaseGlyph)

    def _isCompatible(self, other, reporter):
        """
        This is the environment implementation of
        :meth:`BaseGlyph.isCompatible`.

        Subclasses may override this method.
        """
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
        component_diff = []
        selfComponents = [component.baseGlyph for component in glyph1.components]
        otherComponents = [component.baseGlyph for component in glyph2.components]
        for index, (left, right) in enumerate(
            zip_longest(selfComponents, otherComponents)
        ):
            if left != right:
                component_diff.append((index, left, right))

        if component_diff:
            reporter.warning = True
            reporter.componentDifferences = component_diff
            if not reporter.componentCountDifference and set(selfComponents) == set(
                otherComponents
            ):
                reporter.componentOrderDifference = True

            selfComponents_counted_set = collections.Counter(selfComponents)
            otherComponents_counted_set = collections.Counter(otherComponents)
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
        selfGuidelines = []
        otherGuidelines = []
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
        anchor_diff = []
        selfAnchors = [anchor.name for anchor in glyph1.anchors]
        otherAnchors = [anchor.name for anchor in glyph2.anchors]
        for index, (left, right) in enumerate(zip_longest(selfAnchors, otherAnchors)):
            if left != right:
                anchor_diff.append((index, left, right))

        if anchor_diff:
            reporter.warning = True
            reporter.anchorDifferences = anchor_diff
            if not reporter.anchorCountDifference and set(selfAnchors) == set(
                otherAnchors
            ):
                reporter.anchorOrderDifference = True

            selfAnchors_counted_set = collections.Counter(selfAnchors)
            otherAnchors_counted_set = collections.Counter(otherAnchors)
            missing_from_glyph1 = otherAnchors_counted_set - selfAnchors_counted_set
            if missing_from_glyph1:
                reporter.anchorsMissingFromGlyph1 = sorted(
                    missing_from_glyph1.elements()
                )
            missing_from_glyph2 = selfAnchors_counted_set - otherAnchors_counted_set
            if missing_from_glyph2:
                reporter.anchorsMissingFromGlyph2 = sorted(
                    missing_from_glyph2.elements()
                )

    # ------------
    # Data Queries
    # ------------

    def pointInside(self, point):
        """
        Determine if ``point`` is in the black or white of the glyph.

            >>> glyph.pointInside((40, 65))
            True

        ``point`` must be a :ref:`type-coordinate`.
        """
        point = normalizers.normalizeCoordinateTuple(point)
        return self._pointInside(point)

    def _pointInside(self, point):
        """
        Subclasses may override this method.
        """
        from fontTools.pens.pointInsidePen import PointInsidePen
        pen = PointInsidePen(glyphSet=None, testPoint=point, evenOdd=False)
        self.draw(pen)
        return pen.getResult()

    bounds = dynamicProperty(
        "bounds",
<<<<<<< HEAD
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
=======
        """
        The bounds of the glyph in the form
        ``(x minimum, y minimum, x maximum, y maximum)`` or,
        in the case of empty glyphs ``None``.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

            >>> glyph.bounds
            (10, 30, 765, 643)
        """
    )

    def _get_base_bounds(self):
        value = self._get_bounds()
        if value is not None:
            value = normalizers.normalizeBoundingBox(value)
        return value

    def _get_bounds(self):
        """
        Subclasses may override this method.
        """
        from fontTools.pens.boundsPen import BoundsPen
        pen = BoundsPen(self.layer)
        self.draw(pen)
        return pen.bounds

    area = dynamicProperty(
        "area",
<<<<<<< HEAD
        """Get the area of the glyph

<<<<<<< HEAD
=======
        This property is read-only.

>>>>>>> v1
        :return: An :class:`int` or a :class:` float value representing the
            area of the glyph, or or :obj:`None` if the glyph is empty.

        Example::
=======
        """
        The area of the glyph as a :ref:`type-int-float` or,
        in the case of empty glyphs ``None``.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

            >>> glyph.area
            583
        """
    )

    def _get_base_area(self):
        value = self._get_area()
        if value is not None:
            value = normalizers.normalizeArea(value)
        return value

    def _get_area(self):
        """
        Subclasses may override this method.
        """
        from fontTools.pens.areaPen import AreaPen
        pen = AreaPen(self.layer)
        self.draw(pen)
        return abs(pen.value)

    # -----------------
    # Layer Interaction
    # -----------------

    layers = dynamicProperty(
        "layers",
<<<<<<< HEAD
        """Get the layers of the glyph.

<<<<<<< HEAD
=======
        This property is read-only.

>>>>>>> v1
        :return: A :class:`tuple` of the :class:`BaseLayer` instances belonging
            to the glyph.

        Example::
=======
        """
        Immutable tuple of the glyph's layers.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

            >>> glyphLayers = glyph.layers

        This will return a tuple of all :ref:`type-glyph-layer` in the glyph.
        """
    )

    def _get_layers(self, **kwargs):
        font = self.font
        if font is None:
            return tuple()
        glyphs = []
        for layer in font.layers:
            if self.name in layer:
                glyphs.append(layer[self.name])
        return tuple(glyphs)

    # get

    def getLayer(self, name):
        """
        Get the :ref:`type-glyph-layer` with ``name`` in this glyph.

            >>> glyphLayer = glyph.getLayer("foreground")
        """
        name = normalizers.normalizeLayerName(name)
        return self._getLayer(name)

    def _getLayer(self, name, **kwargs):
        """
        name will be a string, but there may not be a
        layer with a name matching the string. If not,
        a ``ValueError`` must be raised.

        Subclasses may override this method.
        """
        for glyph in self.layers:
            if glyph.layer.name == name:
                return glyph
        raise ValueError("No layer named '%s' in glyph '%s'."
                         % (name, self.name))

    # new

    def newLayer(self, name):
        """
        Make a new layer with ``name`` in this glyph.

            >>> glyphLayer = glyph.newLayer("background")

        This will return the new :ref:`type-glyph-layer`.
        If the layer already exists in this glyph, it
        will be cleared.
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
        # layer._setLayerInGlyph(glyph)
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
=======
    def _newLayer(self, name, **kwargs):
        """
        name will be a string representing a valid layer
        name. The name will have been tested to make sure
        that no layer in the glyph already has the name.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        This must returned the new glyph.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # remove

    def removeLayer(self, layer):
        """
        Remove ``layer`` from this glyph.

            >>> glyph.removeLayer("background")

        Layer can be a :ref:`type-glyph-layer` or a :ref:`type-string`
        representing a layer name.
        """
        if isinstance(layer, BaseGlyph):
            layer = layer.layer.name
        layerName = layer
<<<<<<< HEAD
        layerName = normalizers.normalizeLayerName(layerName)
        if self._getLayer(layerName).layer.name == layerName:
            self._removeLayer(layerName)
<<<<<<< HEAD
=======
        normalizedLayerName = normalizers.normalizeLayerName(layerName)
        if self._getLayer(normalizedLayerName).layer.name == normalizedLayerName:
            self._removeLayer(normalizedLayerName)
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea

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
=======
>>>>>>> parent of 3d67a1d (Update documentation (#739))

    def _removeLayer(self, name, **kwargs):
        """
        name will be a valid layer name. It will
        represent an existing layer in the font.

        Subclasses may override this method.
        """
        self.raiseNotImplementedError()

    # -----
    # Image
    # -----

    image = dynamicProperty(
        "base_image",
<<<<<<< HEAD
        """Get the image for the glyph.

<<<<<<< HEAD
=======
        This property is read-only.

>>>>>>> v1
        :return: The :class:`BaseImage` instance belonging to the glyph.

        """
=======
        "The :class:`BaseImage` for the glyph."
>>>>>>> parent of 3d67a1d (Update documentation (#739))
    )

    def _get_base_image(self):
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
=======
    def _get_image(self):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def addImage(self, path=None, data=None, scale=None,
                 position=None, color=None):
        """
        Set the image in the glyph. This will return the
        assigned :class:`BaseImage`. The image data can be
        defined via ``path`` to an image file:
>>>>>>> parent of 3d67a1d (Update documentation (#739))

            >>> image = glyph.addImage(path="/path/to/my/image.png")

        The image data can be defined with raw image data
        via ``data``.

            >>> image = glyph.addImage(data=someImageData)

        If ``path`` and ``data`` are both provided, a
        :class:`FontPartsError` will be raised. The supported
        image formats will vary across environments. Refer
        to :class:`BaseImage` for complete details.

        ``scale`` indicates the x and y scale values that should be
        applied to the image. It must be a :ref:`type-scale` value
        or ``None``.

            >>> image = glyph.addImage(path="/p/t/image.png", scale=(0.5, 1.0))

        ``position`` indicates the x and y location of the lower left
        point of the image.

            >>> image = glyph.addImage(path="/p/t/image.png", position=(10, 20))

        ``color`` indicates the color to be applied to the image. It must
        be a :ref:`type-color` or ``None``.

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
<<<<<<< HEAD
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

=======
            f = open(path, "rb")
            data = f.read()
            f.close()
        self._addImage(data=data, transformation=transformation, color=color)
        return self.image

    def _addImage(self, data, transformation=None, color=None):
        """
        data will be raw, unnormalized image data.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        Each environment may have different possible
        formats, so this is unspecified.

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
=======
        transformation will be a valid transformation matrix.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        color will be a color tuple or None.

        This must return an Image object. Assigning it
        to the glyph will be handled by the base class.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def clearImage(self):
        """
        Remove the image from the glyph.

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

=======
    def _clearImage(self, **kwargs):
        """
        Subclasses must override this method.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        self.raiseNotImplementedError()

    # ----------
    # Mark color
    # ----------

    markColor = dynamicProperty(
        "base_markColor",
        """
        The glyph's mark color.

            >>> glyph.markColor
            (1, 0, 0, 0.5)
            >>> glyph.markColor = None

        The value may be a :ref:`type-color` or ``None``.
        """
    )

    def _get_base_markColor(self):
        value = self._get_markColor()
        if value is None:
            return None
        normalizedValue = normalizers.normalizeColor(value)
        return Color(normalizedValue)

    def _set_base_markColor(self, value):
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
=======
    def _get_markColor(self):
        """
        Return the mark color value as a color tuple or None.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_markColor(self, value):
        """
        value will be a color tuple or None.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # ----
    # Note
    # ----

    note = dynamicProperty(
        "base_note",
        """
        The glyph's note.

            >>> glyph.note
            "P.B. said this looks 'awesome.'"
            >>> glyph.note = "P.B. said this looks 'AWESOME.'"

        The value may be a :ref:`type-string` or ``None``.
        """
    )

    def _get_base_note(self):
        value = self._get_note()
        if value is not None:
            value = normalizers.normalizeGlyphNote(value)
        return value

    def _set_base_note(self, value):
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

=======
    def _get_note(self):
        """
        Subclasses must override this method.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        self.raiseNotImplementedError()

    def _set_note(self, value):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # ---
    # Lib
    # ---

    lib = dynamicProperty(
        "base_lib",
<<<<<<< HEAD
        """Get the font's lib object.

<<<<<<< HEAD
=======
        This property is read-only.

>>>>>>> v1
        :return: An instance of the :class:`BaseLib` class.

        Example::
=======
        """
        The :class:`BaseLib` for the glyph.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

            >>> lib = glyph.lib
        """
    )

    def _get_base_lib(self):
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

=======
    def _get_lib(self):
        """
        Subclasses must override this method.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        self.raiseNotImplementedError()

    # --------
    # Temp Lib
    # --------

    tempLib = dynamicProperty(
        "base_tempLib",
<<<<<<< HEAD
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
=======
        """
        The :class:`BaseLib` for the glyph.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

            >>> tempLib = glyph.tempLib
        """
    )

    def _get_base_tempLib(self):
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

=======
    def _get_tempLib(self):
        """
        Subclasses must override this method.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        self.raiseNotImplementedError()

    # ---
    # API
    # ---

    def isEmpty(self):
        """
        This will return :ref:`type-bool` indicating if there are contours and/or
        components in the glyph.

            >>> glyph.isEmpty()

        Note: This method only checks for the presence of contours and components.
        Other attributes (guidelines, anchors, a lib, etc.) will not affect what
        this method returns.
        """
        if self.contours:
            return False
        if self.components:
            return False
        return True

    def loadFromGLIF(self, glifData):
        """
        Reads ``glifData``, in
        `GLIF format <http://unifiedfontobject.org/versions/ufo3/glyphs/glif/>`_,
        into this glyph.

            >>> glyph.readGlyphFromString(xmlData)
        """
        self._loadFromGLIF(glifData)

    def _loadFromGLIF(self, glifData):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def dumpToGLIF(self, glyphFormatVersion=2):
        """
        This will return the glyph's contents as a string in
        `GLIF format <http://unifiedfontobject.org/versions/ufo3/glyphs/glif/>`_.

            >>> xml = glyph.writeGlyphToString()

        ``glyphFormatVersion`` must be a :ref:`type-int` that defines
        the preferred GLIF format version.
        """
        glyphFormatVersion = normalizers.normalizeGlyphFormatVersion(
            glyphFormatVersion)
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

=======
    def _dumpToGLIF(self, glyphFormatVersion):
        """
        Subclasses must override this method.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        self.raiseNotImplementedError()

    # ---------
    # Selection
    # ---------

    # contours

    selectedContours = dynamicProperty(
        "base_selectedContours",
        """
        An :ref:`type-immutable-list` of contours selected in the glyph.

<<<<<<< HEAD
            >>> components = glyph.selectedContours
=======
<<<<<<< HEAD
            >>> contours = glyph.selectedContours:
>>>>>>> parent of 3d67a1d (Update documentation (#739))
=======
            >>> contours = glyph.selectedContours
>>>>>>> v1
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
            >>> glyph.selectedContours = otherContours

        It is possible to use a list of :ref:`type-int` representing
        contour indexes when setting the selected contours.

            >>> glyph.selectedContours = [0, 2]
        """
    )

<<<<<<< HEAD
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

=======
    def _get_base_selectedContours(self):
        selected = tuple([normalizers.normalizeContour(contour) for
                         contour in self._get_selectedContours()])
        return selected

    def _get_selectedContours(self):
        """
        Subclasses may override this method.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        return self._getSelectedSubObjects(self.contours)

    def _set_base_selectedContours(self, value):
        normalized = []
        for i in value:
            if isinstance(i, int):
                i = normalizers.normalizeIndex(i)
            else:
                i = normalizers.normalizeContour(i)
            normalized.append(i)
        self._set_selectedContours(normalized)

<<<<<<< HEAD
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

=======
    def _set_selectedContours(self, value):
        """
        Subclasses may override this method.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        return self._setSelectedSubObjects(self.contours, value)

    # components

    selectedComponents = dynamicProperty(
        "base_selectedComponents",
        """
        An :ref:`type-immutable-list` of components selected in the glyph.

            >>> components = glyph.selectedComponents:
            >>> glyph.selectedComponents = otherComponents

        It is possible to use a list of :ref:`type-int` representing
        component indexes when setting the selected components.

            >>> glyph.selectedComponents = [0, 2]
        """
    )

<<<<<<< HEAD
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

=======
    def _get_base_selectedComponents(self):
        selected = tuple([normalizers.normalizeComponent(component) for
                         component in self._get_selectedComponents()])
        return selected

    def _get_selectedComponents(self):
        """
        Subclasses may override this method.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        return self._getSelectedSubObjects(self.components)

    def _set_base_selectedComponents(self, value):
        normalized = []
        for i in value:
            if isinstance(i, int):
                i = normalizers.normalizeIndex(i)
            else:
                i = normalizers.normalizeComponent(i)
            normalized.append(i)
        self._set_selectedComponents(normalized)

<<<<<<< HEAD
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

=======
    def _set_selectedComponents(self, value):
        """
        Subclasses may override this method.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        return self._setSelectedSubObjects(self.components, value)

    # anchors

    selectedAnchors = dynamicProperty(
        "base_selectedAnchors",
        """
        An :ref:`type-immutable-list` of anchors selected in the glyph.

            >>> anchors = glyph.selectedAnchors:
            >>> glyph.selectedAnchors = otherAnchors

        It is possible to use a list of :ref:`type-int` representing
        anchor indexes when setting the selected anchors.

            >>> glyph.selectedAnchors = [0, 2]
        """
    )

<<<<<<< HEAD
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

=======
    def _get_base_selectedAnchors(self):
        selected = tuple([normalizers.normalizeAnchor(anchor) for
                         anchor in self._get_selectedAnchors()])
        return selected

    def _get_selectedAnchors(self):
        """
        Subclasses may override this method.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        return self._getSelectedSubObjects(self.anchors)

    def _set_base_selectedAnchors(self, value):
        normalized = []
        for i in value:
            if isinstance(i, int):
                i = normalizers.normalizeIndex(i)
            else:
                i = normalizers.normalizeAnchor(i)
            normalized.append(i)
        self._set_selectedAnchors(normalized)

<<<<<<< HEAD
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

=======
    def _set_selectedAnchors(self, value):
        """
        Subclasses may override this method.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        return self._setSelectedSubObjects(self.anchors, value)

    # guidelines

    selectedGuidelines = dynamicProperty(
        "base_selectedGuidelines",
        """
        An :ref:`type-immutable-list` of guidelines selected in the glyph.

            >>> guidelines = glyph.selectedGuidelines:
            >>> glyph.selectedGuidelines = otherGuidelines

        It is possible to use a list of :ref:`type-int` representing
        guidelines indexes when setting the selected guidelines.

            >>> glyph.selectedGuidelines = [0, 2]
        """
    )

<<<<<<< HEAD
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

=======
    def _get_base_selectedGuidelines(self):
        selected = tuple([normalizers.normalizeGuideline(guideline) for
                         guideline in self._get_selectedGuidelines()])
        return selected

    def _get_selectedGuidelines(self):
        """
        Subclasses may override this method.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        return self._getSelectedSubObjects(self.guidelines)

    def _set_base_selectedGuidelines(self, value):
        normalized = []
        for i in value:
            if isinstance(i, int):
                i = normalizers.normalizeIndex(i)
            else:
                i = normalizers.normalizeGuideline(i)
            normalized.append(i)
        self._set_selectedGuidelines(normalized)

<<<<<<< HEAD
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

=======
    def _set_selectedGuidelines(self, value):
        """
        Subclasses may override this method.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        return self._setSelectedSubObjects(self.guidelines, value)
