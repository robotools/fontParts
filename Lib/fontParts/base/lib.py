from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, Dict, Iterator, List, Optional, Tuple, TypeVar

from fontParts.base.base import BaseDict, dynamicProperty, reference
from fontParts.base import normalizers
from fontParts.base.deprecated import DeprecatedLib, RemovedLib

if TYPE_CHECKING:
    from fontParts.base.glyph import BaseGlyph
    from fontParts.base.font import BaseFont


class BaseLib(BaseDict, DeprecatedLib, RemovedLib):
    """Represent the basis for a lib object.

    This object behaves like a Python :class:`dict` object. Most of the
    dictionary functionality comes from :class:`BaseDict`. Consult that
    object's documentation for the required environment implementation
    details.

    :cvar KeyNormalizer: A function to normalize the key of the dictionary.
    :cvar ValueNormalizer: A function to normalize the value of the dictionary.

    This object normally created as part of a :class:`BaseFont`.
     An orphan Lib object can be created like this::

        >>> lib = RLib()

    """

    keyNormalizer: Callable[[str], str] = normalizers.normalizeLibKey
    valueNormalizer: Callable[[Any], Any] = normalizers.normalizeLibValue

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

    _glyph: Optional[BaseGlyph] = None

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

    def _set_glyph(self, glyph: Optional[BaseGlyph]) -> None:
        if self._font is not None:
            raise AssertionError("font for lib already set")
        if self._glyph is not None and self._glyph() != glyph:
            raise AssertionError("glyph for lib already set and is not same as glyph")
        if glyph is not None:
            glyph = reference(glyph)
        self._glyph = glyph

    # Font

    _font: Optional[BaseFont] = None

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

    def _set_font(self, font: Optional[BaseFont]) -> None:
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

    def _get_layer(self) -> Optional[Any]:
        if self._glyph is None:
            return None
        return self.glyph.layer

    # ---------------------
    # RoboFab Compatibility
    # ---------------------

    def remove(self, key: str) -> None:
        """Remove the specified key from the Lib.

        :param key: The key to remove as a :class:`str`.

        .. note::

            This is a backwards compatibility method.

        Example::

            >>> font.lib.remove('myKey')

        """
        del self[key]

    def asDict(self) -> Dict[str, Any]:
        """Return the lib as a dictionary.

        :return A :class:`dict` reflecting the contents of the lib.

        .. note::

            This is a backwards compatibility method.

        Example::

            >>> font.lib.asDict()

        """
        d = {}
        for k, v in self.items():
            d[k] = v
        return d

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

    def __getitem__(self, key: str) -> Any:
        """Get the value associated with the given key.

        :param key: The key to retrieve the value for.
        :return: The value associated with the specified key.
        :raise KeyError: If the specified `key` does not exist.

        Example::

            >>> font.lib["public.glyphOrder"]
            ["A", "B", "C"]

        .. note::

            Any changes to the returned lib contents will not be reflected in
            the Lib object. If one wants to make a change to the lib contents,
            one should do the following::

                >>> lib = font.lib["public.glyphOrder"]
                >>> lib.remove("A")
                >>> font.lib["public.glyphOrder"] = lib

        """
        return super(BaseLib, self).__getitem__(key)

    def __iter__(self) -> Iterator[str]:
        """Return an iterator over the keys in the lib.

        The iteration order is not fixed.

        Example::

            >>> for key in font.lib:
            >>>     print key
            "public.glyphOrder"
            "org.robofab.scripts.SomeData"
            "public.postscriptNames"

        """
        return super(BaseLib, self).__iter__()

    def __len__(self) -> int:
        """Returns the number of keys in the lib.

        :return: An :class:`int` representing the number of keys in the lib.

        Example::

            >>> len(font.lib)
            5

        """
        return super(BaseLib, self).__len__()

    def __setitem__(self, key: str, value: Any) -> None:
        """Set the value for a given key in the lib.

        :param key: The key to set as a :class:`str`.
        :param value: The value to set for the given key.

        Example::

            >>> font.lib["public.glyphOrder"] = ["A", "B", "C"]

        """
        super(BaseLib, self).__setitem__(key, value)

    def clear(self) -> None:
        """Removes all keys from the lib.

        This will reset the lib to an empty dictionary.

        Example::

            >>> font.lib.clear()

        """
        super(BaseLib, self).clear()

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Get the value for a given key in the lib.

        If the given `key` is not found, The specified `default` will be returned.

        :param key: The key to look up as a :class:`str`.
        :param default: The default value to return if the key is not found.
            Defaults to :obj:`None`.
        :return: The value for the given key, or the default value if the key is
            not found.

        Example::

            >>> font.lib.get("public.glyphOrder")
            ["A", "B", "C"]
            >>> font.lib.get("missingKey", default="Default Value")
            "Default Value"

        ..note::

            Any changes to the returned key contents will not be reflected in
            the Lib object. If one wants to make a change to the key contents,
            one should do the following::

                >>> lib = font.lib.get("public.glyphOrder")
                >>> lib.remove("A")
                >>> font.lib["public.glyphOrder"] = lib

        """
        return super(BaseLib, self).get(key, default)

    def items(self) -> List[Tuple[str, Any]]:
        """Return an unordered list of the lib's items.

        Each item is represented as a :class:`tuple` of key-value pairs, where:
            - `key` is always a :class:`str`.
            - `value` may be of any type.

        :return: A :class:`list` of :class:`tuple` items of the form ``(key, value)``.

        Example::

            >>> font.lib.items()
            [("public.glyphOrder", ["A", "B", "C"]),
             ("public.postscriptNames", {'be': 'uni0431', 'ze': 'uni0437'})]

        """
        return super(BaseLib, self).items()

    def keys(self) -> List[str]:
        """Return an unordered list of the lib's keys.

        :return: A :class:`list` of keys as :class:`str`.

        Example::

            >>> font.lib.keys()
            ["public.glyphOrder", "org.robofab.scripts.SomeData",
             "public.postscriptNames"]

        """
        return super(BaseLib, self).keys()

    def pop(self, key: str, default: Optional[Any] = None) -> Any:
        """Remove the specified key and return its associated value.

        If the `key` does not exist, the `default` value is returned.

        :param key: The key to remove as a :class:`str`.
        :param default: The optional default value to return if the `key` is not found.
            Defaults to :obj:`None`.
        :return: The value associated with the given `key`, or the `default` value
            if the `key` is not found.

        Example::

            >>> font.lib.pop("public.glyphOrder")
            ["A", "B", "C"]

        """
        return super(BaseLib, self).pop(key, default)

    def update(self, otherLib: BaseDict) -> None:
        """Update the current lib instance with key-value pairs from another.

        For each key in `otherLib`:
            - If the key exists in the current lib, its value is replaced with
              the value from `otherLib`.
            - If the key does not exist in the current lib, it is added.

        Keys that exist in the current lib but are not in `otherLib` remain unchanged.

        :param otherLib: An instance of :class:`BaseDict` or its subclass
            (like :class:`BaseLib`) to update the current lib with.

        Example::

            >>> font.lib.update(newLib)

        """
        super(BaseLib, self).update(otherLib)

    def values(self) -> List[Any]:
        """Return an unordered list of the lib's values.

        :return: A :class:`list` containing the values in the lib.

        Example::

            >>> font.lib.items()
            [["A", "B", "C"], {'be': 'uni0431', 'ze': 'uni0437'}]

        """
        return super(BaseLib, self).values()
