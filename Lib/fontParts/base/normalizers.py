# -*- coding: utf8 -*-

from fontTools.misc.py23 import unicode, basestring, round3
from fontParts.base.errors import FontPartsError

# ----
# Font
# ----

def normalizeFileFormatVersion(value):
    """
    Normalizes a font's file format version.

    * **value** must be a :ref:`type-int-float`.
    * Returned value will be a ``float``.
    """
    if not isinstance(value, (int, float)):
        raise FontPartsError("File format versions must be instances of :ref:`type-int-float`, not %s." % type(value).__name__)
    return value


def normalizeLayerOrder(value, font):
    """
    Normalizes layer order.

    * **value** must be a ``list``.
    * **value** must contain layers that exist in **font**.
    * **value** must not contain duplicate layers.
    * Returned ``list`` will be unencoded ``unicode`` strings for each layer name.
    """
    if not isinstance(value, list):
        raise FontPartsError("Layer order must be a list, not %s." % type(value).__name__)
    fontLayers = [layer.name for layer in font.layers]
    for name in value:
        if name not in fontLayers:
            raise FontPartsError("Layer must exist in font. %s does not exist in font.layers." % name)
    from collections import Counter
    duplicates = [v for v, count in Counter(value).items() if count > 1]
    if len(duplicates) != 0:
        raise FontPartsError("Duplicate layers are not allowed. Layer name(s) '%s' are duplicate(s)." % ", ".join(duplicates))
    return [unicode(v) for v in value]


def normalizeDefaultLayer(value, font):
    """
    Normalizes default layer.

    * **value** must be a :ref:`type-string`.
    * **value** must be a layer in **font**.
    * Returned value will be an unencoded ``unicode`` string.
    """
    if not isinstance(value, basestring):
        raise FontPartsError("Layer names must be strings, not %s." % type(value).__name__)
    if value not in font.layerOrder:
        raise FontPartsError("No layer with the name '%s' exists." % value)
    return unicode(value)


def normalizeGlyphOrder(value):
    """
    Normalizes glyph order.

    * **value** must be a ``list``.
    * **value** items must normalize as glyph names with :func:`normalizeGlyphName`.
    * **value** must not repeat glyph names.
    * Returned value will be a ``list`` of unencoded ``unicode`` strings.
    """
    if not isinstance(value, list):
        raise FontPartsError("Glyph order must be a list, not %s." % type(value).__name__)
    for v in value:
        normalizeGlyphName(v)
    from collections import Counter
    duplicates = sorted(v for v, count in Counter(value).items() if count > 1)
    if len(duplicates) != 0:
        raise FontPartsError("Duplicate glyph names are not allowed. Glyph name(s) '%s' are duplicate." % ", ".join(duplicates))
    return [unicode(v) for v in value]


# -------
# Kerning
# -------


def normalizeKerningKey(value):
    """
    Normalizes kerning key.

    * **value** must be a ``tuple`` or ``list``.
    * **value** must contain only two members.
    * **value** items must be :ref:`type-string`.
    * **value** items must be at least one character long.
    * Returned value will be a two member ``tuple`` of unencoded ``unicode`` strings.
    """
    if not isinstance(value, (tuple, list)):
        raise FontPartsError("Kerning key must be a tuple instance, not %s." % type(value).__name__)
    if len(value) != 2:
        raise FontPartsError("Kerning key must be a tuple containing two items, not %d." % len(value))
    for v in value:
        if not isinstance(v, basestring):
            raise FontPartsError("Kerning key items must be strings, not %s." % type(v).__name__)
        if len(v) < 1:
            raise FontPartsError("Kerning key items must be one character long")
    if value[0].startswith("public.") and not value[0].startswith("public.kern1."):
        raise FontPartsError("Left Kerning key group must start with public.kern1.")
    if value[1].startswith("public.") and not value[1].startswith("public.kern2."):
        raise FontPartsError("Right Kerning key group must start with public.kern2.")
    return tuple([unicode(v) for v in value])


