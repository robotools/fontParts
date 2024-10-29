.. highlight:: python
.. module:: fontParts.base

####
Font
####

.. note::

	This section needs to contain the following:

	* description of what this is ✓
	* sub-object with basic usage ✓
	* bridge to default layer for glyphs for backwards compatibility ✗
	* glyph interaction with basic usage ✗

***********
Description
***********

The :class:`Font <BaseFont>` object is the central part that connects all glyphs with font information like names, key dimensions etc.

:class:`Font <BaseFont>` objects behave like dictionaries: the glyph name is the key and the returned value is a :class:`Glyph <BaseGlyph>` object for that glyph. If the glyph does not exist, :class:`Font <BaseFont>` will raise an ``IndexError``.

:class:`Font <BaseFont>` has a couple of important sub-objects which are worth checking out. The font’s kerning is stored in a :class:`Kerning <BaseKerning>` object and can be reached as an attribute at ``Font.kerning``. Fontnames, key dimensions, flags etc are stored in a :class:`Info <BaseInfo>` object which is available through ``Font.info``. The ``Font.lib`` is a :class:`Lib <BaseLib>` object which behaves as a dictionary.

********
Overview
********

Copy
====

.. autosummary::
    :nosignatures:

    BaseFont.copy

File Operations
===============

.. autosummary::
    :nosignatures:

    BaseFont.path
    BaseFont.save
    BaseFont.generate

Sub-Objects
===========

.. autosummary::
    :nosignatures:

    BaseFont.info
    BaseFont.groups
    BaseFont.kerning
    BaseFont.features
    BaseFont.lib
    BaseFont.tempLib

Layers
======

.. autosummary::
    :nosignatures:

    BaseFont.layers
    BaseFont.layerOrder
    BaseFont.defaultLayer
    BaseFont.getLayer
    BaseFont.newLayer
    BaseFont.removeLayer
    BaseFont.insertLayer
    BaseFont.duplicateLayer

Glyphs
======

.. autosummary::
    :nosignatures:

    BaseFont.__len__
    BaseFont.keys
    BaseFont.glyphOrder
    BaseFont.__iter__
    BaseFont.__contains__
    BaseFont.__getitem__
    BaseFont.newGlyph
    BaseFont.insertGlyph
    BaseFont.removeGlyph

*********
Reference
*********

.. autoclass:: BaseFont

Copy
====

.. automethod:: BaseFont.copy

File Operations
===============

.. autoattribute:: BaseFont.path
.. automethod:: BaseFont.save
.. automethod:: BaseFont.close
.. automethod:: BaseFont.generate

Sub-Objects
===========

.. autoattribute:: BaseFont.info
.. autoattribute:: BaseFont.groups
.. autoattribute:: BaseFont.kerning
.. autoattribute:: BaseFont.features
.. autoattribute:: BaseFont.lib

Layers
======

.. autoattribute:: BaseFont.layers
.. autoattribute:: BaseFont.layerOrder
.. autoattribute:: BaseFont.defaultLayer
.. automethod:: BaseFont.getLayer
.. automethod:: BaseFont.newLayer
.. automethod:: BaseFont.removeLayer
.. automethod:: BaseFont.insertLayer

Glyphs
======

Interacting with glyphs at the font level is a shortcut for interacting with glyphs in the default layer. ::

	>>> glyph = font.newGlyph("A")

Does the same thing as::

	>>> glyph = font.getLayer(font.defaultLayerName).newGlyph("A")

.. automethod:: BaseFont.__len__
.. automethod:: BaseFont.keys
.. autoattribute:: BaseFont.glyphOrder
.. automethod:: BaseFont.__iter__
.. automethod:: BaseFont.__contains__
.. automethod:: BaseFont.__getitem__
.. automethod:: BaseFont.newGlyph
.. automethod:: BaseFont.insertGlyph
.. automethod:: BaseFont.removeGlyph

Guidelines
==========

.. autoattribute:: BaseFont.guidelines
.. automethod:: BaseFont.appendGuideline
.. automethod:: BaseFont.removeGuideline
.. automethod:: BaseFont.clearGuidelines

Interpolation
=============

.. automethod:: BaseFont.isCompatible
.. automethod:: BaseFont.interpolate

Normalization
=============

.. automethod:: BaseFont.round
.. automethod:: BaseFont.autoUnicodes

Environment
===========

.. automethod:: BaseFont.naked
.. automethod:: BaseFont.changed
