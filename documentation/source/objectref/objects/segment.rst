.. highlight:: python
.. module:: fontParts.base

#######
Segment
#######

***********
Description
***********

A :class:`Contour <BaseContour>` object is a list of segments. A :class:`Segment <BaseSegment>` is a list of points with some special attributes and methods.

********
Overview
********

Parents
=======

.. autosummary::
    :nosignatures:

    BaseSegment.contour
    BaseSegment.glyph
    BaseSegment.layer
    BaseSegment.font

Identification
==============

.. autosummary::
    :nosignatures:

    BaseSegment.index

Attributes
==========

.. autosummary::
    :nosignatures:

    BaseSegment.type
    BaseSegment.smooth

Points
======

.. autosummary::
    :nosignatures:

    BaseSegment.points
    BaseSegment.onCurve
    BaseSegment.offCurve

Transformations
===============

.. autosummary::
    :nosignatures:

    BaseSegment.transformBy
    BaseSegment.moveBy
    BaseSegment.scaleBy
    BaseSegment.rotateBy
    BaseSegment.skewBy

Normalization
=============

.. autosummary::
    :nosignatures:

    BaseSegment.round

Environment
===========

.. autosummary::
    :nosignatures:

    BaseSegment.naked
    BaseSegment.changed

*********
Reference
*********

.. autoclass:: BaseSegment

Parents
=======

.. autoattribute:: BaseSegment.contour
.. autoattribute:: BaseSegment.glyph
.. autoattribute:: BaseSegment.layer
.. autoattribute:: BaseSegment.font

Identification
==============

.. autoattribute:: BaseSegment.index

Attributes
==========

.. autoattribute:: BaseSegment.type
.. autoattribute:: BaseSegment.smooth

Points
======

.. autoattribute:: BaseSegment.points
.. autoattribute:: BaseSegment.onCurve
.. autoattribute:: BaseSegment.offCurve

Transformations
===============

.. automethod:: BaseSegment.transformBy
.. automethod:: BaseSegment.moveBy
.. automethod:: BaseSegment.scaleBy
.. automethod:: BaseSegment.rotateBy
.. automethod:: BaseSegment.skewBy

Normalization
=============

.. automethod:: BaseSegment.round

Environment
===========

.. automethod:: BaseSegment.naked
.. automethod:: BaseSegment.changed

