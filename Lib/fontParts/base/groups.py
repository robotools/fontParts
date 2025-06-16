from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Dict, Iterator, List, Optional, Tuple, Union
from collections.abc import MutableMapping

from fontParts.base.base import BaseDict, dynamicProperty, reference
from fontParts.base import normalizers
from fontParts.base.deprecated import DeprecatedGroups, RemovedGroups
from fontParts.base.annotations import CollectionType

if TYPE_CHECKING:
    from fontParts.base.font import BaseFont
    from fontParts.base.base import BaseKeys
    from fontParts.base.base import BaseItems
    from fontParts.base.base import BaseValues

ValueType = Tuple[str, ...]
GroupsDict = Dict[str, ValueType]


class BaseGroups(BaseDict, DeprecatedGroups, RemovedGroups):
    """Represent the basis for a groups object.

    This object behaves like a Python :class:`dict` object. Most of the
    dictionary functionality comes from :class:`BaseDict`. Consult that
    object's documentation for the required environment implementation
    details.

    :cvar keyNormalizer: A function to normalize the key of the dictionary.
        Defaults to :func:`normalizers.normalizeGroupKey`
    :cvar valueNormalizer: A function to normalize the value of the dictionary.
        Defaults to :func:`Normalizers.noramlizeGroupValue`

    This object is normally created as part of a :class:`BaseFont`.
    An orphan :class:`BaseGroups` object instance can be created like this::

        >>> groups = RGroups()

    """

    keyNormalizer: Callable[[str], str] = normalizers.normalizeGroupKey
    valueNormalizer: Callable[[CollectionType[str]], ValueType] = (
        normalizers.normalizeGroupValue
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
        """Get or set the groups's parent font object.

        The value must be a :class:`BaseFont` instance or :obj:`None`.

        :return: The :class:`BaseFont` instance containing the group
            or :obj:`None`.
        :raises AssertionError:
            - If attempting to set the font when it has already been set and is
              not the same as the provided font.

        Example::

            >>> font = groups.font

        """,
    )

    def _get_font(self) -> Optional[BaseFont]:
        if self._font is None:
            return None
        return self._font()

    def _set_font(
        self, font: Optional[Union[BaseFont, Callable[[], BaseFont]]]
    ) -> None:
        if self._font is not None and self._font != font:
            raise AssertionError("font for groups already set and is not same as font")
        if font is not None:
            font = reference(font)
        self._font = font

    # ---------
    # Searching
    # ---------

    def findGlyph(self, glyphName: str) -> List[str]:
        """Retrieve the groups associated with the given glyph.

        :param glyphName: The name of the glyph to search for as a :class:`str`.
        :return: A :class:`list` of :class:`str` items.


        Example::

            >>> font.groups.findGlyph("A")
            ["A_accented"]

        """
        glyphName = normalizers.normalizeGlyphName(glyphName)
        groupNames = self._findGlyph(glyphName)
        return [type(self).keyNormalizer(groupName) for groupName in groupNames]

    def _findGlyph(self, glyphName: str) -> List[str]:
        """Retrieve the groups associated with the given native glyph.

        This is the environment implementation of :meth:`BaseGroups.findGlyph`.

        :param glyphName: The name of the glyph to search for as a :class:`str`.
            The value will have been normalized
            with :func:`normalizers.normalizeGlyphName`.
        :return: A :class:`list` of :class:`str` items.

        .. note::

            Subclasses may override this method.

        """
        found = []
        for key, groupList in self.items():
            if glyphName in groupList:
                found.append(key)
        return found

    # --------------
    # Kerning Groups
    # --------------

    side1KerningGroups: dynamicProperty = dynamicProperty(
        "base_side1KerningGroups",
        """Get all groups marked as potential side 1 (left) kerning members.

        This property is read-only.

        :return: A :class:`dict` of :class:`str` group names mapped
            to a :class:`tuple` of :class:`str` glyph names.

        Example::

            >>> side1Groups = groups.side1KerningGroups

        """,
    )

    def _get_base_side1KerningGroups(self) -> GroupsDict:
        kerningGroups = self._get_side1KerningGroups()
        normalized = {}
        for name, members in kerningGroups.items():
            name = normalizers.normalizeGroupKey(name)
            members = normalizers.normalizeGroupValue(members)
            normalized[name] = members
        return normalized

    def _get_side1KerningGroups(self) -> GroupsDict:
        """Get all native groups marked as potential side 1 (left) kerning members.

        This is the environment implementation of the
        :attr:`BaseGroups.side1KerningGroups` property getter.

        :return: A :class:`dict` of :class:`str` group names mapped
            to a :class:`tuple` of :class:`str` glyph names.

        .. note::

            Subclasses may override this method.

        """
        found = {}
        for name, contents in self.items():
            if name.startswith("public.kern1."):
                found[name] = contents
        return found

    side2KerningGroups: dynamicProperty = dynamicProperty(
        "base_side2KerningGroups",
        """Get all groups marked as potential side 2 (right) kerning members.

        This property is read-only.

        :return: A :class:`dict` of :class:`str` group names mapped
            to a :class:`tuple` of :class:`str` glyph names.

        Example::

            >>> side2Groups = groups.side2KerningGroups

        """,
    )

    def _get_base_side2KerningGroups(self) -> GroupsDict:
        kerningGroups = self._get_side2KerningGroups()
        normalized = {}
        for name, members in kerningGroups.items():
            name = normalizers.normalizeGroupKey(name)
            members = normalizers.normalizeGroupValue(members)
            normalized[name] = members
        return normalized

    def _get_side2KerningGroups(self) -> GroupsDict:
        """Get all native groups marked as potential side 2 (right) kerning members.

        This is the environment implementation of the
        :attr:`BaseGroups.side2KerningGroups` property getter.

        :return: A :class:`dict` of :class:`str` group names mapped
            to a :class:`tuple` of :class:`str` glyph names.

        .. note::

            Subclasses may override this method.

        """
        found = {}
        for name, contents in self.items():
            if name.startswith("public.kern2."):
                found[name] = contents
        return found

    # ---------------------
    # RoboFab Compatibility
    # ---------------------

    def remove(self, groupName: str) -> None:
        """Remove the given group from the current groups.

        :param: groupName: The name of the group to be removed as a :class:`str`.

        .. note::

            This is a backwards compatibility method.

        Example::

            >>> font.groups.remove("myKey")

        """
        del self[groupName]

    def asDict(self) -> GroupsDict:
        """Return the groups as a dictionary.

        :return A :class:`dict` reflecting the contents of the current groups.

        .. note::

            This is a backwards compatibility method.

        Example::

            >>> font.groups.asDict()

        """
        return dict(self)

    # -------------------
    # Inherited Functions
    # -------------------

    def __contains__(self, groupName: str) -> bool:
        """Check if the given key exists in the groups.

        :param groupName: The group name to check for existence as a :class:`str`.
        :return: :obj:`True` if the `groupName` exists in the
            groups, :obj:`False` otherwise.

        Example::

            >>> "myGroup" in font.groups
            True

        """
        return super(BaseGroups, self).__contains__(groupName)

    def __delitem__(self, groupName: str) -> None:
        """Remove the given group from the current groups instance.

        :param groupName: The name of the group to remove as a :class:`str`.

        Example::

            >>> del font.groups["myGroup"]

        """
        super(BaseGroups, self).__delitem__(groupName)

    def __getitem__(self, groupName: str) -> Tuple[str, ...]:
        """Get the contents of the given group.

        :param groupName: The group name to retrieve the value for as a :class:`str`.
        :return: A :class:`tuple` of :class:`str` glyph names.
        :raise KeyError: If the specified `groupName` does not exist.

        Example::

            >>> font.groups["myGroup"]
            ("A", "B", "C")

        .. note::

            Any changes to the returned lib contents will not be reflected in
            it's :class:`BaseGroups` instance. To make changes to this content,
            do the following::

                >>> group = font.groups["myGroup"]
                >>> group.remove("A")
                >>> font.groups["myGroup"] = group

        """
        return super(BaseGroups, self).__getitem__(groupName)

    def __iter__(self) -> Iterator[str]:
        """Return an iterator over the keys in the current groups instance.

        The iteration order is not fixed.

        :return: An :class:`Iterator` over the :class:`str` keys.

        Example::

            >>> for groupName in font.groups:
            >>>     print groupName
            "myGroup"
            "myGroup3"
            "myGroup2"

        """
        return super(BaseGroups, self).__iter__()

    def __len__(self) -> int:
        """Return the number of groups in the current groups instance.

        :return: An :class:`int` representing the number of groups in the
            current groups instance.

        Example::

            >>> len(font.groups)
            5

        """
        return super(BaseGroups, self).__len__()

    def __setitem__(self, groupName: str, glyphNames: CollectionType[str]) -> None:
        """Set the glyph names for a given group in the current groups instance.

        :param groupName: The group name to set as a :class:`str`.
        :param glyphNames: The glyph names to set for the given group as
            a :class:`list` or :class:`tuple` of :class:`str` items.

        Example::

            >>> font.groups["myGroup"] = ["A", "B", "C"]

        """

        super(BaseGroups, self).__setitem__(groupName, glyphNames)

    def clear(self) -> None:
        """Remove all groups from the current groups instance.

        This will reset the :class:`BaseGroups` instance to an empty dictionary.

        Example::

            >>> font.groups.clear()

        """
        super(BaseGroups, self).clear()

    def get(
        self, groupName: str, default: Optional[CollectionType[str]] = None
    ) -> Optional[Tuple[str, ...]]:
        """Get the contents for the given group in the current groups instance.

        If the given `groupName` is not found, The specified `default` will be
        returned.

        :param groupName: The group name to look up as a :class:`str`.
        :param default: The optional default value to return if the `groupName`
            is not found`. The value must be either a class`list` or :class:`tuple`
            of :class:`str` glyph names, or :obj:`None`. Defaults to :obj:`None`.
        :return: The contents of the given group as a :class:`tuple`
            of :class:`str` items, or the `default` value if the group is not found.

        Example::

            >>> font.groups["myGroup"]
            ("A", "B", "C")

        ..note::

            Any changes to the returned lib contents will not be reflected in
            it's :class:`BaseGroups` instance. To make changes to this content,
            do the following::

                >>> group = font.groups["myGroup"]
                >>> group.remove("A")
                >>> font.groups["myGroup"] = group

        """
        return super(BaseGroups, self).get(groupName, default)

    def items(self) -> BaseItems[Tuple[str, ValueType]]:
        """Return the items in the current groups instance.

        Each item is represented as a :class:`tuple` of key-value pairs, where:
            - `key` is a :class:`str` representing a group name.
            - `value` is a :class:`tuple` of :class:`str` glyph names.

        :return: A :ref:`type-view` of the groups' ``(key, value)`` pairs.

        Example::

            >>> font.groups.items()
            BaseGroups_items([("myGroup", ("A", "B", "C")),
            ("myGroup2", ("D", "E", "F")), ...])

        """
        return super(BaseGroups, self).items()

    def keys(self) -> BaseKeys:
        """Return the group names (keys) in the current groups instance.

        :return: A :ref:`type-view` of :class:`str` items representing the groups' keys.

        Example::

            >>> font.groups.keys()
            BaseGroups_keys(["myGroup4", "myGroup1", "myGroup5", ...])

        """
        return super(BaseGroups, self).keys()

    def values(self) -> BaseValues:
        """Return the values in the current groups instance.

        :return: A :ref:`type-view` of the groups' values as :class:`tuple`
            items of :class:`str` glyph names.

        Example::

            >>> font.groups.values()
            BaseGroups_values([("A", "B", "C"), ("D", "E", "F")]

        """
        return super(BaseGroups, self).values()

    def pop(
        self, groupName: str, default: Optional[CollectionType[str]] = None
    ) -> Optional[Tuple[str, ...]]:
        """Remove the specified group and return its associated contents.

        If the `groupName` does not exist, the `default` value is returned.

        :param groupName: The group to remove as a :class:`str`.
        :param default: The optional default value to return if the `groupName`
            is not found`. The value must be either a class`list` or :class:`tuple`
            of :class:`str` glyph names, or :obj:`None`. Defaults to :obj:`None`.
        :return: The contents of the given group as a :class:`tuple`
            of :class:`str` items, or the `default` value if the group is not found.

        Example::

            >>> font.groups.pop("myGroup")
            ("A", "B", "C")

        """
        return super(BaseGroups, self).pop(groupName, default)

    def update(self, otherGroups: MutableMapping[str, CollectionType[str]]) -> None:
        """Update the current groups instance with key-value pairs from another.

        For each group in `otherGroups`:
            - If the group exists in the current groups instance, its value is
              replaced with the value from `otherGroups`.
            - If the key does not exist in the current groups instance, it is added.

        Keys that exist in the current groups instance but are not in `otherLib`
        remain unchanged.

        :param otherLib: A :class:`MutableMapping` of :class:`str` group names
            mapped to a :class:`tuple` of :class:`str` glyph names to update the
            current groups instance with.

        Example::

            >>> font.groups.update(newGroups)

        """
        super(BaseGroups, self).update(otherGroups)
