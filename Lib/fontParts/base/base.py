from __future__ import annotations
from typing import Any, List, Tuple, Optional, Callable, Dict, Type, Union
from numbers import Number
import math
from fontTools.misc import transform
from fontParts.base.errors import FontPartsError
from fontParts.base import normalizers
from fontParts.base.annotations import (
    CoordinateType,
    FactorType,
    IntFloatType,
    ScaleType,
    TransformationMatrixType
)


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

    def __init__(self, name: str, doc: Optional[str] = None) -> None:
        self.name = name
        self.__doc__ = doc
        self.getterName = "_get_" + name
        self.setterName = "_set_" + name

    def __get__(self, obj: Any, cls: Type[Any]) -> Any:
        getter = getattr(obj, self.getterName, None)
        if getter is not None:
            return getter()
        else:
            # obj is None when the property is accessed
            # via the class instead of an instance
            if obj is None:
                return self
            raise FontPartsError("no getter for %r" % self.name)

    def __set__(self, obj: Any, value: Any) -> None:
        setter = getattr(obj, self.setterName, None)
        if setter is not None:
            setter(value)
        else:
            raise FontPartsError("no setter for %r" % self.name)


def interpolate(a: Number, b: Number, v: FactorType) -> float:
    return a + (b - a) * v


# ------------
# Base Objects
# ------------


class BaseObject:
    # --------------
    # Initialization
    # --------------

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._init(*args, **kwargs)

    def _init(self, *args: Any, **kwargs: Any) -> None:
        """
        Subclasses may override this method.
        """

    # ----
    # repr
    # ----

    def __repr__(self) -> str:
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

    @classmethod
    def _reprContents(cls) -> List[str]:
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

    def __eq__(self, other: Any) -> bool:
        """
        Subclasses may override this method.
        """
        if isinstance(other, self.__class__):
            return self.naked() is other.naked()
        return NotImplemented

    def __ne__(self, other: Any) -> bool:
        """
        Subclasses must not override this method.
        """
        equal = self.__eq__(other)
        return NotImplemented if equal is NotImplemented else not equal

    # ----
    # Hash
    # ----

    def __hash__(self) -> int:
        """
        Allow subclasses to be used in hashable collections.
        Subclasses may override this method.
        """
        return id(self.naked())

    # ----
    # Copy
    # ----

    copyClass: Optional[type] = None
    copyAttributes: Tuple[str, ...] = ()

    def copy(self) -> 'BaseObject':
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

    def copyData(self, source: BaseObject) -> None:
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

    def raiseNotImplementedError(self) -> None:
        """
        This exception needs to be raised frequently by
        the base classes. So, it's here for convenience.
        """
        raise NotImplementedError(
            "The {className} subclass does not implement this method."
            .format(className=self.__class__.__name__)
        )

    # ---------------------
    # Environment Fallbacks
    # ---------------------

    def changed(self, *args: Any, **kwargs: Any) -> None:
        """
        Tell the environment that something has changed in
        the object. The behavior of this method will vary
        from environment to environment.
        """

    def naked(self) -> Any:
        """
        Return the environment's native object
        that has been wrapped by this object.
        """
        self.raiseNotImplementedError()


