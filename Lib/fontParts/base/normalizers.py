# -*- coding: utf8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Tuple, Type, Union
from collections import Counter
from fontTools.misc.fixedTools import otRound
from pathlib import Path

from fontParts.base.annotations import (
    T,
    PairType,
    QuadrupleType,
    SextupleType,
    CollectionType,
    PairCollectionType,
    QuadrupleCollectionType,
    SextupleCollectionType,
    IntFloatType,
    TransformationType,
)

if TYPE_CHECKING:
    from fontParts.base.layer import BaseLayer
    from fontParts.base.glyph import BaseGlyph
    from fontParts.base.contour import BaseContour
    from fontParts.base.point import BasePoint
    from fontParts.base.segment import BaseSegment
    from fontParts.base.bPoint import BaseBPoint
    from fontParts.base.component import BaseComponent
    from fontParts.base.anchor import BaseAnchor
    from fontParts.base.guideline import BaseGuideline

# ----
# Font
# ----


def normalizeFileFormatVersion(value: int) -> int:
    """Normalize a font's file format version.

    :param value: The file format verison of the font as an :class:`int`.
    :return: An :class:`int` representing the normalized file format version.
    :raises TypeError: If `value` is not of type :class:`int`.

    """
    if not isinstance(value, int):
        raise TypeError(
            f"Expected file formmat verison 'value' to be of type int, not {type(value).__name__}."
        )
    return value


def normalizeFileStructure(value: str) -> str:
    """Normalize a font's file structure.

    :param value: The file structure to normalize as a :class:`str`.
    :return: A :class:`str` representing the normalized file structure.
    :raises TypeError: If `value` is not a :class:`str`.

    """
    allowedFileStructures = ["zip", "package"]
    if value not in allowedFileStructures:
        raise TypeError(
            f"File Structure must be {', '.join(allowedFileStructures)}, not {value}"
        )
    return value


def normalizeLayerOrder(value: CollectionType[str], font) -> Tuple[str, ...]:
    """Normalize layer order.

    :param value: The layer order to normalize as a :class:`list`
        or :class:`tuple` of layer names. Each item in `value`:
        - must normalize with :func:`normalizeLayerName`.
        - must correspond to an existing layer name in the font.
        - must be unique (no duplicates are allowed).
    :param font: The :class:`BaseFont` (subclass) instance to which the
        normalization applies.
    :return: A :class:`tuple` of layer names in their normalized order.
    :raises TypeError:
        - If `value` is not a :class:`list` or :class:`tuple.
        - If any `value` item is not a :class:`str`.
    :raises ValueError:
        - If `value` contains duplicate values.
        - If any `value` item does not exist in `font`.
        - If any `value` item is an empty :class:`str`.

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


def normalizeDefaultLayerName(value: str, font) -> str:
    """Normalize a default layer name.

    :param value: The layer name to normalize as a :class:`str`. The value:
        - must normalize as layer name with :func:`normalizeLayerName`.
        - must be a layer in `font`.
    :param font: The :class:`BaseFont` (subclass) instance to which the
        normalization applies.
    :return: A :class:`str` representing the normalized default layer name.
    :raises TypeError: If `value` is not a :class:`str`.
    :raises ValueError:
        - If `value` does not exist in `font`.
        - If `value` is an empty :class:`str`.

    """
    value = normalizeLayerName(value)
    if value not in font.layerOrder:
        raise ValueError(f"No layer with the name '{value}' exists.")
    return str(value)


def normalizeGlyphOrder(value: CollectionType[str]) -> Tuple[str, ...]:
    """Normalize glyph order.

    :param value: The glyph order to normalize as a :class:`list`
        or :class:`tuple` of glyph names. Each item in `value`:
        - must normalize as glyph names with :func:`normalizeGlyphName`.
        - must be unique (no duplicates are allowed).
    :return: A :class:`tuple` of glyph names in their normalized order.
    :raises TypeError:
        - If `value` is not a :class:`list` or :class:`tuple.
        - If any `value` item is not a :class:`str`.
    :raises ValueError:
        - If `value` contains duplicate values.
        - If any `value` item is an empty :class:`str`.

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


def normalizeKerningKey(value: PairCollectionType[str]) -> PairType[str]:
    """Normalize a kerning key.

    :param value: The kerning key to normalize as a :class:`tuple`
        or :class:`list` containing two items representing the left and right
        kerning key groups. Each item in `value`:
        - must be a :class:`str`.
        - must be at least one character long.
    :return: The normalized kerning key as a :class:`tuple` of :class:`str` items.
    :raises TypeError:
        - If `value` is not a :class:`list` or :class:`tuple.
        - If any `value` item is not a :class:`str`.
    :raises ValueError:
        - If `value` does not a contain a pair of items.
        - If any `value` item is an empty :class:`str`.
        - If the left kerning key group starts with 'public.' but does not
          start with 'public.kern1.'.
        - If the right kerning key group starts with 'public.' but does not
          start with 'public.kern2.'.

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


