from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Dict, Iterator, List, Optional, Union
from collections.abc import MutableMapping

from fontParts.base.base import BaseDict, dynamicProperty, reference
from fontParts.base import normalizers
from fontParts.base.deprecated import DeprecatedLib, RemovedLib
from fontParts.base.annotations import LibValueType

if TYPE_CHECKING:
    from fontParts.base.glyph import BaseGlyph
    from fontParts.base.font import BaseFont
    from fontparts.base.layer import BaseLayer
    from fontparts.base import BaseItems
    from fontparts.base import BaseKeys
    from fontparts.base import BaseValues


class BaseLib(BaseDict, DeprecatedLib, RemovedLib):
    """Represent the basis for a lib object.

    This object behaves like a Python :class:`dict` object. Most of the
    dictionary functionality comes from :class:`BaseDict`. Consult that
    object's documentation for the required environment implementation
    details.

    :cvar KeyNormalizer: A function to normalize the key of the dictionary.
        Defaults to :func:`normalizers.normalizeLibKey`.
    :cvar ValueNormalizer: A function to normalize the value of the dictionary.
        Defaults to :func:`normalizers.normalizeLibValue`.

    This object is normally created as part of a :class:`BaseFont`.
    An orphan :class:`BaseLib` object instance can be created like this::

        >>> lib = RLib()

    """

    keyNormalizer: Callable[[str], str] = normalizers.normalizeLibKey
    valueNormalizer: Callable[[LibValueType], LibValueType] = (
        normalizers.normalizeLibValue
    )

    def _reprContents(self) -> List[str]:
        contents = []
        if self.glyph is not None:
            contents.append("in glyph")
            contents += self.glyph._reprContents()
        if self.font:
            contents.append("in font")
            contents += self.font._reprContents()
        return contents

    # -------
    # Parents
    # -------

    # Glyph

    _glyph: Optional[Callable[[], BaseGlyph]] = None

    glyph: dynamicProperty = dynamicProperty(
        "glyph",
        """Get or set the lib's parent glyph object.

        The value must be a :class:`BaseGlyph` instance or :obj:`None`.

        :return: The :class:`BaseGlyph` instance containing the lib
            or :obj:`None`.
        :raises AssertionError:
            - If the font for the lib has already been set.
            - If attempting to set the glyph when it has already been set and is
              not the same as the provided glyph.

        Example::

            >>> glyph = lib.glyph

        """,
    )

    def _get_glyph(self) -> Optional[BaseGlyph]:
        if self._glyph is None:
            return None
        return self._glyph()

    def _set_glyph(
        self, glyph: Optional[Union[BaseGlyph, Callable[[], BaseGlyph]]]
    ) -> None:
        if self._font is not None:
            raise AssertionError("font for lib already set")
        if self._glyph is not None and self._glyph() != glyph:
            raise AssertionError("glyph for lib already set and is not same as glyph")
        if glyph is not None:
            glyph = reference(glyph)
        self._glyph = glyph

    # Font

    _font: Optional[Callable[[], BaseFont]] = None

    font: dynamicProperty = dynamicProperty(
        "font",
        """Get or set the lib's parent font object.

        The value must be a :class:`BaseFont` instance or :obj:`None`.

        :return: The :class:`BaseFont` instance containing the lib
            or :obj:`None`.
        :raises AssertionError:
            - If attempting to set the font when it has already been set and is
              not the same as the provided font.
            - If the glyph for the lib has already been set.

        Example::

            >>> font = lib.font

        """,
    )

    def _get_font(self) -> Optional[BaseFont]:
        if self._font is not None:
            return self._font()
        elif self._glyph is not None:
            return self.glyph.font
        return None

    def _set_font(
        self, font: Optional[Union[BaseFont, Callable[[], BaseFont]]]
    ) -> None:
        if self._font is not None and self._font() != font:
            raise AssertionError("font for lib already set and is not same as font")
        if self._glyph is not None:
            raise AssertionError("glyph for lib already set")
        if font is not None:
            font = reference(font)
        self._font = font

    # Layer

    layer: dynamicProperty = dynamicProperty(
        "layer",
        """Get the lib's parent layer object.

        This property is read-only.

        :return: The :class:`BaseLayer` instance containing the contour
            or :obj:`None`.

        Example::

            >>> layer = lib.layer

        """,
    )

    def _get_layer(self) -> Optional[BaseLayer]:
        if self._glyph is None:
            return None
        return self.glyph.layer

    # ---------------------
    # RoboFab Compatibility
    # ---------------------

    def remove(self, key: str) -> None:
        """Remove the specified key from the lib.

        :param key: The key to remove as a :class:`str`.

        .. note::

            This is a backwards compatibility method.

        Example::

            >>> font.lib.remove('myKey')

        """
        del self[key]

    def asDict(self) -> Dict[str, LibValueType]:
        """Return the lib as a dictionary.

        :return A :class:`dict` reflecting the contents of the lib.

        .. note::

            This is a backwards compatibility method.

        Example::

            >>> font.lib.asDict()

        """
        return dict(self)

    # -------------------
    # Inherited Functions
    # -------------------

    def __contains__(self, key: str) -> bool:
        """Check if the given key exists in the lib.

        :param key: The key to check for existence as a :class:`str`.
        :return: :obj:`True` if the `key` exists in the lib :obj:`False` otherwise.

        Example::

            >>> "public.glyphOrder" in font.lib
            True

        """
        return super(BaseLib, self).__contains__(key)

    def __delitem__(self, key: str) -> None:
        """Remove the given key from the lib.

        :param key: The key to remove as a :class:`str`.

        Example::

            >>> del font.lib["public.glyphOrder"]

        """
        super(BaseLib, self).__delitem__(key)

    def __getitem__(self, key: str) -> LibValueType:
        """Get the value associated with the given key.

        :param key: The key to retrieve the value for as a :class:`str`.
        :return: The :ref:`type-lib-value` associated with the specified key.
        :raise KeyError: If the specified `key` does not exist.

        Example::

            >>> font.lib["public.glyphOrder"]
            ["A", "B", "C"]

        .. note::

            Any changes to the returned lib contents will not be reflected in
            it's :class:`BaseLib` instance. To make changes to this content,
            do the following::

                >>> lib = font.lib["public.glyphOrder"]
                >>> lib.remove("A")
                >>> font.lib["public.glyphOrder"] = lib

        """
        return super(BaseLib, self).__getitem__(key)

    def __iter__(self) -> Iterator[str]:
        """Return an iterator over the keys in the lib.

        The iteration order is not fixed.

        :return: An :class:`Iterator` over the :class:`str` keys.

        Example::

            >>> for key in font.lib:
            >>>     print key
            "public.glyphOrder"
            "org.robofab.scripts.SomeData"
            "public.postscriptNames"

        """
        return super(BaseLib, self).__iter__()

    def __len__(self) -> int:
        """Return the number of keys in the lib.

        :return: An :class:`int` representing the number of keys in the lib.

        Example::

            >>> len(font.lib)
            5

        """
        return super(BaseLib, self).__len__()

    def __setitem__(self, key: str, value: LibValueType) -> None:
        """Set the value for a given key in the lib.

        :param key: The key to set as a :class:`str`.
        :param value: The :ref:`type-lib-value` to set for the given key.

        Example::

            >>> font.lib["public.glyphOrder"] = ["A", "B", "C"]

        """
        super(BaseLib, self).__setitem__(key, value)

    def clear(self) -> None:
        """Remove all keys from the lib.

        This will reset the :class:`BaseLib` instance to an empty dictionary.

        Example::

            >>> font.lib.clear()

        """
        super(BaseLib, self).clear()

    def get(
        self, key: str, default: Optional[LibValueType] = None
    ) -> Optional[LibValueType]:
        """Get the value for the given key in the lib.

        If the given `key` is not found, The specified `default` will be returned.

        :param key: The key to look up as a :class:`str`.
        :param default: The optional default :ref:`type-lib-value` to return if
            the `key` is not found. Defaults to :obj:`None`.
        :return: The :ref:`type-lib-value` for the given `key`, or the `default`
            value if the `key` is not found.

        Example::

            >>> font.lib.get("public.glyphOrder")
            ["A", "B", "C"]
            >>> font.lib.get("missingKey", default="Default Value")
            "Default Value"

        ..note::

            Any changes to the returned lib contents will not be reflected in
            it's :class:`BaseLib` instance. To make changes to this content,
            do the following::

                >>> lib = font.lib.get("public.glyphOrder")
                >>> lib.remove("A")
                >>> font.lib["public.glyphOrder"] = lib

        """
        return super(BaseLib, self).get(key, default)

    def items(self) -> BaseItems[str, LibValueType]:
        """Return the lib's items.

        Each item is represented as a :class:`tuple` of key-value pairs, where:
            - `key` is a :class:`str`.
            - `value` is a :ref:`type-lib-value`.

        :return: A :ref:`type-view` of the lib's ``(key, value)`` pairs.

        Example::

            >>> font.lib.items()
            [("public.glyphOrder", ["A", "B", "C"]),
             ("public.postscriptNames", {'be': 'uni0431', 'ze': 'uni0437'})]

        """
        return super(BaseLib, self).items()

    def keys(self) -> BaseKeys[str]:
        """Return the lib's keys.

        :return: A :ref:`type-view` of :class:`str` items representing the lib's keys.

        Example::

            >>> font.lib.keys()
            ["public.glyphOrder", "org.robofab.scripts.SomeData",
             "public.postscriptNames"]

        """
        return super(BaseLib, self).keys()

    def values(self) -> BaseValues[LibValueType]:
        """Return the lib's values.

        :return: A :ref:`type-view` of :ref:`type-lib-value <lib values>`.

        Example::

            >>> font.lib.items()
            [["A", "B", "C"], {'be': 'uni0431', 'ze': 'uni0437'}]

        """
        return super(BaseLib, self).values()

    def pop(
        self, key: str, default: Optional[LibValueType] = None
    ) -> Optional[LibValueType]:
        """Remove the specified key and return its associated value.

        If the `key` does not exist, the `default` value is returned.

        :param key: The key to remove as a :class:`str`.
        :param default: The optional default :ref:`type-lib-value` to return if
            the `key` is not found. Defaults to :obj:`None`.
        :return: The :ref:`type-lib-value` associated with the given `key`, or
            the `default` value if the `key` is not found.

        Example::

            >>> font.lib.pop("public.glyphOrder")
            ["A", "B", "C"]

        """
        return super(BaseLib, self).pop(key, default)

    def update(self, otherLib: MutableMapping[str, LibValueType]) -> None:
        """Update the current lib with key-value pairs from another.

        For each key in `otherLib`:
            - If the key exists in the current lib, its value is replaced with
              the value from `otherLib`.
            - If the key does not exist in the current lib, it is added.

        Keys that exist in the current lib but are not in `otherLib` remain unchanged.

        :param otherLib: A :class:`MutableMapping` of :class:`str` keys mapped
            to :ref:`type-lib-value <lib values>` to update the current lib with.

        Example::

            >>> font.lib.update(newLib)

        """
        super(BaseLib, self).update(otherLib)