class BaseDict(BaseObject):
    keyNormalizer: Optional[Any] = None
    valueNormalizer: Optional[Any] = None

    def copyData(self, source: 'BaseDict') -> None:
        super(BaseDict, self).copyData(source)
        self.update(source)

    def __len__(self) -> int:
        value = self._len()
        return value

    def _len(self) -> int:
        """
        Subclasses may override this method.
        """
        return len(self.keys())

    def keys(self) -> List[Any]:
        keys = self._keys()
        if self.keyNormalizer is not None:
            keys = [self.keyNormalizer.__func__(key) for key in keys]
        return keys

    def _keys(self) -> List[Any]:
        """
        Subclasses may override this method.
        """
        return [k for k, v in self.items()]

    def items(self) -> List[Tuple[Any, Any]]:
        items = self._items()
        if self.keyNormalizer is not None and self.valueNormalizer is not None:
            items = [
                (self.keyNormalizer.__func__(key),
                 self.valueNormalizer.__func__(value))
                for (key, value) in items
            ]
        return items

    def _items(self) -> List[Tuple[Any, Any]]:
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def values(self) -> List[Any]:
        values = self._values()
        if self.valueNormalizer is not None:
            values = [self.valueNormalizer.__func__(value) for value in values]
        return values

    def _values(self) -> List[Any]:
        """
        Subclasses may override this method.
        """
        return [v for k, v in self.items()]

    def __contains__(self, key: Any) -> bool:
        if self.keyNormalizer is not None:
            key = self.keyNormalizer.__func__(key)
        return self._contains(key)

    def _contains(self, key: Any) -> bool:
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.keyNormalizer is not None:
            key = self.keyNormalizer.__func__(key)
        if self.valueNormalizer is not None:
            value = self.valueNormalizer.__func__(value)
        self._setItem(key, value)

    def _setItem(self, key: Any, value: Any) -> None:
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def __getitem__(self, key: Any) -> Any:
        if self.keyNormalizer is not None:
            key = self.keyNormalizer.__func__(key)
        value = self._getItem(key)
        if self.valueNormalizer is not None:
            value = self.valueNormalizer.__func__(value)
        return value

    def _getItem(self, key: Any) -> Any:
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def get(self, key: Any, default: Optional[Any] = None) -> Any:
        if self.keyNormalizer is not None:
            key = self.keyNormalizer.__func__(key)
        if default is not None and self.valueNormalizer is not None:
            default = self.valueNormalizer.__func__(default)
        value = self._get(key, default=default)
        if value is not default and self.valueNormalizer is not None:
            value = self.valueNormalizer.__func__(value)
        return value

    def _get(self, key: Any, default: Optional[Any] = None) -> Any:
        """
        Subclasses may override this method.
        """
        if key in self:
            return self[key]
        return default

    def __delitem__(self, key: Any) -> None:
        if self.keyNormalizer is not None:
            key = self.keyNormalizer.__func__(key)
        self._delItem(key)

    def _delItem(self, key: Any) -> None:
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def pop(self, key: Any, default: Optional[Any] = None) -> Any:
        if self.keyNormalizer is not None:
            key = self.keyNormalizer.__func__(key)
        if default is not None and self.valueNormalizer is not None:
            default = self.valueNormalizer.__func__(default)
        value = self._pop(key, default=default)
        if self.valueNormalizer is not None:
            value = self.valueNormalizer.__func__(value)
        return value

    def _pop(self, key: Any, default: Optional[Any] = None) -> Any:
        """
        Subclasses may override this method.
        """
        value = default
        if key in self:
            value = self[key]
            del self[key]
        return value

    def __iter__(self) -> Any:
        return self._iter()

    def _iter(self) -> Any:
        """
        Subclasses may override this method.
        """
        keys = self.keys()
        while keys:
            key = keys[0]
            yield key
            keys = keys[1:]

    def update(self, other: Dict[Any, Any]) -> None:
        from copy import deepcopy
        other = deepcopy(other)
        if self.keyNormalizer is not None and self.valueNormalizer is not None:
            d = {}
            for key, value in other.items():
                key = self.keyNormalizer.__func__(key)
                value = self.valueNormalizer.__func__(value)
                d[key] = value
            other = d
        self._update(other)

    def _update(self, other: Dict[Any, Any]) -> None:
        """
        Subclasses may override this method.
        """
        for key, value in other.items():
            self[key] = value

    def clear(self) -> None:
        self._clear()

    def _clear(self) -> None:
        """
        Subclasses may override this method.
        """
        for key in self.keys():
            del self[key]


