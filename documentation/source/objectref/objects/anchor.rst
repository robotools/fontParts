.. highlight:: python
.. module:: fontParts.base

######
Anchor
######

***********
Description
***********

Anchors are single points in a glyph which are not part of a contour. They can be used as reference positions for doing things like assembling components. In most font editors, anchors have a special appearance and can be edited.

::

    glyph = CurrentGlyph()
    for anchor in glyph.anchors:
        print(anchor)

********
Overview
********

Copy
====

.. autosummary::
	:nosignatures:

	BaseAnchor.copy

Parents
=======

.. autosummary::
	:nosignatures:

	BaseAnchor.glyph
	BaseAnchor.layer
	BaseAnchor.font

Identification
==============

.. autosummary::
	:nosignatures:

	BaseAnchor.name
	BaseAnchor.color
	BaseAnchor.identifier
	BaseAnchor.index

Coordinate
==========

.. autosummary::
	:nosignatures:

	BaseAnchor.x
	BaseAnchor.y

Transformations
===============

.. autosummary::
	:nosignatures:

	BaseAnchor.transformBy
	BaseAnchor.moveBy
	BaseAnchor.scaleBy
	BaseAnchor.rotateBy
	BaseAnchor.skewBy

Normalization
=============

.. autosummary::
	:nosignatures:

	BaseAnchor.round

Environment
===========

.. autosummary::
	:nosignatures:

	BaseAnchor.naked
	BaseAnchor.changed

*********
Reference
*********

.. autoclass:: BaseAnchor

Copy
====

.. automethod:: BaseAnchor.copy

Parents
=======

.. autoattribute:: BaseAnchor.glyph
.. autoattribute:: BaseAnchor.layer
.. autoattribute:: BaseAnchor.font

Identification
==============

.. autoattribute:: BaseAnchor.name
.. autoattribute:: BaseAnchor.color
.. autoattribute:: BaseAnchor.identifier
.. autoattribute:: BaseAnchor.index

Coordinate
==========

.. autoattribute:: BaseAnchor.x
.. autoattribute:: BaseAnchor.y

Transformations
===============

.. automethod:: BaseAnchor.transformBy
.. automethod:: BaseAnchor.moveBy
.. automethod:: BaseAnchor.scaleBy
.. automethod:: BaseAnchor.rotateBy
.. automethod:: BaseAnchor.skewBy

Normalization
=============

.. automethod:: BaseAnchor.round

Environment
===========

.. automethod:: BaseAnchor.naked
.. automethod:: BaseAnchor.changed
