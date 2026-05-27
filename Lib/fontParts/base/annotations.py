# pylint: disable=C0103, C0114
from __future__ import annotations

import datetime
from typing import Protocol, TypeVar

from fontTools.pens.basePen import AbstractPen
from fontTools.pens.pointPen import AbstractPointPen

# Generic
T = TypeVar("T")

PairType = tuple[T, T]
QuadrupleType = tuple[T, T, T, T]
QuintupleType = tuple[T, T, T, T, T]
SextupleType = tuple[T, T, T, T, T, T]
CollectionType = list[T] | tuple[T, ...]
PairCollectionType = list[T] | PairType[T]
QuadrupleCollectionType = list[T] | QuadrupleType[T]
SextupleCollectionType = list[T] | SextupleType[T]

# Builtins
IntFloatType = int | float

# Point / Offset / Anchor (bPoints)
Coordinate = tuple[IntFloatType, IntFloatType]
CoordinateLike = list[IntFloatType] | Coordinate

# Bounding box — (xMin, yMin, xMax, yMax).
BoundingBox = tuple[float, float, float, float]
BoundingBoxLike = list[IntFloatType] | BoundingBox

# RGBA color — (r, g, b, a) in [0, 1]
RGBA = tuple[float, float, float, float]
RGBALike = list[IntFloatType] | RGBA

# Affine transformation matrix — (xx, xy, yx, yy, dx, dy).
AffineTransformation = tuple[float, float, float, float, float, float]
AffineTransformationLike = list[IntFloatType] | AffineTransformation

# Kerning pair — (first, second) glyph or group names.
KerningPair = tuple[str, str]
KerningPairLike = list[str] | KerningPair

# Compatibility
DiffType = list[tuple[int, str | None, str | None]]

# Pens
PenType = AbstractPen
PointPenType = AbstractPointPen

# Mapping
CharacterMappingType = dict[int, tuple[str, ...]]
ReverseComponentMappingType = dict[str, tuple[str, ...]]

# Kerning
KerningDictType = dict[PairType[str], PairType[str]]

# Lib
LibValueType = (
    str
    | IntFloatType
    | bool
    | CollectionType["LibValueType"]
    | dict[str, "LibValueType"]
    | bytes
    | bytearray
    | datetime.datetime
)


class LibValue:
    # Documentation class for LibValueType
    """A :class:`~fontParts.base.BaseLib` value may be one of the following
    *non-collection* types:

    - :class:`str`
    - :class:`int`
    - :class:`float`
    - :class:`bool`
    - :class:`bytes`
    - :class:`bytearray`
    - :class:`datetime.datetime`

    In addition, a value may also be a :class:`list` or :class:`tuple` containing any of
    the types above, or a :class:`dict` mapping :class:`str` keys to values of those
    same types (including nested lists, tuples, or dicts).

    """


# Transformation
TransformationType = IntFloatType | list[IntFloatType] | PairType[IntFloatType]

# Interpolation
InterpolatableType = TypeVar("InterpolatableType", bound="Interpolatable")


class Interpolatable(Protocol):
    """Represent a protocol for interpolatable types."""

    def __add__(
        self: InterpolatableType, other: InterpolatableType
    ) -> InterpolatableType: ...

    def __sub__(
        self: InterpolatableType, other: InterpolatableType
    ) -> InterpolatableType: ...

    def __mul__(
        self: InterpolatableType, other: TransformationType
    ) -> InterpolatableType: ...
