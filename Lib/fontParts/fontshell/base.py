from __future__ import annotations
from typing import Generic, Optional, Type, TypeVar

RBaseObjectType = TypeVar("RBaseObjectType", bound="RBaseObject")


class RBaseObject(Generic[RBaseObjectType]):
    wrapClass: Optional[Type[RBaseObjectType]] = None
    dirty: bool

    def _init(self, pathOrObject: Optional[RBaseObjectType] = None) -> None:
        if pathOrObject is None and self.wrapClass is not None:
            pathOrObject = self.wrapClass()  # pylint: disable=E1102
        if pathOrObject is not None:
            self._wrapped = pathOrObject

    def changed(self) -> None:
        self.naked().dirty = True

    def naked(self) -> RBaseObjectType:
        if hasattr(self, "_wrapped"):
            return self._wrapped
        return None  # type: ignore[return-value]
