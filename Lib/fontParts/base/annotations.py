# pylint: disable=C0103, C0114
from __future__ import annotations
from typing import Dict, List, Protocol, Tuple, TypeVar, Union
import datetime

from fontTools.pens.basePen import AbstractPen
from fontTools.pens.pointPen import AbstractPointPen

# Generic
T = TypeVar("T")

PairType = Tuple[T, T]
QuadrupleType = Tuple[T, T, T, T]
QuintupleType = Tuple[T, T, T, T, T]
SextupleType = Tuple[T, T, T, T, T, T]
CollectionType = Union[List[T], Tuple[T, ...]]
PairCollectionType = Union[List[T], PairType[T]]
QuadrupleCollectionType = Union[List[T], QuadrupleType[T]]
SextupleCollectionType = Union[List[T], SextupleType[T]]

# Builtins
IntFloatType = Union[int, float]

# Pens
PenType = AbstractPen
PointPenType = AbstractPointPen

# Mapping
CharacterMappingType = Dict[int, Tuple[str, ...]]
ReverseComponentMappingType = Dict[str, Tuple[str, ...]]

# Kerning
KerningDictType = Dict[PairType[str], PairType[str]]

# Lib
LibValueType = Union[
    str,
    IntFloatType,
    bool,
    CollectionType["LibValueType"],
    Dict[str, "LibValueType"],
    bytes,
    bytearray,
    datetime.datetime,
]

class LibValue:
    # Documentation class for LibValueType
    """A :class:`~fontParts.base.BaseLib` value may be one of the following 
    *non-collection* types:

    - :class:`str` 
    - :class:`int` 
    - :class:`float` 
    - :class:`bool`
    - :class:`bytes`,
    - :class:`bytearray` 
    - :class:`datetime.datetime`

    In addition, a value may also be a :class:`list` or :class:`tuple` containing any of 
    the types above, or a :class:`dict` mapping :class:`str` keys to values of those 
    same types (including nested lists, tuples, or dicts).

    """

# Transformation
TransformationType = Union[IntFloatType, List[IntFloatType], PairType[IntFloatType]]

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
