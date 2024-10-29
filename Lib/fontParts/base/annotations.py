# pylint: disable=C0103, C0114
<<<<<<< HEAD
=======

>>>>>>> v1
from __future__ import annotations
from typing import Dict, List, Protocol, Tuple, TypeVar, Union

from fontTools.pens.basePen import AbstractPen
from fontTools.pens.pointPen import AbstractPointPen

<<<<<<< HEAD
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
=======
# ------------
# Type Aliases
# ------------

# Builtins

T = TypeVar('T')
CollectionType = Union[List[T], Tuple[T, ...]]
IntFloatType = Union[int, float]

# FontTools

PenType = AbstractPen
PointPenType = AbstractPointPen

# FontParts

BoundsType = Tuple[IntFloatType, IntFloatType, IntFloatType, IntFloatType]
CharacterMappingType = Dict[int, Tuple[str, ...]]
ColorType = Tuple[IntFloatType, IntFloatType, IntFloatType, IntFloatType]
CoordinateType = Tuple[IntFloatType, IntFloatType]
FactorType = Union[IntFloatType, Tuple[IntFloatType, IntFloatType]]
InterpolatableType = TypeVar('InterpolatableType', bound='Interpolatable')
KerningKeyType = Tuple[str, str]
KerningDictType = Dict[KerningKeyType, IntFloatType]
ReverseComponentMappingType = Dict[str, Tuple[str, ...]]
ScaleType = Tuple[IntFloatType, IntFloatType]
TransformationMatrixType = Tuple[
    IntFloatType, IntFloatType, IntFloatType,
    IntFloatType, IntFloatType, IntFloatType
]
>>>>>>> v1


class Interpolatable(Protocol):
    """Represent a protocol for interpolatable types."""

<<<<<<< HEAD
    def __add__(self, other: InterpolatableType) -> InterpolatableType:
        ...

    def __sub__(self, other: InterpolatableType) -> InterpolatableType:
        ...

    def __mul__(self, other: TransformationType) -> InterpolatableType:
        ...
=======
    def __add__(self, other: InterpolatableType) -> InterpolatableType: ...
    def __sub__(self, other: InterpolatableType) -> InterpolatableType: ...
    def __mul__(self, other: FactorType) -> InterpolatableType: ...
>>>>>>> v1
