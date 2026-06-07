from __future__ import annotations
from collections import namedtuple
from typing import overload, Any

from fontParts.base.normalizers import normalizeColor
from fontParts.base.annotations import IntFloatType, RGBALike

_BaseColor = namedtuple("_BaseColor", ["r", "g", "b", "a"])


class Color(_BaseColor):
    """Represent a color object following the :ref:`type-color`.

    This class accepts either four RGBA component values or a :class:`list` or
    :class:`tuple` of these values.

    :param r: The color's red component as :class:`int` or :class:`float`.
    :param g: The color's green component as :class:`int` or :class:`float`.
    :param b: The color's blue component as :class:`int` or :class:`float`.
    :param a: The color's alpha component as :class:`int` or :class:`float`.

    """

    __slots__ = ()

    @overload
    def __new__(
        cls, r: IntFloatType, g: IntFloatType, b: IntFloatType, a: IntFloatType
    ) -> Color: ...

    @overload
    def __new__(cls, color: RGBALike) -> Color: ...

    def __new__(cls, *args: Any, **kwargs: Any) -> Color:
        if kwargs:
            value = (
                kwargs.get("r", 0),
                kwargs.get("g", 0),
                kwargs.get("b", 0),
                kwargs.get("a", 1),
            )

        else:
            value = args[0] if len(args) == 1 else args
        normalizedValue = normalizeColor(value)  # type: ignore[arg-type]
        return super().__new__(cls, *normalizedValue)

    # Remove auto-generated _BaseCpøpr.__new__ docstring
    __new__.__doc__ = ""
