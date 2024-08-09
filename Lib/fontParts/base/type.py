from typing import Dict, Generic, Iterator, List, Set, Tuple, TypeVar, Union

from fontParts.base.info import BaseInfo
from fontParts.base.groups import BaseGroups
from fontParts.base.kerning import BaseKerning
from fontParts.base.features import BaseFeatures
from fontParts.base.lib import BaseLib
from fontParts.base.layer import BaseLayer
from fontParts.base.glyph import BaseGlyph
from fontParts.base.guideline import BaseGuideline

IntFloat = Union[int, float]
Color = Tuple[(IntFloat,) * 4]
Coordinate = Tuple[IntFloat, IntFloat]
TransformationMatrix = Tuple[(IntFloat,) * 6]
FontType = TypeVar('FontType', bound='BaseFont')
InfoType = TypeVar('InfoType', bound='BaseInfo')
GroupsType = TypeVar('GroupsType', bound='BaseGroups')
KerningType = TypeVar('KerningType', bound='BaseKerning')
FeaturesType = TypeVar('FeaturesType', bound='BaseFeatures')
LibType = TypeVar('LibType', bound='BaseLib')
LayerType = TypeVar('LayerType', bound='BaseLayer')
GlyphType = TypeVar('GlyphType', bound='BaseGlyph')
GuidelineType = TypeVar('GuidelineType', bound='BaseGuideline')
KerningKey = Tuple[str, str]
KerningDict = Dict[KerningKey, IntFloat]
ReverseComponentMapping = Dict[str, Set[str]]
CharacterMapping = Dict[int, List[str]]
