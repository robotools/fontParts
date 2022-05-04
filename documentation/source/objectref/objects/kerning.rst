.. highlight:: python
.. module:: fontParts.base

#######
Kerning
#######

***********
Description
***********

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

Copy
====

.. autosummary::
    :nosignatures:

    BaseKerning.copy

Parents
=======

.. autosummary::
    :nosignatures:

    BaseKerning.font

Dictionary
==========

.. autosummary::
    :nosignatures:

    BaseKerning.__len__
    BaseKerning.keys
    BaseKerning.items
    BaseKerning.values
    BaseKerning.__contains__
    BaseKerning.__setitem__
    BaseKerning.__getitem__
    BaseKerning.get
    BaseKerning.find
    BaseKerning.__delitem__
    BaseKerning.pop
    BaseKerning.__iter__
    BaseKerning.update
    BaseKerning.clear

Transformations
===============

.. autosummary::
    :nosignatures:

    BaseKerning.scaleBy

Interpolation
=============

.. autosummary::
    :nosignatures:

    BaseKerning.interpolate

Normalization
=============

.. autosummary::
    :nosignatures:

    BaseKerning.round

Environment
===========

.. autosummary::
    :nosignatures:

    BaseKerning.naked
    BaseKerning.changed

*********
Reference
*********

.. autoclass:: BaseKerning

Copy
====

.. automethod:: BaseKerning.copy

Parents
=======

.. autoattribute:: BaseKerning.font

Dictionary
==========

.. automethod:: BaseKerning.__len__
.. automethod:: BaseKerning.keys
.. automethod:: BaseKerning.items
.. automethod:: BaseKerning.values
.. automethod:: BaseKerning.__contains__
.. automethod:: BaseKerning.__setitem__
.. automethod:: BaseKerning.__getitem__
.. automethod:: BaseKerning.get
.. automethod:: BaseKerning.find
.. automethod:: BaseKerning.__delitem__
.. automethod:: BaseKerning.pop
.. automethod:: BaseKerning.__iter__
.. automethod:: BaseKerning.update
.. automethod:: BaseKerning.clear

Transformations
===============

.. automethod:: BaseKerning.scaleBy

Interpolation
=============

.. automethod:: BaseKerning.interpolate

Normalization
=============

.. automethod:: BaseKerning.round

Environment
===========

.. automethod:: BaseKerning.naked
.. automethod:: BaseKerning.changed
