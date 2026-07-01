.. highlight:: python
.. module:: fontParts.base

#####
Point
#####

***********
Description
***********

:class:`Point <BasePoint>` represents one single point with a particular coordinate in a contour. It is used to access off-curve and on-curve points alike. Its cousin :class:`BPoint <BaseBPoint>` also provides access to incoming and outgoing bcps. :class:`Point <BasePoint>` is exclusively only one single point.

::

    glyph = CurrentGlyph()
    for contour in glyph:
        for point in contour.points:
            print(point)

********
Overview
********

Copy
====

.. autosummary::
    :nosignatures:

    BasePoint.copy

Parents
=======

.. autosummary::
    :nosignatures:

    BasePoint.contour
    BasePoint.glyph
    BasePoint.layer
    BasePoint.font

Identification
==============

.. autosummary::
    :nosignatures:

    BasePoint.name
    BasePoint.identifier
    BasePoint.index

Coordinate
==========

.. autosummary::
    :nosignatures:

    BasePoint.x
    BasePoint.y

Type
====

.. autosummary::
    :nosignatures:

    BasePoint.type
    BasePoint.smooth

Transformations
===============

.. autosummary::
    :nosignatures:

    BasePoint.transformBy
    BasePoint.moveBy
    BasePoint.scaleBy
    BasePoint.rotateBy
    BasePoint.skewBy

Normalization
=============

.. autosummary::
    :nosignatures:

    BasePoint.round

Environment
===========

.. autosummary::
    :nosignatures:

    BasePoint.naked
    BasePoint.changed

*********
Reference
*********

.. autoclass:: BasePoint

Copy
====

.. automethod:: BasePoint.copy

Parents
=======

.. autoattribute:: BasePoint.contour
.. autoattribute:: BasePoint.glyph
.. autoattribute:: BasePoint.layer
.. autoattribute:: BasePoint.font

Identification
==============

.. autoattribute:: BasePoint.name
.. autoattribute:: BasePoint.identifier
.. autoattribute:: BasePoint.index

Coordinate
==========

.. autoattribute:: BasePoint.x
.. autoattribute:: BasePoint.y

Type
====

.. autoattribute:: BasePoint.type
.. autoattribute:: BasePoint.smooth

Transformations
===============

.. automethod:: BasePoint.transformBy
.. automethod:: BasePoint.moveBy
.. automethod:: BasePoint.scaleBy
.. automethod:: BasePoint.rotateBy
.. automethod:: BasePoint.skewBy

Normalization
=============

.. automethod:: BasePoint.round

Environment
===========

.. automethod:: BasePoint.naked
.. automethod:: BasePoint.changed
