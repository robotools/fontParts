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

# Transformation
TransformationType = Union[IntFloatType, List[IntFloatType], PairType[IntFloatType]]

# Interpolation
InterpolatableType = TypeVar("InterpolatableType", bound="Interpolatable")


class Interpolatable(Protocol):
    """Represent a protocol for interpolatable types."""

    def __add__(self: InterpolatableType, other: InterpolatableType) -> InterpolatableType: ...

    def __sub__(self: InterpolatableType, other: InterpolatableType) -> InterpolatableType: ...

    def __mul__(self: InterpolatableType, other: TransformationType) -> InterpolatableType: ...
