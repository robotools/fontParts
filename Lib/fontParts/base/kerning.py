# pylint: disable=C0103, C0114
from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    TypeVar,
    Union,
)
from collections.abc import MutableMapping

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

BaseKerningType = TypeVar("BaseKerningType", bound="BaseKerning")


class BaseKerning(BaseDict, DeprecatedKerning, RemovedKerning):
    """Represent the basis for a kerning object.

    This object behaves like a Python :class:`dict` object. Most of the
    dictionary functionality comes from :class:`BaseDict`. Consult that
    object's documentation for the required environment implementation
    details.

    :cvar keyNormalizer: A function to normalize the key of the dictionary.
        Defaults to :func:`normalizers.normalizeKerningKey`.
    :cvar valueNormalizer: A function to normalize the value of the dictionary.
        Defaults to :func:`normalizers.normalizeKerningValue`.

    This object is normally created as part of a :class:`BaseFont`.
    An orphan :class:`BaseKerning` object instance can be created like this::

        >>> groups = RKerning()

    """

    keyNormalizer: Callable[[PairCollectionType[str]], PairType[str]] = (
        normalizers.normalizeKerningKey
    )
    valueNormalizer: Callable[[IntFloatType], IntFloatType] = (
        normalizers.normalizeKerningValue
    )

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
        "font",
        """Get or set the kerning's parent font object.

        The value must be a :class:`BaseFont` instance or :obj:`None`.

        :return: The :class:`BaseFont` instance containing the kerning
            or :obj:`None`.
        :raises AssertionError: If attempting to set the font when it has already been 
            set and is not the same as the provided font.

        Example::

            >>> font = kerning.font

        """,
    )

    def _get_font(self) -> Optional[BaseFont]:
        if self._font is None:
            return None
        return self._font()

    def _set_font(
        self, font: Optional[Union[BaseFont, Callable[[], BaseFont]]]
    ) -> None:
        if self._font is not None and self._font() != font:
            raise AssertionError("font for kerning already set and is not same as font")
        if font is not None:
            font = reference(font)
        self._font = font

    # --------------
    # Transformation
    # --------------

    def scaleBy(self, factor: TransformationType) -> None:
        """Scale all kerning values by the specified factor.

        :param factor: The factor by which to scale the kerning. The value may be a
            single :class:`int` or :class:`float` or a :class:`tuple` or :class`list`
            of two :class:`int` or :class:`float` values representing the factors
            ``(x, y)``. In the latter case, the first value is used to scale the
            kerning values.

        Example::

            >>> myKerning.scaleBy(2)
            >>> myKerning.scaleBy((2, 3))

        """
        factor = normalizers.normalizeTransformationScale(factor)
        self._scale(factor)

    def _scale(self, factor: PairType[float]) -> None:
        """Scale all native kerning values by the specified factor.

        This is the environment implementation of :meth:`BaseKerning.scaleBy`.

        :param factor: The factor by which to scale the kerning as a :class:`tuple` of
            two :class:`int` or :class:`float` values representing the factors
            ``(x, y)``. The first value is used to scale the kerning values.

        .. note::

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
        """Round the kerning values to the specified increments.

        :param multiple: The increment to which the kerning values should be rounded
            as an :class:`int`. Defaults to ``1``.

        Example::

            >>> myKerning.round(2)

        """
        if not isinstance(multiple, int):
            raise TypeError(
                f"The round multiple must be an int not {multiple.__class__.__name__}."
            )
        self._round(multiple)

    def _round(self, multiple: int) -> None:
        """Round the native kerning values to the specified increments.

        This is the environment implementation of :meth:`BaseKerning.round`.

        :param multiple: The increment to which the kerning values should be rounded
            as an :class:`int`.

        .. note::

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
        minKerning: BaseKerningType,
        maxKerning: BaseKerningType,
        round: bool = True,
        suppressError: bool = True,
    ) -> None:
        """Interpolate all kerning pairs in the font.

        The kerning data will be replaced by the interpolated kerning.

        :param factor: The interpolation value as a single :class:`int`
            or :class:`float` or a :class:`list` or :class:`tuple` of
            two :class:`int` or :class:`float` values representing the
            factors ``(x, y)``.
        :param minKerning: The :class:`BaseKerning` instance corresponding to the
            0.0 position in the interpolation.
        :param maxKerning: The :class:`BaseKerning` instance corresponding to the
            1.0 position in the interpolation.
        :param round: A :class:`bool` indicating whether the result should
            be rounded to integers. Defaults to :obj:`True`.
        :param suppressError: A :class:`bool` indicating whether to ignore
            incompatible data or raise an error when such
            incompatibilities are found. Defaults to :obj:`True`.
        :raises TypeError: If `minGlyph` or `maxGlyph` are not instances
            of :class:`BaseKerning`.

        Example::

            >>> myKerning.interpolate(kerningOne, kerningTwo)

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
        round: bool,
        suppressError: bool,
    ) -> None:
        """Interpolate all kerning pairs in the native font.

        The kerning data will be replaced by the interpolated kerning.

        :param factor: The interpolation value as a single :class:`int`
            or :class:`float` or a :class:`list` or :class:`tuple` of
            two :class:`int` or :class:`float` values representing the
            factors ``(x, y)``.
        :param minKerning: The :class:`BaseKerning` subclass instance corresponding
            to the 0.0 position in the interpolation.
        :param maxKerning: The :class:`BaseKerning` subclass instance corresponding
            to the 1.0 position in the interpolation.
        :param round: A :class:`bool` indicating whether the result should
            be rounded to integers.
        :param suppressError: A :class:`bool` indicating whether to ignore
            incompatible data or raise an error when such
            incompatibilities are found.

        .. note::

            Subclasses may override this method.

        """
        from fontMath.mathFunctions import setRoundIntegerFunction
        from fontMath import MathKerning

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
        """Remove the specified pair from the Kerning.

        :param pair: The pair to remove as a :class:`tuple` of two :class:`str` values.

        .. note::

            This is a backwards compatibility method.

        Example::

            >>> myKerning.remove(("A", "V"))

        """
        del self[pair]

    def asDict(self, returnIntegers: bool = True) -> Dict[PairType[str], IntFloatType]:
        """Return the kerning as a dictionary.

        :return A :class:`dict` reflecting the contents of the kerning.

        .. note::

            This is a backwards compatibility method.

        Example::

            >>> font.lib.asDict()

        """
        return {
            k: (v if not returnIntegers else normalizers.normalizeVisualRounding(v))
            for k, v in self.items()
        }

    # -------------------
    # Inherited Functions
    # -------------------

    def __contains__(self, pair: PairType[str]) -> bool:
        """Check if the given pair exists in the kerning.

        :param pair: The kerning pair to check for existence as a :class:`tuple` of
            two :class:`str` values.
        :return: :obj:`True` if the `groupName` exists in the groups, :obj:`False`
            otherwise.

        Example::

            >>> ("A", "V") in font.kerning
            True

        """
        return super(BaseKerning, self).__contains__(pair)

    def __delitem__(self, pair: PairType[str]) -> None:
        """Remove the given pair from the kerning.

        :param pair: The pair to remove as a :class:`tuple` of two :class:`str` values.

        Example::

            >>> del font.kerning[("A","V")]

        """
        super(BaseKerning, self).__delitem__(pair)

    def __getitem__(self, pair: PairType[str]) -> IntFloatType:
        """Get the value associated with the given kerning pair.

        :param pair: The pair to remove as a :class:`tuple` of two :class:`str` values.
        :return: The kerning value as an :class:`int` or :class:`float`.

        Example::

            >>> font.kerning[("A", "V")]
            -15

        .. note::

            Any changes to the returned kerning value will not be reflected in
            it's :class:`BaseKerning` instance. To make changes to this value,
            do the following::

                >>> value = font.kerning[("A", "V")]
                >>> value += 10
                >>> font.kerning[("A", "V")] = value

        """
        return super(BaseKerning, self).__getitem__(pair)

    def __iter__(self) -> Iterator[PairType[str]]:
        """Return an iterator over the pairs in the kerning.

        The iteration order is not fixed.

        :return: An :class:`Iterator` over :class:`tuple` instances containing
            two :class:`str` values.

        Example::

            >>> for pair in font.kerning:
            >>>     print pair
            ("A", "Y")
            ("A", "V")
            ("A", "W")

        """
        return super(BaseKerning, self).__iter__()

    def __len__(self) -> int:
        """Return the number of pairs in the kerning.

        :return: An :class:`int` representing the number of pairs in the kerning.

        Example::

            >>> len(font.kerning)
            5

        """
        return super(BaseKerning, self).__len__()

    def __setitem__(self, pair: PairType[str], value: IntFloatType) -> None:
        """Set the value for the given kerning pair.

        :param pair: The pair to set as a :class:`tuple` of two :class:`str` values.
        :param value: The value to set as an :class:`int` or :class:`float`.

        Example::

            >>> font.kerning[("A", "V")] = -20
            >>> font.kerning[("A", "W")] = -10.5

        """
        super(BaseKerning, self).__setitem__(pair, value)

    def clear(self) -> None:
        """Remove all information from kerning.

        This will reset the :class:`BaseKerning` instance to an empty dictionary.

        Example::

            >>> font.kerning.clear()

        """
        super(BaseKerning, self).clear()

    def get(
        self, pair: PairType[str], default: Optional[IntFloatType] = None
    ) -> Optional[IntFloatType]:
        """Get the value for the given kerning pair.

        If the given `pair` is not found, The specified `default` will be returned.

        :param pair: The pair to get as a :class:`tuple` of two :class:`str` values.
        :param default: The optional default value to return if the `pair` is not found.
        :return: A :class:`tuple` of two :class:`str` values representing the value for
            the given `pair`, or the `default` value if the `pair` is not found.

        Example::

            >>> font.kerning.get(("A", "V"))
            -25

        .. note::

            Any changes to the returned kerning value will not be reflected in
            it's :class:`BaseKerning` instance. To make changes to this value,
            do the following::

                >>> value = font.kerning[("A", "V")]
                >>> value += 10
                >>> font.kerning[("A", "V")] = value

        """
        return super(BaseKerning, self).get(pair, default)

    def find(
        self, pair: PairCollectionType[str], default: Optional[IntFloatType] = None
    ) -> Optional[IntFloatType]:
        """Get the value for the given explicit or implicit kerning pair.

        This method will return the value for the given `pair`, even if it only exists
        implicitly (one or both sides may be members of a kerning group). If the `pair`
        is not found, the specified `default` will be returned.

        :param pair: The pair to get as a :class:`tuple` of two :class:`str` values.
        :param default: The optional default value to return if the `pair` is not found.
        :return: A :class:`tuple` of two :class:`str` values representing the value for
            the given `pair`, or the `default` value if the `pair` is not found.

        Example::

            >>> font.kerning.find(("A", "V"))
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
        """Get the value for the given explicit or implicit native kerning pair.

        This is the environment implementation of :attr:`BaseKerning.find`.

        :param pair: The pair to get as a :class:`tuple` of two :class:`str` values.
        :param default: The optional default value to return if the `pair` is not found.
        :return: A :class:`tuple` of two :class:`str` values representing the value for
            the given `pair`, or the `default` value if the `pair` is not found.

        .. note::

            Subclasses may override this method.

        """
        from fontTools.ufoLib.kerning import lookupKerningValue

        font = self.font
        groups = font.groups
        return lookupKerningValue(pair, self, groups, fallback=default)

    def items(self) -> BaseItems[PairType[str], IntFloatType]:
        """Return the kerning's items.

        Each item is represented as a :class:`tuple` of key-value pairs, where:
            - `key` is a :class:`tuple` of two :class:`str` values.
            - `value` is an :class:`int` or a :class:`float`.

        :return: A :ref:`type-view` of the kerning's ``(key, value)`` pairs.

        Example::

            >>> font.kerning.items()
            BaseKerning_items([(("A", "V"), -30), (("A", "W"), -10)])

        """
        return super(BaseKerning, self).items()

    def keys(self) -> BaseKeys[PairType[str]]:
        """Return the kering's pairs (keys).

        :return: A :ref:`type-view` of the kerning's pairs as :class: `tuple` instances
            of two :class:`str` values.

        Example::

            >>> font.kerning.keys()
            BaseKerning_keys([("A", "Y"), ("A", "V"), ("A", "W")])

        """
        return super(BaseKerning, self).keys()

    def values(self) -> BaseValues[IntFloatType]:
        """Return the kerning's values.

        :return: A :ref:`type-view` of :class:`int` or :class:`float` values.

        Example::

            >>> font.kerning.items()
            BaseKerning_values([-20, -15, 5, 3.5])

        """
        return super(BaseKerning, self).values()

    def pop(
        self, pair: PairType[str], default: Optional[IntFloatType] = None
    ) -> Optional[IntFloatType]:
        """Remove the specified kerning pair and return its associated value.

        If the `pair` does not exist, the `default` value is returned.

        :param pair: The pair to remove as a :class:`tuple` of two :class:`str` values.
        :param default: The optional default value to return if the `pair` is not
            found`. The value must be an :class:`int`, a :class:`float` or :obj:`None`.
            Defaults to :obj:`None`.
        :return: The value for the given `pair` as an :class:`int` or :class:`float`,
            or the `default` value if the `pair` is not found.

        Example::

            >>> font.kerning.pop(("A", "V"))
            -20
            >>> font.kerning.pop(("A", "W"))
            -10.5

        """
        return super(BaseKerning, self).pop(pair, default)

    def update(self, otherKerning: MutableMapping[PairType[str], IntFloatType]) -> None:
        """Update the current kerning with key-value pairs from another.

        For each pair in `otherKerning`:
            - If the pair exists in the current kerning, its value is replaced with
              the value from `otherKerning`.
            - If the pair does not exist in the current kerning, it is added.

        Pairs that exist in the current kerning but are not in `otherLib` remain
        unchanged.

        :param otherKerning: A :class:`MutableMapping` of key-value pairs to update the
            current lib with. Keys must be a :class:`tuple` of two :class:`str` values.
            Values must be an :class:`int` or a :class:`float`.

        Example::

            >>> font.kerning.update(newKerning)

        """
        super(BaseKerning, self).update(otherKerning)
