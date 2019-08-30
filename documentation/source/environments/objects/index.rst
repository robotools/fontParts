.. highlight:: python

############################
Subclassing fontObjects.base
############################

.. _implementing-subclassing:

The base objects have been designed to provide common behavior, normalization and type consistency for environments and scripters alike. Environments wrap their native objects with subclasses of fontParts' base objects and implement the necessary translation to the native API. Once this is done, the environment will inherit all of the base behavior from fontParts.

Environments will need to implement their own subclasses of:

.. toctree::
   :maxdepth: 1
   :hidden:

   font
   info
   groups
   kerning
   features
   lib
   layer
   glyph
   contour
   segment
   bpoint
   point
   component
   anchor
   guideline
   image

Each of these require their own specific environment overrides, but the general structure follows this form::

    from fontParts.base import BaseSomething

    class MySomething(BaseSomething):

        # Initialization.
        # This will be called when objects are initialized.
        # The behavior, args and kwargs may be designed by the
        # subclass to implement specific behaviors.

        def _init(self, myObj):
            self.myObj = myObj

        # Comparison.
        # The __eq__ method must be implemented by subclasses.
        # It must return a boolean indicating if the lower level
        # objects are the same object. This does not mean that two
        # objects that have the same content should be considered
        # equal. It means that the object must be the same. The
        # corrilary __ne__ is optional to define.
        #
        # Note that the base implentation of fontParts provides
        # __eq__ and __ne__ methods that test the naked objects
        # for equality. Depending on environmental needs this can
        # be overridden.

        def __eq__(self, other):
            return self.myObj == other.myObj

        def __ne__(self, other):
            return self.myObj != other.myObj

        # Properties.
        # Properties are get and set through standard method names.
        # Within these methods, the subclass may do whatever is
        #   necessary to get/set the value from/to the environment.

        def _get_something(self):
            return self.myObj.getSomething()

        def _set_something(self, value):
            self.myObj.setSomething(value)

        # Methods.
        # Generally, the public methods call internal methods with
        # the same name, but preceded with an underscore. Subclasses
        # may implement the internal method. Any values passed to
        # the internal methods will have been normalized and will
        # be a standard type.

        def _whatever(self, value):
            self.myObj.doWhatever(value)

        # Copying.
        # Copying is handled in most cases by the base objects.
        # If subclasses have a special class that should be used
        # when creating a copy of an object, the class must be
        # defined with the copyClass attribute. If anything special
        # needs to be done during the copying process, the subclass
        # can implement the copyData method. This method will be
        # called automatically. The subclass must call the base class
        # method with super.

        copyClass = MyObjectWithoutUI

        def copyData(self, source):
            super(MySomething, self).copyData(source)
            self.myObj.internalThing = source.internalThing

        # Environment updating.
        # If the environment requires the scripter to manually
        # notify the environment that the object has been changed,
        # the subclass must implement the changed method. Please
        # try to avoid requiring this.

        def changed(self):
            myEnv.goUpdateYourself()

        # Wrapped objects.
        # It is very useful for scripters to have access to the
        # lower level, wrapped object. Subclasses implement this
        # with the naked method.

        def naked(self):
            return self.myObj

All methods that must be overridden are labeled with "Subclasses must override this method." in the method's documentation string. If a method may optionally be overridden, the documentation string is labeled with "Subclasses may override this method." All other methods, attributes and properties **must not** be overridden.

An example implementation that wraps the defcon library with fontParts is located in fontParts/objects/fontshell.

Data Normalization
==================

When possible, incoming and outgoing values are checked for type validity and are coerced to a common type for return. This is done with a set of functions located here:

.. toctree::
   :maxdepth: 1

   objects/normalizers

These are done in a central place rather than within the objects for consitency. There are many cases where a ``(x, y)`` tuple is defined and than rewriting all of the code to check if there are exactly two values, that each is an ``int`` or a ``float`` and so on before finally making sure that the value to be returned is a ``tuple`` not an instance of ``list``, ``OrderedDict`` or some native object we consolidate the code into a single function and call that.

Environment Specific Methods, Attributes and Arguments
======================================================

FontParts is designed to be environment agnostic. Therefore, it is a 100% certainty that it doesn't do *something* that your environment does. You will want to allow your environment's *something* to be accessible through FontParts. *We* want you to allow this, too. The problem is, how do you implement *something* in a way that doesn't conflict with current or future things in FontParts? For example, let's say that you want to add a support for the "Do Something to the Font" feature you have built in your environment. You add a new method to support this::

  class MyFont(BaseFont):

    def doSomething(self, skip=None, double=None):
      # go

This *will* work. However, if FontParts adds a ``doSomething`` method in a later version that does something other than what or accepts different arguments than your method does, it's not going to work. Either the ``doSomething`` method will have to be changed in your implementation or you will not support the FontParts ``doSomething`` method. This is going to be lead to you being mad at FontParts, your scripters being mad at you or something else unpleasant.

The solution to this problem is to prevent it from happening in the first place. To do this, environment specific methods, proprties and attributes must be prefixed with an environment specific tag followed by an ``_`` and then your method name. For example::

  class MyFont(BaseFont):

    def myapp_doSomething(self, skip=None, double=None):
      # go

This applies to any method, attribute or property additions to the FontParts objects. The environment tag is up to you. The only requirement is that it needs to be unique to your own environment.

Method Arguments
----------------

In some cases, you are likely to discover that your environment supports specific options in a method that are not supported by the environment agnostic API. For example, your environment may have an optional heuristic that can be used in the ``font.autoUnicodes`` method. However, the ``font.autoUnicodes`` method does not have a ``useHeuristics`` argument. Unfortunately, Python doesn't offer a way to handle this in a way that is both flexible for developers and friendly for scripters. The only two options for handling this are:

1. Create an environment specific clone of the ``font.autoUnicodes`` method as ``myapp_autoUnicodes`` and add your ``useHeuristics`` argument there.
2. Contact the FontParts developers by opening a GitHub issue requesting support for your argument. If it is generic enough, we may add support for it.

We're experimenting with a third way to handle this. You can see it as the ``**environmentOptions`` argument in the :meth:`BaseFont.generate` method. This may or may not move to other methods. Please contact us if you are interested in this being applied to other methods.
