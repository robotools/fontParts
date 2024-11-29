from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Tuple,
)

from fontParts.base.base import BaseDict, dynamicProperty, reference
from fontParts.base import normalizers
from fontParts.base.deprecated import DeprecatedGroups, RemovedGroups
from fontParts.base.annotations import CollectionType

if TYPE_CHECKING:
    from fontParts.base.glyph import BaseGlyph
    from fontParts.base.font import BaseFont
    from fontparts.base.layer import BaseLayer

ValueType = Tuple[str, ...]
GroupsType = Dict[str, ValueType]
ItemsType = Tuple[str, ValueType]


class BaseGroups(BaseDict, DeprecatedGroups, RemovedGroups):
    """
    A Groups object. This object normally created as part of a
    :class:`BaseFont`. An orphan Groups object can be created like this::

        >>> groups = RGroups()

    This object behaves like a Python dictionary. Most of the dictionary
    functionality comes from :class:`BaseDict`, look at that object for the
    required environment implementation details.

    Groups uses :func:`normalizers.normalizeGroupKey` to normalize the key of
    the ``dict``, and :func:`normalizers.normalizeGroupValue` to normalize the
    value of the ``dict``.
    """

    keyNormalizer: Callable[[str], str] = normalizers.normalizeGroupKey
    valueNormalizer: Callable[[CollectionType[str]], Tuple[str, ...]] = normalizers.normalizeGroupValue

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

    _font = None

    font = dynamicProperty("font", "The Groups' parent :class:`BaseFont`.")

    def _get_font(self) -> Optional[BaseFont]:
        if self._font is None:
            return None
        return self._font()

    def _set_font(self, font: Optional[BaseFont]) -> None:
        if self._font is not None and self._font != font:
            raise AssertionError("font for groups already set and is not same as font")
        if font is not None:
            font = reference(font)
        self._font = font

    # ---------
    # Searching
    # ---------

    def findGlyph(self, glyphName: str) -> List[str]:
        """
        Returns a ``list`` of the group or groups associated with
        **glyphName**.
        **glyphName** will be an :ref:`type-string`. If no group is found
        to contain **glyphName** an empty ``list`` will be returned. ::

            >>> font.groups.findGlyph("A")
            ["A_accented"]
        """
        glyphName = normalizers.normalizeGlyphName(glyphName)
        groupNames = self._findGlyph(glyphName)
        return [type(self).keyNormalizer(groupName) for groupName in groupNames]

    def _findGlyph(self, glyphName: str) -> List[str]:
        """
        This is the environment implementation of
        :meth:`BaseGroups.findGlyph`. **glyphName** will be
        an :ref:`type-string`.

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
        """
        All groups marked as potential side 1
        kerning members.

            >>> side1Groups = groups.side1KerningGroups

        The value will be a :ref:`dict` with
        :ref:`string` keys representing group names
        and :ref:`tuple` contaning glyph names.
        """,
    )

    def _get_base_side1KerningGroups(self) -> GroupsType:
        kerningGroups = self._get_side1KerningGroups()
        normalized = {}
        for name, members in kerningGroups.items():
            name = normalizers.normalizeGroupKey(name)
            members = normalizers.normalizeGroupValue(members)
            normalized[name] = members
        return normalized

    def _get_side1KerningGroups(self) -> GroupsType:
        """
        Subclasses may override this method.
        """
        found = {}
        for name, contents in self.items():
            if name.startswith("public.kern1."):
                found[name] = contents
        return found

    side2KerningGroups: dynamicProperty = dynamicProperty(
        "base_side2KerningGroups",
        """
        All groups marked as potential side 1
        kerning members.

            >>> side2Groups = groups.side2KerningGroups

        The value will be a :ref:`dict` with
        :ref:`string` keys representing group names
        and :ref:`tuple` contaning glyph names.
        """,
    )

    def _get_base_side2KerningGroups(self) -> GroupsType:
        kerningGroups = self._get_side2KerningGroups()
        normalized = {}
        for name, members in kerningGroups.items():
            name = normalizers.normalizeGroupKey(name)
            members = normalizers.normalizeGroupValue(members)
            normalized[name] = members
        return normalized

    def _get_side2KerningGroups(self) -> GroupsType:
        """
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
        """
        Removes a group from the Groups. **groupName** will be
        a :ref:`type-string` that is the group name to
        be removed.

        This is a backwards compatibility method.
        """
        del self[groupName]

    def asDict(self) -> GroupsType:
        """
        Return the Groups as a ``dict``.

        This is a backwards compatibility method.
        """
        d = {}
        for k, v in self.items():
            d[k] = v
        return d

    # -------------------
    # Inherited Functions
    # -------------------

    def __contains__(self, groupName: str) -> bool:
        """
        Tests to see if a group name is in the Groups.
        **groupName** will be a :ref:`type-string`.
        This returns a ``bool`` indicating if the **groupName**
        is in the Groups. ::

            >>> "myGroup" in font.groups
            True
        """
        return super(BaseGroups, self).__contains__(groupName)

    def __delitem__(self, groupName: str) -> None:
        """
        Removes **groupName** from the Groups. **groupName** is a
        :ref:`type-string`.::

            >>> del font.groups["myGroup"]
        """
        super(BaseGroups, self).__delitem__(groupName)

    def __getitem__(self, groupName: str) -> Tuple[str, ...]:
        """
        Returns the contents of the named group. **groupName** is a
        :ref:`type-string`. The returned value will be a
        :ref:`type-immutable-list` of the group contents.::

            >>> font.groups["myGroup"]
            ("A", "B", "C")

        It is important to understand that any changes to the returned group
        contents will not be reflected in the Groups object. If one wants to
        make a change to the group contents, one should do the following::

            >>> group = font.groups["myGroup"]
            >>> group.remove("A")
            >>> font.groups["myGroup"] = group
        """
        return super(BaseGroups, self).__getitem__(groupName)

    def __iter__(self) -> Iterator[str]:
        """
        Iterates through the Groups, giving the key for each iteration. The
        order that the Groups will iterate though is not fixed nor is it
        ordered.::

            >>> for groupName in font.groups:
            >>>     print groupName
            "myGroup"
            "myGroup3"
            "myGroup2"
        """
        return super(BaseGroups, self).__iter__()

    def __len__(self) -> int:
        """
        Returns the number of groups in Groups as an ``int``.::

            >>> len(font.groups)
            5
        """
        return super(BaseGroups, self).__len__()

    def __setitem__(self, groupName: str, glyphNames: CollectionType[str]) -> None:
        """
        Sets the **groupName** to the list of **glyphNames**. **groupName**
        is the group name as a :ref:`type-string` and **glyphNames** is a
        ``list`` of glyph names as :ref:`type-string`.

            >>> font.groups["myGroup"] = ["A", "B", "C"]
        """
        super(BaseGroups, self).__setitem__(groupName, glyphNames)

    def clear(self) -> None:
        """
        Removes all group information from Groups,
        resetting the Groups to an empty dictionary. ::

            >>> font.groups.clear()
        """
        super(BaseGroups, self).clear()

    def get(self, groupName: str, default: Optional[CollectionType[str]] = None) -> Optional[Tuple[str, ...]]:
        """
        Returns the contents of the named group.
        **groupName** is a :ref:`type-string`, and the returned values will
        either be :ref:`type-immutable-list` of group contents or ``None``
        if no group was found. ::

            >>> font.groups["myGroup"]
            ("A", "B", "C")

        It is important to understand that any changes to the returned group
        contents will not be reflected in the Groups object. If one wants to
        make a change to the group contents, one should do the following::

            >>> group = font.groups["myGroup"]
            >>> group.remove("A")
            >>> font.groups["myGroup"] = group
        """
        return super(BaseGroups, self).get(groupName, default)

    def items(self) -> List[ItemsType]:
        """
        Returns a list of ``tuple`` of each group name and group members.
        Group names are :ref:`type-string` and group members are a
        :ref:`type-immutable-list` of :ref:`type-string`. The initial
        list will be unordered.

            >>> font.groups.items()
            [("myGroup", ("A", "B", "C"), ("myGroup2", ("D", "E", "F"))]
        """
        return super(BaseGroups, self).items()

    def keys(self) -> List[str]:
        """
        Returns a ``list`` of all the group names in Groups. This list will be
        unordered.::

            >>> font.groups.keys()
            ["myGroup4", "myGroup1", "myGroup5"]
        """
        return super(BaseGroups, self).keys()

    def pop(self, groupName: str, default: Optional[CollectionType[str]]=None) -> Optional[Tuple[str, ...]]:
        """
        Removes the **groupName** from the Groups and returns the list of
        group members. If no group is found, **default** is returned.
        **groupName** is a :ref:`type-string`. This must return either
        **default** or a :ref:`type-immutable-list` of glyph names as
        :ref:`type-string`.

            >>> font.groups.pop("myGroup")
            ("A", "B", "C")
        """
        return super(BaseGroups, self).pop(groupName, default)

    def update(self, otherGroups: BaseDict) -> None:
        """
        Updates the Groups based on **otherGroups**. *otherGroups** is a
        ``dict`` of groups information. If a group from **otherGroups** is in
        Groups, the group members will be replaced by the group members from
        **otherGroups**. If a group from **otherGroups** is not in the Groups,
        it is added to the Groups. If Groups contain a group name that is not
        in *otherGroups**, it is not changed.

            >>> font.groups.update(newGroups)
        """
        super(BaseGroups, self).update(otherGroups)

    def values(self) -> List[ValueType]:
        """
        Returns a ``list`` of each named group's members.
        This will be a list of lists, the group members will be a
        :ref:`type-immutable-list` of :ref:`type-string`. The initial
        list will be unordered.

            >>> font.groups.items()
            [("A", "B", "C"), ("D", "E", "F")]
        """
        return super(BaseGroups, self).values()