class TransformationMixin(object):

    # ---------------
    # Transformations
    # ---------------

    def transformBy(self,
                    matrix: TransformationMatrixType,
                    origin: Optional[CoordinateType] = None):
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
        if origin is not None:
            t = transform.Transform()
            oX, oY = origin
            t = t.translate(oX, oY)
            t = t.transform(matrix)
            t = t.translate(-oX, -oY)
            matrix = tuple(t)
        self._transformBy(matrix)

    def _transformBy(self,
                     matrix: TransformationMatrixType,
                     **kwargs: Any) -> None:
        """
        This is the environment implementation of
        :meth:`BaseObject.transformBy`.

        **matrix** will be a :ref:`type-transformation`.
        that has been normalized with
        :func:`normalizers.normalizeTransformationMatrix`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def moveBy(self, value: CoordinateType) -> None:
        """
        Move the object.

            >>> obj.moveBy((10, 0))

        **value** must be an iterable containing two
        :ref:`type-int-float` values defining the x and y
        values to move the object by.
        """
        value = normalizers.normalizeTransformationOffset(value)
        self._moveBy(value)

    def _moveBy(self, value: CoordinateType, **kwargs: Any) -> None:
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
        self.transformBy(tuple(t), **kwargs)

    def scaleBy(self,
                value: ScaleType,
                origin: Optional[IntFloatType] = None) -> None:
        """
        Scale the object.

            >>> obj.scaleBy(2.0)
            >>> obj.scaleBy((0.5, 2.0), origin=(500, 500))

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

    def _scaleBy(self,
                 value: ScaleType,
                 origin: Optional[CoordinateType] = None,
                 **kwargs: Any) -> None:
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
        self.transformBy(tuple(t), origin=origin, **kwargs)

    def rotateBy(self,
                 value: IntFloatType,
                 origin: Optional[CoordinateType] = None) -> None:
        """
        Rotate the object.

            >>> obj.rotateBy(45)
            >>> obj.rotateBy(45, origin=(500, 500))

        **value** must be a :ref:`type-int-float` values
        defining the angle to rotate the object by. **origin**
        defines the point at with the rotation should originate.
        It must be a :ref:`type-coordinate` or ``None``.
        The default is ``(0, 0)``.
        """
        value = normalizers.normalizeRotationAngle(value)
        if origin is None:
            origin = (0, 0)
        origin = normalizers.normalizeCoordinateTuple(origin)
        self._rotateBy(value, origin=origin)

    def _rotateBy(self,
                  value: IntFloatType,
                  origin: Optional[CoordinateType] = None,
                  **kwargs: Any) -> None:
        """
        This is the environment implementation of
        :meth:`BaseObject.rotateBy`.

        **value** will be a :ref:`type-int-float` value
        defining the value to rotate the object by.
        It will have been normalized with
        :func:`normalizers.normalizeRotationAngle`.
        **origin** will be a :ref:`type-coordinate` defining
        the point at which the rotation should orginate.

        Subclasses may override this method.
        """
        a = math.radians(value)
        t = transform.Identity.rotate(a)
        self.transformBy(tuple(t), origin=origin, **kwargs)

    def skewBy(self,
               value: FactorType,
               origin: Optional[CoordinateType] = None) -> None:
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

    def _skewBy(self,
                value: FactorType,
                origin: Optional[CoordinateType] = None,
                **kwargs: Any) -> None:
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
        self.transformBy(tuple(t), origin=origin, **kwargs)


class InterpolationMixin(object):

    # -------------
    # Compatibility
    # -------------

    compatibilityReporterClass: Optional[Type[Any]] = None

    def isCompatible(self, other: Any, cls: Type[Any]) -> Tuple[bool, Any]:
        """
        Evaluate interpolation compatibility with other.
        """
        if not isinstance(other, cls):
            raise TypeError(
                """Compatibility between an instance of %r and an \
                instance of %r can not be checked."""
                % (cls.__name__, other.__class__.__name__))
        reporter = self.compatibilityReporterClass(self, other)
        self._isCompatible(other, reporter)
        return not reporter.fatal, reporter

    def _isCompatible(self, other: Any, reporter: Any) -> None:
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()


