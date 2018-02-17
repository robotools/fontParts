import math
from copy import deepcopy
from fontTools.misc import transform
from fontParts.base.errors import FontPartsError
from fontParts.base import normalizers


# ------------
# Base Objects
# ------------

class BaseObject(object):

    # --------------
    # Initialization
    # --------------

    def __init__(self, *args, **kwargs):
        self._init(*args, **kwargs)

    def _init(self, *args, **kwargs):
        """
        Subclasses may override this method.
        """
        pass

    # ----
    # repr
    # ----

    def __repr__(self):
        contents = self._reprContents()
        if contents:
            contents = " ".join(contents)
            contents = " " + contents
        else:
            contents = ""
        s = "<{className}{contents} at {address}>".format(
            className=self.__class__.__name__,
            contents=contents,
            address=id(self)
        )
        return s

    def _reprContents(self):
        """
        Subclasses may override this method to
        provide a list of strings for inclusion
        in ``__repr__``. If so, they should call
        ``super`` and append their additions
        to the returned ``list``.
        """
        return []

    # --------
    # equality
    # --------

    def __eq__(self, other):
        """
        Subclasses may override this method.
        """
        if isinstance(other, self.__class__):
            return self.naked() is other.naked()
        return NotImplemented

    def __ne__(self, other):
        """
        Subclasses must not override this method.
        """
        equal = self.__eq__(other)
        return NotImplemented if equal is NotImplemented else not equal

    # ----
    # Hash
    # ----
    
    __hash__ = None

    # ----
    # Copy
    # ----

    copyClass = None
    copyAttributes = ()

    def copy(self):
        """
        Copy this object into a new object of the same type.
        The returned object will not have a parent object.
        """
        copyClass = self.copyClass
        if copyClass is None:
            copyClass = self.__class__
        copied = copyClass()
        copied.copyData(self)
        return copied

    def copyData(self, source):
        """
        Subclasses may override this method.
        If so, they should call the super.
        """
        for attr in self.copyAttributes:
            selfValue = getattr(self, attr)
            sourceValue = getattr(source, attr)
            if isinstance(selfValue, BaseObject):
                selfValue.copyData(sourceValue)
            else:
                setattr(self, attr, sourceValue)

    # ----------
    # Exceptions
    # ----------

    def raiseNotImplementedError(self):
        """
        This exception needs to be raised frequently by
        the base classes. So, it's here for convenience.
        """
        raise FontPartsError("The {className} subclass does not implement this method.".format(className=self.__class__.__name__))

    # ---------------------
    # Environment Fallbacks
    # ---------------------

    def changed(self, *args, **kwargs):
        """
        Tell the environment that something has changed in
        the object. The behavior of this method will vary
        from environment to environment.

            >>> obj.changed()
        """

    def naked(self):
        """
        Return the environment's native object
        that has been wrapped by this object.

            >>> loweLevelObj = obj.naked()
        """
        self.raiseNotImplementedError()


class BaseDict(BaseObject):

    keyNormalizer = None
    valueNormalizer = None

    def copyData(self, source):
        super(BaseDict, self).copyData(source)
        self.update(source)

    def __len__(self):
        value = self._len()
        return value

    def _len(self):
        """
        Subclasses may override this method.
        """
        return len(self.keys())

    def keys(self):
        keys = self._keys()
        if self.keyNormalizer is not None:
            keys = [self.keyNormalizer.__func__(key) for key in keys]
        return keys

    def _keys(self):
        """
        Subclasses may override this method.
        """
        return [k for k, v in self.items()]

    def items(self):
        items = self._items()
        if self.keyNormalizer is not None and self.valueNormalizer is not None:
            values = [
                (self.keyNormalizer.__func__(key), self.valueNormalizer.__func__(value))
                for (key, value) in items
            ]
        return values

    def _items(self):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def values(self):
        values = self._values()
        if self.valueNormalizer is not None:
            values = [self.valueNormalizer.__func__(value) for value in values]
        return values

    def _values(self):
        """
        Subclasses may override this method.
        """
        return [v for k, v in self.items()]

    def __contains__(self, key):
        if self.keyNormalizer is not None:
            key = self.keyNormalizer.__func__(key)
        return self._contains(key)

    def _contains(self, key):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    has_key = __contains__

    def __setitem__(self, key, value):
        if self.keyNormalizer is not None:
            key = self.keyNormalizer.__func__(key)
        if self.valueNormalizer is not None:
            value = self.valueNormalizer.__func__(value)
        self._setItem(key, value)

    def _setItem(self, key, value):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def __getitem__(self, key):
        if self.keyNormalizer is not None:
            key = self.keyNormalizer.__func__(key)
        return self._getItem(key)

    def _getItem(self, key):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def get(self, key, default=None):
        if self.keyNormalizer is not None:
            key = self.keyNormalizer.__func__(key)
        if default is not None and self.valueNormalizer is not None:
            default = self.valueNormalizer.__func__(default)
        return self._get(key, default=default)

    def _get(self, key, default=None):
        """
        Subclasses may override this method.
        """
        if key in self:
            return self[key]
        return default

    def __delitem__(self, key):
        if self.keyNormalizer is not None:
            key = self.keyNormalizer.__func__(key)
        self._delItem(key)

    def _delItem(self, key):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def pop(self, key, default=None):
        if self.keyNormalizer is not None:
            key = self.keyNormalizer.__func__(key)
        if default is not None and self.valueNormalizer is not None:
            default = self.valueNormalizer.__func__(default)
        return self._pop(key, default=default)

    def _pop(self, key, default=None):
        """
        Subclasses may override this method.
        """
        value = default
        if key in self:
            value = self[key]
            del self[key]
        return value

    def __iter__(self):
        return self._iter()

    def _iter(self):
        """
        Subclasses may override this method.
        """
        keys = self.keys()
        while keys:
            key = keys[0]
            yield key
            keys = keys[1:]

    def update(self, other):
        other = deepcopy(other)
        if self.keyNormalizer is not None and self.valueNormalizer is not None:
            d = {}
            for key, value in other.items():
                key = self.keyNormalizer.__func__(key)
                value = self.valueNormalizer.__func__(value)
                d[key] = value
            value = d
        self._update(other)

    def _update(self, other):
        """
        Subclasses may override this method.
        """
        for key, value in other.items():
            self[key] = value

    def clear(self):
        self._clear()

    def _clear(self):
        """
        Subclasses may override this method.
        """
        for key in self.keys():
            del self[key]


