# pylint: disable=C0103, C0114
from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Dict, Iterator, List, Optional, Union
from collections.abc import MutableMapping

from fontMath import MathKerning
from fontMath.mathFunctions import setRoundIntegerFunction

from fontParts.base.base import BaseDict, dynamicProperty, interpolate, reference
from fontParts.base import normalizers
from fontParts.base.deprecated import DeprecatedKerning, RemovedKerning
from fontParts.base.annotations import (
    IntFloatType,
    PairType,
    PairCollectionType,
    TransformationType,
)

if TYPE_CHECKING:
    from fontParts.base.font import BaseFont
    from fontParts.base.base import BaseItems
    from fontParts.base.base import BaseKeys
    from fontParts.base.base import BaseValues


class BaseKerning(BaseDict, DeprecatedKerning, RemovedKerning):
    """
    A Kerning object. This object normally created as part of a
    :class:`BaseFont`. An orphan Kerning object can be created
    like this::

        >>> groups = RKerning()

    This object behaves like a Python dictionary. Most of the
    dictionary functionality comes from :class:`BaseDict`, look at
    that object for the required environment implementation details.

    Kerning uses :func:`normalizers.normalizeKerningKey` to normalize the
    key of the ``dict``, and :func:`normalizers.normalizeKerningValue`
    to normalize the the value of the ``dict``.
    """

    keyNormalizer = normalizers.normalizeKerningKey
    valueNormalizer = normalizers.normalizeKerningValue

    def _reprContents(self) -> List[str]:
        contents = []
        if self.font is not None:
            contents.append("for font")
            contents += self.font._reprContents()
        return contents

    # -------
    # Parents
    # -------

    # Font

    _font: Optional[Callable[[], BaseFont]] = None

    font: dynamicProperty = dynamicProperty(
        "font", "The Kerning's parent :class:`BaseFont`."
    )

    def _get_font(self) -> Optional[BaseFont]:
        if self._font is None:
            return None
        return self._font()

    def _set_font(self, font: Optional[Union[BaseFont, Callable[[], BaseFont]]]) -> None:
        if self._font is not None and self._font() != font:
            raise AssertionError("font for kerning already set and is not same as font")
        if font is not None:
            font = reference(font)
        self._font = font

    # --------------
    # Transformation
    # --------------

    def scaleBy(self, factor: TransformationType) -> None:
        """
        Scales all kerning values by **factor**. **factor** will be an
        :ref:`type-int-float`, ``tuple`` or ``list``. The first value of the
        **factor** will be used to scale the kerning values.

            >>> myKerning.scaleBy(2)
            >>> myKerning.scaleBy((2, 3))
        """
        factor = normalizers.normalizeTransformationScale(factor)
        self._scale(factor)

    def _scale(self, factor: PairType[float]) -> None:
        """
        This is the environment implementation of :meth:`BaseKerning.scaleBy`.
        **factor** will be a ``tuple``.

        Subclasses may override this method.
        """
        horizontalFactor = factor[0]
        for k, v in self.items():
            v *= horizontalFactor
            self[k] = v

    # -------------
    # Normalization
    # -------------

    def round(self, multiple: int = 1) -> None:
        """
        Rounds the kerning values to increments of **multiple**,
        which will be an ``int``.

        The default behavior is to round to increments of 1.
        """
        if not isinstance(multiple, int):
            raise TypeError(
                f"The round multiple must be an int not {multiple.__class__.__name__}."
            )
        self._round(multiple)

    def _round(self, multiple: int = 1) -> None:
        """
        This is the environment implementation of
        :meth:`BaseKerning.round`. **multiple** will be an ``int``.

        Subclasses may override this method.
        """
        for pair, value in self.items():
            value = (
                int(normalizers.normalizeVisualRounding(value / float(multiple)))
                * multiple
            )
            self[pair] = value

    # -------------
    # Interpolation
    # -------------

    def interpolate(
        self,
        factor: TransformationType,
        minKerning: MathKerning,
        maxKerning: MathKerning,

        round: bool = True,
        suppressError: bool = True,
    ) -> None:
        """
        Interpolates all pairs between two :class:`BaseKerning` objects:

            >>> myKerning.interpolate(kerningOne, kerningTwo)

        **minKerning** and **maxKerning**. The interpolation occurs on a
        0 to 1.0 range where **minKerning** is located at 0 and
        **maxKerning** is located at 1.0. The kerning data is replaced by
        the interpolated kerning.

        * **factor** is the interpolation value. It may be less than 0
          and greater than 1.0. It may be an :ref:`type-int-float`,
          ``tuple`` or ``list``. If it is a ``tuple`` or ``list``,
          the first number indicates the x factor and the second number
          indicates the y factor.
        * **round** is a ``bool`` indicating if the result should be rounded to
          ``int``\s. The default behavior is to round interpolated kerning.
        * **suppressError** is a ``bool`` indicating if incompatible data should
          be ignored or if an error should be raised when such incompatibilities
          are found. The default behavior is to ignore incompatible data.
        """
        factor = normalizers.normalizeInterpolationFactor(factor)
        if not isinstance(minKerning, BaseKerning):
            raise TypeError(
                f"Interpolation to an instance of {self.__class__.__name__!r} can not be performed from an instance of {minKerning.__class__.__name__!r}."
            )
        if not isinstance(maxKerning, BaseKerning):
            raise TypeError(
                f"Interpolation to an instance of {self.__class__.__name__!r} can not be performed from an instance of {maxKerning.__class__.__name__!r}."
            )
        round = normalizers.normalizeBoolean(round)
        suppressError = normalizers.normalizeBoolean(suppressError)
        self._interpolate(
            factor, minKerning, maxKerning, round=round, suppressError=suppressError
        )

    def _interpolate(
        self,
        factor: PairType[float],
        minKerning: BaseKerning,
        maxKerning: BaseKerning,
        round: bool = True,
        suppressError: bool = True,
    ) -> None:
        """
        This is the environment implementation of :meth:`BaseKerning.interpolate`.

        * **factor** will be an :ref:`type-int-float`, ``tuple`` or ``list``.
        * **minKerning** will be a :class:`BaseKerning` object.
        * **maxKerning** will be a :class:`BaseKerning` object.
        * **round** will be a ``bool`` indicating if the interpolated kerning
          should be rounded.
        * **suppressError** will be a ``bool`` indicating if incompatible data
          should be ignored.

        Subclasses may override this method.
        """
        setRoundIntegerFunction(normalizers.normalizeVisualRounding)
        kerningGroupCompatibility = self._testKerningGroupCompatibility(
            minKerning, maxKerning, suppressError=suppressError
        )
        if not kerningGroupCompatibility:
            self.clear()
        else:
            minMathKerning = MathKerning(
                kerning=minKerning, groups=minKerning.font.groups
            )
            maxMathKerning = MathKerning(
                kerning=maxKerning, groups=maxKerning.font.groups
            )
            result = interpolate(minMathKerning, maxMathKerning, factor)
            if round:
                result.round()
            self.clear()
            result.extractKerning(self.font)

    @staticmethod
    def _testKerningGroupCompatibility(
        minKerning: BaseKerning, maxKerning: BaseKerning, suppressError: bool = False
    ) -> bool:
        minGroups = minKerning.font.groups
        maxGroups = maxKerning.font.groups
        match = True
        while match:
            for _, sideAttr in (
                ("side 1", "side1KerningGroups"),
                ("side 2", "side2KerningGroups"),
            ):
                minSideGroups = getattr(minGroups, sideAttr)
                maxSideGroups = getattr(maxGroups, sideAttr)
                if minSideGroups.keys() != maxSideGroups.keys():
                    match = False
                else:
                    for name in minSideGroups.keys():
                        minGroup = minSideGroups[name]
                        maxGroup = maxSideGroups[name]
                        if set(minGroup) != set(maxGroup):
                            match = False
            break
        if not match and not suppressError:
            raise ValueError("The kerning groups must be exactly the same.")
        return match

    # ---------------------
    # RoboFab Compatibility
    # ---------------------

    def remove(self, pair: PairType[str]) -> None:
        """
        Removes a pair from the Kerning. **pair** will
        be a ``tuple`` of two :ref:`type-string`\s.

        This is a backwards compatibility method.
        """
        del self[pair]

    def asDict(self, returnIntegers: bool = True) -> Dict[PairType[str], IntFloatType]:
        """
        Return the Kerning as a ``dict``.

        This is a backwards compatibility method.
        """
        return {
            k: (v if not returnIntegers else normalizers.normalizeVisualRounding(v))
            for k, v in self.items()
        }

    # -------------------
    # Inherited Functions
    # -------------------

    def __contains__(self, pair: PairType[str]) -> bool:
        """
        Tests to see if a pair is in the Kerning.
        **pair** will be a ``tuple`` of two :ref:`type-string`\s.

        This returns a ``bool`` indicating if the **pair**
        is in the Kerning. ::

            >>> ("A", "V") in font.kerning
            True
        """
        return super(BaseKerning, self).__contains__(pair)

    def __delitem__(self, pair: PairType[str]) -> None:
        """
        Removes **pair** from the Kerning. **pair** is a ``tuple`` of two
        :ref:`type-string`\s.::

            >>> del font.kerning[("A","V")]
        """
        super(BaseKerning, self).__delitem__(pair)

    def __getitem__(self, pair: PairType[str]) -> float:
        """
        Returns the kerning value of the pair. **pair** is a ``tuple`` of
        two :ref:`type-string`\s.

        The returned value will be a :ref:`type-int-float`.::

            >>> font.kerning[("A", "V")]
            -15

        It is important to understand that any changes to the returned value
        will not be reflected in the Kerning object. If one wants to make a change to
        the value, one should do the following::

            >>> value = font.kerning[("A", "V")]
            >>> value += 10
            >>> font.kerning[("A", "V")] = value
        """
        return super(BaseKerning, self).__getitem__(pair)

    def __iter__(self) -> Iterator[PairType[str]]:
        """
        Iterates through the Kerning, giving the pair for each iteration. The order that
        the Kerning will iterate though is not fixed nor is it ordered.::

            >>> for pair in font.kerning:
            >>>     print pair
            ("A", "Y")
            ("A", "V")
            ("A", "W")
        """
        return super(BaseKerning, self).__iter__()

    def __len__(self) -> int:
        """
        Returns the number of pairs in Kerning as an ``int``.::

            >>> len(font.kerning)
            5
        """
        return super(BaseKerning, self).__len__()

    def __setitem__(self, pair, value: IntFloatType) -> None:
        """
        Sets the **pair** to the list of **value**. **pair** is the
        pair as a ``tuple`` of two :ref:`type-string`\s and **value**

        is a :ref:`type-int-float`.

            >>> font.kerning[("A", "V")] = -20
            >>> font.kerning[("A", "W")] = -10.5
        """
        super(BaseKerning, self).__setitem__(pair, value)

    def clear(self) -> None:
        """
        Removes all information from Kerning,
        resetting the Kerning to an empty dictionary. ::

            >>> font.kerning.clear()
        """
        super(BaseKerning, self).clear()

    def get(
        self, pair: PairType[str], default: Optional[IntFloatType] = None
    ) -> Optional[IntFloatType]:
        """
        Returns the value for the kerning pair.
        **pair** is a ``tuple`` of two :ref:`type-string`\s, and the returned
        values will either be :ref:`type-int-float` or ``None``
        if no pair was found. ::

            >>> font.kerning[("A", "V")]
            -25

        It is important to understand that any changes to the returned value
        will not be reflected in the Kerning object. If one wants to make a change to
        the value, one should do the following::

            >>> value = font.kerning[("A", "V")]
            >>> value += 10
            >>> font.kerning[("A", "V")] = value
        """
        return super(BaseKerning, self).get(pair, default)

    def find(
        self, pair: PairCollectionType[str], default: Optional[IntFloatType] = None
    ) -> Optional[IntFloatType]:
        """
        Returns the value for the kerning pair - even if the pair only exists
        implicitly (one or both sides may be members of a kerning group).

        **pair** is a ``tuple`` of two :ref:`type-string`\s, and the returned
        values will either be :ref:`type-int-float` or ``None``
        if no pair was found. ::

            >>> font.kerning[("A", "V")]
            -25
        """
        pair = normalizers.normalizeKerningKey(pair)
        value = self._find(pair, default)
        if value and value != default:
            value = normalizers.normalizeKerningValue(value)
        return value

    def _find(
        self, pair: PairType[str], default: Optional[IntFloatType] = None
    ) -> Optional[IntFloatType]:
        """
        This is the environment implementation of
        :attr:`BaseKerning.find`. This must return an
        :ref:`type-int-float` or `default`.
        """
        from fontTools.ufoLib.kerning import lookupKerningValue

        font = self.font
        groups = font.groups
        return lookupKerningValue(pair, self, groups, fallback=default)

    def items(self) -> BaseItems[PairType[str], IntFloatType]:
        """
        Returns a list of ``tuple``\s of each pair and value. Pairs are a
        ``tuple`` of two :ref:`type-string`\s and values are :ref:`type-int-float`.

        The initial list will be unordered.

            >>> font.kerning.items()
            [(("A", "V"), -30), (("A", "W"), -10)]
        """
        return super(BaseKerning, self).items()

    def keys(self) -> BaseKeys[PairType[str]]:
        """
        Returns a ``list`` of all the pairs in Kerning. This list will be
        unordered.::

            >>> font.kerning.keys()
            [("A", "Y"), ("A", "V"), ("A", "W")]
        """
        return super(BaseKerning, self).keys()

    def pop(
        self, pair: PairType[str], default: Optional[IntFloatType] = None
    ) -> Optional[IntFloatType]:
        """
        Removes the **pair** from the Kerning and returns the value as an ``int``.
        If no pair is found, **default** is returned. **pair** is a
        ``tuple`` of two :ref:`type-string`\s. This must return either

        **default** or a :ref:`type-int-float`.

            >>> font.kerning.pop(("A", "V"))
            -20
            >>> font.kerning.pop(("A", "W"))
            -10.5
        """
        return super(BaseKerning, self).pop(pair, default)

    def update(self, otherKerning: MutableMapping[PairType[str], IntFloatType]) -> None:
        """
        Updates the Kerning based on **otherKerning**. **otherKerning** is a ``dict`` of
        kerning information. If a pair from **otherKerning** is in Kerning, the pair
        value will be replaced by the value from **otherKerning**. If a pair
        from **otherKerning** is not in the Kerning, it is added to the pairs. If Kerning
        contains a pair that is not in **otherKerning**, it is not changed.

            >>> font.kerning.update(newKerning)
        """
        super(BaseKerning, self).update(otherKerning)

    def values(self) -> BaseValues[IntFloatType]:
        """
        Returns a ``list`` of each pair's values, the values will be
        :ref:`type-int-float`\s.

        The list will be unordered.

            >>> font.kerning.items()
            [-20, -15, 5, 3.5]
        """
        return super(BaseKerning, self).values()