def normalizeKerningValue(value: IntFloatType) -> IntFloatType:
    """Normalize a kerning value.

    :param value: The kerning value to normalize as an :class:`int` or :class:`float`.
    :return: An :class:`int` or :class:`flaot` representing the normalized
        kerning value.
    raises TypeError: If `value` is not an :class:`int` or a :class:`float`.

    """
    if not isinstance(value, (int, float)):
        raise TypeError(
            f"Kerning value must be a int or a float, not {type(value).__name__}."
        )
    return value


# ------
# Groups
# ------


def normalizeGroupKey(value: str) -> str:
    """Normalize a group key.

    :param value: The group key to normalize as a non-empty :class:`str`.
    :return: A :class:`str` representing the normalized group key.
    :raises TyypeError: If `value` is not a :class:`str`.
    raises ValueError: If `value` is an empty :class:`str`.

    """
    if not isinstance(value, str):
        raise TypeError(f"Group key must be a string, not {type(value).__name__}.")
    if len(value) < 1:
        raise ValueError("Group key must be at least one character long.")
    return value


def normalizeGroupValue(value: CollectionType[str]) -> Tuple[str, ...]:
    """Normalize a group value.

    :param value: The group value to normalize as a :class:`list`
        or :class:`tuple` of :class:`str` items representing the names of the
        glyphs in the group. All `value` items must
        normalize :func:`normalizeGlyphName`.
    :return: A :class:`tuple` of :class:`str` items representing the normalized
        gorup value.
    :raises TyypeError: If `value` is not a :class:`list` or :class:`tuple`.

    """
    if not isinstance(value, (tuple, list)):
        raise TypeError(f"Group value must be a list, not {type(value).__name__}.")
    value = [normalizeGlyphName(v) for v in value]
    return tuple(value)


# --------
# Features
# --------


def normalizeFeatureText(value: str) -> str:
    """Normalize feature text.

    :param value: The feature text to normalize as a :class:`str`.
    :return: A :class:`str` representing the normalized feature text.
    :raises TypeError: If `value` is not a :class:`str`.

    """
    if not isinstance(value, str):
        raise TypeError(f"Feature text must be a string, not {type(value).__name__}.")
    return value


# ---
# Lib
# ---


def normalizeLibKey(value: str) -> str:
    """Normalize a lib key.

    :param value: The lib key to normalize as a non-empty :class:`str`.
    :return: A :class:`str` representing the noramlized lib key.
    :raises TypeError: If `value` is not a :class:`str`.
    :raises ValueError: If `value` is an empty :class:`str`.

    """
    if not isinstance(value, str):
        raise TypeError(f"Lib key must be a string, not {type(value).__name__}.")
    if len(value) < 1:
        raise ValueError("Lib key must be at least one character.")
    return value