class TransformationMixin(object):

    # ---------------
    # Transformations
    # ---------------

    def transformBy(self, matrix, origin=None):
        """
        Transform the object.

            >>> obj.transformBy((0.5, 0, 0, 2.0, 10, 0))
            >>> obj.transformBy((0.5, 0, 0, 2.0, 10, 0), origin=(500, 500))

        **matrix** must be a :ref:`type-transformation`.
        **origin** defines the point at with the transformation
        should originate. It must be a :ref:`type-coordinate`
        or ``None``. The default is ``(0, 0)``.
        """
        matrix = normalizers.normalizeTransformationMatrix(matrix)
        if origin is None:
            origin = (0, 0)
        origin = normalizers.normalizeCoordinateTuple(origin)
        # calculate the origin offset
        if origin == (0, 0):
            originOffset = (0, 0)
        else:
            t = transform.Transform(*matrix)
            bx, by = origin
            ax, ay = t.transformPoint((bx, by))
            originOffset = (bx - ax, by - ay)
        # apply
        self._transformBy(matrix, origin=origin, originOffset=originOffset)

    def _transformBy(self, matrix, origin=None, originOffset=None, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseObject.transformBy`.

        **matrix** will be a :ref:`type-transformation`.
        that has been normalized with :func:`normalizers.normalizeTransformationMatrix`.
        **origin** will be a :ref:`type-coordinate` defining
        the point at which the transformation should orginate.
        **originOffset** will be a precalculated offset
        (x, y) that represents the deltas necessary to
        realign the post-transformation origin point
        with the pre-transformation origin point.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def moveBy(self, value):
        """
        Move the object.

            >>> obj.transformBy((10, 0))

        **value** must be an iterable containing two
        :ref:`type-int-float` values defining the x and y
        values to move the object by.
        """
        value = normalizers.normalizeTransformationOffset(value)
        self._moveBy(value)

    def _moveBy(self, value, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseObject.moveBy`.

        **value** will be an iterable containing two
        :ref:`type-int-float` values defining the x and y
        values to move the object by. It will have been
        normalized with :func:`normalizers.normalizeTransformationOffset`.

        Subclasses may override this method.
        """
        x, y = value
        t = transform.Offset(x, y)
        self.transformBy(tuple(t))

    def scaleBy(self, value, origin=None):
        """
        Scale the object.

            >>> obj.transformBy(2.0)
            >>> obj.transformBy((0.5, 2.0), origin=(500, 500))

        **value** must be an iterable containing two
        :ref:`type-int-float` values defining the x and y
        values to scale the object by. **origin** defines the
        point at with the scale should originate. It must be
        a :ref:`type-coordinate` or ``None``. The default is
        ``(0, 0)``.
        """
        value = normalizers.normalizeTransformationScale(value)
        if origin is None:
            origin = (0, 0)
        origin = normalizers.normalizeCoordinateTuple(origin)
        self._scaleBy(value, origin=origin)

    def _scaleBy(self, value, origin=None, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseObject.scaleBy`.

        **value** will be an iterable containing two
        :ref:`type-int-float` values defining the x and y
        values to scale the object by. It will have been
        normalized with :func:`normalizers.normalizeTransformationScale`.
        **origin** will be a :ref:`type-coordinate` defining
        the point at which the scale should orginate.

        Subclasses may override this method.
        """
        x, y = value
        t = transform.Identity.scale(x=x, y=y)
        self.transformBy(tuple(t), origin=origin)

    def rotateBy(self, value, origin=None):
        """
        Rotate the object.

            >>> obj.transformBy(45)
            >>> obj.transformBy(45, origin=(500, 500))

        **value** must be a :ref:`type-int-float` values
        defining the angle to rotate the object by. **origin**
        defines the point at with the rotation should originate.
        It must be a :ref:`type-coordinate` or ``None``.
        The default is ``(0, 0)``.
        """
        value = normalizers.normalizeTransformationRotationAngle(value)
        if origin is None:
            origin = (0, 0)
        origin = normalizers.normalizeCoordinateTuple(origin)
        self._rotateBy(value, origin=origin)

    def _rotateBy(self, value, origin=None, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseObject.rotateBy`.

        **value** will be a :ref:`type-int-float` value
        defining the value to rotate the object by.
        It will have been normalized with
        :func:`normalizers.normalizeTransformationRotationAngle`.
        **origin** will be a :ref:`type-coordinate` defining
        the point at which the rotation should orginate.

        Subclasses may override this method.
        """
        a = math.radians(value)
        t = transform.Identity.rotate(a)
        self.transformBy(tuple(t), origin=origin)

    def skewBy(self, value, origin=None):
        """
        Skew the object.

            >>> obj.skewBy(11)
            >>> obj.skewBy((25, 10), origin=(500, 500))

        **value** must be rone of the following:

        * single :ref:`type-int-float` indicating the
          value to skew the x direction by.
        * iterable cointaining type :ref:`type-int-float`
          defining the values to skew the x and y directions by.

        **origin** defines the point at with the skew should
        originate. It must be a :ref:`type-coordinate` or
        ``None``. The default is ``(0, 0)``.
        """
        value = normalizers.normalizeTransformationSkewAngle(value)
        if origin is None:
            origin = (0, 0)
        origin = normalizers.normalizeCoordinateTuple(origin)
        self._skewBy(value, origin=origin)

    def _skewBy(self, value, origin=None, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseObject.skewBy`.

        **value** will be an iterable containing two
        :ref:`type-int-float` values defining the x and y
        values to skew the object by. It will have been
        normalized with :func:`normalizers.normalizeTransformationSkewAngle`.
        **origin** will be a :ref:`type-coordinate` defining
        the point at which the skew should orginate.

        Subclasses may override this method.
        """
        x, y = value
        x = math.radians(x)
        y = math.radians(y)
        t = transform.Identity.skew(x=x, y=y)
        self.transformBy(tuple(t), origin=origin)



# -------
# Helpers
# -------

class dynamicProperty(object):

    """
    This implements functionality that is very similar
    to Python's built in property function, but makes
    it much easier for subclassing. Here is an example
    of why this is needed:

        class BaseObject(object):

            _foo = 1

            def _get_foo(self):
                return self._foo

            def _set_foo(self, value):
                self._foo = value

            foo = property(_get_foo, _set_foo)


        class MyObject(BaseObject):

            def _set_foo(self, value):
                self._foo = value * 100


        >>> m = MyObject()
        >>> m.foo
        1
        >>> m.foo = 2
        >>> m.foo
        2

    The expected value is 200. The _set_foo method
    needs to be reregistered. Doing that also requires
    reregistering the _get_foo method. It's possible
    to do this, but it's messy and will make subclassing
    less than ideal.

    Using dynamicProperty solves this.

        class BaseObject(object):

            _foo = 1

            foo = dynamicProperty("foo")

            def _get_foo(self):
                return self._foo

            def _set_foo(self, value):
                self._foo = value


        class MyObject(BaseObject):

            def _set_foo(self, value):
                self._foo = value * 100


        >>> m = MyObject()
        >>> m.foo
        1
        >>> m.foo = 2
        >>> m.foo
        200
    """

    def __init__(self, name, doc=None):
        self.name = name
        self.__doc__ = doc
        self.getterName = "_get_" + name
        self.setterName = "_set_" + name

    def __get__(self, obj, cls):
        getter = getattr(obj, self.getterName, None)
        if getter is not None:
            return getter()
        else:
            raise FontPartsError("no getter for %r" % self.name)

    def __set__(self, obj, value):
        setter = getattr(obj, self.setterName, None)
        if setter is not None:
            setter(value)
        else:
            raise FontPartsError("no setter for %r" % self.name)


def interpolate(a, b, v):
    return a + (b - a) * v



class PointPositionMixin(object):

    """
    This adds a ``position`` attribute as a dyanmicProperty,
    for use as a mixin with objects that have ``x`` and ``y``
    attributes.
    """

    position = dynamicProperty("base_position", "The point position.")

    def _get_base_position(self):
        value = self._get_position()
        value = normalizers.normalizeCoordinateTuple(value)
        return value

    def _set_base_position(self, value):
        value = normalizers.normalizeCoordinateTuple(value)
        self._set_position(value)

    def _get_position(self):
        """
        Subclasses may override this method.
        """
        return (self.x, self.y)

    def _set_position(self, value):
        """
        Subclasses may override this method.
        """
        pX, pY = self.position
        x, y = value
        dX = x - pX
        dY = y - pY
        self.moveBy((dX, dY))


def reference(obj):
    # import weakref
    # return weakref.ref(obj)
    def wrapper():
        return obj
    return wrapper
