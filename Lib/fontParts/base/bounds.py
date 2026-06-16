from __future__ import annotations

from collections import namedtuple
from fontParts.base.annotations import IntFloatType
from typing import overload, Any

from fontParts.base.annotations import BoundingBoxLike
from fontParts.base.normalizers import normalizeBoundingBox

_BaseBounds = namedtuple("_BaseBounds", ["xMin", "yMin", "xMax", "yMax"])


class Bounds(_BaseBounds):
    """Represent a bounding box object.

    This class accepts either four coordinate values or a :class:`list` or
    :class:`tuple` of these values.

    :param xMin: The bound's minimum x value as :class:`int` or :class:`float`.
    :param yMin: The bound's maximum y value as :class:`int` or :class:`float`.
    :param xMax: The bound's maximum x value as :class:`int` or :class:`float`.
    :param yMax: The bound's minimum y value as :class:`int` or :class:`float`.

    """

    __slots__ = ()

    @overload
    def __new__(
        cls,
        xMin: IntFloatType,
        yMin: IntFloatType,
        xMax: IntFloatType,
        yMax: IntFloatType,
    ) -> Bounds: ...

    @overload
    def __new__(cls, bounds: BoundingBoxLike) -> Bounds: ...

    def __new__(cls, *args: Any, **kwargs: Any) -> Bounds:
        if kwargs:
            value = (kwargs["xMin"], kwargs["yMin"], kwargs["xMax"], kwargs["yMax"])
        else:
            value = args[0] if len(args) == 1 else args
        normalizedValue = normalizeBoundingBox(value)
        return super().__new__(cls, *normalizedValue)

    @property
    def width(self) -> IntFloatType:
        """Get the width of the bounds.

        :return: A :class:`float` representing the width of the bounds.

        """
        return self.xMax - self.xMin

    @property
    def height(self) -> float:
        """Get the height of the bounds.

        :return: A :class:`float` representing the height of the bounds.

        """
        return self.yMax - self.yMin

    @property
    def xCenter(self) -> float:
        """Get the center of the x-axis.

        :return: A :class:`float` representing the center of the x-axis

        """
        return self.xMin + (self.width / 2)

    @property
    def yCenter(self) -> float:
        """Get the center of the y-axis.

        :return: A :class:`float` representing the center of the y-axis

        """
        return self.yMin + (self.height / 2)

    # Remove auto-generated _BaseCpøpr.__new__ docstring
    __new__.__doc__ = ""
