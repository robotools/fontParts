.. highlight:: python
.. module:: fontParts.base

#####
Layer
#####

.. note::

	This section needs to contain the following:

	* description of what this is
	* sub-object with basic usage
	* glyph interaction with basic usage

********
Overview
********

Copy
====

.. autosummary::
    :nosignatures:

    BaseLayer.copy

Parents
=======

.. autosummary::
    :nosignatures:

    BaseLayer.font

Attributes
==========

.. autosummary::
    :nosignatures:

    BaseLayer.name
    BaseLayer.color

Sub-Objects
===========

.. autosummary::
    :nosignatures:

    BaseLayer.lib
    BaseLayer.tempLib

Glyphs
======

.. autosummary::
    :nosignatures:

    BaseLayer.__len__
    BaseLayer.keys
    BaseLayer.__iter__
    BaseLayer.__contains__
    BaseLayer.__getitem__
    BaseLayer.newGlyph
    BaseLayer.insertGlyph
    BaseLayer.removeGlyph

Interpolation
=============

.. autosummary::
    :nosignatures:

    BaseLayer.isCompatible
    BaseLayer.interpolate

Normalization
=============

.. autosummary::
    :nosignatures:

    BaseLayer.round
    BaseLayer.autoUnicodes

Environment
===========

.. autosummary::
    :nosignatures:

    BaseLayer.naked
    BaseLayer.changed


*********
Reference
*********

.. autoclass:: BaseLayer

Copy
====

.. automethod:: BaseLayer.copy

Parents
=======

.. autoattribute:: BaseLayer.font

Attributes
==========

.. autoattribute:: BaseLayer.name
.. autoattribute:: BaseLayer.color

Sub-Objects
===========

.. autoattribute:: BaseLayer.lib

Glyphs
======

.. automethod:: BaseLayer.__len__
.. automethod:: BaseLayer.keys
.. automethod:: BaseLayer.__iter__
.. automethod:: BaseLayer.__contains__
.. automethod:: BaseLayer.__getitem__
.. automethod:: BaseLayer.newGlyph
.. automethod:: BaseLayer.insertGlyph
.. automethod:: BaseLayer.removeGlyph

Interpolation
=============

.. automethod:: BaseLayer.isCompatible
.. automethod:: BaseLayer.interpolate

Normalization
=============

.. automethod:: BaseLayer.round
.. automethod:: BaseLayer.autoUnicodes

Environment
===========

.. automethod:: BaseLayer.naked
.. automethod:: BaseLayer.changed