class SelectionMixin(object):

    # -------------
    # Selected Flag
    # -------------

    selected: dynamicProperty = dynamicProperty(
        "base_selected",
        """
        The object's selection state.

            >>> obj.selected
            False
            >>> obj.selected = True
        """
    )

    def _get_base_selected(self) -> bool:
        value = self._get_selected()
        value = normalizers.normalizeBoolean(value)
        return value

    def _set_base_selected(self, value: bool) -> None:
        value = normalizers.normalizeBoolean(value)
        self._set_selected(value)

    def _get_selected(self) -> bool:
        """
        This is the environment implementation of
        :attr:`BaseObject.selected`. This must return a
        **boolean** representing the selection state
        of the object. The value will be normalized
        with :func:`normalizers.normalizeBoolean`.

        Subclasses must override this method if they
        implement object selection.
        """
        self.raiseNotImplementedError()

    def _set_selected(self, value: bool) -> None:
        """
        This is the environment implementation of
        :attr:`BaseObject.selected`. **value** will
        be a **boolean** representing the object's
        selection state. The value will have been
        normalized with :func:`normalizers.normalizeBoolean`.

        Subclasses must override this method if they
        implement object selection.
        """
        self.raiseNotImplementedError()

    # -----------
    # Sub-Objects
    # -----------
    @classmethod
    def _getSelectedSubObjects(cls, subObjects: List[Any]) -> List[Any]:
        selected = [obj for obj in subObjects if obj.selected]
        return selected

    @classmethod
    def _setSelectedSubObjects(cls,
                               subObjects: List[Any],
                               selected: List[Any]) -> None:
        for obj in subObjects:
            obj.selected = obj in selected


class PointPositionMixin(object):

    """
    This adds a ``position`` attribute as a dyanmicProperty,
    for use as a mixin with objects that have ``x`` and ``y``
    attributes.
    """

    position: dynamicProperty = dynamicProperty(
        "base_position", "The point position."
    )

    def _get_base_position(self) -> CoordinateType:
        value = self._get_position()
        value = normalizers.normalizeCoordinateTuple(value)
        return value

    def _set_base_position(self, value: CoordinateType) -> None:
        value = normalizers.normalizeCoordinateTuple(value)
        self._set_position(value)

    def _get_position(self) -> CoordinateType:
        """
        Subclasses may override this method.
        """
        return (self.x, self.y)

    def _set_position(self, value: CoordinateType) -> None:
        """
        Subclasses may override this method.
        """
        pX, pY = self.position
        x, y = value
        dX = x - pX
        dY = y - pY
        self.moveBy((dX, dY))


class IdentifierMixin(object):

    # identifier

    identifier: dynamicProperty = dynamicProperty(
        "base_identifier",
        """
        The unique identifier for the object.
        This value will be an :ref:`type-identifier` or a ``None``.
        This attribute is read only. ::

            >>> object.identifier
            'ILHGJlygfds'

        To request an identifier if it does not exist use
        `object.getIdentifier()`
        """
    )

    def _get_base_identifier(self) -> Optional[str]:
        value = self._get_identifier()
        if value is not None:
            value = normalizers.normalizeIdentifier(value)
        return value

    def _get_identifier(self) -> Optional[str]:
        """
        This is the environment implementation of
        :attr:`BaseObject.identifier`. This must
        return an :ref:`type-identifier`. If
        the native object does not have an identifier
        assigned one should be assigned and returned.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def getIdentifier(self) -> str:
        """
        Create a new, unique identifier for and assign it to the object.
        If the object already has an identifier, the existing one should
        be returned.
        """
        return self._getIdentifier()

    def _getIdentifier(self) -> str:
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _setIdentifier(self, value: str) -> None:
        """
        This method is used internally to force a specific
        identifier onto an object in certain situations.
        Subclasses that allow setting an identifier to a
        specific value may override this method.
        """


def reference(obj: Any) -> Callable[[], Any]:
    # import weakref
    # return weakref.ref(obj)
    def wrapper() -> Any:
        return obj
    return wrapper


class FuzzyNumber(object):
    """
    A number like object with a threshold.
    Use it to compare numbers where a threshold is needed.
    """

    def __init__(self, value: IntFloatType, threshold: IntFloatType) -> None:
        self.value = value
        self.threshold = threshold

    def __repr__(self) -> str:
        return "[%f %f]" % (self.value, self.threshold)

    def __lt__(self, other: Union[FuzzyNumber, IntFloatType]) -> bool:
        if hasattr(other, "value"):
            if abs(self.value - other.value) < self.threshold:
                return False
            else:
                return self.value < other.value
        return self.value < other

    def __eq__(self, other: Union[FuzzyNumber, IntFloatType]) -> bool:
        if hasattr(other, "value"):
            return abs(self.value - other.value) < self.threshold
        return self.value == other

    def __hash__(self) -> int:
        return hash((self.value, self.threshold))
