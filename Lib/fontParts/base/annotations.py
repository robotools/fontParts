# pylint: disable=C0103, C0114
from __future__ import annotations
from typing import Dict, List, Protocol, Tuple, TypeVar, Union

from fontTools.pens.basePen import AbstractPen
from fontTools.pens.pointPen import AbstractPointPen

# Generic
T = TypeVar('T')

Pair = Tuple[T, T]
Quadruple = Tuple[T, T, T, T]
Sextuple = Tuple[T, T, T, T, T, T]
CollectionType = Union[List[T], Tuple[T, ...]]
PairCollectionType = Union[List[T], Pair[T]]
QuadrupleCollectionType = Union[List[T], Quadruple[T]]
SextupleCollectionType = Union[List[T], Sextuple[T]]

# Builtins
IntFloatType = Union[int, float]

# Pens
PenType = AbstractPen
PointPenType = AbstractPointPen

# Mapping
CharacterMappingType = Dict[int, Tuple[str, ...]]
ReverseComponentMappingType = Dict[str, Tuple[str, ...]]

# Transformation
TransformationType = Union[IntFloatType, List[IntFloatType], Pair[IntFloatType]]

# Interpolation
InterpolatableType = TypeVar('InterpolatableType', bound='Interpolatable')


class Interpolatable(Protocol):
    """Represent a protocol for interpolatable types."""

    def __add__(self, other: InterpolatableType) -> InterpolatableType:
        ...

    def __sub__(self, other: InterpolatableType) -> InterpolatableType:
        ...

    def __mul__(self, other: TransformationType) -> InterpolatableType:
        ...