def normalizeKerningValue(value):
    """
    Normalizes kerning value.

    * **value** must be an :ref:`type-int-float`.
    * Returned value is the same type as input value.
    """
    if not isinstance(value, (int, float)):
        raise FontPartsError("Kerning value must be a int or a float, not %s." % type(value).__name__)
    return value


# ------
# Groups
# ------

def normalizeGroupKey(value):
    """
    Normalizes group key.

    * **value** must be a :ref:`type-string`.
    * **value** must be least one character long.
    * Returned value will be an unencoded ``unicode`` string.
    """
    if not isinstance(value, basestring):
        raise FontPartsError("Group key must be a string, not %s." % type(value).__name__)
    if len(value) < 1:
        raise FontPartsError("Group key must be at least one character long.")
    return unicode(value)


def normalizeGroupValue(value):
    """
    Normalizes group value.

    * **value** must be a ``list``.
    * **value** items must normalize as glyph names with :func:`normalizeGlyphName`.
    * Returned value will be a ``list`` of unencoded ``unicode`` strings.
    """
    if not isinstance(value, list):
        raise FontPartsError("Group value must be a list, not %s." % type(value).__name__)
    for v in value:
        normalizeGlyphName(v)
    return [unicode(v) for v in value]


# --------
# Features
# --------

def normalizeFeatureText(value):
    """
    Normalizes feature text.

    * **value** must be a :ref:`type-string`.
    * Returned value will be an unencoded ``unicode`` string.
    """
    if not isinstance(value, basestring):
        raise FontPartsError("Feature text must be a string, not %s." % type(value).__name__)
    return unicode(value)


# ---
# Lib
# ---

def normalizeLibKey(value):
    """
    Normalizes lib key.

    * **value** must be a :ref:`type-string`.
    * **value** must be at least one character long.
    * Returned value will be an unencoded ``unicode`` string.
    """
    if not isinstance(value, basestring):
        raise FontPartsError("Lib key must be a string, not %s." % type(value).__name__)
    if len(value) < 1:
        raise FontPartsError("Lib key must be at least one character.")
    return unicode(value)


def normalizeLibValue(value):
    """
    Normalizes lib value.

    * **value** must not be ``None``.
    * Returned value is the same type as the input value.
    """
    if value is None:
        raise FontPartsError("Lib value must not be None.")
    if isinstance(value, (list, tuple)):
        for v in value:
            normalizeLibValue(v)
    elif isinstance(value, dict):
        for k, v in value.items():
            normalizeLibKey(k)
            normalizeLibValue(v)
    return value


# -----
# Layer
# -----

def normalizeLayerName(value):
    """
    Normalizes layer name.

    * **value** must be a :ref:`type-string`.
    * **value** must be at least one character long.
    * Returned value will be an unencoded ``unicode`` string.
    """
    if not isinstance(value, basestring):
        raise FontPartsError("Layer names must be strings, not %s." % type(value).__name__)
    if len(value) < 1:
        raise FontPartsError("Layer names must be at least one character long.")
    return unicode(value)


# -----
# Glyph
# -----

def normalizeGlyphName(value):
    """
    Normalizes glyph name.

    * **value** must be a :ref:`type-string`.
    * **value** must be at least one character long.
    * Returned value will be an unencoded ``unicode`` string.
    """
    if not isinstance(value, basestring):
        raise FontPartsError("Glyph names must be strings, not %s." % type(value).__name__)
    if len(value) < 1:
        raise FontPartsError("Glyph names must be at least one character long.")
    return unicode(value)


def normalizeGlyphUnicodes(value):
    """
    Normalizes glyph unicodes.

    * **value** must be a ``list``.
    * **value** items must normalize as glyph unicodes with :func:`normalizeGlyphUnicode`.
    * Returned value will be a ``list`` of ints.
    """
    if not isinstance(value, list):
        raise FontPartsError("Glyph unicodes must be a list, not %s." % type(value).__name__)
    return [normalizeGlyphUnicode(v) for v in value]


