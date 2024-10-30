from fontParts.base.base import (
    BaseObject,
    InterpolationMixin,
    SelectionMixin,
    dynamicProperty,
    reference
)
from fontParts.base import normalizers
from fontParts.base.compatibility import LayerCompatibilityReporter
from fontParts.base.color import Color
from fontParts.base.deprecated import DeprecatedLayer, RemovedLayer


class _BaseGlyphVendor(
                       BaseObject,
                       SelectionMixin,
                       ):

    """
    This class exists to provide common glyph
    interaction code to BaseFont and BaseLayer.
    It should not be directly subclassed.
    """

    # -----------------
    # Glyph Interaction
    # -----------------

    def _setLayerInGlyph(self, glyph):
        if glyph.layer is None:
            if isinstance(self, BaseLayer):
                layer = self
            else:
                layer = self.defaultLayer
            glyph.layer = layer

<<<<<<< HEAD
    def __len__(self) -> int:
        """Return the number of glyphs in the layer.

        :return: The number of :class:`BaseGlyph` instances in
            the layer as an :class:`int`.
<<<<<<< HEAD

=======
<<<<<<< HEAD
    def __len__(self):
=======

        Example::

            >>> len(layer)
            256

>>>>>>> v1
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
        """
        An ``int`` representing number of glyphs in the layer. ::

            >>> len(layer)
            256
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        return self._len()

    def _len(self, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseLayer.__len__` and :meth:`BaseFont.__len__`
        This must return an ``int`` indicating
        the number of glyphs in the layer.

        Subclasses may override this method.
        """
        return len(self.keys())

<<<<<<< HEAD
    def __iter__(self) -> Iterator[BaseGlyph]:
        """Iterate through the glyphs in the layer.

        :return: An iterator over :class:`BaseGlyph` instances.
<<<<<<< HEAD

=======

        Example::

<<<<<<< HEAD
=======
    def __iter__(self):
        """
        Iterate through the :class:`BaseGlyph` objects in the layer. ::

=======
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
            >>> for glyph in layer:
            ...     glyph.name
            "A"
            "B"
            "C"
<<<<<<< HEAD
>>>>>>> parent of 3d67a1d (Update documentation (#739))
=======

>>>>>>> v1
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
        """
        return self._iter()

    def _iter(self, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseLayer.__iter__` and :meth:`BaseFont.__iter__`
        This must return an iterator that returns
        instances of a :class:`BaseGlyph` subclass.

        Subclasses may override this method.
        """
        for name in self.keys():
            yield self[name]

<<<<<<< HEAD
    def __getitem__(self, name: str) -> BaseGlyph:
        """Get the specified glyph from the layer.

        :param name: The name representing the glyph to retrieve.
        :return: a :class:`BaseGlyph` instance with the specified name.
        :raises KeyError: If no glyph with the given name exists in the layer.
<<<<<<< HEAD
=======

        Example::

             >>> glyph = layer["A"]
>>>>>>> v1

=======
    def __getitem__(self, name):
        """
        Get the :class:`BaseGlyph` with name from the layer. ::

            >>> glyph = layer["A"]
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        name = normalizers.normalizeGlyphName(name)
        if name not in self:
            raise KeyError("No glyph named '%s'." % name)
        glyph = self._getItem(name)
        self._setLayerInGlyph(glyph)
        return glyph

<<<<<<< HEAD
    def _getItem(self, name: str, **kwargs: Any) -> BaseGlyph:
=======
    def _getItem(self, name: str, **kwargs: Any) -> BaseGlyph:  # type: ignore[return]
>>>>>>> v1
        r"""Get the specified glyph from the native layer.

        This is the environment implementation of
        :meth:`BaseLayer.__getitem__` and :meth:`BaseFont.__getitem__`.

        :param name: The name representing the glyph to get. The value
<<<<<<< HEAD
            will be normalized with :func:`normalizers.normalizeGlyphName`.
=======
            will have been normalized with :func:`normalizers.normalizeGlyphName`.
>>>>>>> v1
        :param \**kwargs: Additional keyword arguments.
        :return: an instance of a :class:`BaseGlyph` subclass with the
            specified name.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.
=======
    def _getItem(self, name, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseLayer.__getitem__` and :meth:`BaseFont.__getitem__`
        This must return an instance of a :class:`BaseGlyph`
        subclass. **name** will be a :ref:`type-string` representing
        a name of a glyph that is in the layer. It will have been
        normalized with :func:`normalizers.normalizeGlyphName`.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def __setitem__(self, name, glyph):
        """
        Insert **glyph** into the layer. ::

            >>> glyph = font.insertGlyph(otherGlyph, name="glyph2")

        This will not insert the glyph directly. Rather, a
        new glyph will be created and the data from **glyph**
        will be copied to the new glyph. **name** indicates
        the name that should be assigned to the glyph after
        insertion. If **name** is not given, the glyph's original
        name must be used. If the glyph does not have a name,
        an error must be raised. The data that will be inserted
        from **glyph** is the same data as documented in
        :meth:`BaseGlyph.copy`.
        """
        name = normalizers.normalizeGlyphName(name)
        if name in self:
            del self[name]
        return self._insertGlyph(glyph, name=name)

<<<<<<< HEAD
    def __delitem__(self, name: str) -> None:
<<<<<<< HEAD
        """Remove the glyph with name from the layer."""
=======
<<<<<<< HEAD
    def __delitem__(self, name):
        """
        Remove the glyph with name from the layer. ::

            >>> del layer["A"]
        """
>>>>>>> parent of 3d67a1d (Update documentation (#739))
=======
        """Remove the glyph with name from the layer.

        Example::

            >>> del layer["A"]

        """
>>>>>>> v1
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
        name = normalizers.normalizeGlyphName(name)
        if name not in self:
            raise KeyError("No glyph named '%s'." % name)
        self._removeGlyph(name)

<<<<<<< HEAD
    def keys(self) -> Tuple[str, ...]:
        """Get the names of all glyphs in the layer.
<<<<<<< HEAD
=======

        This method returns an unordered :class:`tuple` of glyph names
        representing all the :class:`BaseGlyph` instances in the active
        layer. If called from a :class:`BaseFont` instance, it returns
        the glyphs from the default layer. If called from
        a :class:`BaseLayer` instance, it returns the glyphs from the
        current layer.

        :return: A :class:`tuple` of glyph names representing the glyphs
            in the current or default :class:`BaseLayer` instance.

        Example::
>>>>>>> v1

        This method returns an unordered :class:`tuple` of glyph names
        representing all the :class:`BaseGlyph` instances in the active
        layer. If called from a :class:`BaseFont` instance, it returns
        the glyphs from the default layer. If called from
        a :class:`BaseLayer` instance, it returns the glyphs from the
        current layer.

        :return: A :class:`tuple` of glyph names representing the glyphs
            in the current or default :class:`BaseLayer` instance.

        """
        return self._keys()

<<<<<<< HEAD
    def _keys(self, **kwargs: Any) -> Tuple[str, ...]:
=======
    def _keys(self, **kwargs: Any) -> Tuple[str, ...]:  # type: ignore[return]
>>>>>>> v1
        r"""Get the names of all glyphs in the native layer.

=======
    def keys(self):
        """
        Get a list of all glyphs in the layer. ::

            >>> layer.keys()
            ["B", "C", "A"]

        The order of the glyphs is undefined.
        """
        return self._keys()

    def _keys(self, **kwargs):
        """
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        This is the environment implementation of
        :meth:`BaseLayer.keys` and :meth:`BaseFont.keys`
        This must return an :ref:`type-immutable-list`
        of the names representing all glyphs in the layer.
        The order is not defined.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

<<<<<<< HEAD
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
<<<<<<< HEAD

=======
<<<<<<< HEAD
    def __contains__(self, name):
        """
        Test if the layer contains a glyph with **name**. ::

            >>> "A" in layer
            True
>>>>>>> parent of 3d67a1d (Update documentation (#739))
=======

        Example::

            >>> "A" in layer
            True

>>>>>>> v1
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
        """
        name = normalizers.normalizeGlyphName(name)
        return self._contains(name)

    def _contains(self, name, **kwargs):
        """
        This is the environment implementation of
<<<<<<< HEAD
        :meth:`BaseLayer.__contains__` and :meth:`BaseFont.__contains__`.
<<<<<<< HEAD
        :func:`normalizers.normalizeGlyphName`.

        :param name: The name of the glyph to check. The value will be
            normalized with :func:`normalizers.normalizeGlyphName`.
        :param \**kwargs: Additional keyword arguments.
        :return: :obj:`True` if the glyph exists in the layer,
            :obj:`False` otherwise.

        .. note::

            Subclasses may override this method.
=======
        :meth:`BaseLayer.__contains__` and :meth:`BaseFont.__contains__`
        This must return ``bool`` indicating if the
        layer has a glyph with the defined name.
        **name** will be a :ref-type-string` representing
        a glyph name. It will have been normalized with
        :func:`normalizers.normalizeGlyphName`.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

<<<<<<< HEAD
        Subclasses may override this method.
=======
=======

        :param name: The name of the glyph to check. The value will have been
            normalized with :func:`normalizers.normalizeGlyphName`.
        :param \**kwargs: Additional keyword arguments.
        :return: :obj:`True` if the glyph exists in the layer,
            :obj:`False` otherwise.

        .. note::

            Subclasses may override this method.

>>>>>>> v1
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
        """
        return name in self.keys()

<<<<<<< HEAD
    def newGlyph(self, name: str, clear: bool = True) -> BaseGlyph:
        """Create a new glyph in the layer.
<<<<<<< HEAD

        This method creates a new glyph with the given `name` in the
        layer. If a glyph with the same name already exists and `clear`
        is set to :obj:`True`, the existing glyph will be removed before
        creating the new one. If `clear` is set to :obj:`False`, the
        existing glyph will be returned without modification.

=======

        This method creates a new glyph with the given `name` in the
        layer. If a glyph with the same name already exists and `clear`
        is set to :obj:`True`, the existing glyph will be removed before
        creating the new one. If `clear` is set to :obj:`False`, the
        existing glyph will be returned without modification.

>>>>>>> v1
        When called from a :class:`BaseFont` instance, the glyph is
        created in the default layer. When called from
        a :class:`BaseLayer` instance, the glyph is created in the
        current layer.

        :param name: The name of the glyph to create.
        :param clear: Whether to clear any preexisting glyph with the
            specified `name` before creation. Defaults to :obj:`True`
        :return: A newly created :class:`BaseGlyph` instance.
<<<<<<< HEAD
=======

        Example::

            >>> glyph = layer.newGlyph("A")
>>>>>>> v1

=======
    def newGlyph(self, name, clear=True):
        """
        Make a new glyph with **name** in the layer. ::

            >>> glyph = layer.newGlyph("A")

        The newly created :class:`BaseGlyph` will be returned.

        If the glyph exists in the layer and clear is set to ``False``,
        the existing glyph will be returned, otherwise the default
        behavior is to clear the exisiting glyph.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
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

<<<<<<< HEAD
    def _newGlyph(self, name: str, **kwargs: Any) -> BaseGlyph:
=======
    def _newGlyph(self, name: str, **kwargs: Any) -> BaseGlyph:  # type: ignore[return]
>>>>>>> v1
        r"""Create a new glyph in the native layer.

        This is the environment implementation of
        :meth:`BaseLayer.newGlyph` and :meth:`BaseFont.newGlyph`.

<<<<<<< HEAD
        :param name: The name of the glyph to create. The value will be
=======
        :param name: The name of the glyph to create. The value will have been
>>>>>>> v1
            normalized with :func:`normalizers.normalizeGlyphName` and
            tested to make sure that it is unique to the layer.
        :param \**kwargs: Additional keyword arguments.
        :return: An instance of a :class:`BaseGlyph` subclass.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.
=======
    def _newGlyph(self, name, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseLayer.newGlyph` and :meth:`BaseFont.newGlyph`
        This must return an instance of a :class:`BaseGlyph` subclass.
        **name** will be a :ref:`type-string` representing
        a glyph name. It will have been normalized with
        :func:`normalizers.normalizeGlyphName`. The
        name will have been tested to make sure that
        no glyph with the same name exists in the layer.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

<<<<<<< HEAD
    def removeGlyph(self, name: str) -> None:
        """Remove the specified glyph from the layer.
<<<<<<< HEAD
=======

        This method removes the glyph with the given `name` from the
        layer. When called from a :class:`BaseFont` instance, it
        removes the glyph from the default layer. When called from
        a :class:`BaseLayer` instance, it removes the glyph from the
        current layer.

        :param name: The name of the glyph to remove.

        Example::
>>>>>>> v1

        This method removes the glyph with the given `name` from the
        layer. When called from a :class:`BaseFont` instance, it
        removes the glyph from the default layer. When called from
        a :class:`BaseLayer` instance, it removes the glyph from the
        current layer.

        :param name: The name of the glyph to remove.

=======
    def removeGlyph(self, name):
        """
        Remove the glyph with name from the layer. ::

            >>> layer.removeGlyph("A")

        This method is deprecated. :meth:`BaseFont.__delitem__` instead.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        del self[name]

    def _removeGlyph(self, name, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseLayer.removeGlyph` and :meth:`BaseFont.removeGlyph`.
        **name** will be a :ref:`type-string` representing a
        glyph name of a glyph that is in the layer. It will
        have been normalized with :func:`normalizers.normalizeGlyphName`.
        The newly created :class:`BaseGlyph` must be returned.

<<<<<<< HEAD
        :param name: The name of the glyph to remove. The value will
<<<<<<< HEAD
            be normalized with :func:`normalizers.normalizeGlyphName`.
=======
            have been normalized with :func:`normalizers.normalizeGlyphName`.
>>>>>>> v1
        :param \**kwargs: Additional keyword arguments.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

=======
        Subclasses must override this method.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        self.raiseNotImplementedError()

<<<<<<< HEAD
    def insertGlyph(self, glyph, name=None):
        """
        Insert **glyph** into the layer. ::
=======
    def insertGlyph(self, glyph: BaseGlyph, name: Optional[str] = None) -> None:
        """Insert a specified glyph into the layer.

        .. deprecated::

            This method is deprecated. Use :meth:`BaseFont.__setitem__` instead.

        This method will not insert a glyph directly, but rather create
        a new :class:`BaseGlyph` instance containing the data from
        `glyph`. The data inserted from `glyph` is the same data as
        documented in :meth:`BaseGlyph.copy`.
<<<<<<< HEAD

        :param glyph: The :class:`BaseGlyph` instance to insert.
        :param name: The name to assign to the new layer after
            insertion. If value is :obj:`None`, the origninal name will
            be used. Defaults to :obj:`None`.
        :return: The newly inserted :class:`BaseGlyph` instance.

=======

        :param glyph: The :class:`BaseGlyph` instance to insert.
        :param name: The name to assign to the new layer after
            insertion. If value is :obj:`None`, the origninal name will
            be used. Defaults to :obj:`None`.
        :return: The newly inserted :class:`BaseGlyph` instance.

>>>>>>> v1
        Example::
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea

            >>> glyph = layer.insertGlyph(otherGlyph, name="A")

        This method is deprecated. :meth:`BaseFont.__setitem__` instead.
        """
        if name is None:
            name = glyph.name
        self[name] = glyph

    def _insertGlyph(self, glyph, name, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseLayer.__setitem__` and :meth:`BaseFont.__setitem__`.
<<<<<<< HEAD

        An environment must not insert `glyph` directly, but rather copy
        it's data to a new layer.

        :param glyph: A glyph object with the attributes necessary
            for copying as defined in :meth:`BaseGlyph.copy`
        :param name: The name to assign to the new glyph after
<<<<<<< HEAD
            insertion. The value will be normalized
=======
            insertion. The value will have been normalized
>>>>>>> v1
            with :func:`normalizers.normalizeGlyphName` and tested to
            make sure that it is unique to the layer.
        :param \**kwargs: Additional keyword arguments.
        :return: The newly inserted :class:`BaseLayer` subclass instance.

        .. note::

            Subclasses may override this method.

=======
        This must return an instance of a :class:`BaseGlyph` subclass.
        **glyph** will be a glyph object with the attributes necessary
        for copying as defined in :meth:`BaseGlyph.copy` An environment
        must not insert **glyph** directly. Instead the data from
        **glyph** should be copied to a new glyph instead. **name**
        will be a :ref:`type-string` representing a glyph name. It
        will have been normalized with :func:`normalizers.normalizeGlyphName`.
        **name** will have been tested to make sure that no glyph with
        the same name exists in the layer.

        Subclasses may override this method.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
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

    selectedGlyphs = dynamicProperty(
        "base_selectedGlyphs",
<<<<<<< HEAD
        """
        A list of glyphs selected in the layer.

<<<<<<< HEAD
=======
        Getting selected glyph objects:
=======
        """Get or set the selected glyphs in the layer.
<<<<<<< HEAD
=======
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea

            >>> for glyph in layer.selectedGlyphs:
            ...     glyph.markColor = (1, 0, 0, 0.5)

        Setting selected glyph objects:

<<<<<<< HEAD
            >>> layer.selectedGlyphs = someGlyphs
>>>>>>> parent of 3d67a1d (Update documentation (#739))
=======
        Getting selected glyph objects::
>>>>>>> v1

        The value must be a :class:`list` or :class:`tuple`
        of :class:`BaseGlyph` instances.

<<<<<<< HEAD
        :return: An unordered :class:`tuple` of currently selected
            :class:`BaseGlyph` instances.

=======
        Setting selected glyph objects::

            >>> layer.selectedGlyphs = someGlyphs

>>>>>>> v1
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
        """
    )

    def _get_base_selectedGlyphs(self):
        selected = tuple([normalizers.normalizeGlyph(glyph) for glyph in
                         self._get_selectedGlyphs()])
        return selected

<<<<<<< HEAD
    def _get_selectedGlyphs(self) -> Tuple[BaseGlyph]:
        """Get the selected glyphs in the native layer.

        This is the environment implementation of
        the :attr:`BaseLayer.selectedGlyphs` property getter.

        :return: An unordered :class:`tuple` of selected :class:`BaseGlyph`
<<<<<<< HEAD
            subclass instances.
=======
            subclass instances. Each value item will be normalized
            with :func:`normalizers.normalizeGlyph`.
>>>>>>> v1

        .. note::

            Subclasses may override this method.

=======
    def _get_selectedGlyphs(self):
        """
        Subclasses may override this method.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        return self._getSelectedSubObjects(self)

    def _set_base_selectedGlyphs(self, value):
        normalized = [normalizers.normalizeGlyph(glyph) for glyph in value]
        self._set_selectedGlyphs(normalized)

<<<<<<< HEAD
    def _set_selectedGlyphs(self, value: CollectionType[BaseGlyph]) -> None:
        """Set the selected glyphs in the native layer.

        This is the environment implementation of
        the :attr:`BaseLayer.selectedGlyphs` property setter.

        :param value: A :class:`list` or :class:`tuple` of :class:`BaseGlyph`
<<<<<<< HEAD
            subclass instances to select.
=======
            subclass instances to select. Each value item will have been normalized
            with :func:`normalizers.normalizeGlyph`.
>>>>>>> v1

        .. note::

            Subclasses may override this method.

=======
    def _set_selectedGlyphs(self, value):
        """
        Subclasses may override this method.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        return self._setSelectedSubObjects(self, value)

    selectedGlyphNames = dynamicProperty(
        "base_selectedGlyphNames",
<<<<<<< HEAD
        """
        A list of names of glyphs selected in the layer.
=======
        """Get or set the selected glyph names in the layer.
<<<<<<< HEAD
=======

        The value must be a :class:`list` or :class:`tuple` of names
        representing :class:`BaseGlyph` instances.

        :return: An unordered :class:`tuple` of glyph names representing
            the currently selected :class:`BaseGlyph` instances.
>>>>>>> v1
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea

<<<<<<< HEAD
=======
        Getting selected glyph names:

            >>> for name in layer.selectedGlyphNames:
            ...     print(name)

        Setting selected glyph names:

<<<<<<< HEAD
            >>> layer.selectedGlyphNames = ["A", "B", "C"]
>>>>>>> parent of 3d67a1d (Update documentation (#739))
=======
<<<<<<< HEAD
=======
        Setting selected glyph names:

            >>> layer.selectedGlyphNames = ["A", "B", "C"]

>>>>>>> v1
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
        """
    )

    def _get_base_selectedGlyphNames(self):
        selected = tuple([normalizers.normalizeGlyphName(name) for name in
                         self._get_selectedGlyphNames()])
        return selected

<<<<<<< HEAD
    def _get_selectedGlyphNames(self) -> Tuple[str, ...]:
        """Get the selected glyph names in the layer.

        This is the environment implementation of
        the :attr:`BaseLayer.selectedGlyphNames` property getter.

<<<<<<< HEAD
        :return: An unordered :class:`tuple` of glyph names representing
            the currently selected :class:`BaseGlyph` subclass instances.
=======
        :return: An unordered :class:`tuple` of glyph names representing the
            currently selected :class:`BaseGlyph` subclass instances. Each value
            item will be normalized with :func:`normalizers.normalizeGlyphName`.
>>>>>>> v1

        .. note::

            Subclasses may override this method.

=======
    def _get_selectedGlyphNames(self):
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        Subclasses may override this method.
        """
        selected = [glyph.name for glyph in self.selectedGlyphs]
        return selected

    def _set_base_selectedGlyphNames(self, value):
        normalized = [normalizers.normalizeGlyphName(name) for name in value]
        self._set_selectedGlyphNames(normalized)

<<<<<<< HEAD
    def _set_selectedGlyphNames(self, value: CollectionType[str]) -> None:
        """Set the selected glyph names in the layer.

        This is the environment implementation of
        the :attr:`BaseLayer.selectedGlyphNames` property setter.

        :param value: A :class:`list` or :class:`tuple` of names representing
<<<<<<< HEAD
            the :class:`BaseGlyph` subclass instances to select.
=======
            the :class:`BaseGlyph` subclass instances to select. Each value item
            will have been normalized with :func:`normalizers.normalizeGlyphName`.
>>>>>>> v1

        .. note::

            Subclasses may override this method.

=======
    def _set_selectedGlyphNames(self, value):
        """
        Subclasses may override this method.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        select = [self[name] for name in value]
        self.selectedGlyphs = select

    # --------------------
    # Legacy Compatibility
    # --------------------

<<<<<<< HEAD
    has_key = __contains__
=======
    has_key: Callable[[_BaseGlyphVendor, str], bool] = __contains__

<<<<<<< HEAD
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea


class BaseLayer(_BaseGlyphVendor, InterpolationMixin, DeprecatedLayer, RemovedLayer):

<<<<<<< HEAD
    def _reprContents(self):
        contents = [
           "'%s'" % self.name,
=======
=======

class BaseLayer(_BaseGlyphVendor,
                InterpolationMixin,
                DeprecatedLayer,
                RemovedLayer):
    """Represent the basis for a layer object.

    This object will almost always be created by retrieving it from a
    font object. It can exist at either the font or glyph level.
    See :ref:`layers`.

>>>>>>> v1
    """

    def _reprContents(self) -> List[str]:
        contents: List[str] = [
            "'%s'" % self.name,
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
        ]
        if self.color:
            contents.append("color=%r" % str(self.color))
        return contents

    # ----
    # Copy
    # ----

    copyAttributes = (
        "name",
        "color",
        "lib"
    )

    def copy(self):
        """
        Copy the layer into a new layer that does not
        belong to a font. ::

            >>> copiedLayer = layer.copy()

        This will copy:

        * name
        * color
        * lib
        * glyphs
        """
        return super(BaseLayer, self).copy()

<<<<<<< HEAD
    def copyData(self, source: BaseLayer) -> None:
<<<<<<< HEAD
        """Copy data from `source` into the current layer.
=======
        """Copy data from another layer instance.
>>>>>>> v1

        Refer to :meth:`BaseLayer.copy` for a list of values that will
            be copied.

        :param source: The source :class`BaseLayer` instance from which
            to copy data.

        Example::

            >>> sourceFont = MyFont('path/to/source.ufo')
            >>> font.copyData(sourceFont)

=======
    def copyData(self, source):
        """
        Copy data from **source** into this layer.
        Refer to :meth:`BaseLayer.copy` for a list
        of values that will be copied.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
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

    font = dynamicProperty(
        "font",
<<<<<<< HEAD
        """Get the layer's parent font object.

        :return: An instance of the :class:`BaseFont` class.
=======
        """Get  or set the layer's parent font object.

        The value must be a :class:`BaseFont` instance or :obj:`None`.

        :return: The :class:`BaseFont` instance containing the layer
            or :obj:`None`.
>>>>>>> v1
        :raises AssertionError: If attempting to set the font when it
            has already been set.

        Example::
=======
        """
        The layer's parent :class:`BaseFont`. ::
>>>>>>> parent of 3d67a1d (Update documentation (#739))

            >>> font = layer.font
        """
    )

    def _get_font(self):
        if self._font is None:
            return None
        return self._font()

    def _set_font(self, font):
        if self._font is not None:
            raise AssertionError("font for layer already set")
        if font is not None:
            font = reference(font)
        self._font = font

    # --------------
    # Identification
    # --------------

    # name

    name = dynamicProperty(
        "base_name",
        """
        The name of the layer. ::

            >>> layer.name
            "foreground"
            >>> layer.name = "top"
        """
    )

    def _get_base_name(self):
        value = self._get_name()
        if value is not None:
            value = normalizers.normalizeLayerName(value)
        return value

    def _set_base_name(self, value):
        if value == self.name:
            return
        value = normalizers.normalizeLayerName(value)
        font = self.font
        if font is not None:
            existing = self.font.layerOrder
            if value in existing:
                raise ValueError("A layer with the name '%s' already exists."
                                 % value)
        self._set_name(value)

<<<<<<< HEAD
    def _get_name(self) -> Optional[str]:
=======
    def _get_name(self) -> Optional[str]:  # type: ignore[return]
>>>>>>> v1
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
=======
    def _get_name(self):
        """
        This is the environment implementation of :attr:`BaseLayer.name`.
        This must return a :ref:`type-string` defining the name of the
        layer. If the layer is the default layer, the returned value
        must be ``None``. It will be normalized with
        :func:`normalizers.normalizeLayerName`.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

<<<<<<< HEAD
    def _set_name(self, value: str, **kwargs: Any) -> None:
        r"""Set the name of the native layer.

        This is the environment implementation of the :attr:`BaseLayer.name`
            property setter.

<<<<<<< HEAD
        :param value: The name to assign to the layer. The value will be
            normalized with :func:`normalizers.normalizeLayerName` and must be
            unique to the font.
=======
        :param value: The name to assign to the layer. The value must be unique
            to the font and will have been normalized
            with :func:`normalizers.normalizeLayerName`
>>>>>>> v1
        :param \**kwargs: Additional keyword arguments.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.
=======
    def _set_name(self, value, **kwargs):
        """
        This is the environment implementation of :attr:`BaseLayer.name`.
        **value** will be a :ref:`type-string` defining the name of the
        layer. It will have been normalized with
        :func:`normalizers.normalizeLayerName`.
        No layer with the same name will exist.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # color

    color = dynamicProperty(
        "base_color",
        """
        The layer's color. ::

            >>> layer.color
            None
            >>> layer.color = (1, 0, 0, 0.5)
        """
    )

    def _get_base_color(self):
        value = self._get_color()
        if value is not None:
            value = normalizers.normalizeColor(value)
            value = Color(value)
        return value

    def _set_base_color(self, value):
        if value is not None:
            value = normalizers.normalizeColor(value)
        self._set_color(value)

<<<<<<< HEAD
    def _get_color(self) -> ColorType:
=======
    def _get_color(self) -> ColorType:  # type: ignore[return]
>>>>>>> v1
        """Get the color of the layer.

        This is the environment implementation of
        the :attr:`BaseLayer.color` property getter.

<<<<<<< HEAD
        :return: A : defining the :ref:`type-color` assigned to the
            layer or :obj`None` to indicate that the layer does not have
            an assigned color. The value will be normalized with
            :func:`normalizers.normalizeColor`.
=======
        :return: The :ref:`type-color` assigned to the layer, or :obj`None` to
            indicate that the layer does not have an assigned color. The value
            will be normalized with :func:`normalizers.normalizeColor`.
>>>>>>> v1
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.
=======
    def _get_color(self):
        """
        This is the environment implementation of :attr:`BaseLayer.color`.
        This must return a :ref:`type-color` defining the
        color assigned to the layer. If the layer does not
        have an assigned color, the returned value must be
        ``None``. It will be normalized with
        :func:`normalizers.normalizeColor`.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

<<<<<<< HEAD
    def _set_color(self, value: ColorType, **kwargs: Any) -> None:
        r"""Get or set the color of the layer.

        This is the environment implementation of
        the :attr:`BaseLayer.color` property setter.

        :param value: A :ref:`type-color` or :obj:`None` defining the
<<<<<<< HEAD
            color to assign to the layer. The value will be normalized
=======
            color to assign to the layer. The value will have been normalized
>>>>>>> v1
            with :func:`normalizers.normalizeColor`.
        :param \**kwargs: Additional keyword arguments.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.
=======
    def _set_color(self, value, **kwargs):
        """
        This is the environment implementation of :attr:`BaseLayer.color`.
        **value** will be a :ref:`type-color` or ``None`` defining the
        color to assign to the layer. It will have been normalized with
        :func:`normalizers.normalizeColor`.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # -----------
    # Sub-Objects
    # -----------

    # lib

    lib = dynamicProperty(
        "base_lib",
<<<<<<< HEAD
        """Get the layer's lib object.

<<<<<<< HEAD
=======
        This property is read-only.

>>>>>>> v1
        :return: An instance of the :class:`BaseLib` class.

        Example::
=======
        """
        The layer's :class:`BaseLib` object. ::
>>>>>>> parent of 3d67a1d (Update documentation (#739))

            >>> layer.lib["org.robofab.hello"]
            "world"
        """
    )

    def _get_base_lib(self):
        lib = self._get_lib()
        lib.font = self
        return lib

<<<<<<< HEAD
    def _get_lib(self) -> BaseLib:
=======
    def _get_lib(self) -> BaseLib:  # type: ignore[return]
>>>>>>> v1
        """Get the native layer's :class:`BaseLib` object.

        This is the environment implementation of
        the :attr:`BaseLayer.lib` property getter.

        :return: An instance of a :class:`BaseLib` subclass.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

=======
    def _get_lib(self):
        """
        This is the environment implementation of :attr:`BaseLayer.lib`.
        This must return an instance of a :class:`BaseLib` subclass.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        self.raiseNotImplementedError()

    # tempLib

    tempLib = dynamicProperty(
        "base_tempLib",
<<<<<<< HEAD
        """Get the layer's temporary lib object.

<<<<<<< HEAD
=======
        This property is read-only.

>>>>>>> v1
        This property provides access to a temporary instance of
        the :class:`BaseLib` class, used for storing data that should
        not be persisted. It is similar to :attr:`BaseLayer.lib`,
        except that its contents will not be saved when calling
        the :meth:`BaseLayer.save` method.

        :return: A temporary instance of the :class:`BaseLib` class.

        Example::
=======
        """
        The layer's :class:`BaseLib` object. ::
>>>>>>> parent of 3d67a1d (Update documentation (#739))

            >>> layer.tempLib["org.robofab.hello"]
            "world"
        """
    )

    def _get_base_tempLib(self):
        lib = self._get_tempLib()
        lib.font = self
        return lib

<<<<<<< HEAD
    def _get_tempLib(self) -> BaseLib:
=======
    def _get_tempLib(self) -> BaseLib:  # type: ignore[return]
>>>>>>> v1
        """Get the layer's temporary lib object.

        This is the environment implementation of
        the :attr:`BaseLayer.lib` property setter.

        :return: A temporary instance of a :class:`BaseLib` subclass.
        :raises NotImplementedError: If the method has not been
            overridden by a subclass.

        .. important::

            Subclasses must override this method.

=======
    def _get_tempLib(self):
        """
        This is the environment implementation of :attr:`BaseLayer.tempLib`.
        This must return an instance of a :class:`BaseLib` subclass.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        self.raiseNotImplementedError()

    # -----------------
    # Global Operations
    # -----------------

    def round(self):
        """
        Round all approriate data to integers. ::

            >>> layer.round()

        This is the equivalent of calling the round method on:

        * all glyphs in the layer
        """
        self._round()

    def _round(self):
        """
        This is the environment implementation of :meth:`BaseLayer.round`.

        Subclasses may override this method.
        """
        for glyph in self:
            glyph.round()

    def autoUnicodes(self):
        """
        Use heuristics to set Unicode values in all glyphs. ::

            >>> layer.autoUnicodes()

        Environments will define their own heuristics for
        automatically determining values.
        """
        self._autoUnicodes()

    def _autoUnicodes(self):
        """
        This is the environment implementation of
        :meth:`BaseLayer.autoUnicodes`.

        Subclasses may override this method.
        """
        for glyph in self:
            glyph.autoUnicodes()

    # -------------
    # Interpolation
    # -------------

    def interpolate(self, factor, minLayer, maxLayer, round=True,
                    suppressError=True):
        """
        Interpolate all possible data in the layer. ::

            >>> layer.interpolate(0.5, otherLayer1, otherLayer2)
            >>> layer.interpolate((0.5, 2.0), otherLayer1, otherLayer2, round=False)

        The interpolation occurs on a 0 to 1.0 range where **minLayer**
        is located at 0 and **maxLayer** is located at 1.0. **factor**
        is the interpolation value. It may be less than 0 and greater
        than 1.0. It may be a :ref:`type-int-float` or a tuple of
        two :ref:`type-int-float`. If it is a tuple, the first
        number indicates the x factor and the second number indicates
        the y factor. **round** indicates if the result should be
        rounded to integers. **suppressError** indicates if incompatible
        data should be ignored or if an error should be raised when
        such incompatibilities are found.
        """
        factor = normalizers.normalizeInterpolationFactor(factor)
        if not isinstance(minLayer, BaseLayer):
            raise TypeError(("Interpolation to an instance of %r can not be "
                             "performed from an instance of %r.")
                            % (self.__class__.__name__, minLayer.__class__.__name__))
        if not isinstance(maxLayer, BaseLayer):
            raise TypeError(("Interpolation to an instance of %r can not be "
                             "performed from an instance of %r.")
                            % (self.__class__.__name__, maxLayer.__class__.__name__))
        round = normalizers.normalizeBoolean(round)
        suppressError = normalizers.normalizeBoolean(suppressError)
        self._interpolate(factor, minLayer, maxLayer,
                          round=round, suppressError=suppressError)

<<<<<<< HEAD
    def _interpolate(self,
                     factor: FactorType,
                     minLayer: BaseLayer,
                     maxLayer: BaseLayer,
<<<<<<< HEAD
                     round: bool = True,
                     suppressError: bool = True) -> None:
=======
                     round: bool,
                     suppressError: bool) -> None:
>>>>>>> v1
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
<<<<<<< HEAD
            be rounded to integers. Defaults to :obj:`True`.
        :param suppressError: A :class:`bool` indicating whether to ignore
            incompatible data or raise an error when such
            incompatibilities are found. Defaults to :obj:`True`.
=======
            be rounded to integers.
        :param suppressError: A :class:`bool` indicating whether to ignore
            incompatible data or raise an error when such
            incompatibilities are found.
>>>>>>> v1
        :raises FontPartsError: If ``suppressError=False`` and the interpolation
            data is incompatible.

        .. note::

            Subclasses may override this method.
=======
    def _interpolate(self, factor, minLayer, maxLayer, round=True,
                     suppressError=True):
        """
        This is the environment implementation of
        :meth:`BaseLayer.interpolate`.
>>>>>>> parent of 3d67a1d (Update documentation (#739))

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
            dstGlyph.interpolate(factor, minGlyph, maxGlyph,
                                 round=round, suppressError=suppressError)

    compatibilityReporterClass = LayerCompatibilityReporter

<<<<<<< HEAD
    def isCompatible(self, other):
        """
        Evaluate interpolation compatibility with **other**. ::

            >>> compat, report = self.isCompatible(otherLayer)
            >>> compat
=======
    def isCompatible(self, other: BaseLayer) -> tuple[bool, str]:
        """Evaluate interpolation compatibility with another layer.

        :param other: The other :class:`BaseLayer` instance to check
            compatibility with.
        :return: A :class:`tuple` where the first element is a :class:`bool`
            indicating compatibility, and the second element is a :class:`str`
            of compatibility notes.
<<<<<<< HEAD

        Example::

=======

        Example::

>>>>>>> v1
            >>> compatible, report = self.isCompatible(otherLayer)
            >>> compatible
>>>>>>> 22b80489e1d622ce017f67062fcffa4595ce82ea
            False
            >>> report
            A
            -
            [Fatal] The glyphs do not contain the same number of contours.

        This will return a ``bool`` indicating if the layer is
        compatible for interpolation with **other** and a
        :ref:`type-string` of compatibility notes.
        """
        return super(BaseLayer, self).isCompatible(other, BaseLayer)

    def _isCompatible(self, other, reporter):
        """
        This is the environment implementation of
        :meth:`BaseLayer.isCompatible`.

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

<<<<<<< HEAD
    def getReverseComponentMapping(self) -> ReverseComponentMappingType:
        """Get a reversed map of the layer's component references.

        This method creates a :class:`dict` mapping the name of each
        component base glyph in the font to a :class:`tuple` containing
        the composite glyph names that include the comoponent. All
        glyphs are loaded.

<<<<<<< HEAD
        Note that one glyph can have multiple unicode values, and a
        unicode value can have multiple glyphs pointing to it.

=======
>>>>>>> v1
        :return: A :class:`dict` of component glyph names mapped to
            tuples of composite glyph names.

        Example::

<<<<<<< HEAD
            >>> mapping = getReverseComponentMapping()
=======
            >>> mapping = layer.getReverseComponentMapping()
>>>>>>> v1
            >>> mapping
            {'A': ('Aacute', 'Aring'), 'acute': ('Aacute',),
            'ring': ('Aring',), ...}

=======
    def getReverseComponentMapping(self):
        """
        Create a dictionary of unicode -> [glyphname, ...] mappings.
        All glyphs are loaded. Note that one glyph can have multiple
        unicode values, and a unicode value can have multiple glyphs
        pointing to it.
>>>>>>> parent of 3d67a1d (Update documentation (#739))
        """
        return self._getReverseComponentMapping()

    def _getReverseComponentMapping(self):
        """
        This is the environment implementation of
        :meth:`BaseFont.getReverseComponentMapping`.

        Subclasses may override this method.
        """
<<<<<<< HEAD
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

<<<<<<< HEAD
=======
        .. note::

            One glyph can have multiple unicode values, and a unicode value can
            have multiple glyphs pointing to it.

>>>>>>> v1
        :return: A :class:`dict` mapping Unicode values to tuples of
            glyph names.
=======
        self.raiseNotImplementedError()
>>>>>>> parent of 3d67a1d (Update documentation (#739))

    def getCharacterMapping(self):
        """
        Get a reversed map of component references in the font.
        {
        'A' : ['Aacute', 'Aring']
        'acute' : ['Aacute']
        'ring' : ['Aring']
        etc.
        }
        """
        return self._getCharacterMapping()

    def _getCharacterMapping(self):
        """
        This is the environment implementation of
        :meth:`BaseFont.getCharacterMapping`.

        Subclasses may override this method.
        """
        self.raiseNotImplementedError()
