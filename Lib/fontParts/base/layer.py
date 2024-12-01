# pylint: disable=C0103, C0302, C0114, W0613
from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, Iterator, List, Optional, Tuple
import collections

from fontParts.base.base import (
    BaseObject,
    InterpolationMixin,
    SelectionMixin,
    dynamicProperty,
    reference,
)
from fontParts.base import normalizers
from fontParts.base.compatibility import LayerCompatibilityReporter
from fontParts.base.color import Color
from fontParts.base.deprecated import DeprecatedLayer, RemovedLayer
from fontParts.base.annotations import (
    CharacterMappingType,
    CollectionType,
    QuadrupleCollectionType,
    TransformationType,
    ReverseComponentMappingType,
    IntFloatType,
)

if TYPE_CHECKING:
    from fontParts.base.font import BaseFont
    from fontParts.base.glyph import BaseGlyph
    from fontParts.base.lib import BaseLib


class _BaseGlyphVendor(BaseObject, SelectionMixin):
    """Provide common glyph interaction.

    This class provides common glyph interaction code to the
    to :class:`BaseFont` and :class`BaseLayer` classes.

    .. important::

        This class should not be directly subclassed.

    """

    # -----------------
    # Glyph Interaction
    # -----------------

    def _setLayerInGlyph(self, glyph: BaseGlyph) -> None:
        if glyph.layer is None:
            if isinstance(self, BaseLayer):
                layer = self
            else:
                layer = self.defaultLayer
            glyph.layer = layer

    def __len__(self) -> int:
        """Return the number of glyphs in the layer.

        :return: The number of :class:`BaseGlyph` instances in
            the layer as an :class:`int`.

        Example::

            >>> len(layer)
            256

        """
        return self._len()

    def _len(self, **kwargs: Any) -> int:
        r"""Return the number of glyphs in the native layer.

        This is the environment implementation of
        :meth:`BaseLayer.__len__` and :meth:`BaseFont.__len__`

        :param \**kwargs: Additional keyword arguments.
        :return: The number of :class:`BaseGlyph` subclass instances in
            the layer as an :class:`int`.

        .. note::

            Subclasses may override this method.

        """
        return len(self.keys())

    def __iter__(self) -> Iterator[BaseGlyph]:
        """Iterate through the glyphs in the layer.

        :return: An iterator over :class:`BaseGlyph` instances.

        Example::

            >>> for glyph in layer:
            ...     glyph.name
            "A"
            "B"
            "C"

        """
        return self._iter()

    def _iter(self, **kwargs: Any) -> Iterator[BaseGlyph]:
        """Iterate through the glyphs in the native layer.

        This is the environment implementation of
        :meth:`BaseLayer.__iter__` and :meth:`BaseFont.__iter__`.

        :return: An iterator over instances of a :class:`BaseGlyph` subclass.

        .. note::

            Subclasses may override this method.

        """
        for name in self.keys():
            yield self[name]

    def __getitem__(self, name: str) -> BaseGlyph:
        """Get the specified glyph from the layer.

        :param name: The name representing the glyph to retrieve.
        :return: a :class:`BaseGlyph` instance with the specified name.
        :raises KeyError: If no glyph with the given name exists in the layer.

        Example::

             >>> glyph = layer["A"]

        """
        name = normalizers.normalizeGlyphName(name)
        if name not in self:
            raise KeyError(f"No glyph named '{name}'.")
        glyph = self._getItem(name)
        self._setLayerInGlyph(glyph)
        return glyph

    def _getItem(self, name: str, **kwargs: Any) -> BaseGlyph:  # type: ignore[return]
        r"""Get the specified glyph from the native layer.

        This is the environment implementation of
        :meth:`BaseLayer.__getitem__` and :meth:`BaseFont.__getitem__`.

        :param name: The name representing the glyph to get. The value
            will have been normalized with :func:`normalizers.normalizeGlyphName`.
        :param \**kwargs: Additional keyword arguments.
        :return: an instance of a :class:`BaseGlyph` subclass with the
            specified name.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def __setitem__(self, name: str, glyph: BaseGlyph) -> BaseGlyph:
        """Insert a specified glyph into the layer.

        This method will not insert a glyph directly, but rather create
        a new :class:`BaseGlyph` instance containing the data from
        `glyph`. The data inserted from `glyph` is the same data as
        documented in :meth:`BaseGlyph.copy`.

        :param name: The name to assign to the new layer after insertion.
        :param glyph: The :class:`BaseGlyph` instance to insert.
        :return: The newly inserted :class:`BaseGlyph` instance.
        :raises KeyError: If no glyph with the given name exists in the layer.

        Example::

            >>> glyph = layer["A"] = otherGlyph

        """
        name = normalizers.normalizeGlyphName(name)
        if name in self:
            del self[name]
        return self._insertGlyph(glyph, name=name)

    def __delitem__(self, name: str) -> None:
        """Remove the glyph with name from the layer.

        Example::

            >>> del layer["A"]

        """
        name = normalizers.normalizeGlyphName(name)
        if name not in self:
            raise KeyError(f"No glyph named '{name}'.")
        self._removeGlyph(name)

    def keys(self) -> Tuple[str, ...]:
        """Get the names of all glyphs in the layer.

        This method returns an unordered :class:`tuple` of glyph names
        representing all the :class:`BaseGlyph` instances in the active
        layer. If called from a :class:`BaseFont` instance, it returns
        the glyphs from the default layer. If called from
        a :class:`BaseLayer` instance, it returns the glyphs from the
        current layer.

        :return: A :class:`tuple` of glyph names representing the glyphs
            in the current or default :class:`BaseLayer` instance.

        Example::

            >>> layer.keys()
            ["B", "C", "A"]

        """
        return self._keys()

    def _keys(self, **kwargs: Any) -> Tuple[str, ...]:  # type: ignore[return]
        r"""Get the names of all glyphs in the native layer.

        This is the environment implementation of
        :meth:`BaseLayer.keys` and :meth:`BaseFont.keys`.

        :param \**kwargs: Additional keyword arguments.
        :return: An unordered :class:`tuple` of glyph names representing
            the glyphs in the current or default :class:`BaseLayer` instance.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

         .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def __contains__(self, name: str) -> bool:
        """Check if the layer contains the specified glyph.

        This method checks whether a glyph with the given `name` exists
        in the layer. When called from a :class:`BaseFont` instance, it
        checks the default layer. When called from a :class:`BaseLayer`
        instance, it checks the current layer.

        :param name: The name of the glyph to check for.
        :return: :obj:`True` if the glyph exists in the layer,
            :obj:`False` otherwise.

        .. note::

            :meth:`has_key` is provided as an alias for this method for
            backward compatibility but may be deprecated in the future.
            It is advisable to use :meth:`__contains__` instead.

        Example::

            >>> "A" in layer
            True

        """
        name = normalizers.normalizeGlyphName(name)
        return self._contains(name)

    def _contains(self, name: str, **kwargs: Any) -> bool:
        r"""Test if the native layer contains the specified glyph.

        This is the environment implementation of
        :meth:`BaseLayer.__contains__` and :meth:`BaseFont.__contains__`.

        :param name: The name of the glyph to check. The value will have been
            normalized with :func:`normalizers.normalizeGlyphName`.
        :param \**kwargs: Additional keyword arguments.
        :return: :obj:`True` if the glyph exists in the layer,
            :obj:`False` otherwise.

        .. note::

            Subclasses may override this method.

        """
        return name in self.keys()

    def newGlyph(self, name: str, clear: bool = True) -> BaseGlyph:
        """Create a new glyph in the layer.

        This method creates a new glyph with the given `name` in the
        layer. If a glyph with the same name already exists and `clear`
        is set to :obj:`True`, the existing glyph will be removed before
        creating the new one. If `clear` is set to :obj:`False`, the
        existing glyph will be returned without modification.

        When called from a :class:`BaseFont` instance, the glyph is
        created in the default layer. When called from
        a :class:`BaseLayer` instance, the glyph is created in the
        current layer.

        :param name: The name of the glyph to create.
        :param clear: Whether to clear any preexisting glyph with the
            specified `name` before creation. Defaults to :obj:`True`
        :return: A newly created :class:`BaseGlyph` instance.

        Example::

            >>> glyph = layer.newGlyph("A")

        """
        name = normalizers.normalizeGlyphName(name)
        if name not in self:
            glyph = self._newGlyph(name)
        elif clear:
            self.removeGlyph(name)
            glyph = self._newGlyph(name)
        else:
            glyph = self._getItem(name)
        self._setLayerInGlyph(glyph)
        return glyph

    def _newGlyph(self, name: str, **kwargs: Any) -> BaseGlyph:  # type: ignore[return]
        r"""Create a new glyph in the native layer.

        This is the environment implementation of
        :meth:`BaseLayer.newGlyph` and :meth:`BaseFont.newGlyph`.

        :param name: The name of the glyph to create. The value will have been
            normalized with :func:`normalizers.normalizeGlyphName` and
            tested to make sure that it is unique to the layer.
        :param \**kwargs: Additional keyword arguments.
        :return: An instance of a :class:`BaseGlyph` subclass.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def removeGlyph(self, name: str) -> None:
        """Remove the specified glyph from the layer.

        This method removes the glyph with the given `name` from the
        layer. When called from a :class:`BaseFont` instance, it
        removes the glyph from the default layer. When called from
        a :class:`BaseLayer` instance, it removes the glyph from the
        current layer.

        :param name: The name of the glyph to remove.

        Example::

            >>> layer.removeGlyph("A")

        """
        del self[name]

    def _removeGlyph(self, name: str, **kwargs: Any) -> None:
        r"""Remove the specified glyph from the native layer.

        This is the environment implementation of
        :meth:`BaseLayer.removeGlyph` and :meth:`BaseFont.removeGlyph`.

        :param name: The name of the glyph to remove. The value will
            have been normalized with :func:`normalizers.normalizeGlyphName`.
        :param \**kwargs: Additional keyword arguments.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def insertGlyph(self, glyph: BaseGlyph, name: Optional[str] = None) -> None:
        """Insert a specified glyph into the layer.

        .. deprecated::

            This method is deprecated. Use :meth:`BaseFont.__setitem__` instead.

        This method will not insert a glyph directly, but rather create
        a new :class:`BaseGlyph` instance containing the data from
        `glyph`. The data inserted from `glyph` is the same data as
        documented in :meth:`BaseGlyph.copy`.

        :param glyph: The :class:`BaseGlyph` instance to insert.
        :param name: The name to assign to the new layer after
            insertion. If value is :obj:`None`, the origninal name will
            be used. Defaults to :obj:`None`.
        :return: The newly inserted :class:`BaseGlyph` instance.

        Example::

            >>> glyph = font.insertGlyph(otherGlyph, name="glyph2")

        """
        if name is None:
            name = glyph.name
        self[name] = glyph

    def _insertGlyph(self, glyph: BaseGlyph, name: str, **kwargs: Any) -> BaseGlyph:
        r"""Insert a specified glyph into the native layer.

        This is the environment implementation of
        :meth:`BaseLayer.__setitem__` and :meth:`BaseFont.__setitem__`.

        An environment must not insert `glyph` directly, but rather copy
        it's data to a new layer.

        :param glyph: A glyph object with the attributes necessary
            for copying as defined in :meth:`BaseGlyph.copy`
        :param name: The name to assign to the new glyph after
            insertion. The value will have been normalized
            with :func:`normalizers.normalizeGlyphName` and tested to
            make sure that it is unique to the layer.
        :param \**kwargs: Additional keyword arguments.
        :return: The newly inserted :class:`BaseLayer` subclass instance.

        .. note::

            Subclasses may override this method.

        """
        if glyph.name is None or name != glyph.name:
            glyph = glyph.copy()
            glyph.name = name
        dest = self.newGlyph(name, clear=kwargs.get("clear", True))
        dest.copyData(glyph)
        return dest

    # ---------
    # Selection
    # ---------

    selectedGlyphs: dynamicProperty = dynamicProperty(
        "base_selectedGlyphs",
        """Get or set the selected glyphs in the layer.

        The value must be a :class:`list` or :class:`tuple`
        of :class:`BaseGlyph` instances.

        :return: An unordered :class:`tuple` of currently selected
            :class:`BaseGlyph` instances.

        Getting selected glyph objects::

            >>> for glyph in layer.selectedGlyphs:
            ...     glyph.markColor = (1, 0, 0, 0.5)

        Setting selected glyph objects::

            >>> layer.selectedGlyphs = someGlyphs

        """,
    )

    def _get_base_selectedGlyphs(self) -> Tuple[BaseGlyph, ...]:
        selected = tuple(
            normalizers.normalizeGlyph(glyph) for glyph in self._get_selectedGlyphs()
        )
        return selected

    def _get_selectedGlyphs(self) -> Tuple[BaseGlyph, ...]:
        """Get the selected glyphs in the native layer.

        This is the environment implementation of
        the :attr:`BaseLayer.selectedGlyphs` property getter.

        :return: An unordered :class:`tuple` of selected :class:`BaseGlyph`
            subclass instances. Each value item will be normalized
            with :func:`normalizers.normalizeGlyph`.

        .. note::

            Subclasses may override this method.

        """
        return self._getSelectedSubObjects(self)

    def _set_base_selectedGlyphs(self, value: CollectionType[BaseGlyph]) -> None:
        normalized = [normalizers.normalizeGlyph(glyph) for glyph in value]
        self._set_selectedGlyphs(normalized)

    def _set_selectedGlyphs(self, value: CollectionType[BaseGlyph]) -> None:
        """Set the selected glyphs in the native layer.

        This is the environment implementation of
        the :attr:`BaseLayer.selectedGlyphs` property setter.

        :param value: A :class:`list` or :class:`tuple` of :class:`BaseGlyph`
            subclass instances to select. Each value item will have been normalized
            with :func:`normalizers.normalizeGlyph`.

        .. note::

            Subclasses may override this method.

        """
        return self._setSelectedSubObjects(self, value)

    selectedGlyphNames: dynamicProperty = dynamicProperty(
        "base_selectedGlyphNames",
        """Get or set the selected glyph names in the layer.

        The value must be a :class:`list` or :class:`tuple` of names
        representing :class:`BaseGlyph` instances.

        :return: An unordered :class:`tuple` of glyph names representing
            the currently selected :class:`BaseGlyph` instances.

        Getting selected glyph names:

            >>> for name in layer.selectedGlyphNames:
            ...     print(name)

        Setting selected glyph names:

            >>> layer.selectedGlyphNames = ["A", "B", "C"]

        """,
    )

    def _get_base_selectedGlyphNames(self) -> Tuple[str, ...]:
        selected = tuple(
            normalizers.normalizeGlyphName(name)
            for name in self._get_selectedGlyphNames()
        )
        return selected

    def _get_selectedGlyphNames(self) -> Tuple[str, ...]:
        """Get the selected glyph names in the layer.

        This is the environment implementation of
        the :attr:`BaseLayer.selectedGlyphNames` property getter.

        :return: An unordered :class:`tuple` of glyph names representing the
            currently selected :class:`BaseGlyph` subclass instances. Each value
            item will be normalized with :func:`normalizers.normalizeGlyphName`.

        .. note::

            Subclasses may override this method.

        """
        selected = tuple(glyph.name for glyph in self.selectedGlyphs)
        return selected

    def _set_base_selectedGlyphNames(self, value: CollectionType[str]) -> None:
        normalized = [normalizers.normalizeGlyphName(name) for name in value]
        self._set_selectedGlyphNames(normalized)

    def _set_selectedGlyphNames(self, value: CollectionType[str]) -> None:
        """Set the selected glyph names in the layer.

        This is the environment implementation of
        the :attr:`BaseLayer.selectedGlyphNames` property setter.

        :param value: A :class:`list` or :class:`tuple` of names representing
            the :class:`BaseGlyph` subclass instances to select. Each value item
            will have been normalized with :func:`normalizers.normalizeGlyphName`.

        .. note::

            Subclasses may override this method.

        """
        select = [self[name] for name in value]
        self.selectedGlyphs = select

    # --------------------
    # Legacy Compatibility
    # --------------------

    has_key: Callable[[_BaseGlyphVendor, str], bool] = __contains__