def normalizeGlyphUnicode(value):
    """
    Normalizes glyph unicode.

    * **value** must be an int or hex (represented as a string).
    * **value** must be in a unicode range.
    * Returned value will be an ``int``.
    """
    if not isinstance(value, (int, basestring)):
        raise FontPartsError("Glyph unicode must be a int or hex string, not %s." % type(value).__name__)
    if isinstance(value, basestring):
        try:
            value = int(value, 16)
        except ValueError:
            raise FontPartsError("Glyph unicode hex must be a valid hex string.")
    if value < 0 or value > 1114111:
        raise FontPartsError("Glyph unicode must be in the Unicode range.")
    return value


def normalizeGlyphWidth(value):
    """
    Normalizes glyph width.

    * **value** must be a :ref:`type-int-float`.
    * Returned value is the same type as the input value.
    """
    if not isinstance(value, (int, float)):
        raise FontPartsError("Glyph width must be an :ref:`type-int-float`, not %s." % type(value).__name__)
    return value


def normalizeGlyphLeftMargin(value):
    """
    Normalizes glyph left margin.

    * **value** must be a :ref:`type-int-float`.
    * Returned value is the same type as the input value.
    """
    if not isinstance(value, (int, float)):
        raise FontPartsError("Glyph left margin must be an :ref:`type-int-float`, not %s." % type(value).__name__)
    return value


def normalizeGlyphRightMargin(value):
    """
    Normalizes glyph right margin.

    * **value** must be a :ref:`type-int-float`.
    * Returned value is the same type as the input value.
    """
    if not isinstance(value, (int, float)):
        raise FontPartsError("Glyph right margin must be an :ref:`type-int-float`, not %s." % type(value).__name__)
    return value


def normalizeGlyphHeight(value):
    """
    Normalizes glyph height.

    * **value** must be a :ref:`type-int-float`.
    * Returned value is the same type as the input value.
    """
    if not isinstance(value, (int, float)):
        raise FontPartsError("Glyph height must be an :ref:`type-int-float`, not %s." % type(value).__name__)
    return value


def normalizeGlyphBottomMargin(value):
    """
    Normalizes glyph bottom margin.

    * **value** must be a :ref:`type-int-float`.
    * Returned value is the same type as the input value.
    """
    if not isinstance(value, (int, float)):
        raise FontPartsError("Glyph bottom margin must be an :ref:`type-int-float`, not %s." % type(value).__name__)
    return value


def normalizeGlyphTopMargin(value):
    """
    Normalizes glyph top margin.

    * **value** must be a :ref:`type-int-float`.
    * Returned value is the same type as the input value.
    """
    if not isinstance(value, (int, float)):
        raise FontPartsError("Glyph top margin must be an :ref:`type-int-float`, not %s." % type(value).__name__)
    return value

def normalizeGlyphFormatVersion(value):
    """
    Normalizes glyph format version for saving to XML string.

    * **value** must be a :ref:`type-int-float` of either 1 or 2.
    * Returned value will be an int.
    """
    if not isinstance(value, (int, float)):
        raise FontPartsError("Glyph Format Version must be an :ref:`type-int-float`, not %s." % type(value).__name__)
    value = int(value)
    if value not in (1, 2):
        raise FontPartsError("Glyph Format Version must be either 1 or 2, not %s." % value)
    return value

# -------
# Contour
# -------

def normalizeContourIndex(value):
    """
    Normalizes contour index.

    * **value** must normalize as an index with :func:`normalizeIndex`.
    * Returned value is the same type as input value.
    """
    return normalizeIndex(value)


def normalizeContour(value):
    """
    Normalizes contour.

    * **value** must be a instance of :class:`BaseContour`
    * Returned value is the same type as the input value.
    """
    from fontParts.base.contour import BaseContour
    if not isinstance(value, BaseContour):
        raise FontPartsError("Contour must be a Contour instance, not %s." % type(value).__name__)
    return value


# -----
# Point
# -----

