##################
Common Value Types
##################

FontParts scripts are built on with objects that represent fonts, glyphs, contours and so on. The objects are obtained through :ref:`fontparts-world`.


.. _fontparts-objects:

FontParts uses some common value types.

.. toctree::
   :maxdepth: 2
   :hidden:

   valuetypes

.. _type-string:

String
------

Unicode (unencoded) or string. Internally everything is a unicode string.


.. _type-int-float:

Integer/Float
-------------

Integers and floats are interchangeable in FontParts (unless the specification states that only one is allowed).


.. _type-coordinate:

Coordinate
----------

An immutable iterable containing two :ref:`type-int-float` representing:

#. x
#. y


.. _type-angle:

Angle
-----

XXX define the angle specifications here. Direction, degrees, etc. This will always be a float.


.. _type-identifier:

Identifier
----------

A :ref:`type-string` following the `UFO identifier conventions <http://unifiedfontobject.org/versions/ufo3/conventions/#identifiers>`_.


.. _type-color:

Color
-----

An immutable iterable containing four :ref:`type-int-float` representing:

#. red
#. green
#. blue
#. alpha

Values are from 0 to 1.0.


.. _type-transformation:

Transformation Matrix
---------------------

An immutable iterable defining a 2x2 transformation plus offset (aka Affine transform). The default is ``(1, 0, 0, 1, 0, 0)``.


.. _type-immutable-list:

Immutable List
--------------

This must be an immutable, ordered iterable like a ``tuple``.