def normalizeLibValue(value: Any) -> Any:
    """Normalize a lib value.

    If `value` is a collection (:class:`list`, :class:`tuple`, or :class:`dict`),
    its elements will be normalized recursively.

    :param value: The lib value to normalize. The value (or any item) must not
        be :obj:`None`.
    :return: The normalized lib value, of the same type as `value`.
    :raises ValueError: If `value` or any of it's items is :obj:`None`.

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


def normalizeLayer(value: BaseLayer) -> BaseLayer:
    """Normalize a layer.

    :param value: The layer to normalize as an instance of :class:`BaseLayer`.
    :return: The normalized :class:`BaseLayer`instance.
    :raises TypeError: If `value` is not an instance of :class:`BaseLayer`.

    """
    from fontParts.base.layer import BaseLayer

    return normalizeInternalObjectType(value, BaseLayer, "Layer")


def normalizeLayerName(value: str) -> str:
    """Normalize a layer name.

    :param value: The layer name to normalize as a non-empty :class:`str`.
    :return: A :class:`str` representing the normalized layer name.
    :raises TypeError: If `value` is not a :class:`str`.
    :raises ValueError: If `value` is an empty :class:`str`.

    """
    if not isinstance(value, str):
        raise TypeError(f"Layer names must be strings, not {type(value).__name__}.")
    if len(value) < 1:
        raise ValueError("Layer names must be at least one character long.")
    return value


# -----
# Glyph
# -----


def normalizeGlyph(value: BaseGlyph) -> BaseGlyph:
    """Normalize a glyph.

    :param value: The glyph to normalize as an instance of :class:`BaseGlyph`.
    :return: The normalized :class:`BaseGlyph` instance.
    :raises TypeError: If `value` is not an instance of :class:`BaseGlyph`.

    """
    from fontParts.base.glyph import BaseGlyph

    return normalizeInternalObjectType(value, BaseGlyph, "Glyph")


def normalizeGlyphName(value: str) -> str:
    """Normalize a glyph's name.

    :param value: The glyph name to normalize as a non-empty :class:`str`.
    :return: A :class:`str` representing the normalized glyph name.
    :raises TypeError: If `value` is not a :class:`str`.
    :raises ValueError: If `value` is an empty string.

    """
    if not isinstance(value, str):
        raise TypeError(f"Glyph names must be strings, not {type(value).__name__}.")
    if len(value) < 1:
        raise ValueError("Glyph names must be at least one character long.")
    return value


def normalizeGlyphUnicodes(value: CollectionType[int]) -> Tuple[int, ...]:
    """Normalize a glyph's unicodes.

    :param value: The glyph unicodes to normalize as a :class:`list`
        or :class:`tuple` of Unicode values. Each item in `value`:
        - must normalize as glyph unicodes with :func:`normalizeGlyphUnicode`.
        - must be unique (no duplicates are allowed).
    :return: A :class:`tuple of :class:`int` values representing the noramlized
        glyph unicodes.
    :raises TypeError: If `value` is not a :class:`list` or :class:`tuple`.
    :raises ValueError:
        - If `value` contains duplicate values.
        - If any `value` item is not a valid hexadelimal value.
        - If any `value` item is not within the unicode range.

    """
    if not isinstance(value, (tuple, list)):
        raise TypeError(f"Glyph unicodes must be a list, not {type(value).__name__}.")
    values = [normalizeGlyphUnicode(v) for v in value]
    duplicates = [v for v, count in Counter(value).items() if count > 1]
    if len(duplicates) != 0:
        raise ValueError("Duplicate unicode values are not allowed.")
    return tuple(values)


def normalizeGlyphUnicode(value: Union[int, str]) -> int:
    """Normalize a glyph's unicode.

    :param value: The glyph Unicode value to normalize as an :class:`int` or a
        hexadecimal :class:`str`. The value must be within the unicode range.
    :return: An :class:`int` representing the noramlized unicode value.
    :raises TypeError: If `value` is not and :class:`int` or a :class:`str`.
    :raises ValueError:
        - If `value` is not a valid hexadelimal value.
        - If `value` is not within the unicode range.

    """
    if not isinstance(value, (int, str)) or isinstance(value, bool):
        raise TypeError(
            f"Glyph unicode must be an int or hex string, not {type(value).__name__}."
        )
    if isinstance(value, str):
        try:
            value = int(value, 16)
        except ValueError:
            raise ValueError("Glyph unicode hex must be a valid hex string.")
    if value < 0 or value > 1114111:
        raise ValueError("Glyph unicode must be in the Unicode range.")
    return value


def normalizeGlyphWidth(value: IntFloatType) -> IntFloatType:
    """Normalize a glyph's width.

    :param value: The glyph width to normalize as an :class:`int` or :class:`float`.
    :return: The normalized glyph width, of the same type as `value`.
    :raises TypeError: if `value` is not an :class:`int` or a :class:`float`.

    """
    if not isinstance(value, (int, float)):
        raise TypeError(
            f"Glyph width must be an :ref:`type-int-float`, not {type(value).__name__}."
        )
    return value


def normalizeGlyphLeftMargin(value: Optional[IntFloatType]) -> Optional[IntFloatType]:
    """Normalize a glyph's left margin.

    :param value: The glyph left margin to normalize as
        an :class:`int`, :class:`float`, or :obj:`None`.
    :return: The normalized glyph left margin, of the same type as `value`.
    :raises TypeError: if `value` is not an :class:`int` or a :class:`float`.

    """
    if not isinstance(value, (int, float)) and value is not None:
        raise TypeError(
            f"Glyph left margin must be an :ref:`type-int-float`, not {type(value).__name__}."
        )
    return value


def normalizeGlyphRightMargin(value: Optional[IntFloatType]) -> Optional[IntFloatType]:
    """Normalize a glyph's right margin.

    :param value: The glyph right margin to normalize as
        an :class:`int`, :class:`float`, or :obj:`None`.
    :return: The normalized glyph right margin, of the same type as `value`.
    :raises TypeError: if `value` is not an :class:`int` or a :class:`float`.

    """
    if not isinstance(value, (int, float)) and value is not None:
        raise TypeError(
            f"Glyph right margin must be an :ref:`type-int-float`, not {type(value).__name__}."
        )
    return value


def normalizeGlyphHeight(value: IntFloatType) -> IntFloatType:
    """Normalize a glyph's height.

    :param value: The glyph height to normalize as an :class:`int` or :class:`float`.
    :return: The normalized glyph height, of the same type as `value`.
    :raises TypeError: if `value` is not an :class:`int` or a :class:`float`.

    """
    if not isinstance(value, (int, float)):
        raise TypeError(
            f"Glyph height must be an :ref:`type-int-float`, not {type(value).__name__}."
        )
    return value


def normalizeGlyphBottomMargin(value: Optional[IntFloatType]) -> Optional[IntFloatType]:
    """Normalize a glyph's bottom margin.

    :param value: The glyph bottom margin to normalize as
        an :class:`int`, :class:`float`, or :obj:`None`.
    :return: The normalized glyph bottom margin, of the same type as `value`.
    :raises TypeError: if `value` is not an :class:`int` or a :class:`float`.

    """
    if not isinstance(value, (int, float)) and value is not None:
        raise TypeError(
            f"Glyph bottom margin must be an :ref:`type-int-float`, not {type(value).__name__}."
        )
    return value


def normalizeGlyphTopMargin(value: Optional[IntFloatType]) -> Optional[IntFloatType]:
    """Normalize a glyph's top margin.

    :param value: The glyph top margin to normalize as
        an :class:`int`, :class:`float`, or :obj:`None`.
    :return: The normalized glyph top margin, of the same type as `value`.
    :raises TypeError: If `value` is not an :class:`int` or a :class:`float`.

    """
    if not isinstance(value, (int, float)) and value is not None:
        raise TypeError(
            f"Glyph top margin must be an :ref:`type-int-float`, not {type(value).__name__}."
        )
    return value


def normalizeGlyphFormatVersion(value: IntFloatType) -> int:
    """Normalize a glyph's format version for saving to XML string.

    :param value: The format version to normalize as
        an :class:`int` or a :class:`float` equal to either ``1`` or ``2``.
    :return: An :class:`int` representing the normalized glyph format version.
    :raises TypeError: If `value` is not an :class:`int` or a :class:`float`.
    :raises ValueError: If `value` is not equal to ``1`` or ``2``.

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


def normalizeContour(value: BaseContour) -> BaseContour:
    """Normalize a contour.

    :param value: The contour to normalize as an instance of :class:`BaseContour`.
    :return: The normalized :class:`BaseContour` instance.
    :raises TypeError: If `value` is not an instance of :class:`BaseContour`.

    """
    from fontParts.base.contour import BaseContour

    return normalizeInternalObjectType(value, BaseContour, "Contour")


# -----
# Point
# -----


def normalizePointType(value: str) -> str:
    """Normalize a point type.

    :param value: The point type to normalize as a :class:`str` containing one
        of the following values:

        +----------------+---------------------------------------------------+
        | Value          | Description                                       |
        +----------------+---------------------------------------------------+
        | ``'move'``     | The first point in an open contour.               |
        | ``'line'``     | A straight line from the previous point.          |
        | ``'offcurve'`` | A control point in a curve or qcurve.             |
        | ``'curve'``    | A cubic Bézier curve from the previous point.     |
        | ``'qcurve'``   | A quadratic Bézier curve from the previous point. |
        +----------------+---------------------------------------------------+

    :return: A :class:`str` representing the normalized point type.
    :raises TypeError: If `value` is not a :class:`str`.
    :raises ValueError: If `value` is not one of the allowed types.

    """
    allowedTypes = ["move", "line", "offcurve", "curve", "qcurve"]
    if not isinstance(value, str):
        raise TypeError(f"Point type must be a string, not {type(value).__name__}.")
    if value not in allowedTypes:
        raise ValueError(
            "Point type must be '%s'; not %r." % ("', '".join(allowedTypes), value)
        )
    return value


def normalizePointName(value: str) -> str:
    """Normalize a point name.

    :param value: The point name to normalize as a non-empty :class:`str`.
    :return: A :class:`str` representing the normalized point name.
    :raises TypeError: If `value` is not a :class:`str`.
    :raises ValueError: If `value` is an empty :class:`str`.

    """
    if not isinstance(value, str):
        raise TypeError(f"Point names must be strings, not {type(value).__name__}.")
    if len(value) < 1:
        raise ValueError("Point names must be at least one character long.")
    return value


def normalizePoint(value: BasePoint) -> BasePoint:
    """Normalize a point.

    :param value: The contour to normalize as an instance of :class:`BasePoint`.
    :return: The normalized :class:`BasePoint` instance.
    :raises TypeError: If `value` is not an instance of :class:`BasePoint`.

    """
    from fontParts.base.point import BasePoint

    return normalizeInternalObjectType(value, BasePoint, "Point")


# -------
# Segment
# -------


def normalizeSegment(value: BaseSegment) -> BaseSegment:
    """Normalize a segment.

    :param value: The contour to normalize as an instance of :class:`BaseSegment`.
    :return: The normalized :class:`BaseSegment` instance.
    :raises TypeError: If `value` is not an instance of :class:`BaseSegment`.

    """
    from fontParts.base.segment import BaseSegment

    return normalizeInternalObjectType(value, BaseSegment, "Segment")


def normalizeSegmentType(value: str) -> str:
    """Normalize a segment type.

    :param value: The segment type to normalize as a :class:`str` containing one
        of the following values:

        +--------------+-------------------------------------------------+
        | Value        | Description                                     |
        +--------------+-------------------------------------------------+
        | ``'move'``   | The start of an open contour.                   |
        | ``'line'``   | A straight segment between two on-curve points. |
        | ``'curve'``  | A cubic Bézier curve segment.                   |
        | ``'qcurve'`` | A quadratic Bézier curve segment.               |
        +--------------+-------------------------------------------------+

    :return: A :class:`str` representing the normalized segment type.
    :raises TypeError: If `value` is not a :class:`str`.
    :raises ValueError: If `value` is not one of the allowed types.

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


def normalizeBPoint(value: BaseBPoint) -> BaseBPoint:
    """Normalize a bPoint.

    :param value: The contour to normalize as an instance of :class:`BaseBPoint`.
    :return: The normalized :class:`BaseBPoint` instance.
    :raises TypeError: If `value` is not an instance of :class:`BaseBPoint`.

    """
    from fontParts.base.bPoint import BaseBPoint

    return normalizeInternalObjectType(value, BaseBPoint, "bPoint")


def normalizeBPointType(value: str) -> str:
    """Normalize a bPoint type.

    :param value: The bPoint type to normalize as a :class:`str` containing one
        of the following values:

        +--------------+---------------------------------------------------------+
        | Value        | Description                                             |
        +--------------+---------------------------------------------------------+
        | ``'curve'``  | A point where bcpIn and bcpOut are smooth (linked).     |
        | ``'corner'`` | A point where bcpIn and bcpOut are not smooth (linked). |
        +--------------+---------------------------------------------------------+

    :return: A :class:`str` representing the normalized bPoint type.
    :raises TypeError: If `value` is not a :class:`str`.
    :raises ValueError: If `value` is not one of the allowed types.

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


def normalizeComponent(value: BaseComponent) -> BaseComponent:
    """Normalize a component.

    :param value: The contour to normalize as an instance of :class:`BaseComponent`.
    :return: The normalized :class:`BaseComponent` instance.
    :raises TypeError: If `value` is not an instance of :class:`BaseComponent`.

    """
    from fontParts.base.component import BaseComponent

    return normalizeInternalObjectType(value, BaseComponent, "Component")


def normalizeComponentScale(value: PairCollectionType[IntFloatType]) -> PairType[float]:
    """Normalize a component scale.

    :param value: The component scale to noramlize as a :class:`list`
        or :class:`tuple` of two :class:`int` or :class:`float` values.
    :return: A :class:`tuple` of two :class:`float` values representing the
        normalized component scale.

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
        value = tuple(float(v) for v in value)
    return value


# ------
# Anchor
# ------


def normalizeAnchor(value: BaseAnchor) -> BaseAnchor:
    """Normalize an anchor.

    :param value: The contour to normalize as an instance of :class:`BaseAnchor`.
    :return: The normalized :class:`BaseAnchor` instance.
    :raises TypeError: If `value` is not an instance of :class:`BaseAnchor`.

    """
    from fontParts.base.anchor import BaseAnchor

    return normalizeInternalObjectType(value, BaseAnchor, "Anchor")


def normalizeAnchorName(value: str) -> str:
    """Normalize an anchor name.

    :param value: The anchor name to normalize as a non-empty :class:`str`,
        or :obj:`None`.
    :return: A :class:`str` representing the normalized anchor name, or :obj:`None`.
    :raises TypeError: If `value` is not a :class:`str` or :obj:`None`.
    :raises ValueError: If `value` is an empty :class:`str`.

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


def normalizeGuideline(value: BaseGuideline) -> BaseGuideline:
    """Normalize a guideline.

    :param value: The contour to normalize as an instance of :class:`BaseGuideline`.
    :return: The normalized :class:`BaseGuideline` instance.
    :raises TypeError: If `value` is not an instance of :class:`BaseGuideline`.

    """
    from fontParts.base.guideline import BaseGuideline

    return normalizeInternalObjectType(value, BaseGuideline, "Guideline")


def normalizeGuidelineName(value: str) -> str:
    """Normalize a guideline name.

    :param value: The guideline name to normalize as a non-empty :class:`str`
    :return: A :class:`str` representing the normalized guideline name.
    :raises TypeError: If `value` is not a :class:`str`.
    :raises ValueError: If `value` is an empty :class:`str`.

    """
    if not isinstance(value, str):
        raise TypeError(f"Guideline names must be strings, not {type(value).__name__}.")
    if len(value) < 1:
        raise ValueError("Guideline names must be at least one character " "long.")
    return value


# -------
# Generic
# -------


def normalizeInternalObjectType(value: object, cls: Type[T], name: str) -> T:
    """Normalize an internal object type.

    :param value: The object instance to normalize.
    :param cls: The class against which to check the type of `value`.
    :param name: The name of the variable being checked (for error messages).
    :return: The normalized object, of the same type as `value`.
    :raise TypeError: If `value` is not an instance of `cls`.

    """
    if not isinstance(value, cls):
        raise TypeError(
            f"{name} must be a {name} instance, not {type(value).__name__}."
        )
    return value


def normalizeBoolean(value: int) -> bool:
    """Normalize a boolean.

    :param value: The boolean to normalize as an :class:`int` of ``0`` or
        ``1``, or a :class:`bool`.
    :return: A :class:`bool` representing the normalized value.
    :raise ValueError: If `value` is not a valid :class:`bool` or :class:`int`.

    """
    if isinstance(value, int) and value in (0, 1):
        value = bool(value)
    if not isinstance(value, bool):
        raise ValueError(f"Boolean values must be True or False, not '{value}'.")
    return value


# Identification


def normalizeIndex(value: Optional[int]) -> Optional[int]:
    """Normalize an index.

    :param value: The index to normalize as an :class:`int`, or :obj:`None`.
    :return: The normalized index, of the same type as `value`.
    :raise ValueError: If `value` is not an :class:`int` or :obj:`None`.

    """
    if value is not None:
        if not isinstance(value, int):
            raise TypeError(
                f"Indexes must be None or integers, not {type(value).__name__}."
            )
    return value


def normalizeIdentifier(value: Optional[str]) -> Optional[str]:
    """Normalize an identifier.

    :param value: The identifier to normalize as a non-empty :class:`str`,
        or :obj:`None`. The value:
        - must not be longer than 100 characters.
        - must not contain a character out of the range ``0x20`` - ``0x7E``.
    :return: The normalized identifier, of the same type as `value`.
    :raises TypeError: If `value` is not a :class:`str` or :obj:`None`.
    :raises ValueError:
        - If `value` is an empty :class:`str`.
        - If `value` is longer than 100 characters.
        - If `value` contains a character outside the range ``0x20`` - ``0x7E``.

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
                f"The identifier string ('{value}') contains a character outside of the range 0x20 - 0x7E."
            )
    return value


# Coordinates


def normalizeX(value: IntFloatType) -> IntFloatType:
    """Normalize an x-coordinate.

    :param value: The x-coordinate to normalize as an :class:`int` or :class:`float`.
    :return: The normalized glyph top margin, of the same type as `value`.
    :raises TypeError: If `value` is not an :class:`int` or a :class:`float`.

    """
    if not isinstance(value, (int, float)):
        raise TypeError(
            f"X-coordinates must be instances of :ref:`type-int-float`, not {type(value).__name__}."
        )
    return value


def normalizeY(value: IntFloatType) -> IntFloatType:
    """Normalize a y-coordinate.

    :param value: The y-coordinate to normalize as an :class:`int` or :class:`float`.
    :return: The normalized glyph top margin, of the same type as `value`.
    :raises TypeError: If `value` is not an :class:`int` or a :class:`float`.

    """
    if not isinstance(value, (int, float)):
        raise TypeError(
            f"Y-coordinates must be instances of :ref:`type-int-float`, not {type(value).__name__}."
        )
    return value


def normalizeCoordinateTuple(
    value: PairCollectionType[IntFloatType],
) -> PairType[IntFloatType]:
    """Normalize a coordinate tuple.

    :param value: The coordinate tuple to noramlize as a :class:`list`
        or :class:`tuple` of two :class:`int` or :class:`float` values.
    :return: :return: A :class:`tuple` of two values of the same type as the
         items in `value`, representing the normalized coordinates.
    :raises TypeError: If `value` is not a :class:`list` or :class:`tuple`.
    :raises ValueError: If `value` does not contain exactly two items.

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


def normalizeBoundingBox(
    value: QuadrupleCollectionType[IntFloatType],
) -> QuadrupleType[float]:
    """Normalize a bounding box.

    :param value: The bounding box to normalize as a :class:`list`
        or :class:`tuple` of four :class:`int` or :class:`float` values
        representing the coordinates (in order) xMin, yMin, xMax, and yMax. The
        xMin and yMin values must be less than or equal to the corresponding xMax,
        yMax values.
    :return: A :class:`tuple` of four :class:`float` values representing the
        normalized bounding box.
    :raises TypeError:
        - If `value` is not a :class:`tuple` or :class:`list`.
        - If any `value` item is not an :class:`int` or a :class:`float`.
    :raises ValueError:
        - If `value` does not contain exactly four items.
        - If xMin is greater than xMax.
        - If yMin is greater than yMax.

    """
    if not isinstance(value, (tuple, list)):
        raise TypeError(
            f"Bounding box must be tuple instances, not {type(value).__name__}."
        )
    if len(value) != 4:
        raise ValueError(
            f"Bounding box must be tuples containing four items, not {len(value)}."
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


def normalizeArea(value: IntFloatType) -> float:
    """Normalize an area.

    :param value: The area to normalize as a positive :class:`int` or :class:`float`.
    :return: A positive :class:`float` representing the normalized area.
    :raises TypeError: If `value` is not an :class:`int` or a :class:`float`.
    :raises ValueError: If `value` is not a positive value.

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


def normalizeRotationAngle(value: IntFloatType) -> float:
    """Normalize an angle.

    :param value: The angle to normalize as an :class:`int` or a :class:`float`
        between ``-360 and ``360``. If the value is negative, it is normalized by
        adding it to ``360``.
    :return: A :class:`float` between ``0.0`` and ``360.0`` representing the
        normalized rotation angle.
    :raises TypeError: If `value` is not an :class:`int` or a :class:`float`.
    :raises ValueError: If `value` is not between ``-360 and ``360``.

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


def normalizeColor(
    value: QuadrupleCollectionType[IntFloatType],
) -> QuadrupleType[float]:
    """Normalize a color.

    :param value: The color to normalize as a :class:`list` or :class:`tuple`
        of four :class:`int` or :class:`float` values between ``0`` and ``1``,
        corresponding to the red, green, blue, and alpha (RGBA) channels, in that
        order.
    :return: A :class:`tuple` of four :class:`float` values representing the
        noramlized color.
    :raises TypeError:
        - If `value` is not a :class:`list` or :class:`tuple`.
        - If any `value` item is not an :class:`int` or a :class:`float`.
    :raises ValueError:
        - If `value` does not contain exactly four items.
        - If any `value` item is not between ``0`` and ``1``.

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
    return tuple(float(v) for v in value)


# Note


def normalizeGlyphNote(value: str) -> str:
    """Normalize a glyph note.

    :param value: The glyph note to normalize as a :class:`str`.
    :return: A :class:`str` representing the noramlized glyph note.
    :raises TypeError if `value` is not a :class:`str`.

    """
    if not isinstance(value, str):
        raise TypeError(f"Note must be a string, not {type(value).__name__}.")
    return value


# File Path


def normalizeFilePath(value: Union[str, Path]) -> str:
    """Normalize a file path.

    :param value: The file path to normalize as a :class:`str` or :class:`pathlib.Path`.
    :return: A :class:`str` representing the normalized file path.
    :raises TypeError if `value` is not a :class:`str` or :class:`pathlib.Path`.
    :raises FileNotFoundError: If the file path cannot be resolved because it does not exist.

    """
    if not isinstance(value, (str, Path)):
        raise TypeError(
            f"File paths must be strings or Path objects, not {type(value).__name__}."
        )
    return str(value)


# Interpolation


def normalizeInterpolationFactor(value: TransformationType) -> PairType[float]:
    """Normalize an interpolation factor.

    :param value: The interpolation factor to normalize as a single :class:`int`
        or :class:`float`, or a :class:`tuple` or :class:`list` of
        two :class:`int` or :class:`float` values.
    :return: A :class:`tuple` of two :class:`float` values representing the
        normalized interpolation factor.
    :raises TypeError:
        - If `value` is not an :class:`int`, :class:`float`, :class:`tuple`,
          or :class:`list`.
        - If any `value` item is not an :class:`int` or a :class:`float`.
    :raises ValueError:
        - If `value` is a :class:`tuple` or :class:`list` and does not contain
          exactly two items.

    """
    if not isinstance(value, (int, float, list, tuple)):
        raise TypeError(
            f"Interpolation factor must be an int, float, tuple, or list, not {type(value).__name__}."
        )
    if isinstance(value, (int, float)):
        value = (float(value), float(value))
    else:
        if len(value) != 2:
            raise ValueError(
                f"Interpolation factor tuple must contain two items, not {len(value)}."
            )
        for v in value:
            if not isinstance(v, (int, float)):
                raise TypeError(
                    f"Interpolation factor tuple values must be instances of int or float, not {type(v).__name__}."
                )
        value = tuple(float(v) for v in value)
    return value


# ---------------
# Transformations
# ---------------


def normalizeTransformationMatrix(
    value: SextupleCollectionType[IntFloatType],
) -> SextupleType[float]:
    """Normalize a transformation matrix.

    :param value: The transformation matrix to normalize as a :class:`list`
        or :class:`tuple` of six :class:`int` or :class:`float` values.
    :return: A :class:`tuple` of six :class:`float` values representing the
        normalized transformation matrix.
    :raises TypeError:
        - If `value` is not a :class:`tuple` or :class:`list`.
        - If any `value` item is not an :class:`int` or a :class:`float`.
    :raises ValueError: If `value` does not contain exactly six items.

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
    return tuple(float(v) for v in value)


def normalizeTransformationOffset(
    value: PairCollectionType[IntFloatType],
) -> PairType[IntFloatType]:
    """Normalize a transformation offset.

    :param value: The transformation offset to normalize as a :class:`list`
        or :class:`tuple` of two :class:`int` or :class:`float` values.
    :return: A :class:`tuple` of two :class:`float` values representing the
        normalized transformation offset.
    :raises TypeError:
        - If `value` is not a :class:`tuple`.
        - If any `value` item is not an :class:`int` or a :class:`float`.
    :raises ValueError: If `value` does not contain exactly two items.

    """
    return normalizeCoordinateTuple(value)


def normalizeTransformationSkewAngle(value: TransformationType) -> PairType[float]:
    """Normalize a transformation skew angle.

    :param value: The skew angle to normalize as a single :class:`int`
     or :class:`float`, or a :class:`tuple` or :class:`list` of
     two :class:`int` or :class:`float` values. Each value must be
     between ``-360 and ``360``. If the value is negative, it is normalized by
     adding it to ``360``.
    :return: A :class:`tuple` of two :class:`float` values between ``0.0`` and
        ``360.0`` representing the normalized skew angle.
    :raises TypeError:
        - If `value` is not an :class:`int`, :class:`float`, :class:`tuple`,
          or :class:`list`.
        - If any `value` item is not an :class:`int` or a :class:`float`.
    :raises ValueError:
        - If `value` is a :class:`tuple` or :class:`list` and does not contain
          exactly two items.
    :raises ValueError:
        - If `value` does not contain exactly two items.
        - If any `value` item is not between ``-360`` and ``360``.

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
        value = tuple(float(v) for v in value)
    for v in value:
        if abs(v) > 360:
            raise ValueError(
                "Transformation skew angle must be between -360 " "and 360."
            )
    return tuple(float(v + 360) if v < 0 else float(v) for v in value)


def normalizeTransformationScale(value: TransformationType) -> PairType[float]:
    """Normalize a transformation scale.

    :param value: The scale to normalize as a single :class:`int`
        or :class:`float`, or a :class:`tuple` or :class:`list` of
        two :class:`int` or :class:`float` values.
    :return: A :class:`tuple` of two :class:`float` values representing the
        normalized scale.
    :raises TypeError:
        - If `value` is not an :class:`int`, :class:`float`, :class:`tuple`,
          or :class:`list`.
        - If any `value` item is not an :class:`int` or a :class:`float`.
    :raises ValueError:
        - If `value` is a :class:`tuple` or :class:`list` and does not contain
          exactly two items.

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
        value = tuple(float(v) for v in value)
    return value


def normalizeVisualRounding(value: IntFloatType) -> int:
    """Normalize rounding.

    Python 3 uses banker’s rounding, meaning anything that is at 0.5 will round
    to the nearest even number. This isn't always ideal for point coordinates,
    so instead, this function rounds to the higher number
    with :func:`fontTools.misc.roundTools.otRound`.

    :param value: The value to round as an :class:`int` or a :class:`float`.
    :return: An :class:`int` representing the normalized rounding.
    :raises TypeError: If `value` is not an :class:`int` or a :class:`float`.

    """
    if not isinstance(value, (int, float)):
        raise TypeError(
            f"Value to round must be an int or float, not {type(value).__name__}."
        )
    return otRound(value)