def normalizePointType(value):
    """
    Normalizes point type.

    * **value** must be an string.
    * **value** must be one of the following:

      +----------+
      | move     |
      +----------+
      | line     |
      +----------+
      | offcurve |
      +----------+
      | curve    |
      +----------+
      | qcurve   |
      +----------+

    * Returned value will be an unencoded ``unicode`` string.
    """
    allowedTypes = ['move', 'line', 'offcurve', 'curve', 'qcurve']
    if not isinstance(value, basestring):
        raise FontPartsError("Point type must be a string, not %s." % type(value).__name__)
    if value not in allowedTypes:
        raise FontPartsError("Point type must be '%s'; not %r." % ("', '".join(allowedTypes), value))
    return unicode(value)


def normalizePointName(value):
    """
    Normalizes point name.

    * **value** must be a :ref:`type-string`.
    * **value** must be at least one character long.
    * Returned value will be an unencoded ``unicode`` string.
    """
    if not isinstance(value, basestring):
        raise FontPartsError("Point names must be strings, not %s." % type(value).__name__)
    if len(value) < 1:
        raise FontPartsError("Point names must be at least one character long.")
    return unicode(value)


def normalizePoint(value):
    """
    Normalizes point.

    * **value** must be a instance of :class:`BasePoint`
    * Returned value is the same type as the input value.
    """
    from fontParts.base.point import BasePoint
    if not isinstance(value, BasePoint):
        raise FontPartsError("Point must be a Point instance, not %s." % type(value).__name__)
    return value

# -------
# Segment
# -------

def normalizeSegmentType(value):
    """
    Normalizes segment type.

    * **value** must be a :ref:`type-string`.
    * **value** must be one of the following:

    +--------+
    | move   |
    +--------+
    | line   |
    +--------+
    | curve  |
    +--------+
    | qcurve |
    +--------+

    * Returned value will be an unencoded ``unicode`` string.
    """
    allowedTypes = ['move', 'line', 'curve', 'qcurve']
    if not isinstance(value, basestring):
        raise FontPartsError("Segment type must be a string, not %s." % type(value).__name__)
    if value not in allowedTypes:
        raise FontPartsError("Segment type must be '%s'; not %r." % ("', '".join(allowedTypes), value))
    return unicode(value)


# ----
# Type
# ----

def normalizeBPointType(value):
    """
    Normalizes bPoint type.

    * **value** must be an string.
    * **value** must be one of the following:

      +--------+
      | corner |
      +--------+
      | curve  |
      +--------+

    * Returned value will be an unencoded ``unicode`` string.
    """
    allowedTypes = ['corner', 'curve']
    if not isinstance(value, basestring):
        raise FontPartsError("bPoint type must be a string, not %s." % type(value).__name__)
    if value not in allowedTypes:
        raise FontPartsError("bPoint type must be 'corner' or 'curve', not %r." % value)
    return unicode(value)


# ---------
# Component
# ---------

def normalizeComponentIndex(value):
    """
    Normalizes component index.

    * **value** must normalize as an index with :func:`normalizeIndex`.
    * Returned value is the same type as the input value.
    """
    return normalizeIndex(value)


# ------
# Anchor
# ------

def normalizeAnchorIndex(value):
    """
    Normalizes anchor index.

    * **value** must normalize as an index with :func:`normalizeIndex`.
    * Returned value is the same type as the input value.
    """
    return normalizeIndex(value)


def normalizeAnchorName(value):
    """
    Normalizes anchor name.

    * **value** must be a :ref:`type-string`.
    * **value** must be at least one character long.
    * Returned value will be an unencoded ``unicode`` string.
    """
    if not isinstance(value, basestring):
        raise FontPartsError("Anchor names must be strings, not %s." % type(value).__name__)
    if len(value) < 1:
        raise FontPartsError("Anchor names must be at least one character long.")
    return unicode(value)


# ---------
# Guideline
# ---------

def normalizeGuidelineIndex(value):
    """
    Normalizes guideline index.

    * **value** must normalize as an index with :func:`normalizeIndex`.
    * Returned value is the same type as the input value.
    """
    return normalizeIndex(value)


