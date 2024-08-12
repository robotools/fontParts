.. highlight:: python

###########
Documenting
###########

In general, follow the suggestions `here <https://docs.python.org/devguide/documenting.html>`_.

**************
Tones of Voice
**************

The documentation needs to speak to three different groups of people, each with different needs.

    #. Designers writing scripts that use fontParts. This is the *Public API*.
    #. Developers implementing fontParts inside their own application. This is the *Implementation API*.
    #. Developers working on fontParts itself. This is the *Internal Stuff*.

Each of these needs a different tone of voice, level of detail and so on.

Public API
==========

Most people reading the Public API will be looking for specific information about a specific method, property, etc. The text needs to be brief, easy to understand and quick to get the gist of.

    * write as if talking
    * don't assume that the reader has more than basic Python proficiency
    * be detailed, but not overwhelming
    * keep technical jargon to a minimum
    * show examples

Examples
--------

Examples should be simple and concise. They should show what is being documented and nothing else. The point of the documentation examples is to show how to use the method/function being explained, not to make a fully functional script. (Fully functional demo scripts will be a separate type of documentation.)

  * use interactive prompt style with ``>>>``
  * use Python 3 syntax
  * don't show more functionality than is necessary for what the documentation is explaining
  * don't show ``import`` statements unless necessary
  * don't show constructors unless that is what is being demonstrated
  * multiple examples each showing one thing are better than one example showing multiple things

Do this: ::

  >>> font.glyphOrder = ["A", "B", "C"]
  >>> font.glyphOrder
  ["A", "B", "C"]

Don't do this: ::

  import random
  from fontParts.world import *

  font = CurrentFont()
  print(font.glyphOrder)
  font.glyphOrder = sorted(font.glyphOrder)
  print(font.glyphOrder)
  order = list(font.glyphOrder)
  random.shuffle(order)
  font.glyphOrder = order
  print(font.glyphOrder)


Implementation API
==================

Developers reading the Implementation API will be looking for detailed information about what they need to do. The text needs to make their work as easy as possible.

    * write concisely
    * assume that the reader has computer science proficiency
    * cover requirements thoroughly
    * explain what can be expected of incoming data
    * explain what is expected of outgoing data
    * don't leave anything to assumption or interpretation
    * always use may/must/should terminology


Internal Stuff
==============

The code within fontParts itself should be written such that what the code is doing is immediately apparent. Thus, it should require very limited documentation, if any at all.

    * assume that the reader knows how fontParts works
    * funny jokes are allowed, but only if they are funny


*********************
Documentation Strings
*********************

Most of the documentation will be contained with the source code itself. Here's the structure of how it should be done:

::

    class BaseThing(BaseOtherThing):

        """
        This is a very brief explanation of the object.
        A note about when to create this object may be added.
        This text will be prepended to the string in __init__
        in the compiled documentation.
        """

        def aMethod(arg, kwarg="blah"):
            """
            A very brief description calling out majorly significant ``args``.

                >>> blah.public()
                "output"

            The next level of documentation is presented in paragraph
            form. This will detail what ``arg`` means/does, it's potential
            options (linking to :ref:`type-detail` or :class:`ObjectClass`
            as needed, the default value, any possible errors and so on.
            If a list is needed to detail what the method does, it should be
            presented as a list:

                * this happens
                * that happens
                * finally this happens

            It should read very simply and clearly. Next is a description
            of ``kwarg`` following the same form. If an argument has
            options they are to be presented as a table.

            +---------+-----------------------+
            | option1 | Sentence description. |
            +---------+-----------------------+
            | option2 | Sentence description. |
            +---------+-----------------------+

            Further explanations carry on for additional arguments
            and so on.

            .. note::

               If there is a special note, put it in a note section.
            """

        def _aMethod(arg, kwarg="blah"):
            """
            This is the environment implementation of :meth:`BaseThing.aMethod`.
            ``arg`` will be a :ref:`type-detail` that has been normalized with
            :func:`normalizers.normalizeValue`. If there are any notes
            on how to interpret this, it goes here. ``kwarg`` is now explained.
            The options for kwarg are detailed in :meth:`BaseThing.aMethod` rather
            than duplicated here. If something goes wrong a :exc:`FontPartsError`
            (or other applicable) error must be raised. This method must return
            a result of :ref:`type-detail` and the returned value will be normalized
            with :func:`normalizers.normalizeValue`.

            Subclassing statement such as: Subclasses may override this method.
            """

        aProperty = dynamicProperty(
            "base_aProperty",
            """
            A very brief description with optional :ref:`type-detail`.

                >>> print(font.aProperty)
                "output"

            Additional info if needed.
            """
        )


***************
Quick Reference
***************


Basic Formatting
================

::

    *emphasis (italics)*
    **strong (bold)**
    ``code`` Always use this for things like args, kwargs, ``True``, ``False`` and ``None``.

    `Some text <http://target>`_
    :mod:`module`
    :func:`module.functionName`
    :class:`ClassName`
    :meth:`ClassName.methodName`
    :attr:`ClassName.attribute`
    :exc:`ExceptionName`
    :ref:`my-reference-label`

    * unordered
    * list

    #. ordered
    #. list

    +---------+--------------+
    | option1 | Description. |
    +---------+--------------+
    | option2 | Description. |
    +---------+--------------+


Frequently Used Stuff
=====================

Statements
----------

* This attribute is read only.
* Subclasses must override this method.
* Subclasses may override this method.

Value Types
-----------

fontParts
^^^^^^^^^

* ``:ref:`type-string```
* ``:ref:`type-int-float```
* ``:ref:`type-coordinate```
* ``:ref:`type-angle```
* ``:ref:`type-identifier```
* ``:ref:`type-color```
* ``:ref:`type-transformation```
* ``:ref:`type-immutable-list```

general
^^^^^^^

* ``:ref:`type-string```
* ``:ref:`type-int```
* ``:ref:`type-float```
* ``:ref:`type-hex```
* ``:ref:`type-bool```
* ``:ref:`type-tuple```
* ``:ref:`type-list```
* ``:ref:`type-dict```
* ``:ref:`type-set```


Heading Levels
==============

::

    #######
    Level 1
    #######

    *******
    Level 2
    *******

    Level 3
    =======

    Level 4
    -------

    Level 5
    ^^^^^^^

    Level 6
    """""""


Special Sections
================

::

    .. note::
    .. warning::
    .. versionadded::
    .. versionchanged::
    .. seealso::
