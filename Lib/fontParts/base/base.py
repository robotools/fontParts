# pylint: disable=C0103, C0114
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generic,
    Iterable,
    Iterator,
    List,
    NoReturn,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)
from copy import deepcopy
import math
from collections.abc import MutableMapping

from fontTools.misc import transform
from fontParts.base.errors import FontPartsError
from fontParts.base import normalizers
from fontParts.base.annotations import (
    PairType,
    CollectionType,
    PairCollectionType,
    SextupleCollectionType,
    IntFloatType,
    TransformationType,
    InterpolatableType,
)

if TYPE_CHECKING:
    from collections.abc import ItemsView

BaseObjectType = TypeVar("BaseObjectType", bound="BaseObject")
KeyType = TypeVar("KeyType")
ValueType = TypeVar("ValueType")

# -------
# Helpers
# -------


class dynamicProperty:
    """Represent a property for simplified subclassing.

    This class implements functionality that is very similar to Python's built
    in :class:`property`, but allows the getter and setter methods to be
    automatically resolved by name, making it possible to partially override
    the property in a subclass without having to re-register both the getter
    and setter methods.

    :param name: The base name of the property, used to resolve the getter and
        setter method names.
    :param doc: Optional documentation string for the property.
    :raises: FontPartsError: If the getter or setter method is not defined.

    Example of why this is needed:

    .. code-block:: python

        class BaseObject:

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

    The expected value is ``200``. The ``_set_foo`` method needs to be
    reregistered. Doing that also requires reregistering the ``_get_foo``
    method. It's possible to do this, but it's messy and will make subclassing
    less than ideal.

    Using dynamicProperty solves this:

    .. code-block:: python

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
            raise FontPartsError(f"no getter for {self.name!r}")

    def __set__(self, obj: Any, value: Any) -> None:
        setter = getattr(obj, self.setterName, None)
        if setter is not None:
            setter(value)
        else:
            raise FontPartsError(f"no setter for {self.name!r}")


def interpolate(
    minValue: InterpolatableType,
    maxValue: InterpolatableType,
    factor: TransformationType,
) -> InterpolatableType:
    """Interpolate between two number-like objects.

    This method performs linear interpolation, calculating a value that is
    proportionally between `minValue` and `maxValue`, determined by the factor `factor`.

    :param minValue: The value corresponding to the 0.0 position in the interpolation
        as any object :ref:`emulating numeric types <numeric-types>`.
    :param maxValue: The value corresponding to the 1.0 position in the interpolation
        as any object :ref:`emulating numeric types <numeric-types>`.
    :param factor: The factor value determining the interpolation between
        `minValue` and `maxValue` as a single :class:`int` or :class:`float`.
        If `minValue` and `maxValue` supports it, `factor` may also be
        a :class:`tuple` of two :class:`int` or :class:`float` values representing
        the factors ``(x, y)``.
    :return: The interpolated value as any object :ref:`emulating numeric types
        <numeric-types>`.
    :raises TypeError: If `minValue` or `maxValue` does not support the provided
        `factor` type.

    """
    try:
        return minValue + (maxValue - minValue) * factor
    except TypeError as exc:
        raise TypeError(
            f"Factor must be an int or minValue float, not {type(factor).__name__}."
        ) from exc


# ------------
# Base Objects
# ------------


class BaseObject(Generic[BaseObjectType]):
    r"""Provide common base functionality to objects.

    This class is intended to serve as a foundation for other classes, supplying
    essential behaviors like initialization, string representation, comparison,
    and copying, while leaving more specific implementations to be provided by
    subclasses.

    Subclasses are expected to override or extend methods to suit their own
    behavior.

    :cvar copyClass: The class used for copying, defaults to the subclass being copied.
    :cvar copyAttributes: A tuple of attribute names to be copied when calling `copyData`.
    :param \*args: Any positional arguments.
    :param \**kwargs: Any keyword arguments.

    """

    # --------------
    # Initialization
    # --------------

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._init(*args, **kwargs)

    def _init(self, *args: Any, **kwargs: Any) -> None:
        r"""Initialize the native object.

        This is the environment implementation of :meth:`BaseObject.__init__`.

        :param \*args: Any positional arguments.
        :param \**kwargs: Any keyword arguments.

        .. note::

            Subclasses may override this method.

        """

    # ----
    # repr
    # ----

    def __repr__(self) -> str:
        contents = self._reprContents()
        if contents:
            contentString = " ".join(contents)
            contentString = " " + contentString
        else:
            contentString = ""
        return f"<{self.__class__.__name__}{contentString} at {id(self)}>"

    def _reprContents(self) -> List[str]:
        """Provide a list of strings for inclusion in :meth:`BaseObject.__repr__.

        :return: A :class:`list` of :class:`str` items.

        .. note::

            Subclasses may override this method.
            If so, they should call :class:`super` and append their additions.

        """
        return []

    # --------
    # equality
    # --------

    def __eq__(self, other: Any) -> bool:
        """Check for equality with another object.

        :param other: The object to compare with.
        :return: :obj:`True` if the objects are equal, :obj:`False` otherwise.

        .. note::

            Subclasses may override this method.

        """
        if isinstance(other, self.__class__):
            return self.naked() is other.naked()
        return NotImplemented

    def __ne__(self, other: Any) -> bool:
        """Check for inequality with another object.

        :param other: The object to compare with.
        :return: :obj:`True` if the objects are unequal, :obj:`False` otherwise.

        .. note::

            Subclasses must not override this method.

        """
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal

    # ----
    # Hash
    # ----

    def __hash__(self) -> int:
        """Return the hash value for the object.

        This allows subclasses to be used in hashable collections such as sets
        and dictionaries.

        :return: The hash value for the object as an :class:`int`.

        .. note::

            Subclasses may override this method.

        """
        return id(self.naked())

    # ----
    # Copy
    # ----

    copyClass: Optional[Type[Any]] = None
    copyAttributes: Tuple[str, ...] = ()

    def copy(self: BaseObjectType) -> BaseObjectType:
        """Copy the current object into a new object of the same type.

        The returned object will not have a parent object.

        :return: A new :class:`BaseObject` subclass instance with the same attributes.

        """
        copyClass = self.copyClass
        if copyClass is None:
            copyClass = self.__class__
        copied = copyClass()
        copied.copyData(self)
        return copied

    def copyData(self, source: BaseObjectType) -> None:
        """Copy data from `source` into the current object.

        .. note::

            Subclasses may override this method.
            If so, they should call the :class:`super`.

        """
        for attr in self.copyAttributes:
            selfValue = getattr(self, attr)
            sourceValue = getattr(source, attr)
            if isinstance(selfValue, BaseObject):
                selfValue.copyData(sourceValue)
            else:
                setattr(self, attr, deepcopy(sourceValue))

    # ----------
    # Exceptions
    # ----------

    def raiseNotImplementedError(self) -> NoReturn:
        """Raise a :class:`NotImplementedError`.

        This exception needs to be raised frequently by the :mod:`fontParts.base`
        classes, so, it's here for convenience.

        :raises NotImplementedError: Whenever this method is called.

        """
        raise NotImplementedError(
            f"The {self.__class__.__name__} subclass does not implement this method."
        )

    # ---------------------
    # Environment Fallbacks
    # ---------------------

    def changed(self, *args: Any, **kwargs: Any) -> None:
        r"""Tell the environment that something has changed in the object.

        The behavior of this method will vary from environment to environment.

        :param \*args: Any positional arguments.
        :param \**kwargs: Any keyword arguments.

        Example::

            >>> obj.changed()

        """

    def naked(self) -> Any:
        """Return the environment's native object wrapped by the current object.

        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        Example::

            >>> loweLevelObj = obj.naked()

        """
        self.raiseNotImplementedError()


class BaseItems(Generic[KeyType, ValueType]):
    """Provide the given mapping with an items view object.

    This class provides a view of the key-value pairs in a mapping, similar to
    the behavior of Python's :meth:`dict.items` method. The view dynamically
    reflects any changes made to the parent mapping object, ensuring it remains
    up-to-date.

    The normalization method :meth:`_normalizeItems` must be defined by the
    parent `mapping` class.

    :param mapping: The parent :class:`BaseDict` instance whose items are
        represented by this view.

    """

    def __init__(self, mapping: BaseDict[KeyType, ValueType]) -> None:
        self._mapping = mapping

    def __contains__(self, item: Tuple[KeyType, ValueType]) -> bool:
        """Check if a key-value pair exists in the mapping.

        :param item: The key-value pair to check for existence as a :class:`tuple`.
        :return: :obj:`True` if the key-value pair exists, :obj:`False` otherwise.

        """
        key, value = item
        normalizedItem = (
            self._mapping._normalizeKey(key),
            self._mapping._normalizeValue(value),
        )
        return normalizedItem in self._mapping._normalizeItems()

    def __iter__(self) -> Iterator[Tuple[KeyType, ValueType]]:
        """Return an iterator over the key-value pairs in the mapping.

        This method yields each item one by one, removing it from the list of
        keys after it is yielded.

        :returns: An iterator over the mapping's key-value pairs.

        """
        return iter(self._mapping._normalizeItems())

    def __len__(self) -> int:
        """Return the number of keys-value pairs in the mapping.

        :return: An :class:`int` representing the number of mapping items.

        """
        return len(self._mapping._normalizeItems())

    def __repr__(self) -> str:
        """Return a string representation of the items view.

        :return: A representation of the keys view as a :class:`str`.

        """
        return f"{self._mapping.__class__.__name__}_items({list(self)})"


class BaseKeys(Generic[KeyType]):
    """Provide the given mapping with a keys view object.

    This class provides a view of the keys in a mapping, similar to the behavior
    of Python's :meth:`dict.keys` method. The view dynamically reflects any
    changes made to the parent mapping object, ensuring it remains up-to-date.

    The normalization method :meth:`_normalizeItems` must be defined by the
    parent `mapping` class.

    :param mapping: The parent :class:`BaseDict` instance whose keys are
        represented by this view.

    """

    def __init__(self, mapping: BaseDict[KeyType, Any]) -> None:
        self._mapping = mapping

    def __contains__(self, key: KeyType) -> bool:
        """Check if a key exists in the mapping.

        :param key: The key to check for existence.
        :return: :obj:`True` if the key exists, :obj:`False` otherwise.

        """
        return any(k == key for k, _ in self._mapping._normalizeItems())

    def __iter__(self) -> Iterator[KeyType]:
        """Return an iterator over the keys in the mapping.

        This method yields each key one by one, removing it from the list of
        keys after it is yielded.

        :returns: An iterator over the mapping's keys.

        """
        return (k for k, _ in self._mapping._normalizeItems())

    def __len__(self) -> int:
        """Return the number of keys in the mapping.

        :return: An :class:`int` representing the number of mapping keys.

        """
        return len(self._mapping._normalizeItems())

    def __repr__(self) -> str:
        """Return a string representation of the keys view.

        :return: A representation of the keys view as a :class:`str`.

        """
        return f"{self._mapping.__class__.__name__}_keys({list(self)})"

    def isdisjoint(self, other: Iterable[KeyType]) -> bool:
        """Check if the keys view has no common elements with another iterable.

        :param other: The iterable to compare against.
        :return: :obj:`True` if there are no common elements, :obj:`False` otherwise.

        """
        return set(self).isdisjoint(other)


class BaseValues(Generic[ValueType]):
    """Provide the given mapping with a values view object.

    This class provides a view of the values in a mapping, similar to the behavior
    of Python's :meth:`dict.values` method. The view dynamically reflects any
    changes made to the parent mapping object, ensuring it remains up-to-date.

    The normalization method :meth:`_normalizeItems` must be defined by the
    parent `mapping` class.

    :param mapping: The parent :class:`BaseDict` instance whose keys are
        represented by this view.

    """

    def __init__(self, mapping: BaseDict[Any, ValueType]) -> None:
        self._mapping = mapping

    def __contains__(self, value: ValueType) -> bool:
        """Check if a value exists in the mapping.

        :param value: The value to check for existence.
        :return: :obj:`True` if the value exists, :obj:`False` otherwise.

        """
        return any(v == value for _, v in self._mapping._normalizeItems())

    def __iter__(self) -> Iterator[ValueType]:
        """Return an iterator over the values in the mapping.

        This method yields each value one by one, removing it from the list of
        values after it is yielded.

        :returns: An iterator over the mapping's values.

        """
        return (v for _, v in self._mapping._normalizeItems())

    def __len__(self) -> int:
        """Return the number of values in the mapping.

        :return: An :class:`int` representing the number of mapping values.

        """
        return len(self._mapping._normalizeItems())

    def __repr__(self) -> str:
        """Return a string representation of the values view.

        :return: A representation of the values view as a :class:`str`.

        """
        return f"{self._mapping.__class__.__name__}_values({list(self)})"


class BaseDict(BaseObject, Generic[KeyType, ValueType]):
    """Provide objects with basic dictionary-like functionality.

    :cvar keyNormalizer: An optional normalizer function for keys.
    :cvar valueNormalizer: An optional normalizer function for values.

    """

    keyNormalizer: Optional[Callable[[KeyType], KeyType]] = None
    valueNormalizer: Optional[Callable[[ValueType], ValueType]] = None

    def _normalizeKey(self, key: KeyType) -> KeyType:
        keyNormalizer = type(self).keyNormalizer
        return keyNormalizer(key) if keyNormalizer is not None else key

    def _normalizeValue(self, value: ValueType) -> ValueType:
        valueNormalizer = type(self).valueNormalizer
        return valueNormalizer(value) if valueNormalizer is not None else value

    def _normalizeItems(self) -> List[Tuple[KeyType, ValueType]]:
        items = self._items()
        return [(self._normalizeKey(k), self._normalizeValue(v)) for (k, v) in items]

    def copyData(self, source: BaseObjectType) -> None:
        """Copy data from another object instance.

        This method calls the superclass's :meth:`copyData` method and updates
        the current :class:`BaseDict` instance with the contents of the `source`,
        provided it qualifies as a :class:`MutableMapping`.

        param source: The source :class:`BaseObject` instance from which
            to copy data.

        """
        super(BaseDict, self).copyData(source)
        if isinstance(source, MutableMapping):
            self.update(source)

    def __len__(self) -> int:
        """Return the number of items in the object.

        :return: An :class:`int` representing the number of dictionary items.

        """
        value = self._len()
        return value

    def _len(self) -> int:
        """Return the number of items in the native object.

        This is the environment implementation of :attr:`BaseDict.__len__`.

        :return: An :class:`int` representing the number of dictionary items.

        .. note::

            Subclasses may override this method.

        """
        return len(self.keys())

    def keys(self) -> BaseKeys[KeyType]:
        """Return a view of the keys in the object.

        :return: A :class:`BaseKeys` object instance of :class:`str` items.

        """
        return self._keys()

    def _keys(self) -> BaseKeys[KeyType]:
        """Return a view of the keys in the native object.

        This is the environment implementation of :meth:`BaseDict.keys`.

        :return: A :class:`BaseKeys` object instance of :class:`str` items. If
            a :cvar:`BaseDict.keyNormalizer` is set, it will be applied to each
            key in the returned view.

        .. note::

            Subclasses may override this method.

        """
        return BaseKeys(self)

    def items(self) -> BaseItems:
        """Return a view of the key-value pairs in the object.

        :return: A :class:`BaseItems` object instance.

        """
        return BaseItems(self)

    def _items(self) -> ItemsView[KeyType, ValueType]:
        """Return a view of the key-value pairs in the native object.

        This is the environment implementation of :meth:`BaseDict.items`.

        :return: A :class:`ItemsView` object instance.
            If both :cvar:`BaseDict.keyNormalizer` and :cvar:`BaseDict.valueNormalizer`
            are set, they will be applied to each key and value in the returned object.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def values(self) -> BaseValues[ValueType]:
        """Return a view of the values in the object.

        :return: A :class:`BaseValues` object instance.

        """
        return self._values()

    def _values(self) -> BaseValues[ValueType]:
        """Return a view of the values in the native object.

        This is the environment implementation of :meth:`BaseDict.values`.

        :return: A :class:`BaseValues` object instance. If
            a :cvar:`BaseDict.valueNormalizer` is set, it will be applied to each
            value in the returned view.

        .. note::

            Subclasses may override this method.

        """
        return BaseValues(self)

    def __contains__(self, key: KeyType) -> bool:
        """Check if a key is in the object.

        :param key: The key to check for.
        :return: :obj:`True` if the key is present, :obj:`False` otherwise.

        """
        key = self._normalizeKey(key)
        return self._contains(key)

    def _contains(self, key: KeyType) -> bool:
        """Check if a key is in the native object.

        This is the environment implementation of :meth:`BaseDict.__contains__`.

        :param key: The key to check for. If a :cvar:`BaseDict.keyNormalizer`
            is set, it will have been applied to the key before checking.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    has_key = __contains__

    def __setitem__(self, key: KeyType, value: ValueType) -> None:
        """Set the value for a given key in the object.

        :param key: The key to set.
        :param value: The value to set for the given key.

        """
        key = self._normalizeKey(key)
        value = self._normalizeValue(value)
        self._setItem(key, value)

    def _setItem(self, key: KeyType, value: ValueType) -> None:
        """Set the value for a given key in the native object.

        This is the environment implementation of :meth:`BaseDict.__setitem__`.

        :param key: The key to set. If a :cvar:`BaseDict.keyNormalizer`
            is set, it will have been applied to the value in the calling method.
        :param value: The value to set for the given key. If
            a :cvar:`BaseDict.valueNormalizer` is set, it will have been applied
            to the value in the calling method .
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def __getitem__(self, key: KeyType) -> ValueType:
        """Get the value for a given key from the object.

        :param key: The key to retrieve the value for.
        :return: The value for the given key.

        """
        key = self._normalizeKey(key)
        value = self._getItem(key)
        return self._normalizeValue(value)

    def _getItem(self, key: KeyType) -> ValueType:
        """Get the value for a given key from the native object.

        This is the environment implementation of :meth:`BaseDict.__getitem__`.

        :param key: The key to retrieve the value for. If
            a :cvar:`BaseDict.keyNormalizer` is set, it will have been applied to
            the key in the calling method.
        :return: The value for the given key. If
            a :cvar:`BaseDict.valueNormalizer` is set, it will be applied in the
            calling method to the returned value.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def get(
        self, key: KeyType, default: Optional[ValueType] = None
    ) -> Optional[ValueType]:
        """Get the value for a given key in the object.

        If the given key is not found, The specified `default` will be returned.

        :param key: The key to look up.
        :param default: The default value to return if the key is not found.
            Defaults to :obj:`None`.
        :return: The value for the given key, or the default value if the key is
            not found.

        """
        key = self._normalizeKey(key)
        default = self._normalizeValue(default) if default is not None else default
        value = self._get(key, default=default)
        if value is not None and value is not default:
            value = self._normalizeValue(value)
        return value

    def _get(self, key: KeyType, default: Optional[ValueType]) -> Optional[ValueType]:
        """Get the value for a given key in the native object.

        This is the environment implementation of :meth:`BaseDict.get`.

        :param key: The key to look up. If a :cvar:`BaseDict.keyNormalizer` is
            set, it will have been applied to the given key.
        :param default: The default value to return if the key is not found.
        :return: The value associated with the given key, or the default value
            if the key is not found. If a :cvar:`BaseDict.valueNormalizer` is set,
            it will be applied in the calling method to the returned value.

        .. note::

            Subclasses may override this method.

        """
        if key in self:
            return self[key]
        return default

    def __delitem__(self, key: KeyType) -> None:
        """Delete a key-value pair from the object.

        :param key: The key to delete.

        """
        key = self._normalizeKey(key)
        self._delItem(key)

    def _delItem(self, key: KeyType) -> None:
        """Delete a key-value pair from the native object.

        This is the environment implementation of :meth:`BaseDict.__delitem__`.

        :param key: The key to delete. If a :cvar:`BaseDict.keyNormalizer` is
            set, it will have been applied to the given key.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def pop(
        self, key: KeyType, default: Optional[ValueType] = None
    ) -> Optional[ValueType]:
        """Remove a key from the object and return it's value.

        If the given key is not found, The specified `default` will be returned.

        :param key: The key to remove.
        :param default: The optional default value to return if the key is not found.
            Defaults to :obj:`None`.
        :return: The value associated with the given key, or the default value
            if the key is not found.

        """
        key = self._normalizeKey(key)
        if default is not None:
            default = self._normalizeValue(default)
        value = self._pop(key, default=default)
        if value is not None:
            value = self._normalizeValue(value)
        return value

    def _pop(self, key: KeyType, default: Optional[ValueType]) -> Optional[ValueType]:
        """Remove a key from the native object and return it's value.

        This is the environment implementation of :meth:`BaseDict.pop`.

        :param key: The key to remove. If a :cvar:`BaseDict.keyNormalizer` is
            set, it will have been applied to the given key.
        :param default: The default value to return if the key is not found.
        :return: The value associated with the given key, or the default value
            if the key is not found. If a :cvar:`BaseDict.valueNormalizer` is set,
            it will be applied in the calling method to the returned value.

        .. note::

            Subclasses may override this method.

        """
        value = default
        if key in self:
            value = self[key]
            del self[key]
        return value

    def __iter__(self) -> Iterator[KeyType]:
        """Return an iterator over the keys of the object.

        This method yields each key one by one, removing it from the list of
        keys after it is yielded.

        :returns: An iterator over the object's keys.

        """
        return self._iter()

    def _iter(self) -> Iterator[KeyType]:
        """Return an iterator over the keys of the native object.

        This is the environment implementation of :meth:`BaseDict.__iter__`.

        :returns: An iterator over the object's keys.

        .. note::

            Subclasses may override this method.

        """
        for key in self.keys():
            yield key

    def update(self, other: MutableMapping[KeyType, ValueType]) -> None:
        """Update the current object instance with key-value pairs from another.

        :param other: A :class:`MutableMapping` of key-value pairs to update
            this dictionary with.

        """
        otherCopy = deepcopy(other)
        d = {}
        for key, value in otherCopy.items():
            key = self._normalizeKey(key)
            value = self._normalizeValue(value)
            d[key] = value
        otherCopy = d
        self._update(otherCopy)

    def _update(self, other: MutableMapping[KeyType, ValueType]) -> None:
        """Update the current native object instance with key-value pairs from another.

        This is the environment implementation of :meth:`BaseDict.update`.

        :param other: A :class:`MutableMapping` of key-value pairs to update
            this dictionary with. If both :cvar:`BaseDict.keyNormalizer`
            and :cvar:`BaseDict.valueNormalizer` are set, they will have been
            applied to the keys and values, respectively.

        .. note::

            Subclasses may override this method.

        """
        for key, value in other.items():
            self[key] = value

    def clear(self) -> None:
        """Remove all items from the object."""
        self._clear()

    def _clear(self) -> None:
        """Remove all items from the native object.

        This is the environment implementation of :meth:`BaseDict.clear`.

        .. note::

            Subclasses may override this method.

        """
        for key in self.keys():
            del self[key]


class TransformationMixin(ABC):
    """Provide objects transformation-related functionality."""

    # ---------------
    # Transformations
    # ---------------

    def transformBy(
        self,
        matrix: SextupleCollectionType[IntFloatType],
        origin: Optional[PairCollectionType[IntFloatType]] = None,
    ) -> None:
        """Transform the object according to the given matrix.

        :param matrix: The :ref:`type-transformation` to apply.
        :param origin: The optional point at which the transformation
            should originate as a:ref:`type-coordinate`. Defaults to :obj:`None`,
            representing an origin of ``(0, 0)``.

        Example::

            >>> obj.transformBy((0.5, 0, 0, 2.0, 10, 0))
            >>> obj.transformBy((0.5, 0, 0, 2.0, 10, 0), origin=(500, 500))

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

    def _transformBy(
        self, matrix: SextupleCollectionType[IntFloatType], **kwargs: Any
    ) -> None:
        r"""Transform the native object according to the given matrix.

        This is the environment implementation of :meth:`TransformationMixin.transformBy`.

        :param matrix: The :ref:`type-transformation` to apply. The value will
            have been normalized with
            :func:`normalizers.normalizeTransformationMatrix`.
        :param \**kwargs: Additional keyword arguments.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def moveBy(self, value: PairCollectionType[IntFloatType]) -> None:
        """Move the object according to the given coordinates.

        :param value: The x and y values to move the object by as
            a :ref:`type-coordinate`.

        Example::

            >>> obj.moveBy((10, 0))

        """
        value = normalizers.normalizeTransformationOffset(value)
        self._moveBy(value)

    def _moveBy(self, value: PairType[IntFloatType], **kwargs: Any) -> None:
        r"""Move the native object according to the given coordinates.

        This is the environment implementation of :meth:`BaseObject.moveBy`.

        :param value: The x and y values to move the object by as
            a :ref:`type-coordinate`. The value will have been normalized with
            :func:`normalizers.normalizeTransformationOffset`.
        :param \**kwargs: Additional keyword arguments.

        .. note::

            Subclasses may override this method.

        """
        x, y = value
        t = transform.Offset(x, y)
        self.transformBy(tuple(t), **kwargs)

    def scaleBy(
        self,
        value: TransformationType,
        origin: Optional[PairCollectionType[IntFloatType]] = None,
    ) -> None:
        """Scale the object according to the given values.

        :param value: The value to scale the glyph by as a single :class:`int`
            or :class:`float`, or a :class:`tuple` or :class:`list` of
            two :class:`int` or :class:`float` values representing the values
            ``(x, y)``.
        :param origin: The optional point at which the scale should originate as
            a :ref:`type-coordinate`. Defaults to :obj:`None`, representing an
            origin of ``(0, 0)``.

        Example::

            >>> obj.scaleBy(2.0)
            >>> obj.scaleBy((0.5, 2.0), origin=(500, 500))

        """
        value = normalizers.normalizeTransformationScale(value)
        if origin is None:
            origin = (0, 0)
        origin = normalizers.normalizeCoordinateTuple(origin)
        self._scaleBy(value, origin=origin)

    def _scaleBy(
        self, value: PairType[float], origin: PairType[IntFloatType], **kwargs: Any
    ) -> None:
        r"""Scale the native object according to the given values.

        This is the environment implementation of :meth:`BaseObject.scaleBy`.

        :param value: The value to scale the glyph by as a single :class:`int`
            or :class:`float`, or a :class:`tuple` or :class:`list` of
            two :class:`int` or :class:`float` values representing the values
            ``(x, y)``. The value will have been normalized
            with :func:`normalizeTransformationScale`.
        :param origin: The point at which the scale should originate as
            a :ref:`type-coordinate` or :obj:`None`. The value will have been
            normalized with :func:`normalizers.normalizeCoordinateTuple`.
        :param \**kwargs: Additional keyword arguments.

        .. note::

            Subclasses may override this method.

        """
        x, y = value
        t = transform.Identity.scale(x=x, y=y)
        self.transformBy(tuple(t), origin=origin, **kwargs)

    def rotateBy(
        self,
        value: IntFloatType,
        origin: Optional[PairCollectionType[IntFloatType]] = None,
    ) -> None:
        """Rotate the object by the specified value.

        :param value: The angle at which to rotate the object as an :class:`int`
            or a :class:`float`.
        :param origin: The optional point at which the rotation should originate
            as a :ref:`type-coordinate`. Defaults to :obj:`None`, representing an
            origin of ``(0, 0)``.

        Example::

            >>> obj.rotateBy(45)
            >>> obj.rotateBy(45, origin=(500, 500))

        """
        value = normalizers.normalizeRotationAngle(value)
        if origin is None:
            origin = (0, 0)
        origin = normalizers.normalizeCoordinateTuple(origin)
        self._rotateBy(value, origin=origin)

    def _rotateBy(
        self, value: float, origin: PairType[IntFloatType], **kwargs: Any
    ) -> None:
        r"""Rotate the native object by the specified value.

        This is the environment implementation of :meth:`TransformationMixin.rotateBy`.

        :param value: The angle at which to rotate the object as an :class:`int`
            or a :class:`float`. The value will have been normalized with
            :func:`normalizers.normalizeRotationAngle`.
        :param origin: The point at which the rotation should originate as
            a :ref:`type-coordinate` or :obj:`None`. The value will have been
            normalized with :func:`normalizers.normalizeCoordinateTuple`.
        :param \**kwargs: Additional keyword arguments.

        .. note::

            Subclasses may override this method.

        """
        a = math.radians(value)
        t = transform.Identity.rotate(a)
        self.transformBy(tuple(t), origin=origin, **kwargs)

    def skewBy(
        self,
        value: TransformationType,
        origin: Optional[PairCollectionType[IntFloatType]] = None,
    ) -> None:
        """Skew the object by the given value.

        :param value: The value by which to skew the object as either a
            single :class:`int` or :class:`float` corresponding to the x
            direction, or a :class:`tuple` of two :class:`int` or :class:`float`
            values corresponding to the x and y directions.
        :param origin: The optional point at which the rotation should originate
            as a :ref:`type-coordinate`. Defaults to :obj:`None`, representing an
            origin of ``(0, 0)``.

        Example::

            >>> obj.skewBy(11)
            >>> obj.skewBy((25, 10), origin=(500, 500))

        """
        value = normalizers.normalizeTransformationSkewAngle(value)
        if origin is None:
            origin = (0, 0)
        origin = normalizers.normalizeCoordinateTuple(origin)
        self._skewBy(value, origin=origin)

    def _skewBy(
        self, value: PairType[float], origin: PairType[IntFloatType], **kwargs: Any
    ) -> None:
        r"""Skew the native object by the given value.

        This is the environment implementation of :meth:`TransformationMixin.skewBy`.

        :param value: The value by which to skew the object as either a
            single :class:`int` or :class:`float` corresponding to the x
            direction, or a :class:`tuple` of two :class:`int` or :class:`float`
            values corresponding to the x and y directions. The value will have
            been normalized with :func:`normalizers.normalizeTransformationSkewAngle`.
        :param origin: The point at which the rotation should originate
            as a :ref:`type-coordinate` or :obj:`None`. The value will have been
            normalized with :func:`normalizers.normalizeCoordinateTuple`.
        :param \**kwargs: Additional keyword arguments.

        .. note::

            Subclasses may override this method.

        """
        x, y = value
        x = math.radians(x)
        y = math.radians(y)
        t = transform.Identity.skew(x=x, y=y)
        self.transformBy(tuple(t), origin=origin, **kwargs)

    # ----------------
    # Abstract members
    # ----------------

    @abstractmethod
    def raiseNotImplementedError(self):
        pass


class InterpolationMixin(ABC):
    """Provide objects with interpolation-related functionality.

    :cvar compatibilityReporterClass:  A class used for reporting interpolation
        compatibility between two objects. If :obj:`None`, compatibility
        reporting is not enabled.

    """

    # -------------
    # Compatibility
    # -------------

    compatibilityReporterClass: Optional[Type[Any]] = None

    def isCompatible(self, other: Any, cls: Type[Any]) -> Tuple[bool, Any]:
        """Evaluate interpolation compatibility with another object.

        :param other: The other object instance to check compatibility with.
        :param cls: The class type to check the `other` object against.
        :return: A :class:`tuple` where the first element is a :class:`bool`
            indicating whether the objects are compatible, and the second
            element is the compatibility reporter instance.
        :raises TypeError: If `other` is not an instance of `cls`.

        """
        if not isinstance(other, cls):
            raise TypeError(
                f"""Compatibility between an instance of {cls.__name__!r}
                and an instance of {other.__class__.__name__!r} can not be checked."""
            )
        if self.compatibilityReporterClass is None:
            raise ValueError("The compatibility reporter class cannot be None.")
        reporter = self.compatibilityReporterClass(self, other)
        self._isCompatible(other, reporter)
        return not reporter.fatal, reporter

    def _isCompatible(self, other: Any, reporter: Any) -> None:
        """Evaluate interpolation compatibility with another native object.

        This is the environment implementation of :meth:`InterpolationMixin.isCompatible`.

        :param other: The other object instance to check compatibility with.
        :param reporter: An object used to report compatibility issues.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    # ----------------
    # Abstract members
    # ----------------

    @abstractmethod
    def raiseNotImplementedError(self):
        pass


class SelectionMixin(ABC):
    """Provide objects with selection-related functionality."""

    # -------------
    # Selected Flag
    # -------------

    selected: dynamicProperty = dynamicProperty(
        "base_selected",
        """Get or set the object's selection state.

        The value must be a :class:`bool` indicating whether the object is
        selected or not.

        :return: :obj:`True` if the object is selected, :obj:`False` otherwise.

        Example::

            >>> obj.selected
            False
            >>> obj.selected = True

        """,
    )

    def _get_base_selected(self) -> bool:
        value = self._get_selected()
        value = normalizers.normalizeBoolean(value)
        return value

    def _set_base_selected(self, value: bool) -> None:
        value = normalizers.normalizeBoolean(value)
        self._set_selected(value)

    def _get_selected(self) -> bool:  # type: ignore[return]
        """Get or the object's selection state.

        This is the environment implementation
        of :attr:`BaseObject.selected` property getter.

        :return: :obj:`True` if the object is selected, :obj:`False` otherwise.
            The value will be normalized with :func:`normalizers.normalizeBoolean`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method if they implement object selection.

        """
        self.raiseNotImplementedError()

    def _set_selected(self, value: bool) -> None:
        """Set the object's selection state.

        This is the environment implementation of the
        :attr:`SelectionMixin.selected` property setter.

        :param value: Whether the object is selected. The value will have been
            normalized with :func:`normalizers.normalizeBoolean`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method if they implement object selection.

        """
        self.raiseNotImplementedError()

    # -----------
    # Sub-Objects
    # -----------
    @classmethod
    def _getSelectedSubObjects(cls, subObjects: Any) -> Tuple[Any]:
        selected = tuple(obj for obj in subObjects if obj.selected)
        return selected

    @classmethod
    def _setSelectedSubObjects(cls, subObjects: Any, selected: Any) -> None:
        for obj in subObjects:
            obj.selected = obj in selected

    # ----------------
    # Abstract members
    # ----------------

    @abstractmethod
    def raiseNotImplementedError(self):
        pass


class PointPositionMixin(ABC):
    """Provide objects with the ability to determine point position.

    This class adds a `position` attribute as a :class:`dyanmicProperty`, for
    use as a mixin with objects that have `x` and `y` attributes.

    """

    position: dynamicProperty = dynamicProperty(
        "base_position",
        """Get or set the point position of the object.

        The value must be a :ref:`type-coordinate`.

        :return: The current point position as a :ref:`type-coordinate`.

        """,
    )

    def _get_base_position(self) -> PairType[IntFloatType]:
        value = self._get_position()
        value = normalizers.normalizeCoordinateTuple(value)
        return value

    def _set_base_position(self, value: PairCollectionType[IntFloatType]) -> None:
        value = normalizers.normalizeCoordinateTuple(value)
        self._set_position(value)

    def _get_position(self) -> PairType[IntFloatType]:
        """Get the point position of the object.

        This is the environment implementation of
        the :attr:`PointPositionMixin.position` property getter.

        :return: The current point position as a :ref:`type-coordinate`.
            The value will be normalized
            with :func:`normalizers.normalizeCoordinateTuple`.

        .. note::

            Subclasses may override this method.

        """
        return (self.x, self.y)

    def _set_position(self, value: PairCollectionType[IntFloatType]) -> None:
        """Set the point position of the object.

        This is the environment implementation of
        the :attr:`PointPositionMixin.position` property setter.

        :param value: The point position to set as a :ref:`type-coordinate`.
            The value will have been normalized
            with :func:`normalizers.normalizeCoordinateTuple`.

        .. note::

            Subclasses may override this method.

        """
        pX, pY = self.position
        x, y = value
        dX = x - pX
        dY = y - pY
        self.moveBy((dX, dY))

    # ----------------
    # Abstract members
    # ----------------

    x: dynamicProperty = dynamicProperty("base_x")

    @abstractmethod
    def _get_base_x(self) -> IntFloatType:
        pass

    @abstractmethod
    def _set_base_x(self, value: IntFloatType) -> None:
        pass

    @abstractmethod
    def _get_x(self) -> IntFloatType:
        pass

    @abstractmethod
    def _set_x(self, value: IntFloatType) -> None:
        pass

    y: dynamicProperty = dynamicProperty("base_y")

    @abstractmethod
    def _get_base_y(self) -> IntFloatType:
        pass

    @abstractmethod
    def _set_base_y(self, value: IntFloatType) -> None:
        pass

    @abstractmethod
    def _get_y(self) -> IntFloatType:
        pass

    @abstractmethod
    def _set_y(self, value: IntFloatType) -> None:
        pass

    @abstractmethod
    def moveBy(self, value):
        pass

    @abstractmethod
    def raiseNotImplementedError(self):
        pass


class IdentifierMixin(ABC):
    """Provide objects with a unique identifier."""

    # identifier

    identifier: dynamicProperty = dynamicProperty(
        "base_identifier",
        """Get the object's unique identifier.

        This attribute is read-only. Use :meth:`IdentifierMixin.getIdentifier`
        to request an identifier if it does not exist.

        :return: The unique identifier assigned to the object as a :class:`str`,
            or :obj:`None` indicating the object has no identifier.

        Example ::

            >>> object.identifier
            'ILHGJlygfds'

        """,
    )

    def _get_base_identifier(self) -> Optional[str]:
        value = self._get_identifier()
        if value is not None:
            value = normalizers.normalizeIdentifier(value)
        return value

    def _get_identifier(self) -> Optional[str]:  # type: ignore[return]
        """Get the native object's unique identifier.

        This is the environment implementation of :attr:`IdentifierMixin.identifier`.

        If the native object does not have an identifier assigned, one may be
        assigned with :meth:`IdentifierMixin.getIdentifier`

        :return: The unique identifier assigned to the object as a :class:`str`,
            or :obj:`None` indicating the object has no identifier.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def getIdentifier(self) -> str:
        """Generate and assign a unique identifier to the object.

        If the object already has an identifier, the existing one should
        be returned.

        :return: A unique object identifier as a :class:`str`.

        """
        return self._getIdentifier()

    def _getIdentifier(self) -> str:  # type: ignore[return]
        """Generate and assign a unique identifier to the native object.

        This is the environment implementation of :meth:`IdentifierMixin.getIdentifier`.

        :return: A unique object identifier as a :class:`str`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _setIdentifier(self, value: str) -> None:
        """Force a specific identifier onto an object.

        This method is used internally to force a specific identifier onto an
        object in certain situations.

        :param value: The identifier to set as a :class:`str` or :obj:`None`.

        .. note::

            Subclasses that allow setting an identifer may override this method.

        """
        pass

    # ----------------
    # Abstract members
    # ----------------

    @abstractmethod
    def raiseNotImplementedError(self):
        pass


def reference(obj: Any) -> Callable[[], Any]:
    """
    This code returns a simple function that returns the given object.
    This is a backwards compatibility function that is under review (see issue #749).
    We used to use weak references, but they proved problematic (see issue #71),
    so this function was put in place to make sure existing code continued to
    function. The need for it is questionable, so it may be deleted soon.
    """

    def wrapper() -> Any:
        return obj

    return wrapper


class FuzzyNumber:
    """Represent a number like object with a threshold.

    This class should be used to compare numbers where a threshold is needed.

    """

    def __init__(self, value: IntFloatType, threshold: IntFloatType) -> None:
        self.value = value
        self.threshold = threshold

    def __repr__(self) -> str:
        return f"[{self.value:f} {self.threshold:f}]"

    def __lt__(self, other: Union[FuzzyNumber, IntFloatType]) -> bool:
        if hasattr(other, "value"):
            if abs(self.value - other.value) < self.threshold:
                return False
            else:
                return self.value < other.value
        return self.value < other

    def __eq__(self, other: object) -> bool:
        if hasattr(other, "value"):
            return abs(self.value - other.value) < self.threshold
        return self.value == other

    def __hash__(self) -> int:
        return hash((self.value, self.threshold))
