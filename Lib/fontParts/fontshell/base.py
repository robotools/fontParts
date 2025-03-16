from __future__ import annotations
from typing import Generic, Optional, Type, TypeVar

RBaseObjectType = TypeVar("RBaseObjectType", bound="RBaseObject")


class RBaseObject(Generic[RBaseObjectType]):
    wrapClass: Optional[Type[RBaseObjectType]] = None
    dirty: bool

    def _init(self, pathOrObject: Optional[RBaseObjectType] = None) -> None:
        if pathOrObject is not None:
            self._wrapped = pathOrObject
        if self.wrapClass is not None:
            pathOrObject = self.wrapClass()

    def changed(self) -> None:
        naked = self.naked()
        if naked is not None:
            naked.dirty = True

    def naked(self) -> Optional[RBaseObjectType]:
        if hasattr(self, "_wrapped"):
            return self._wrapped
        return None
