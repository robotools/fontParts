.. highlight:: python
.. module:: fontParts.base

#####
Glyph
#####

.. autosummarymethodlist::

	BaseGlyph

***********
Description
***********

The :class:`Glyph <BaseGlyph>` object represents a glyph, its parts and associated data.

:class:`Glyph <BaseGlyph>` can be used as a list of :class:`Contour <BaseContour>` objects.

When a :class:`Glyph <BaseGlyph>` is obtained from a :class:`Font <BaseFont>` object, the font is the parent object of the glyph.

********
Overview
********

Copy
====

.. autosummary::
    :nosignatures:

    BaseGlyph.copy

Parents
=======

.. autosummary::
    :nosignatures:

    BaseGlyph.layer
    BaseGlyph.font

Identification
==============

.. autosummary::
    :nosignatures:

    BaseGlyph.name
    BaseGlyph.unicodes
    BaseGlyph.unicode

Metrics
=======

.. autosummary::
    :nosignatures:

    BaseGlyph.width
    BaseGlyph.leftMargin
    BaseGlyph.rightMargin
    BaseGlyph.height
    BaseGlyph.bottomMargin
    BaseGlyph.topMargin

Queries
=======

.. autosummary::
    :nosignatures:

    BaseGlyph.bounds
    BaseGlyph.pointInside

Pens and Drawing
================

.. autosummary::
    :nosignatures:

    BaseGlyph.getPen
    BaseGlyph.getPointPen
    BaseGlyph.draw
    BaseGlyph.drawPoints

Layers
======

.. autosummary::
    :nosignatures:

    BaseGlyph.layers
    BaseGlyph.getLayer
    BaseGlyph.newLayer
    BaseGlyph.removeLayer

Global
======

.. autosummary::
    :nosignatures:

    BaseGlyph.clear
    BaseGlyph.appendGlyph

Contours
========

.. autosummary::
    :nosignatures:

    BaseGlyph.contours
    BaseGlyph.__len__
    BaseGlyph.__iter__
    BaseGlyph.__getitem__
    BaseGlyph.appendContour
    BaseGlyph.removeContour
    BaseGlyph.clearContours
    BaseGlyph.removeOverlap

Components
==========

.. autosummary::
    :nosignatures:

    BaseGlyph.components
    BaseGlyph.appendComponent
    BaseGlyph.removeComponent
    BaseGlyph.clearComponents
    BaseGlyph.decompose

Anchors
=======

.. autosummary::
    :nosignatures:

    BaseGlyph.anchors
    BaseGlyph.appendAnchor
    BaseGlyph.removeAnchor
    BaseGlyph.clearAnchors

Guidelines
==========

.. autosummary::
    :nosignatures:

    BaseGlyph.guidelines
    BaseGlyph.appendGuideline
    BaseGlyph.removeGuideline
    BaseGlyph.clearGuidelines

Image
=====

.. autosummary::
    :nosignatures:

    BaseGlyph.image
    BaseGlyph.addImage
    BaseGlyph.clearImage

Note
====

.. autosummary::
    :nosignatures:

    BaseGlyph.note
    BaseGlyph.markColor

Sub-Objects
===========

.. autosummary::
    :nosignatures:

    BaseGlyph.lib
    BaseGlyph.tempLib

Transformations
===============

.. autosummary::
    :nosignatures:

    BaseGlyph.transformBy
    BaseGlyph.moveBy
    BaseGlyph.scaleBy
    BaseGlyph.rotateBy
    BaseGlyph.skewBy

Interpolation
=============

.. autosummary::
    :nosignatures:

    BaseGlyph.isCompatible
    BaseGlyph.interpolate

Normalization
=============

.. autosummary::
    :nosignatures:

    BaseGlyph.round
    BaseGlyph.autoUnicodes

Environment
===========

.. autosummary::
    :nosignatures:

    BaseGlyph.naked
    BaseGlyph.changed

*********
Reference
*********

.. autoclass:: BaseGlyph

