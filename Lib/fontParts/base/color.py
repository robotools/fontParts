from __future__ import annotations
from typing import Union

from fontParts.base.normalizers import normalizeColor
from fontParts.base.annotations import IntFloatType, QuadrupleCollectionType


class Color(tuple):
    """Represent a color object following the :ref:`type-color`.

    This class takes either individual RGBA component values or a :class:`list`
    or :class:`tuple` of values.

    """

    def __new__(
        cls, *args: Union[IntFloatType, QuadrupleCollectionType[IntFloatType]]
    ) -> Color:
        value = args[0] if len(args) == 1 else args
        normalizedValue = normalizeColor(value)  # type: ignore[arg-type]

        return super().__new__(cls, normalizedValue)

    def __repr__(self):
        return (
            f"<{__class__.__name__} r={self.r}, g={self.g}, "
            f"b={self.b}, a={self.a} at {id(self)}>"
        )

    @property
    def r(self) -> IntFloatType:
        """The color's red component as an :class:`int` or a :class:`float`."""
        return self[0]

    @property
    def g(self) -> IntFloatType:
        """The color's green component as an :class:`int` or a :class:`float`."""
        return self[1]

    @property
    def b(self) -> IntFloatType:
        """The color's blue component as an :class:`int` or a :class:`float`."""
        return self[2]

    @property
    def a(self) -> IntFloatType:
        """The color's alpha component as an :class:`int` or a :class:`float`."""
        return self[3]
