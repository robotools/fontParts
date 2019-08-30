.. highlight:: python
.. module:: fontParts.base

#######
Contour
#######

***********
Description
***********

A Contour is a single path of any number of points. A Glyph usually consists of a couple of contours, and this is the object that represents each one. The :class:`Contour <BaseContour>` object offers access to the outline matter in various ways. The parent of :class:`Contour <BaseContour>` is usually :class:`Glyph <BaseGlyph>`.

********
Overview
********

Copy
====

.. autosummary::
    :nosignatures:

    BaseContour.copy

Parents
=======

.. autosummary::
    :nosignatures:

    BaseContour.glyph
    BaseContour.layer
    BaseContour.font

Identification
==============

.. autosummary::
    :nosignatures:

    BaseContour.identifier
    BaseContour.index

Winding Direction
=================

.. autosummary::
    :nosignatures:

    BaseContour.clockwise
    BaseContour.reverse

Queries
=======

.. autosummary::
    :nosignatures:

    BaseContour.bounds
    BaseContour.pointInside

Pens and Drawing
================

.. autosummary::
    :nosignatures:

    BaseContour.draw
    BaseContour.drawPoints

Segments
========

.. autosummary::
    :nosignatures:

    BaseContour.segments
    BaseContour.__len__
    BaseContour.__iter__
    BaseContour.__getitem__
    BaseContour.appendSegment
    BaseContour.insertSegment
    BaseContour.removeSegment
    BaseContour.setStartSegment
    BaseContour.autoStartSegment

bPoints
=======

.. autosummary::
    :nosignatures:

    BaseContour.bPoints
    BaseContour.appendBPoint
    BaseContour.insertBPoint

Points
======

.. autosummary::
    :nosignatures:

    BaseContour.points
    BaseContour.appendPoint
    BaseContour.insertPoint
    BaseContour.removePoint

Transformations
===============

.. autosummary::
    :nosignatures:

    BaseContour.transformBy
    BaseContour.moveBy
    BaseContour.scaleBy
    BaseContour.rotateBy
    BaseContour.skewBy

Normalization
=============

.. autosummary::
    :nosignatures:

    BaseContour.round

Environment
===========

.. autosummary::
    :nosignatures:

    BaseContour.naked
    BaseContour.changed

*********
Reference
*********

.. autoclass:: BaseContour

Copy
====

.. automethod:: BaseContour.copy

Parents
=======

.. autoattribute:: BaseContour.glyph
.. autoattribute:: BaseContour.layer
.. autoattribute:: BaseContour.font

Identification
==============

.. autoattribute:: BaseContour.identifier
.. autoattribute:: BaseContour.index

Winding Direction
=================

.. autoattribute:: BaseContour.clockwise
.. automethod:: BaseContour.reverse

Queries
=======

.. autoattribute:: BaseContour.bounds
.. automethod:: BaseContour.pointInside

Pens and Drawing
================

.. automethod:: BaseContour.draw
.. automethod:: BaseContour.drawPoints

Segments
========

.. autoattribute:: BaseContour.segments
.. automethod:: BaseContour.__len__
.. automethod:: BaseContour.__iter__
.. automethod:: BaseContour.__getitem__
.. automethod:: BaseContour.appendSegment
.. automethod:: BaseContour.insertSegment
.. automethod:: BaseContour.removeSegment
.. automethod:: BaseContour.setStartSegment
.. automethod:: BaseContour.autoStartSegment

bPoints
=======

.. autoattribute:: BaseContour.bPoints
.. automethod:: BaseContour.appendBPoint
.. automethod:: BaseContour.insertBPoint

Points
======

.. autoattribute:: BaseContour.points
.. automethod:: BaseContour.appendPoint
.. automethod:: BaseContour.insertPoint
.. automethod:: BaseContour.removePoint

Transformations
===============

.. automethod:: BaseContour.transformBy
.. automethod:: BaseContour.moveBy
.. automethod:: BaseContour.scaleBy
.. automethod:: BaseContour.rotateBy
.. automethod:: BaseContour.skewBy

Normalization
=============

.. automethod:: BaseContour.round

Environment
===========

.. automethod:: BaseContour.naked
.. automethod:: BaseContour.changed
