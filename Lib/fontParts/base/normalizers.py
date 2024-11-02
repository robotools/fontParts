# -*- coding: utf8 -*-

from collections import Counter
from fontTools.misc.fixedTools import otRound

# ----
# Font
# ----


def normalizeFileFormatVersion(value):
    """
    Normalizes a font's file format version.

    * **value** must be a :ref:`type-int`.
    * Returned value will be a ``int``.
    """
    if not isinstance(value, int):
        raise TypeError(
            f"File format versions must be instances of :ref:`type-int`, not {type(value).__name__}."
        )
    return value


def normalizeFileStructure(value):
    """
    Normalizes a font's file structure.

    * **value** must be a :ref:`type-string`.
    * Returned value will be a ``string``.
    """
    allowedFileStructures = ["zip", "package"]
    if value not in allowedFileStructures:
        raise TypeError(
            f"File Structure must be {', '.join(allowedFileStructures)}, not {value}"
        )
    return value


def normalizeLayerOrder(value, font):
    """
    Normalizes layer order.

    ** **value** must be a ``tuple`` or ``list``.
    * **value** items must normalize as layer names with
      :func:`normalizeLayerName`.
    * **value** must contain layers that exist in **font**.
    * **value** must not contain duplicate layers.
    * Returned ``tuple`` will be unencoded ``unicode`` strings
      for each layer name.
    """
    if not isinstance(value, (tuple, list)):
        raise TypeError(f"Layer order must be a list, not {type(value).__name__}.")
    for v in value:
        normalizeLayerName(v)
    fontLayers = [layer.name for layer in font.layers]
    for name in value:
        if name not in fontLayers:
            raise ValueError(
                f"Layer must exist in font. {name} does not exist in font.layers."
            )
    duplicates = [v for v, count in Counter(value).items() if count > 1]
    if len(duplicates) != 0:
        raise ValueError(
            f"Duplicate layers are not allowed. Layer name(s) '{', '.join(duplicates)}' are duplicate(s)."
        )
    return tuple(value)


def normalizeDefaultLayerName(value, font):
    """
    Normalizes default layer name.

    * **value** must normalize as layer name with
      :func:`normalizeLayerName`.
    * **value** must be a layer in **font**.
    * Returned value will be an unencoded ``unicode`` string.
    """
    value = normalizeLayerName(value)
    if value not in font.layerOrder:
        raise ValueError(f"No layer with the name '{value}' exists.")
    return str(value)