def normalizeGuidelineAngle(value):
    """
    Normalizes a guideline's angle.

    * Value must be a :ref:`type-int-float`.
    * Value must be between -360 and 360.
    * If the value is negative, it is normalized by adding it to 360
    * Returned value is a ``float`` between 0 and 360.
    """
    if not isinstance(value, (int, float)):
        raise FontPartsError("Guideline angle must be instances of :ref:`type-int-float`, not %s." % type(value).__name__)
    if abs(value) > 360:
        raise FontPartsError("Guideline angle must be between -360 and 360.")
    if value < 0:
        value = value + 360
    return float(value)


def normalizeGuidelineName(value):
    """
    Normalizes guideline name.

    * **value** must be a :ref:`type-string`.
    * **value** must be at least one character long.
    * Returned value will be an unencoded ``unicode`` string.
    """
    if not isinstance(value, basestring):
        raise FontPartsError("Guideline names must be strings, not %s." % type(value).__name__)
    if len(value) < 1:
        raise FontPartsError("Guideline names must be at least one character long.")
    return unicode(value)


# -------
# Generic
# -------

def normalizeBoolean(value):
    """
    Normalizes a boolean.

    * **value** must be an ``int`` with value of 0 or 1, or a ``bool``.
    * Returned value will be a boolean.
    """
    if isinstance(value, int):
        value = bool(value)
    if not isinstance(value, bool):
        raise FontPartsError("Boolean values must be True or False, not '%s'." % value)
    return value


# Identification

def normalizeIndex(value):
    """
    Normalizes index.

    * **value** must be an ``int`` or ``None``.
    * Returned value is the same type as the input value.
    """
    if value is not None:
        if not isinstance(value, int):
            raise FontPartsError("Indexes must be None or integers, not %s." % type(value).__name__)
    return value


def normalizeIdentifier(value):
    """
    Normalizes identifier.

    * **value** must be an :ref:`type-string` or `None`.
    * **value** must not be longer than 100 characters.
    * **value** must not contain a character out the range of 0x20 - 0x7E.
    * Returned value is an unencoded ``unicode`` string.
    """
    if value is None:
        return value
    if not isinstance(value, basestring):
        raise FontPartsError("Identifiers must be strings, not %s." % type(value).__name__)
    if len(value) > 100:
        raise FontPartsError("The identifier string has a length (%d) greater than the maximum allowed (100)." % len(value))
    for c in value:
        v = ord(c)
        if v < 0x20 or v > 0x7E:
            raise FontPartsError("The identifier string ('%s') contains a character out size of the range 0x20 - 0x7E." % value)
    return unicode(value)


# Coordinates

def normalizeX(value):
    """
    Normalizes x coordinate.

    * **value** must be an :ref:`type-int-float`.
    * Returned value is the same type as the input value.
    """
    if not isinstance(value, (int, float)):
        raise FontPartsError("X coordinates must be instances of :ref:`type-int-float`, not %s." % type(value).__name__)
    return value


def normalizeY(value):
    """
    Normalizes y coordinate.

    * **value** must be an :ref:`type-int-float`.
    * Returned value is the same type as the input value.
    """
    if not isinstance(value, (int, float)):
        raise FontPartsError("Y coordinates must be instances of :ref:`type-int-float`, not %s." % type(value).__name__)
    return value


def normalizeCoordinateTuple(value):
    """
    Normalizes coordinate tuple.

    * **value** must be a ``tuple`` or ``list``.
    * **value** must have exactly two items.
    * **value** items must be an :ref:`type-int-float`.
    * Returned value is a ``tuple`` of two values of the same type as the input values.
    """
    if not isinstance(value, (tuple, list)):
        raise FontPartsError("Coordinates must be tuple instances, not %s." % type(value).__name__)
    if len(value) != 2:
        raise FontPartsError("Coordinates must be tuples containing two items, not %d." % len(value))
    x, y = value
    x = normalizeX(x)
    y = normalizeY(y)
    return (x, y)