class BaseLayer(_BaseGlyphVendor, InterpolationMixin, DeprecatedLayer, RemovedLayer):
    """Represent the basis for a layer object.

    This object will almost always be created by retrieving it from a
    font object. It can exist at either the font or glyph level.
    See :ref:`layers`.

    """

    def _reprContents(self) -> List[str]:
        contents: List[str] = [
            f"'{self.name}'",
        ]
        if self.color:
            contents.append(f"color={self.color!r}")
        return contents

    # ----
    # Copy
    # ----

    copyAttributes: Tuple[str, ...] = ("name", "color", "lib")

    def copy(self) -> BaseLayer:
        """Copy data from the current layer into a new layer.

        This will copy:

        - :attr:`~BaseLayer.name`
        - :attr:`~BaseLayer.color`
        - :attr:`~BaseLayer.lib`
        - :meth:`glyphs<__iter__>`

        :return: A new :class:`BaseLayer` instance with the same attributes.

        Example::

            >>> copiedLayer = layer.copy()

        """
        return super(BaseLayer, self).copy()

    def copyData(self, source: BaseLayer) -> None:
        """Copy data from another layer instance.

        Refer to :meth:`BaseLayer.copy` for a list of values that will
            be copied.

        :param source: The source :class`BaseLayer` instance from which
            to copy data.

        Example::

            >>> sourceFont = MyFont('path/to/source.ufo')
            >>> font.copyData(sourceFont)

        """
        super(BaseLayer, self).copyData(source)
        for name in source.keys():
            glyph = self.newGlyph(name)
            glyph.copyData(source[name])

    # -------
    # Parents
    # -------

    # Font

    _font = None

    font: dynamicProperty = dynamicProperty(
        "font",
        """Get  or set the layer's parent font object.

        The value must be a :class:`BaseFont` instance or :obj:`None`.

        :return: The :class:`BaseFont` instance containing the layer
            or :obj:`None`.
        :raises AssertionError: If attempting to set the font when it
            has already been set.

        Example::

            >>> font = layer.font

        """,
    )

    def _get_font(self) -> Optional[BaseFont]:
        if self._font is None:
            return None
        return self._font()

    def _set_font(self, font: Optional[BaseFont]) -> None:
        if self._font is not None:
            raise AssertionError("font for layer already set")
        if font is not None:
            font = reference(font)
        self._font = font

    # --------------
    # Identification
    # --------------

    # name

    name: dynamicProperty = dynamicProperty(
        "base_name",
        """Get or set the name of the layer.

        The value must be a :class:`str`.

        :return: A :class:`str` defining the name of the current layer
            or :obj:`None` if the layer is the default layer.
        :raises ValueError: If attempting to set the name to one that
            already exists in the font.

        Example::

            >>> layer.name
            "foreground"
            >>> layer.name = "top"

        """,
    )

    def _get_base_name(self) -> Optional[str]:
        value = self._get_name()
        if value is not None:
            value = normalizers.normalizeLayerName(value)
        return value

    def _set_base_name(self, value: str) -> None:
        if value == self.name:
            return
        value = normalizers.normalizeLayerName(value)
        font = self.font
        if font is not None:
            existing = self.font.layerOrder
            if value in existing:
                raise ValueError(f"A layer with the name '{value}' already exists.")
        self._set_name(value)

    def _get_name(self) -> Optional[str]:  # type: ignore[return]
        """Get the name of the native layer.

        This is the environment implementation of the :attr:`BaseLayer.name`
            property getter.

        :return A :class:`str` defining the name of the current layer
            or :obj:`None` to indicate that the layer is the default.
            The value will be normalized with :func:`normalizers.normalizeLayerName`.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_name(self, value: str, **kwargs: Any) -> None:
        r"""Set the name of the native layer.

        This is the environment implementation of the :attr:`BaseLayer.name`
            property setter.

        :param value: The name to assign to the layer. The value must be unique
            to the font and will have been normalized
            with :func:`normalizers.normalizeLayerName`
        :param \**kwargs: Additional keyword arguments.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # color

    color: dynamicProperty = dynamicProperty(
        "base_color",
        """Get or set the color of the layer.

        The value must be a :class:`tuple` of :class:`int`
        or :class:`float` numbers representing a :ref:`type-color`,
        or :obj`None` to indicate that the layer does not have an
        assigned color.

        :return: A :class:`tuple` containing :class:`int`
            or :class:`float` values representing the color,
            or :obj:`None` if no color is assigned.


        Example::

            >>> layer.color
            None
            >>> layer.color = (1, 0, 0, 0.5)

        """,
    )

    def _get_base_color(self) -> QuadrupleCollectionType[IntFloatType]:
        value = self._get_color()
        if value is not None:
            value = normalizers.normalizeColor(value)
            value = Color(value)
        return value

    def _set_base_color(self, value: QuadrupleCollectionType[IntFloatType]) -> None:
        if value is not None:
            value = normalizers.normalizeColor(value)
        self._set_color(value)

    def _get_color(self) -> QuadrupleCollectionType[IntFloatType]:  # type: ignore[return]
        """Get the color of the layer.

        This is the environment implementation of
        the :attr:`BaseLayer.color` property getter.

        :return: The :ref:`type-color` assigned to the layer, or :obj`None` to
            indicate that the layer does not have an assigned color. The value
            will be normalized with :func:`normalizers.normalizeColor`.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_color(
        self, value: QuadrupleCollectionType[IntFloatType], **kwargs: Any
    ) -> None:
        r"""Get or set the color of the layer.

        This is the environment implementation of
        the :attr:`BaseLayer.color` property setter.

        :param value: A :ref:`type-color` or :obj:`None` defining the
            color to assign to the layer. The value will have been normalized
            with :func:`normalizers.normalizeColor`.
        :param \**kwargs: Additional keyword arguments.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # -----------
    # Sub-Objects
    # -----------

    # lib

    lib: dynamicProperty = dynamicProperty(
        "base_lib",
        """Get the layer's lib object.

        This property is read-only.

        :return: An instance of the :class:`BaseLib` class.

        Example::

            >>> layer.lib["org.robofab.hello"]
            "world"

        """,
    )

    def _get_base_lib(self) -> BaseLib:
        lib = self._get_lib()
        lib.font = self
        return lib

    def _get_lib(self) -> BaseLib:  # type: ignore[return]
        """Get the native layer's :class:`BaseLib` object.

        This is the environment implementation of
        the :attr:`BaseLayer.lib` property getter.

        :return: An instance of a :class:`BaseLib` subclass.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        """
        self.raiseNotImplementedError()

    # tempLib

    tempLib: dynamicProperty = dynamicProperty(
        "base_tempLib",
        """Get the layer's temporary lib object.

        This property is read-only.

        This property provides access to a temporary instance of
        the :class:`BaseLib` class, used for storing data that should
        not be persisted. It is similar to :attr:`BaseLayer.lib`,
        except that its contents will not be saved when calling
        the :meth:`BaseLayer.save` method.

        :return: A temporary instance of the :class:`BaseLib` class.

        Example::

            >>> layer.tempLib["org.robofab.hello"]
            "world"

        """,
    )

    def _get_base_tempLib(self) -> BaseLib:
        lib = self._get_tempLib()
        lib.font = self
        return lib

    def _get_tempLib(self) -> BaseLib:  # type: ignore[return]
        """Get the layer's temporary lib object.

        This is the environment implementation of
        the :attr:`BaseLayer.lib` property setter.

        :return: A temporary instance of a :class:`BaseLib` subclass.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # -----------------
    # Global Operations
    # -----------------

    def round(self) -> None:
        """Round all approriate layer data to integers.

        This is the equivalent of calling the :meth:`BaseGlyph.round`
        method on all glyphs in the layer.

        Example::

            >>> layer.round()

        """
        self._round()

    def _round(self) -> None:
        """Round all approriate native layer data to integers.

        This is the environment implementation of :meth:`BaseLayer.round`.

        .. note::

            Subclasses may override this method.

        """
        for glyph in self:
            glyph.round()

    def autoUnicodes(self) -> None:
        """Use heuristics to set Unicode values in all font glyphs.

        Environments will define their own heuristics for
        automatically determining values.

        Example::

            >>> layer.autoUnicodes()

        """
        self._autoUnicodes()

    def _autoUnicodes(self) -> None:
        """Use heuristics to set Unicode values in all native font glyphs.

        This is the environment implementation of :meth:`BaseLayer.autoUnicodes`.

        .. note::

            Subclasses may override this method.

        """
        for glyph in self:
            glyph.autoUnicodes()

    # -------------
    # Interpolation
    # -------------

    def interpolate(
        self,
        factor: TransformationType,
        minLayer: BaseLayer,
        maxLayer: BaseLayer,
        round: bool = True,
        suppressError: bool = True,
    ) -> None:
        """Interpolate all possible data in the layer.

        The interpolation occurs on a 0 to 1.0 range between `minLayer`
        and `maxLayer`, using the specified `factor`.

        :param factor: The interpolation value as a single :class:`int`
            or :class:`float` or a :class:`tuple` of two :class:`int`
            or :class:`float` values representing the factors ``(x, y)``.
        :param minLayer: The :class:`BaseLayer` instance corresponding to the
            0.0 position in the interpolation.
        :param maxLayer: The :class:`BaseLayer` instance corresponding to the
            1.0 position in the interpolation.
        :param round: A :class:`bool` indicating whether the result should
            be rounded to integers. Defaults to :obj:`True`.
        :param suppressError: A :class:`bool` indicating whether to ignore
            incompatible data or raise an error when such
            incompatibilities are found. Defaults to :obj:`True`.
        :raises TypeError: If `minLayer` or `maxLayer` are not instances
            of :class:`BaseLayer`.

        Example::

            >>> layer.interpolate(0.5, otherLayer1, otherLayer2)
            >>> layer.interpolate((0.5, 2.0), otherLayer1, otherLayer2, round=False)

        """
        factor = normalizers.normalizeInterpolationFactor(factor)
        if not isinstance(minLayer, BaseLayer):
            raise TypeError(
                f"Interpolation to an instance of {self.__class__.__name__!r} can not be performed from an instance of {minLayer.__class__.__name__!r}."
            )
        if not isinstance(maxLayer, BaseLayer):
            raise TypeError(
                f"Interpolation to an instance of {self.__class__.__name__!r} can not be performed from an instance of {maxLayer.__class__.__name__!r}."
            )
        round = normalizers.normalizeBoolean(round)
        suppressError = normalizers.normalizeBoolean(suppressError)
        self._interpolate(
            factor, minLayer, maxLayer, round=round, suppressError=suppressError
        )

    def _interpolate(
        self,
        factor: TransformationType,
        minLayer: BaseLayer,
        maxLayer: BaseLayer,
        round: bool,
        suppressError: bool,
    ) -> None:
        """Interpolate all possible data in the native layer.

        This is the environment implementation of :meth:`BaseLayer.interpolate`.

        :param factor: The interpolation value as a single :class:`int`
            or :class:`float` or a :class:`tuple of two :class:`int`
            or :class:`float` values representing the factors ``(x, y)``.
        :param minLayer: The :class:`BaseLayer` subclass instance
            corresponding to the 0.0 position in the interpolation.
        :param maxLayer: The :class:`BaseLayer` subclass instance
            corresponding to the 1.0 position in the interpolation.
        :param round: A :class:`bool` indicating whether the result should
            be rounded to integers.
        :param suppressError: A :class:`bool` indicating whether to ignore
            incompatible data or raise an error when such
            incompatibilities are found.
        :raises FontPartsError: If ``suppressError=False`` and the interpolation
            data is incompatible.

        .. note::

            Subclasses may override this method.

        """
        for glyphName in self.keys():
            del self[glyphName]
        for glyphName in minLayer.keys():
            if glyphName not in maxLayer:
                continue
            minGlyph = minLayer[glyphName]
            maxGlyph = maxLayer[glyphName]
            dstGlyph = self.newGlyph(glyphName)
            dstGlyph.interpolate(
                factor, minGlyph, maxGlyph, round=round, suppressError=suppressError
            )

    compatibilityReporterClass = LayerCompatibilityReporter

    def isCompatible(self, other: BaseLayer) -> Tuple[bool, LayerCompatibilityReporter]:
        """Evaluate interpolation compatibility with another layer.

        :param other: The other :class:`BaseLayer` instance to check
            compatibility with.
        :return: A :class:`tuple` where the first element is a :class:`bool`
            indicating compatibility, and the second element is
            a :class:`fontParts.base.compatibility.LayerCompatibilityReporter`
            instance.

        Example::

            >>> compatible, report = self.isCompatible(otherLayer)
            >>> compatible
            False
            >>> report
            A
            -
            [Fatal] The glyphs do not contain the same number of contours.

        """
        return super(BaseLayer, self).isCompatible(other, BaseLayer)

    def _isCompatible(
        self, other: BaseLayer, reporter: LayerCompatibilityReporter
    ) -> None:
        """Evaluate interpolation compatibility with another native layer.

        This is the environment implementation of :meth:`BaseFont.isCompatible`.

        :param other: The other :class:`BaseLayer` subclass instance to check
            compatibility with.
        :param reporter: An object used to report compatibility issues.

        .. note::

            Subclasses may override this method.

        """
        layer1 = self
        layer2 = other

        # incompatible number of glyphs
        glyphs1 = set(layer1.keys())
        glyphs2 = set(layer2.keys())
        if len(glyphs1) != len(glyphs2):
            reporter.glyphCountDifference = True
            reporter.warning = True
        if len(glyphs1.difference(glyphs2)) != 0:
            reporter.warning = True
            reporter.glyphsMissingFromLayer2 = list(glyphs1.difference(glyphs2))
        if len(glyphs2.difference(glyphs1)) != 0:
            reporter.warning = True
            reporter.glyphsMissingInLayer1 = list(glyphs2.difference(glyphs1))
        # test glyphs
        for glyphName in sorted(glyphs1.intersection(glyphs2)):
            glyph1 = layer1[glyphName]
            glyph2 = layer2[glyphName]
            glyphCompatibility = glyph1.isCompatible(glyph2)[1]
            if glyphCompatibility.fatal or glyphCompatibility.warning:
                if glyphCompatibility.fatal:
                    reporter.fatal = True
                if glyphCompatibility.warning:
                    reporter.warning = True
                reporter.glyphs.append(glyphCompatibility)

    # -------
    # mapping
    # -------

    def getReverseComponentMapping(self) -> ReverseComponentMappingType:
        """Get a reversed map of the layer's component references.

        This method creates a :class:`dict` mapping the name of each
        component base glyph in the font to a :class:`tuple` containing
        the composite glyph names that include the comoponent. All
        glyphs are loaded.

        :return: A :class:`dict` of component glyph names mapped to
            tuples of composite glyph names.

        Example::

            >>> mapping = layer.getReverseComponentMapping()
            >>> mapping
            {'A': ('Aacute', 'Aring'), 'acute': ('Aacute',),
            'ring': ('Aring',), ...}

        """
        return self._getReverseComponentMapping()

    def _getReverseComponentMapping(self) -> ReverseComponentMappingType:
        """Get a reversed map of the native layer's component references.

        This is the environment implementation of
        :meth:`BaseFont.getReverseComponentMapping`.

        .. note::

            Subclasses may override this method.

        """
        mapping = collections.defaultdict(list)
        for glyph in self:
            if not glyph.components:
                continue
            for component in glyph.components:
                baseGlyph = component.baseGlyph
                mapping[baseGlyph].append(glyph.name)

        return {k: tuple(v) for k, v in mapping.items()}

    def getCharacterMapping(self) -> CharacterMappingType:
        """Get the layer's character mapping.

        This method creates a :class:`dict` mapping Unicode values to
        tuples of glyph names. Each Unicode value corresponds to one or
        more glyphs, and the glyph names represent these glyphs in the
        mapping.

        .. note::

            One glyph can have multiple unicode values, and a unicode value can
            have multiple glyphs pointing to it.

        :return: A :class:`dict` mapping Unicode values to tuples of
            glyph names.

        """
        return self._getCharacterMapping()

    def _getCharacterMapping(self) -> CharacterMappingType:
        """Get the native layer's character mapping.

        This is the environment implementation of
        :meth:`BaseFont.getCharacterMapping`.

        .. note::

            Subclasses may override this method.

        """
        mapping = collections.defaultdict(list)
        for glyph in self:
            if not glyph.unicodes:
                continue
            for code in glyph.unicodes:
                mapping[code].append(glyph.name)
        return {k: tuple(v) for k, v in mapping.items()}