def normalizeGlyphOrder(value):
    """
    Normalizes glyph order.

    ** **value** must be a ``tuple`` or ``list``.
    * **value** items must normalize as glyph names with
      :func:`normalizeGlyphName`.
    * **value** must not repeat glyph names.
    * Returned value will be a ``tuple`` of unencoded ``unicode`` strings.
    """
    if not isinstance(value, (tuple, list)):
        raise TypeError(f"Glyph order must be a list, not {type(value).__name__}.")
    for v in value:
        normalizeGlyphName(v)
    duplicates = sorted(v for v, count in Counter(value).items() if count > 1)
    if len(duplicates) != 0:
        raise ValueError(
            f"Duplicate glyph names are not allowed. Glyph name(s) '{', '.join(duplicates)}' are duplicate."
        )
    return tuple(value)


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
    * Returned value will be a two member ``tuple`` of unencoded
      ``unicode`` strings.
    """
    if not isinstance(value, (tuple, list)):
        raise TypeError(
            f"Kerning key must be a tuple instance, not {type(value).__name__}."
        )
    if len(value) != 2:
        raise ValueError(
            f"Kerning key must be a tuple containing two items, not {len(value)}."
        )
    for v in value:
        if not isinstance(v, str):
            raise TypeError(
                f"Kerning key items must be strings, not {type(v).__name__}."
            )
        if len(v) < 1:
            raise ValueError("Kerning key items must be at least one character long")
    if value[0].startswith("public.") and not value[0].startswith("public.kern1."):
        raise ValueError("Left Kerning key group must start with " "public.kern1.")
    if value[1].startswith("public.") and not value[1].startswith("public.kern2."):
        raise ValueError("Right Kerning key group must start with " "public.kern2.")
    return tuple(value)


def normalizeKerningValue(value):
    """
    Normalizes kerning value.

    * **value** must be an :ref:`type-int-float`.
    * Returned value is the same type as input value.
    """
    if not isinstance(value, (int, float)):
        raise TypeError(
            f"Kerning value must be a int or a float, not {type(value).__name__}."
        )
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
    if not isinstance(value, str):
        raise TypeError(f"Group key must be a string, not {type(value).__name__}.")
    if len(value) < 1:
        raise ValueError("Group key must be at least one character long.")
    return value


def normalizeGroupValue(value):
    """
    Normalizes group value.

    * **value** must be a ``list``.
    * **value** items must normalize as glyph names with
      :func:`normalizeGlyphName`.
    * Returned value will be a ``tuple`` of unencoded ``unicode`` strings.
    """
    if not isinstance(value, (tuple, list)):
        raise TypeError(f"Group value must be a list, not {type(value).__name__}.")
    value = [normalizeGlyphName(v) for v in value]
    return tuple(value)


# --------
# Features
# --------


def normalizeFeatureText(value):
    """
    Normalizes feature text.

    * **value** must be a :ref:`type-string`.
    * Returned value will be an unencoded ``unicode`` string.
    """
    if not isinstance(value, str):
        raise TypeError(f"Feature text must be a string, not {type(value).__name__}.")
    return value


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
    if not isinstance(value, str):
        raise TypeError(f"Lib key must be a string, not {type(value).__name__}.")
    if len(value) < 1:
        raise ValueError("Lib key must be at least one character.")
    return value


def normalizeLibValue(value):
    """
    Normalizes lib value.

    * **value** must not be ``None``.
    * Returned value is the same type as the input value.
    """
    if value is None:
        raise ValueError("Lib value must not be None.")
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


def normalizeLayer(value):
    """
    Normalizes layer.

    * **value** must be a instance of :class:`BaseLayer`
    * Returned value is the same type as the input value.
    """
    from fontParts.base.layer import BaseLayer

    return normalizeInternalObjectType(value, BaseLayer, "Layer")


def normalizeLayerName(value):
    """
    Normalizes layer name.

    * **value** must be a :ref:`type-string`.
    * **value** must be at least one character long.
    * Returned value will be an unencoded ``unicode`` string.
    """
    if not isinstance(value, str):
        raise TypeError(f"Layer names must be strings, not {type(value).__name__}.")
    if len(value) < 1:
        raise ValueError("Layer names must be at least one character long.")
    return value


# -----
# Glyph
# -----


def normalizeGlyph(value):
    """
    Normalizes glyph.

    * **value** must be a instance of :class:`BaseGlyph`
    * Returned value is the same type as the input value.
    """
    from fontParts.base.glyph import BaseGlyph

    return normalizeInternalObjectType(value, BaseGlyph, "Glyph")


def normalizeGlyphName(value):
    """
    Normalizes glyph name.

    * **value** must be a :ref:`type-string`.
    * **value** must be at least one character long.
    * Returned value will be an unencoded ``unicode`` string.
    """
    if not isinstance(value, str):
        raise TypeError(f"Glyph names must be strings, not {type(value).__name__}.")
    if len(value) < 1:
        raise ValueError("Glyph names must be at least one character long.")
    return value


def normalizeGlyphUnicodes(value):
    """
    Normalizes glyph unicodes.

    * **value** must be a ``list``.
    * **value** items must normalize as glyph unicodes with
      :func:`normalizeGlyphUnicode`.
    * **value** must not repeat unicode values.
    * Returned value will be a ``tuple`` of ints.
    """
    if not isinstance(value, (tuple, list)):
        raise TypeError(f"Glyph unicodes must be a list, not {type(value).__name__}.")
    values = [normalizeGlyphUnicode(v) for v in value]
    duplicates = [v for v, count in Counter(value).items() if count > 1]
    if len(duplicates) != 0:
        raise ValueError("Duplicate unicode values are not allowed.")
    return tuple(values)


def normalizeGlyphUnicode(value):
    """
    Normalizes glyph unicode.

    * **value** must be an int or hex (represented as a string).
    * **value** must be in a unicode range.
    * Returned value will be an ``int``.
    """
    if not isinstance(value, (int, str)) or isinstance(value, bool):
        raise TypeError(
            f"Glyph unicode must be a int or hex string, not {type(value).__name__}."
        )
    if isinstance(value, str):
        try:
            value = int(value, 16)
        except ValueError:
            raise ValueError("Glyph unicode hex must be a valid hex string.")
    if value < 0 or value > 1114111:
        raise ValueError("Glyph unicode must be in the Unicode range.")
    return value


def normalizeGlyphWidth(value):
    """
    Normalizes glyph width.

    * **value** must be a :ref:`type-int-float`.
    * Returned value is the same type as the input value.
    """
    if not isinstance(value, (int, float)):
        raise TypeError(
            f"Glyph width must be an :ref:`type-int-float`, not {type(value).__name__}."
        )
    return value


def normalizeGlyphLeftMargin(value):
    """
    Normalizes glyph left margin.

    * **value** must be a :ref:`type-int-float` or `None`.
    * Returned value is the same type as the input value.
    """
    if not isinstance(value, (int, float)) and value is not None:
        raise TypeError(
            f"Glyph left margin must be an :ref:`type-int-float`, not {type(value).__name__}."
        )
    return value


def normalizeGlyphRightMargin(value):
    """
    Normalizes glyph right margin.

    * **value** must be a :ref:`type-int-float` or `None`.
    * Returned value is the same type as the input value.
    """
    if not isinstance(value, (int, float)) and value is not None:
        raise TypeError(
            f"Glyph right margin must be an :ref:`type-int-float`, not {type(value).__name__}."
        )
    return value


def normalizeGlyphHeight(value):
    """
    Normalizes glyph height.

    * **value** must be a :ref:`type-int-float`.
    * Returned value is the same type as the input value.
    """
    if not isinstance(value, (int, float)):
        raise TypeError(
            f"Glyph height must be an :ref:`type-int-float`, not {type(value).__name__}."
        )
    return value


def normalizeGlyphBottomMargin(value):
    """
    Normalizes glyph bottom margin.

    * **value** must be a :ref:`type-int-float` or `None`.
    * Returned value is the same type as the input value.
    """
    if not isinstance(value, (int, float)) and value is not None:
        raise TypeError(
            f"Glyph bottom margin must be an :ref:`type-int-float`, not {type(value).__name__}."
        )
    return value


def normalizeGlyphTopMargin(value):
    """
    Normalizes glyph top margin.

    * **value** must be a :ref:`type-int-float` or `None`.
    * Returned value is the same type as the input value.
    """
    if not isinstance(value, (int, float)) and value is not None:
        raise TypeError(
            f"Glyph top margin must be an :ref:`type-int-float`, not {type(value).__name__}."
        )
    return value


def normalizeGlyphFormatVersion(value):
    """
    Normalizes glyph format version for saving to XML string.

    * **value** must be a :ref:`type-int-float` of either 1 or 2.
    * Returned value will be an int.
    """
    if not isinstance(value, (int, float)):
        raise TypeError(
            f"Glyph Format Version must be an :ref:`type-int-float`, not {type(value).__name__}."
        )
    value = int(value)
    if value not in (1, 2):
        raise ValueError(f"Glyph Format Version must be either 1 or 2, not {value}.")
    return value


# -------
# Contour
# -------


def normalizeContour(value):
    """
    Normalizes contour.

    * **value** must be a instance of :class:`BaseContour`
    * Returned value is the same type as the input value.
    """
    from fontParts.base.contour import BaseContour

    return normalizeInternalObjectType(value, BaseContour, "Contour")


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
    allowedTypes = ["move", "line", "offcurve", "curve", "qcurve"]
    if not isinstance(value, str):
        raise TypeError(f"Point type must be a string, not {type(value).__name__}.")
    if value not in allowedTypes:
        raise ValueError(
            "Point type must be '%s'; not %r." % ("', '".join(allowedTypes), value)
        )
    return value


def normalizePointName(value):
    """
    Normalizes point name.

    * **value** must be a :ref:`type-string`.
    * **value** must be at least one character long.
    * Returned value will be an unencoded ``unicode`` string.
    """
    if not isinstance(value, str):
        raise TypeError(f"Point names must be strings, not {type(value).__name__}.")
    if len(value) < 1:
        raise ValueError("Point names must be at least one character long.")
    return value


def normalizePoint(value):
    """
    Normalizes point.

    * **value** must be a instance of :class:`BasePoint`
    * Returned value is the same type as the input value.
    """
    from fontParts.base.point import BasePoint

    return normalizeInternalObjectType(value, BasePoint, "Point")


# -------
# Segment
# -------


def normalizeSegment(value):
    """
    Normalizes segment.

    * **value** must be a instance of :class:`BaseSegment`
    * Returned value is the same type as the input value.
    """
    from fontParts.base.segment import BaseSegment

    return normalizeInternalObjectType(value, BaseSegment, "Segment")


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
    allowedTypes = ["move", "line", "curve", "qcurve"]
    if not isinstance(value, str):
        raise TypeError(f"Segment type must be a string, not {type(value).__name__}.")
    if value not in allowedTypes:
        raise ValueError(
            "Segment type must be '%s'; not %r." % ("', '".join(allowedTypes), value)
        )
    return value


# ------
# BPoint
# ------


def normalizeBPoint(value):
    """
    Normalizes bPoint.

    * **value** must be a instance of :class:`BaseBPoint`
    * Returned value is the same type as the input value.
    """
    from fontParts.base.bPoint import BaseBPoint

    return normalizeInternalObjectType(value, BaseBPoint, "bPoint")


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
    allowedTypes = ["corner", "curve"]
    if not isinstance(value, str):
        raise TypeError(f"bPoint type must be a string, not {type(value).__name__}.")
    if value not in allowedTypes:
        raise ValueError(f"bPoint type must be 'corner' or 'curve', not {value!r}.")
    return value


# ---------
# Component
# ---------


def normalizeComponent(value):
    """
    Normalizes component.

    * **value** must be a instance of :class:`BaseComponent`
    * Returned value is the same type as the input value.
    """
    from fontParts.base.component import BaseComponent

    return normalizeInternalObjectType(value, BaseComponent, "Component")


def normalizeComponentScale(value):
    """
    Normalizes component scale.

    * **value** must be a `tuple`` or ``list``.
    * **value** must have exactly two items.
      These items must be instances of :ref:`type-int-float`.
    * Returned value is a ``tuple`` of two ``float``\s.
    """
    if not isinstance(value, (list, tuple)):
        raise TypeError(
            f"Component scale must be a tuple instance, not {type(value).__name__}."
        )
    else:
        if not len(value) == 2:
            raise ValueError(
                f"Transformation scale tuple must contain two values, not {len(value)}."
            )
        for v in value:
            if not isinstance(v, (int, float)):
                raise TypeError(
                    f"Transformation scale tuple values must be an :ref:`type-int-float`, not {type(value).__name__}."
                )
        value = tuple([float(v) for v in value])
    return value


# ------
# Anchor
# ------


def normalizeAnchor(value):
    """
    Normalizes anchor.

    * **value** must be a instance of :class:`BaseAnchor`
    * Returned value is the same type as the input value.
    """
    from fontParts.base.anchor import BaseAnchor

    return normalizeInternalObjectType(value, BaseAnchor, "Anchor")


def normalizeAnchorName(value):
    """
    Normalizes anchor name.

    * **value** must be a :ref:`type-string` or ``None``.
    * **value** must be at least one character long if :ref:`type-string`.
    * Returned value will be an unencoded ``unicode`` string or ``None``.
    """
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError(f"Anchor names must be strings, not {type(value).__name__}.")
    if len(value) < 1:
        raise ValueError(
            ("Anchor names must be at least one character " "long or None.")
        )
    return value


# ---------
# Guideline
# ---------


def normalizeGuideline(value):
    """
    Normalizes guideline.

    * **value** must be a instance of :class:`BaseGuideline`
    * Returned value is the same type as the input value.
    """
    from fontParts.base.guideline import BaseGuideline

    return normalizeInternalObjectType(value, BaseGuideline, "Guideline")


def normalizeGuidelineName(value):
    """
    Normalizes guideline name.

    * **value** must be a :ref:`type-string`.
    * **value** must be at least one character long.
    * Returned value will be an unencoded ``unicode`` string.
    """
    if not isinstance(value, str):
        raise TypeError(f"Guideline names must be strings, not {type(value).__name__}.")
    if len(value) < 1:
        raise ValueError("Guideline names must be at least one character " "long.")
    return value


# -------
# Generic
# -------


def normalizeInternalObjectType(value, cls, name):
    """
    Normalizes an internal object type.

    * **value** must be a instance of **cls**.
    * Returned value is the same type as the input value.
    """
    if not isinstance(value, cls):
        raise TypeError(
            f"{name} must be a {name} instance, not {type(value).__name__}."
        )
    return value


def normalizeBoolean(value):
    """
    Normalizes a boolean.

    * **value** must be an ``int`` with value of 0 or 1, or a ``bool``.
    * Returned value will be a boolean.
    """
    if isinstance(value, int) and value in (0, 1):
        value = bool(value)
    if not isinstance(value, bool):
        raise ValueError(f"Boolean values must be True or False, not '{value}'.")
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
            raise TypeError(
                f"Indexes must be None or integers, not {type(value).__name__}."
            )
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
    if not isinstance(value, str):
        raise TypeError(f"Identifiers must be strings, not {type(value).__name__}.")
    if len(value) == 0:
        raise ValueError("The identifier string is empty.")
    if len(value) > 100:
        raise ValueError(
            f"The identifier string has a length ({len(value)}) greater than the maximum allowed (100)."
        )
    for c in value:
        v = ord(c)
        if v < 0x20 or v > 0x7E:
            raise ValueError(
                f"The identifier string ('{value}') contains a character out size of the range 0x20 - 0x7E."
            )
    return value


# Coordinates


def normalizeX(value):
    """
    Normalizes x coordinate.

    * **value** must be an :ref:`type-int-float`.
    * Returned value is the same type as the input value.
    """
    if not isinstance(value, (int, float)):
        raise TypeError(
            f"X coordinates must be instances of :ref:`type-int-float`, not {type(value).__name__}."
        )
    return value


def normalizeY(value):
    """
    Normalizes y coordinate.

    * **value** must be an :ref:`type-int-float`.
    * Returned value is the same type as the input value.
    """
    if not isinstance(value, (int, float)):
        raise TypeError(
            f"Y coordinates must be instances of :ref:`type-int-float`, not {type(value).__name__}."
        )
    return value


def normalizeCoordinateTuple(value):
    """
    Normalizes coordinate tuple.

    * **value** must be a ``tuple`` or ``list``.
    * **value** must have exactly two items.
    * **value** items must be an :ref:`type-int-float`.
    * Returned value is a ``tuple`` of two values of the same type as
      the input values.
    """
    if not isinstance(value, (tuple, list)):
        raise TypeError(
            f"Coordinates must be tuple instances, not {type(value).__name__}."
        )
    if len(value) != 2:
        raise ValueError(
            f"Coordinates must be tuples containing two items, not {len(value)}."
        )
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
        raise TypeError(f"Bounding box be tuple instances, not {type(value).__name__}.")
    if len(value) != 4:
        raise ValueError(
            f"Bounding box be tuples containing four items, not {len(value)}."
        )
    for v in value:
        if not isinstance(v, (int, float)):
            raise TypeError(
                f"Bounding box values must be instances of :ref:`type-int-float`, not {type(value).__name__}."
            )
    if value[0] > value[2]:
        raise ValueError("Bounding box xMin must be less than or equal to " "xMax.")
    if value[1] > value[3]:
        raise ValueError("Bounding box yMin must be less than or equal to " "yMax.")
    return tuple(float(v) for v in value)


def normalizeArea(value):
    """
    Normalizes area.

    * **value** must be a positive :ref:`type-int-float`.
    """
    if not isinstance(value, (int, float)):
        raise TypeError(
            f"Area must be an instance of :ref:`type-int-float`, not {type(value).__name__}."
        )
    if value < 0:
        raise ValueError(
            f"Area must be a positive :ref:`type-int-float`, not {repr(value)}."
        )
    return float(value)


def normalizeRotationAngle(value):
    """
    Normalizes an angle.

    * Value must be a :ref:`type-int-float`.
    * Value must be between -360 and 360.
    * If the value is negative, it is normalized by adding it to 360
    * Returned value is a ``float`` between 0 and 360.
    """
    if not isinstance(value, (int, float)):
        raise TypeError(
            f"Angle must be instances of :ref:`type-int-float`, not {type(value).__name__}."
        )
    if abs(value) > 360:
        raise ValueError("Angle must be between -360 and 360.")
    if value < 0:
        value = value + 360
    return float(value)


# Color


def normalizeColor(value):
    """
    Normalizes :ref:`type-color`.

    * **value** must be an ``tuple`` or ``list``.
    * **value** must have exactly four items.
    * **value** color components must be between 0 and 1.
    * Returned value is a ``tuple`` containing four ``float`` values.
    """
    from fontParts.base.color import Color

    if not isinstance(value, (tuple, list, Color)):
        raise TypeError(f"Colors must be tuple instances, not {type(value).__name__}.")
    if not len(value) == 4:
        raise ValueError(f"Colors must contain four values, not {len(value)}.")
    for component, v in zip("rgba", value):
        if not isinstance(v, (int, float)):
            raise TypeError(
                f"The value for the {component} component ({v}) is not an int or float."
            )
        if v < 0 or v > 1:
            raise ValueError(
                f"The value for the {component} component ({v}) is not between 0 and 1."
            )
    return tuple([float(v) for v in value])


# Note


def normalizeGlyphNote(value):
    """
    Normalizes Glyph Note.

    * **value** must be a :ref:`type-string`.
    * Returned value is an unencoded ``unicode`` string
    """
    if not isinstance(value, str):
        raise TypeError(f"Note must be a string, not {type(value).__name__}.")
    return value


# File Path


def normalizeFilePath(value):
    """
    Normalizes file path.

    * **value** must be a :ref:`type-string`.
    * Returned value is an unencoded ``unicode`` string
    """
    if not isinstance(value, str):
        raise TypeError(f"File paths must be strings, not {type(value).__name__}.")
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
        raise TypeError(
            f"Interpolation factor must be an int, float, or tuple instances, not {type(value).__name__}."
        )
    if isinstance(value, (int, float)):
        value = (float(value), float(value))
    else:
        if not len(value) == 2:
            raise ValueError(
                f"Interpolation factor tuple must contain two values, not {len(value)}."
            )
        for v in value:
            if not isinstance(v, (int, float)):
                raise TypeError(
                    f"Interpolation factor tuple values must be an :ref:`type-int-float`, not {type(value).__name__}."
                )
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
        raise TypeError(
            f"Transformation matrices must be tuple instances, not {type(value).__name__}."
        )
    if not len(value) == 6:
        raise ValueError(
            f"Transformation matrices must contain six values, not {len(value)}."
        )
    for v in value:
        if not isinstance(v, (int, float)):
            raise TypeError(
                f"Transformation matrix values must be instances of :ref:`type-int-float`, not {type(v).__name__}."
            )
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
        raise TypeError(
            f"Transformation skew angle must be an int, float, or tuple instances, not {type(value).__name__}."
        )
    if isinstance(value, (int, float)):
        value = (float(value), 0)
    else:
        if not len(value) == 2:
            raise ValueError(
                f"Transformation skew angle tuple must contain two values, not {len(value)}."
            )
        for v in value:
            if not isinstance(v, (int, float)):
                raise TypeError(
                    f"Transformation skew angle tuple values must be an :ref:`type-int-float`, not {type(value).__name__}."
                )
        value = tuple([float(v) for v in value])
    for v in value:
        if abs(v) > 360:
            raise ValueError(
                "Transformation skew angle must be between -360 " "and 360."
            )
    return tuple(float(v + 360) if v < 0 else float(v) for v in value)


def normalizeTransformationScale(value):
    """
    Normalizes transformation scale.

    * **value** must be an :ref:`type-int-float`, ``tuple`` or ``list``.
    * If **value** is a ``tuple`` or ``list``, it must have exactly two items.
      These items must be instances of :ref:`type-int-float`.
    * Returned value is a ``tuple`` of two ``float``\s.
    """
    if not isinstance(value, (int, float, list, tuple)):
        raise TypeError(
            f"Transformation scale must be an int, float, or tuple instances, not {type(value).__name__}."
        )
    if isinstance(value, (int, float)):
        value = (float(value), float(value))
    else:
        if not len(value) == 2:
            raise ValueError(
                f"Transformation scale tuple must contain two values, not {len(value)}."
            )
        for v in value:
            if not isinstance(v, (int, float)):
                raise TypeError(
                    f"Transformation scale tuple values must be an :ref:`type-int-float`, not {type(value).__name__}."
                )
        value = tuple([float(v) for v in value])
    return value


def normalizeVisualRounding(value):
    """
    Normalizes rounding.
    Python 3 uses banker’s rounding, meaning anything that is at 0.5
    will go to the even number. This isn't always ideal for point
    coordinates, so instead round to the higher number.

    * **value** must be an :ref:`type-int-float`
    * Returned value is a ``int``
    """

    if not isinstance(value, (int, float)):
        raise TypeError(
            f"Value to round must be an int or float, not {type(value).__name__}."
        )
    return otRound(value)
