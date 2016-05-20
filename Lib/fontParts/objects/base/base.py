import math
from copy import deepcopy
from fontTools.misc import transform

from .errors import FontPartsError
import validators

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
    # Copy
    # ----

    copyClass = None
    copyAttributes = ()

    def copy(self):
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

    def update(self, *args, **kwargs):
        """
        Tell the environment that something has changed in
        the object. The behavior of this method will vary
        from environment to environment.

            >>> obj.update()  # doctest: +SKIP
        """

    def naked(self):
        """
        Return the wrapped object.

            >>> lowLevelObj = obj.naked()  # doctest: +SKIP
        """
        self.raiseNotImplementedError()


class BaseDict(BaseObject):

    keyValidator = None
    valueValidator = None

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
        if self.keyValidator is not None:
            keys = [self.keyValidator.im_func(key) for key in keys]
        return keys

    def _keys(self):
        """
        Subclasses may override this method.
        """
        return [k for k, v in self.items()]

    def items(self):
        items = self._items()
        if self.keyValidator is not None and self.valueValidator is not None:
            values = [
                (self.keyValidator.im_func(key), self.valueValidator.im_func(value))
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
        if self.valueValidator is not None:
            values = [self.valueValidator.im_func(value) for value in value]
        return values

    def _values(self):
        """
        Subclasses may override this method.
        """
        return [v for k, v in self.items()]

    def __contains__(self, key):
        if self.keyValidator is not None:
            key = self.keyValidator.im_func(key)
        return self._contains(key)

    def _contains(self, key):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    has_key = __contains__

    def __setitem__(self, key, value):
        if self.keyValidator is not None:
            key = self.keyValidator.im_func(key)
        if self.valueValidator is not None:
            value = self.valueValidator.im_func(value)
        self._setItem(key, value)

    def _setItem(self, key, value):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def __getitem__(self, key):
        if self.keyValidator is not None:
            key = self.keyValidator.im_func(key)
        return self._getItem(key)

    def _getItem(self, key):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def get(self, key, default=None):
        if self.keyValidator is not None:
            key = self.keyValidator.im_func(key)
        if default is not None and self.valueValidator is not None:
            default = self.valueValidator.im_func(default)
        return self._get(key, default=default)

    def _get(self, key, default=None):
        """
        Subclasses may override this method.
        """
        if key in self:
            return self[key]
        return default

    def __delitem__(self, key):
        if self.keyValidator is not None:
            key = self.keyValidator.im_func(key)
        self._delItem(key)

    def _delItem(self, key):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def pop(self, key, default=None):
        if self.keyValidator is not None:
            key = self.keyValidator.im_func(key)
        if default is not None and self.valueValidator is not None:
            default = self.valueValidator.im_func(default)
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
        if self.keyValidator is not None and self.valueValidator is not None:
            d = {}
            for key, value in other.items():
                key = self.keyValidator.im_func(key)
                value = self.valueValidator.im_func(value)
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
        Transform the object with the transformation matrix.

            >>> obj.transformBy((0.5, 0, 0, 2.0, 10, 0))                     # doctest: +SKIP
            >>> obj.transformBy((0.5, 0, 0, 2.0, 10, 0), origin=(500, 500))  # doctest: +SKIP

        The matrix must be a tuple defining a 2x2 transformation
        plus offset, aka Affine transform.

        origin, (x, y) or None, defines the point at which the
        transformation should orginate. The default is (0, 0).
        """
        matrix = validators.validateTransformationMatrix(matrix)
        if origin is None:
            origin = (0, 0)
        origin = validators.validateCoordinateTuple(origin)
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
        Transform the object with the matrix.
        The matrix will be a tuple of floats defining a 2x2
        transformation plus offset, aka Affine transform.
        origin will be a coordinate tuple (x, y).
        originOffset will be a precalculated offset (x, y)
        that represents the delta necessary to realign
        the post-transformation origin point with the
        pre-transformation point.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def moveBy(self, value):
        """
        Move the object by value.

            >>> obj.transformBy((10, 0))  # doctest: +SKIP

        Value must be a tuple defining x and y values.
        """
        value = validators.validateTransformationOffset(value)
        self._moveBy(value)

    def _moveBy(self, value, **kwargs):
        """
        Move the object by value.
        The value will be a tuple of (x, y) where
        x and y are ints or floats.

        Subclasses may override this method.
        """
        x, y = value
        t = transform.Offset(x, y)
        self.transformBy(tuple(t))

    def scaleBy(self, value, origin=None):
        """
        Scale the object by value.

            >>> obj.transformBy(2.0)                            # doctest: +SKIP
            >>> obj.transformBy((0.5, 2.0), origin=(500, 500))  # doctest: +SKIP

        value must be a tuple defining x and y values or a number.

        origin, (x, y) or None, defines the point at which the
        transformation should orginate. The default is (0, 0).
        """
        value = validators.validateTransformationScale(value)
        if origin is None:
            origin = (0, 0)
        origin = validators.validateCoordinateTuple(origin)
        self._scaleBy(value, origin=origin)

    def _scaleBy(self, value, origin=None, **kwargs):
        """
        Scale the object by value.
        The value will be a tuple of x, y factors.
        origin will be a coordinate tuple (x, y).

        Subclasses may override this method.
        """
        x, y = value
        t = transform.Identity.scale(x=x, y=y)
        self.transformBy(tuple(t), origin=origin)

    def rotateBy(self, value, origin=None):
        """
        Rotate the object by value.

            >>> obj.transformBy(45)                     # doctest: +SKIP
            >>> obj.transformBy(45, origin=(500, 500))  # doctest: +SKIP

        origin, (x, y) or None, defines the point at which the
        transformation should orginate. The default is (0, 0).
        """
        value = validators.validateTransformationRotationAngle(value)
        if origin is None:
            origin = (0, 0)
        origin = validators.validateCoordinateTuple(origin)
        self._rotateBy(value, origin=origin)

    def _rotateBy(self, value, origin=None, **kwargs):
        """
        Rotate the object by value.
        The value will be a float between 0 and 360 degrees.
        origin will be a coordinate tuple (x, y).

        Subclasses may override this method.
        """
        a = math.radians(value)
        t = transform.Identity.rotate(a)
        self.transformBy(tuple(t), origin=origin)

    def skewBy(self, value, origin=None):
        """
        Skew the object by value.

            >>> obj.skewBy(11)                           # doctest: +SKIP
            >>> obj.skewBy((25, 10), origin=(500, 500))  # doctest: +SKIP

        value can be a single number indicating an x skew or
        a tuple indicating an x, y skew.

        origin, (x, y) or None, defines the point at which the
        transformation should orginate. The default is (0, 0).
        """
        value = validators.validateTransformationSkewAngle(value)
        if origin is None:
            origin = (0, 0)
        origin = validators.validateCoordinateTuple(origin)
        self._skewBy(value, origin=origin)

    def _skewBy(self, value, origin=None, **kwargs):
        """
        Rotate the object by value.
        The value will be a tuple of two angles between
        0 and 360 degrees.
        origin will be a coordinate tuple (x, y).

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

class dynamicProperty(property):
    """
    This implements functionality that is very similar
    to Python's built in property function, but makes
    it much easier for subclassing. Here is an example
    of why this is needed:

        >>> class ParentObject(object):
        ...
        ...     _foo = 1
        ...
        ...     def _get_foo(self):
        ...         return self._foo
        ...
        ...     def _set_foo(self, value):
        ...         self._foo = value
        ...
        ...     foo = property(_get_foo, _set_foo)
        ...
        >>> class MyObject(ParentObject):
        ...
        ...     def _set_foo(self, value):
        ...         self._foo = value * 100
        ...
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

        >>> class DynamicParentObject(object):
        ...
        ...     _foo = 1
        ...
        ...     foo = dynamicProperty("foo")
        ...
        ...     def _get_foo(self):
        ...         return self._foo
        ...
        ...     def _set_foo(self, value):
        ...         self._foo = value
        ...
        >>> class MyDynamicObject(DynamicParentObject):
        ...
        ...     def _set_foo(self, value):
        ...         self._foo = value * 100
        ...
        >>> m = MyDynamicObject()
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
            raise AttributeError("no getter for %r" % self.name)

    def __set__(self, obj, value):
        setter = getattr(obj, self.setterName, None)
        if setter is not None:
            setter(value)
        else:
            raise AttributeError("no setter for %r" % self.name)

    def __call__(self, *args, **kwargs): pass

def interpolate(a, b, v):
    return a + (b - a) * v
