from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, List, Optional

from fontParts.base.base import BaseDict, dynamicProperty, reference
from fontParts.base import normalizers
from fontParts.base.deprecated import DeprecatedLib, RemovedLib

if TYPE_CHECKING:
    from fontParts.base.glyph import BaseGlyph
    from fontParts.base.font import BaseFont


class BaseLib(BaseDict, DeprecatedLib, RemovedLib):
    """
    A Lib object. This object normally created as part of a
    :class:`BaseFont`. An orphan Lib object can be created like this::

        >>> lib = RLib()

    This object behaves like a Python dictionary. Most of the dictionary
    functionality comes from :class:`BaseDict`, look at that object for the
    required environment implementation details.

    Lib uses :func:`normalizers.normalizeLibKey` to normalize the key of
    the ``dict``, and :func:`normalizers.normalizeLibValue` to normalize the
    value of the ``dict``.
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

    glyph: dynamicProperty = dynamicProperty("glyph", "The lib's parent glyph.")

    def _get_glyph(self) -> Optional[BaseGLyph]:
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

    font: dynamicProperty = dynamicProperty("font", "The lib's parent font.")

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

    layer: dynamicProperty = dynamicProperty("layer", "The lib's parent layer.")

    def _get_layer(self) -> Optional[Any]:
        if self._glyph is None:
            return None
        return self.glyph.layer

    # ---------------------
    # RoboFab Compatibility
    # ---------------------

    def remove(self, key: str) -> None:
        """
        Removes a key from the Lib. **key** will be
        a :ref:`type-string` that is the key to
        be removed.

        This is a backwards compatibility method.
        """
        del self[key]

    def asDict(self) -> Dict[str, Any]:
        """
        Return the Lib as a ``dict``.

        This is a backwards compatibility method.
        """
        d = {}
        for k, v in self.items():
            d[k] = v
        return d

    # -------------------
    # Inherited Functions
    # -------------------

    def __contains__(self, key: str) -> bool:
        """
        Tests to see if a lib name is in the Lib.
        **key** will be a :ref:`type-string`.
        This returns a ``bool`` indicating if the **key**
        is in the Lib. ::

            >>> "public.glyphOrder" in font.lib
            True
        """
        return super(BaseLib, self).__contains__(key)

    def __delitem__(self, key: str) -> None:
        """
        Removes **key** from the Lib. **key** is a :ref:`type-string`.::

            >>> del font.lib["public.glyphOrder"]
        """
        super(BaseLib, self).__delitem__(key)

    def __getitem__(self, key: str) -> Any:
        """
        Returns the contents of the named lib. **key** is a
        :ref:`type-string`.
        The returned value will be a ``list`` of the lib contents.::

            >>> font.lib["public.glyphOrder"]
            ["A", "B", "C"]

        It is important to understand that any changes to the returned lib
        contents will not be reflected in the Lib object. If one wants to
        make a change to the lib contents, one should do the following::

            >>> lib = font.lib["public.glyphOrder"]
            >>> lib.remove("A")
            >>> font.lib["public.glyphOrder"] = lib
        """
        return super(BaseLib, self).__getitem__(key)

    def __iter__(self) -> Iterator[str]:
        """
        Iterates through the Lib, giving the key for each iteration. The
        order that the Lib will iterate though is not fixed nor is it
        ordered.::

            >>> for key in font.lib:
            >>>     print key
            "public.glyphOrder"
            "org.robofab.scripts.SomeData"
            "public.postscriptNames"
        """
        return super(BaseLib, self).__iter__()

    def __len__(self) -> int:
        """
        Returns the number of keys in Lib as an ``int``.::

            >>> len(font.lib)
            5
        """
        return super(BaseLib, self).__len__()

    def __setitem__(self, key: str, items: Any) -> None:
        """
        Sets the **key** to the list of **items**. **key**
        is the lib name as a :ref:`type-string` and **items** is a
        ``list`` of items as :ref:`type-string`.

            >>> font.lib["public.glyphOrder"] = ["A", "B", "C"]
        """
        super(BaseLib, self).__setitem__(key, items)

    def clear(self) -> None:
        """
        Removes all keys from Lib,
        resetting the Lib to an empty dictionary. ::

            >>> font.lib.clear()
        """
        super(BaseLib, self).clear()

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Returns the contents of the named key.
        **key** is a :ref:`type-string`, and the returned values will
        either be ``list`` of key contents or ``None`` if no key was
        found. ::

            >>> font.lib["public.glyphOrder"]
            ["A", "B", "C"]

        It is important to understand that any changes to the returned key
        contents will not be reflected in the Lib object. If one wants to
        make a change to the key contents, one should do the following::

            >>> lib = font.lib["public.glyphOrder"]
            >>> lib.remove("A")
            >>> font.lib["public.glyphOrder"] = lib
        """
        return super(BaseLib, self).get(key, default)

    def items(self) -> List[Tuple[str, Any]]:
        """
        Returns a list of ``tuple`` of each key name and key items.
        Keys are :ref:`type-string` and key members are a ``list``
        of :ref:`type-string`. The initial list will be unordered.

            >>> font.lib.items()
            [("public.glyphOrder", ["A", "B", "C"]),
             ("public.postscriptNames", {'be': 'uni0431', 'ze': 'uni0437'})]
        """
        return super(BaseLib, self).items()

    def keys(self) -> List[str]:
        """
        Returns a ``list`` of all the key names in Lib. This list will be
        unordered.::

            >>> font.lib.keys()
            ["public.glyphOrder", "org.robofab.scripts.SomeData",
             "public.postscriptNames"]
        """
        return super(BaseLib, self).keys()

    def pop(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Removes the **key** from the Lib and returns the ``list`` of
        key members. If no key is found, **default** is returned.
        **key** is a :ref:`type-string`. This must return either
        **default** or a ``list`` of items as :ref:`type-string`.

            >>> font.lib.pop("public.glyphOrder")
            ["A", "B", "C"]
        """
        return super(BaseLib, self).pop(key, default)

    def update(self, otherLib: Dict[str, Any]) -> None:
        """
        Updates the Lib based on **otherLib**. *otherLib** is a
        ``dict`` of keys. If a key from **otherLib** is in Lib
        the key members will be replaced by the key members from
        **otherLib**. If a key from **otherLib** is not in the Lib,
        it is added to the Lib. If Lib contain a key name that is not
        in *otherLib**, it is not changed.

            >>> font.lib.update(newLib)
        """
        super(BaseLib, self).update(otherLib)

    def values(self) -> List[Any]:
        """
        Returns a ``list`` of each named key's members. This will be a list
        of lists, the key members will be a ``list`` of :ref:`type-string`.
        The initial list will be unordered.

            >>> font.lib.items()
            [["A", "B", "C"], {'be': 'uni0431', 'ze': 'uni0437'}]
        """
        return super(BaseLib, self).values()
