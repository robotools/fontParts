# pylint: disable=C0103, C0114

from __future__ import annotations
from typing import Dict, List, Protocol, Tuple, TypeVar, Union

from fontTools.pens.basePen import AbstractPen
from fontTools.pens.pointPen import AbstractPointPen

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


class Interpolatable(Protocol):
    """Represent a protocol for interpolatable types."""

    def __add__(self, other: TInterpolatable) -> TInterpolatable: ...
    def __sub__(self, other: TInterpolatable) -> TInterpolatable: ...
    def __mul__(self, other: FactorType) -> TInterpolatable: ...