def normalizeBoundingBox(value):
    """
    Normalizes bounding box.

    * **value** must be an ``tuple`` or ``list``.
    * **value** must have exactly four items.
    * **value** items must be :ref:`type-int-float`.
    * xMin and yMin must be less than or equal to the corresponding xMax, yMax.
    * Returned value will be a tuple of four ``float``.
    """
    if not isinstance(value, (tuple, list)):
        raise FontPartsError("Bounding box be tuple instances, not %s." % type(value).__name__)
    if len(value) != 4:
        raise FontPartsError("Bounding box be tuples containing four items, not %d." % len(value))
    for v in value:
        if not isinstance(v, (int, float)):
            raise FontPartsError("Bounding box values must be instances of :ref:`type-int-float`, not %s." % type(value).__name__)
    if value[0] > value[2]:
        raise FontPartsError("Bounding box xMin must be less than or equal to xMax.")
    if value[1] > value[3]:
        raise FontPartsError("Bounding box yMin must be less than or equal to yMax.")
    return tuple([float(v) for v in value])


# Color

def normalizeColor(value):
    """
    Normalizes :ref:`type-color`.

    * **value** must be an ``tuple`` or ``list``.
    * **value** must have exactly four items.
    * **value** color components must be between 0 and 1.
    * Returned value is a ``tuple``.
    """
    from fontParts.base.color import Color
    if not isinstance(value, (tuple, list, Color)):
        raise FontPartsError("Colors must be tuple instances, not %s." % type(value).__name__)
    if not len(value) == 4:
        raise FontPartsError("Colors must contain four values, not %d." % len(value))
    for component, v in zip("rgba", value):
        if v < 0 or v > 1:
            raise FontPartsError("The value for the %s component (%s) is not between 0 and 1." % (component, v))
    return tuple(value)

# Note

def normalizeGlyphNote(value):
    """
    Normalizes Glyph Note.

    * **value** must be a :ref:`type-string`.
    * Returned value is an unencoded ``unicode`` string
    """
    if not isinstance(value, basestring):
        raise FontPartsError("Note must be a string, not %s." % type(value).__name__)
    return unicode(value)

# File Path

def normalizeFilePath(value):
    """
    Normalizes file path.

    * **value** must be a :ref:`type-string`.
    * Returned value is the same type as the input value.
    """
    if not isinstance(value, basestring):
        raise FontPartsError("File paths must be strings, not %s." % type(value).__name__)
    return value


# Interpolation

def normalizeInterpolationFactor(value):
    """
    Normalizes interpolation factor.

    * **value** must be an :ref:`type-int-float`, ``tuple`` or ``list``.
    * If **value** is a ``tuple`` or ``list``, it must have exactly two items.
      These items must be instances of :ref:`type-int-float`.
    * Returned value is a ``tuple`` of two ``float``.
    """
    if not isinstance(value, (int, float, list, tuple)):
        raise FontPartsError("Interpolation factor must be an int, float, or tuple instances, not %s." % type(value).__name__)
    if isinstance(value, (int, float)):
        value = (float(value), float(value))
    elif isinstance(value, (list, tuple)):
        if not len(value) == 2:
            raise FontPartsError("Interpolation factor tuple must contain two values, not %d." % len(value))
        for v in value:
            if not isinstance(v, (int, float)):
                raise FontPartsError("Interpolation factor tuple values must be an :ref:`type-int-float`, not %s." % type(value).__name__)
        value = tuple([float(v) for v in value])
    return value


# ---------------
# Transformations
# ---------------

def normalizeTransformationMatrix(value):
    """
    Normalizes transformation matrix.

    * **value** must be an ``tuple`` or ``list``.
    * **value** must have exactly six items. Each of these
      items must be an instance of :ref:`type-int-float`.
    * Returned value is a ``tuple`` of six ``float``.
    """
    if not isinstance(value, (tuple, list)):
        raise FontPartsError("Transformation matrices must be tuple instances, not %s." % type(value).__name__)
    if not len(value) == 6:
        raise FontPartsError("Transformation matrices must contain six values, not %d." % len(value))
    for v in value:
        if not isinstance(v, (int, float)):
            raise FontPartsError("Transformation matrix values must be instances of :ref:`type-int-float`, not %s." % type(value).__name__)
    return tuple([float(v) for v in value])


