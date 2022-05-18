.. highlight:: python
.. module:: fontParts.base

######
Groups
######

***********
Description
***********

Groups are collections of glyphs. Groups are used for many things, from OpenType features, kerning, or just keeping track of a collection of related glyphs. The name of the group must be at least one character, with no limit to the maximum length for the name, nor any limit on the characters used in a name. With the exception of the kerning groups defined below, glyphs may be in more than one group and they may appear within the same group more than once. Glyphs in the groups are not required to be in the font.

Groups behave like a Python dictionary. Anything you can do with a dictionary in Python, you can do with Groups.

::

    font = CurrentFont()
    for name, members in font.groups.items():
        print(name)
        print(members)

It is important to understand that any changes to the returned group contents will not be reflected in the groups object. This means that the following will not update the font's groups:

::

    group = list(font.groups["myGroup"])
    group.remove("A")

If one wants to make a change to the group contents, one should do the following instead:

::

    group = list(font.groups["myGroup"])
    group.remove("A")
    font.groups["myGroup"] = group

Kerning Groups
==============

Groups may be used as members of kerning pairs in :class:`BaseKerning`. These groups are divided into two types: groups that appear on the first side of a kerning pair and groups that appear on the second side of a kerning pair.

Kerning groups must begin with standard prefixes. The prefix for groups intended for use in the first side of a kerning pair is ``public.kern1.``. The prefix for groups intended for use in the second side of a kerning pair is ``public.kern2.``. One or more characters must follow the prefix.

Kerning groups must strictly adhere to the following rules:

#. Kerning group names must begin with the appropriate prefix.
#. Only kerning groups are allowed to use the kerning group prefixes in their names.
#. Kerning groups are not required to appear in the kerning pairs.
#. Glyphs must not appear in more than one kerning group per side.

These rules come from the `Unified Font Object <http://unifiedfontobject.org/versions/ufo3/groups.plist/>`_, more information on implementation details for application developers can be found there.

********
Overview
********

.. autosummary::
    :nosignatures:

    BaseGroups.copy
    BaseGroups.font
    BaseGroups.__contains__
    BaseGroups.__delitem__
    BaseGroups.__getitem__
    BaseGroups.__iter__
    BaseGroups.__len__
    BaseGroups.__setitem__
    BaseGroups.clear
    BaseGroups.get
    BaseGroups.items
    BaseGroups.keys
    BaseGroups.pop
    BaseGroups.update
    BaseGroups.values
    BaseGroups.findGlyph
    BaseGroups.naked
    BaseGroups.changed

*********
Reference
*********

.. autoclass:: BaseGroups

Copy
====

.. automethod:: BaseGroups.copy

Parents
=======

* :attr:`~BaseGroups.font` The groups' parent :class:`BaseFont`.

Dictionary
==========

.. automethod:: BaseGroups.__contains__
.. automethod:: BaseGroups.__delitem__
.. automethod:: BaseGroups.__getitem__
.. automethod:: BaseGroups.__iter__
.. automethod:: BaseGroups.__len__
.. automethod:: BaseGroups.__setitem__
.. automethod:: BaseGroups.clear
.. automethod:: BaseGroups.get
.. automethod:: BaseGroups.items
.. automethod:: BaseGroups.keys
.. automethod:: BaseGroups.pop
.. automethod:: BaseGroups.update
.. automethod:: BaseGroups.values

Queries
=======

.. automethod:: BaseGroups.findGlyph

Environment
===========

.. automethod:: BaseGroups.naked
.. automethod:: BaseGroups.changed
