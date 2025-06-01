from __future__ import annotations
from typing import Tuple, Dict, ItemsView

import defcon
from fontParts.base import BaseGroups
from fontParts.base.annotations import CollectionType
from fontParts.fontshell.base import RBaseObject

ValueType = Tuple[str, ...]
GroupsDict = Dict[str, ValueType]


class RGroups(RBaseObject, BaseGroups):
    wrapClass = defcon.Groups

    def _get_side1KerningGroups(self) -> GroupsDict:
        groups = self.naked()
        representation = groups.getRepresentation("defcon.groups.kerningSide1Groups")
        return {k: tuple(v) for k, v in representation.items()}

    def _get_side2KerningGroups(self) -> GroupsDict:
        groups = self.naked()
        representation = groups.getRepresentation("defcon.groups.kerningSide2Groups")
        return {k: tuple(v) for k, v in representation.items()}

    def _items(self) -> ItemsView[str, Tuple[str]]:
        groups = self.naked()
        formatted = {k: tuple(v) for k, v in groups.items()}
        return formatted.items()

    def _contains(self, key: str) -> bool:
        groups = self.naked()
        return key in groups

    def _setItem(self, key: str, value: CollectionType[str]) -> None:
        groups = self.naked()
        groups[key] = tuple(value)

    def _getItem(self, key: str) -> Tuple[str]:
        groups = self.naked()
        return tuple(groups[key])

    def _delItem(self, key: str) -> None:
        groups = self.naked()
        del groups[key]