def normalizeTransformationOffset(value):
    """
    Normalizes transformation offset.

    * **value** must be an ``tuple``.
    * **value** must have exactly two items. Each item
      must be an instance of :ref:`type-int-float`.
    * Returned value is a ``tuple`` of two ``float``.
    """
    return normalizeCoordinateTuple(value)


def normalizeTransformationRotationAngle(value):
    """
    Normalizes transformation angle.

    * **value** must be a :ref:`type-int-float`.
    * **value** must be between -360 and 360.
    * If the value is negative, it is normalized by adding it to 360
    * Returned value is a `float` between 0 and 360.
    """
    if not isinstance(value, (int, float)):
        raise FontPartsError("Angles must be instances of :ref:`type-int-float`, not %s." % type(value).__name__)
    if abs(value) > 360:
        raise FontPartsError("The value for the angle (%s) is not between -360 and 360." % value)
    if value < 0:
        value = value + 360
    return float(value)


def normalizeTransformationSkewAngle(value):
    """
    Normalizes transformation skew angle.

    * **value** must be an :ref:`type-int-float`, ``tuple`` or ``list``.
    * If **value** is a ``tuple`` or ``list``, it must have exactly two items.
      These items must be instances of :ref:`type-int-float`.
    * **value** items must be between -360 and 360.
    * If the value is negative, it is normalized by adding it to 360
    * Returned value is a ``tuple`` of two ``float`` between 0 and 360.
    """
    if not isinstance(value, (int, float, list, tuple)):
        raise FontPartsError("Transformation skew angle must be an int, float, or tuple instances, not %s." % type(value).__name__)
    if isinstance(value, (int, float)):
        value = (float(value), 0)
    elif isinstance(value, (list, tuple)):
        if not len(value) == 2:
            raise FontPartsError("Transformation skew angle tuple must contain two values, not %d." % len(value))
        for v in value:
            if not isinstance(v, (int, float)):
                raise FontPartsError("Transformation skew angle tuple values must be an :ref:`type-int-float`, not %s." % type(value).__name__)
        value = tuple([float(v) for v in value])
    for v in value:
        if abs(v) > 360:
            raise FontPartsError("Transformation skew angle must be between -360 and 360.")
    return tuple([v + 360 if v < 0 else v for v in value])


def normalizeTransformationScale(value):
    """
    Normalizes transformation scale.

    * **value** must be an :ref:`type-int-float`, ``tuple`` or ``list``.
    * If **value** is a ``tuple`` or ``list``, it must have exactly two items.
      These items must be instances of :ref:`type-int-float`.
    * Returned value is a ``tuple`` of two ``float``\s.
    """
    if not isinstance(value, (int, float, list, tuple)):
        raise FontPartsError("Transformation scale must be an int, float, or tuple instances, not %s." % type(value).__name__)
    if isinstance(value, (int, float)):
        value = (float(value), float(value))
    elif isinstance(value, (list, tuple)):
        if not len(value) == 2:
            raise FontPartsError("Transformation scale tuple must contain two values, not %d." % len(value))
        for v in value:
            if not isinstance(v, (int, float)):
                raise FontPartsError("Transformation scale tuple values must be an :ref:`type-int-float`, not %s." % type(value).__name__)
        value = tuple([float(v) for v in value])
    return value

def normalizeRounding(value):
    """
    Normalizes rounding.

    Python 2 and Python 3 handing the rounding of halves (0.5, 1.5, etc) differently.
    This normalizes rounding to be the same (Python 3 style) in both environments.

    * **value** must be an :ref:`type-int-float`
    * Returned value is a ``int``

    """
    if not isinstance(value, (int, float)):
        raise FontPartsError("Value to round must be an int or float, not %s." % type(value).__name__)
    return round3(value)
