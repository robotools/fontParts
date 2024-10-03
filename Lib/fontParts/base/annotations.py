# pylint: disable=C0103, C0114

from __future__ import annotations

from typing import Dict, List, Tuple, TypeVar, Union

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
FactorType = Union[IntFloatType, Tuple[float, float]]
KerningKeyType = Tuple[str, str]
KerningDictType = Dict[KerningKeyType, IntFloatType]
ReverseComponentMappingType = Dict[str, Tuple[str, ...]]
ScaleType = Tuple[IntFloatType, IntFloatType]
TransformationMatrixType = Tuple[
    IntFloatType, IntFloatType, IntFloatType,
    IntFloatType, IntFloatType, IntFloatType
]