Copy
====

.. automethod:: BaseGlyph.copy

Parents
=======

.. autoattribute:: BaseGlyph.layer
.. autoattribute:: BaseGlyph.font

Identification
==============

.. autoattribute:: BaseGlyph.name
.. autoattribute:: BaseGlyph.unicodes
.. autoattribute:: BaseGlyph.unicode

Metrics
=======

.. autoattribute:: BaseGlyph.width
.. autoattribute:: BaseGlyph.leftMargin
.. autoattribute:: BaseGlyph.rightMargin
.. autoattribute:: BaseGlyph.height
.. autoattribute:: BaseGlyph.bottomMargin
.. autoattribute:: BaseGlyph.topMargin

Queries
=======

.. autoattribute:: BaseGlyph.bounds
.. automethod:: BaseGlyph.pointInside

Pens and Drawing
================

.. automethod:: BaseGlyph.getPen
.. automethod:: BaseGlyph.getPointPen
.. automethod:: BaseGlyph.draw
.. automethod:: BaseGlyph.drawPoints

Layers
======

Layer interaction in glyphs is very similar to the layer interaction in fonts. When you ask a glyph for a layer, you get a *glyph layer* in return. A glyph layer lets you do anything that you can do to a glyph. In fact a glyph layer is really just a glyph.

    >>> bgdGlyph = glyph.newLayer('background')
    >>> bgdGlyph.appendGlyph(glyph)
    >>> bgdGlyph.appendGuideline((10, 10), 45)

.. autoattribute:: BaseGlyph.layers
.. automethod:: BaseGlyph.getLayer
.. automethod:: BaseGlyph.newLayer
.. automethod:: BaseGlyph.removeLayer

Global
======

.. automethod:: BaseGlyph.clear
.. automethod:: BaseGlyph.appendGlyph

Contours
========

.. autoattribute:: BaseGlyph.contours
.. automethod:: BaseGlyph.__len__
.. automethod:: BaseGlyph.__iter__
.. automethod:: BaseGlyph.__getitem__
.. automethod:: BaseGlyph.appendContour
.. automethod:: BaseGlyph.removeContour
.. automethod:: BaseGlyph.clearContours
.. automethod:: BaseGlyph.removeOverlap

Components
==========

.. autoattribute:: BaseGlyph.components
.. automethod:: BaseGlyph.appendComponent
.. automethod:: BaseGlyph.removeComponent
.. automethod:: BaseGlyph.clearComponents
.. automethod:: BaseGlyph.decompose

Anchors
=======

.. autoattribute:: BaseGlyph.anchors
.. automethod:: BaseGlyph.appendAnchor
.. automethod:: BaseGlyph.removeAnchor
.. automethod:: BaseGlyph.clearAnchors

Guidelines
==========

.. autoattribute:: BaseGlyph.guidelines
.. automethod:: BaseGlyph.appendGuideline
.. automethod:: BaseGlyph.removeGuideline
.. automethod:: BaseGlyph.clearGuidelines

Image
=====

.. autoattribute:: BaseGlyph.image
.. automethod:: BaseGlyph.addImage
.. automethod:: BaseGlyph.clearImage

Note
====

.. autoattribute:: BaseGlyph.note
.. autoattribute:: BaseGlyph.markColor

Sub-Objects
===========

.. autoattribute:: BaseGlyph.lib

Transformations
===============

.. automethod:: BaseGlyph.transformBy
.. automethod:: BaseGlyph.moveBy
.. automethod:: BaseGlyph.scaleBy
.. automethod:: BaseGlyph.rotateBy
.. automethod:: BaseGlyph.skewBy

Interpolation
=============

.. automethod:: BaseGlyph.isCompatible
.. automethod:: BaseGlyph.interpolate

Normalization
=============

.. automethod:: BaseGlyph.round
.. automethod:: BaseGlyph.autoUnicodes

Environment
===========

.. automethod:: BaseGlyph.naked
.. automethod:: BaseGlyph.changed
