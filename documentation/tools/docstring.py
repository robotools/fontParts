# pylint: disable=R0904, R0913, C0103, C0114, C0415
"""Docstring generation module for FontParts.

This module provides tools for generating docstrings formatted according to
the :ref:`style-guide`, which can then be inserted into object source code.

Classes
    - :class:`Docstring`: A class representation of a docstring, split into
      various sections.
    - :class:`DynamicPropertyMixin`: A mixin to
      handle :class:`base.dynamicProperty` objects specifically.
    - :class:`CodeAnalyzer`: An :class:`ast.NodeVisitor` subclass that analyzes
      source code to locate specific object references.

Functions
    - :func:`generateDocstring`: Creates instances of the classes in this module
      to generate a docstring formatted for a given object.
    - :func:`insertDocstring`: Inserts the generated docstring into the source
      code of an object.

Customization
    This module allows for the following customizations:

    - Variadic argument preservation: Includes or excludes the asterisk symbol
      `*args` and `**kwargs` in generated docstrings.
    - Indentation level and line length: Controls the indentation and maximum
      line length in generated docstrings.

Example
    To create a docstring for a method in a certain class::

        >>> docstring = generateDocstring(
        ...     someMethod,
        ...     globalNamespace=globals(),
        ...     containingClass=SomeClass
        ... )

    To generate new source code for the method including the new docstring::

        >>> insertDocstring(someMethod, docstring)

.. note::

    Generating docstrings for dynamic base properties is not supported. The
    contents of :meth:`dynamicProperty.doc` is however used as a basis for
    creating any docstrings for derived native environment getter and setter
    methods.

"""

from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    get_type_hints,
    get_origin,
    get_args,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Union
)

from abc import ABC, abstractmethod
import ast
import inspect
import logging
import re
import textwrap

if TYPE_CHECKING:
    from fontParts.base.base import dynamicProperty

OptionalCallable = Optional[Callable]
GetterSetterType = Tuple[OptionalCallable, OptionalCallable]
ParsedAnnotation = Union[str, Tuple[str, List[Any]]]

NORMALIZATION_MODULE = 'normalizers'
DEPRECATION_ID = 'This method is deprecated.'
INDENT = ' ' * 4
LINE_LENGTH = 72

FORMAT_STRINGS: Dict[str, str] = {
    'implementationNote': (
        "This is the environment implementation of {baseObject}."
    ),
    'getterImplementationNote': (
        "This is the environment implementation of the {baseObject} property getter."
    ),
    'setterImplementationNote': (
        "This is the environment implementation of the {baseObject} property setter."
    ),
    'deprecated': (
        "This method is deprecated. Use {replacement} instead."
    ),
    'mayOverride': (
        "Subclasses may override this method."
    ),
    'mustOverride': (
        "Subclasses must override this method."
    ),
    'parameter': (
        ":param {parameterName}: Description of {typeString}."
    ),
    'normalizer': (
        " The value will have been normalized with :func:`{normalizer}`."
    ),
    'default': (
        " Defaults to {value}."
    ),
    'raises': (
        ":raises {exception}: If {condition}."
    ),
    'exception': (
        "description"
    ),
    'notImplementedError': (
        "the method has not been overridden by a subclass"
    ),
    'return': (
        ":return: {typeString}."
    ),
    'setterValue': (
        "The value must be {typeString}."
    ),
}


ROLE_PREFIXES: Dict[str, str] = {
    'function': ':func:',
    'method': ':meth:',
    'property': ':attr:',
    'attribute': ':attr:',
    'NoneType': ':obj:',
    'None': ':obj:',
    'True': ':obj:',
    'False': ':obj:',
    'list': ':class:',
    'tuple': ':class:',
    'dict': ':class:`',
    'int': ':class:',
    'float': ':class:',
    'str': ':class:',
}

DIRECTIVES: Dict[str, str] = {
    'deprecated': '.. deprecated::',
    'note': '.. note::',
    'important': '.. important::',
    'seealso': '.. seealso::',
    'tip': '.. tip::',
    'todo': '.. todo::'
}


class DynamicPropertyMixin(ABC):
    """Provide functionality specific to :class:`base.dynamicProperty` objects.

    This mixin class provides methods for managing dynamic properties,
    such as retrieving getter and setter methods, merging their signatures,
    and combining type hints.

    Subclasses must implement several abstract methods and properties,
    including those for managing the object's type hints, signature information,
    and object name.

    """

    def _getGetterSetter(self) -> GetterSetterType:
        # Retrieve getter and setter functions for the dynamic property.
        if self.containingClass:
            getter = getattr(self.containingClass, self.obj.getterName, None)
            setter = getattr(self.containingClass, self.obj.setterName, None)
            return getter, setter
        return (None, None)

    def _mergeSignatures(self) -> Optional[inspect.Signature]:
        # Merge the signatures of the getter and setter
        if not self.getterObject:
            return None

        getterSignature = inspect.signature(self.getterObject)
        if not self.setterObject:
            return getterSignature

        setterSignature = inspect.signature(self.setterObject)
        params = list(setterSignature.parameters.values())
        returnAnnotation = getterSignature.return_annotation
        return inspect.Signature(parameters=params, return_annotation=returnAnnotation)

    def _mergeTypeHints(self) -> Dict[str, Optional[Any]]:
        """Merge the type hints from the getter and setter."""
        if not self.getterObject:
            return {}

        typeHints = {}
        getterHints = get_type_hints(
            self.getterObject, globalns=self.globalNamespace
        )
        typeHints['value'] = getterHints.get('return', None)
        if self.setterObject:
            setterHints = get_type_hints(
                self.setterObject, globalns=self.globalNamespace
            )
            typeHints['return'] = setterHints.get('value', None)
        return typeHints

    def _formatValue(self, value: Any) -> str:
        """Format a value for inclusion in the docstring."""
        if isinstance(value, str):
            return f"``'{value}'``"
        if isinstance(value, (bool, type(None))):
            return self._assignRole(str(value))
        return f"``{value}``"

    @property
    def dynamicPropertyObject(self) -> Optional[dynamicProperty]:
        """Get the current object's associated dynamicProperty."""
        if self.isGetter or self.isSetter:
            dynamicPropertyName = self.dynamicPropertyQualname.split('.')[1]
            return getattr(self.containingClass, dynamicPropertyName)
        return None

    @property
    def isGetter(self) -> bool:
        """Check if the current object is a getter."""
        return '_get_' in self.objectName

    @property
    def isSetter(self) -> bool:
        """Check if the current object is a setter."""
        return '_set_' in self.objectName

    @property
    def dynamicPropertyQualname(self) -> str:
        """Get the qualified name of the dynamic property."""
        return re.sub(r'_base|_get_|_set_', '', self.objectName)

    @property
    def getterObject(self) -> OptionalCallable:
        """Get the getter function of the dynamic property."""
        return self._getGetterSetter()[0]

    @property
    def setterObject(self) -> OptionalCallable:
        """Get the setter function of the dynamic property."""
        return self._getGetterSetter()[1]

    # ----------------
    # Abstract members
    # ----------------

    @abstractmethod
    def _assignRole(self, objectName: str) -> str:
        """Subclasses must define this method."""

    @abstractmethod
    def _createTypeString(self, key: str) -> str:
        """Subclasses must define this method."""

    @abstractmethod
    def _getSignatureInfo(self) -> Dict[str, Any]:
        """Subclasses must define this method."""

    @property
    @abstractmethod
    def obj(self) -> Any:
        """Subclasses must define this attribute."""

    @property
    @abstractmethod
    def containingClass(self) -> Optional[Any]:
        """Subclasses must define this attribute."""

    @property
    @abstractmethod
    def globalNamespace(self) -> Dict[str, Any]:
        """Subclasses must define this attribute."""

    @property
    @abstractmethod
    def preserveVariadics(self) -> bool:
        """Subclasses must define this attribute."""

    @property
    @abstractmethod
    def objectName(self) -> str:
        """Subclasses must define this attribute."""

    @property
    @abstractmethod
    def publicQualname(self) -> str:
        """Subclasses must define this attribute."""

    @staticmethod
    @abstractmethod
    def _getNormalizers(source: str) -> Dict[str, str]:
        """Subclasses must define this method."""

    # ------------------
    # Docstring Elements
    # ------------------

    @property
    def setterValueDescription(self) -> str:
        """Generate the description string for the setter value."""
        signature = self._mergeSignatures()
        if not signature or not self.setterObject:
            return ''

        for name in signature.parameters:
            if name == 'self':
                continue

            typeString = self._createTypeString(name)
            formatString = FORMAT_STRINGS['setterValue'].format(
                parameterName=name, typeString=typeString
            )

            source = inspect.getsource(self.setterObject)
            normalizerDict = self._getNormalizers(source)
            if normalizerDict and name in normalizerDict:
                normalizer = normalizerDict[name]
                formatString += FORMAT_STRINGS['normalizer'].format(
                    normalizer=normalizer
                )

            defaults = self._getSignatureInfo().get('defaults')
            if defaults and name in defaults:
                value = self._formatValue(defaults[name])
                formatString += FORMAT_STRINGS['default'].format(value=value)

        wrapped = textwrap.fill(formatString, LINE_LENGTH, subsequent_indent=INDENT)
        return wrapped

    @property
    def implementationNote(self) -> str:
        """Generate an implementation note for the dynamic property."""
        if not self.publicQualname:
            return ''

        role = self._assignRole(self.publicQualname)
        if self.isGetter:
            formatString = FORMAT_STRINGS['getterImplementationNote'].format(
                baseObject=role
            )
        elif self.isSetter:
            formatString = FORMAT_STRINGS['setterImplementationNote'].format(
                baseObject=role
            )
        else:
            formatString = FORMAT_STRINGS['implementationNote'].format(
                baseObject=role
            )
        return textwrap.fill(formatString, LINE_LENGTH)


class CodeAnalyzer(ast.NodeVisitor):
    """Analyze source code to retrieve specific elements.

    This class traverses the Abstract Syntax Tree (AST) of the provided source
    code to find:

    - Raised exceptions using :keyword:`raise` statements.
    - Calls to normalization functions from a specified module.
    - Identifies if a return value has passed through a normalization function.

    :param normalizationModule: The name of the module containing normalization
        functions as a :class:`str`. Defaults to :const:`NORMALIZATION_MODULE`.
    :ivar exceptions: A :class:`set` of exception names that are raised within
        the source code.
    :ivar normalizers: A :class:`dict` of argument names mapped to the
        corresponding normalizer function names.

    """

    def __init__(self, normalizationModule: str = 'normalizers'):
        self.exceptions: Set[str] = set()
        self.normalizers: Dict[str, str] = {}
        self.normalizationModule = normalizationModule

    def _extractNormalizer(self, node: ast.Call) -> Optional[str]:
        """Extract the normalizer function."""
        if (isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
                and node.func.value.id == self.normalizationModule):
            return f'{self.normalizationModule}.{node.func.attr}'
        return None

    def visit_Raise(self, node: ast.Raise) -> None:
        """Analyze exception raises."""
        # Extract raised exceptions
        if node.exc and isinstance(node.exc, ast.Call):
            if isinstance(node.exc.func, ast.Name):
                self.exceptions.add(node.exc.func.id)
        elif node.exc and isinstance(node.exc, ast.Name):
            self.exceptions.add(node.exc.id)

        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        """Analyze function calls."""
        if (hasattr(node.func, 'attr')
                and node.func.attr == 'raiseNotImplementedError'):
            self.exceptions.add('NotImplementedError')

        normalizer = self._extractNormalizer(node)
        if normalizer and node.args and isinstance(node.args[0], ast.Name):
            self.normalizers[node.args[0].id] = normalizer

        self.generic_visit(node)

    def visit_Return(self, node: ast.Return) -> None:
        """Analyze return values for normalization."""
        if isinstance(node.value, ast.Call):
            normalizer = self._extractNormalizer(node.value)
            if normalizer and isinstance(node.value.args[0], ast.Name):
                self.normalizers['return'] = normalizer
        elif isinstance(node.value, ast.Name):
            returnValue = node.value.id
            if returnValue in self.normalizers:
                self.normalizers['return'] = self.normalizers[returnValue]

        self.generic_visit(node)


class Docstring(DynamicPropertyMixin):
    """Represent a formatted docstring for a given object.

    :param obj: The object to which the docstring belongs.
    :param containingClass: The class containing the object, if any.
        Defaults to :obj:`None`.
    :param description: A detailed description to add to the docstring.
        Defaults to :obj:`None`.
    :param examples: Examples to add to the docstring. These will
        override any examples in the object's existing docstring.
        Defaults to :obj:`None`.
    :param preeserveVariadics: Whether to preserve and escape variadic
        parameters (`*args` and `**kwargs`) in the outputted docstring.
        Defaults to :obj:`True`.
    :param globalNamespace: A global namespace dictionary to be used for
         type hints. Defaults to the current global namespace.

    .. note::

        When ``preserveVariadics=True``, the generated docstring should
        be inserted into your source code as a raw string to correctly
        preserve the asterisk symbols.

    """

    def __init__(self,
                 obj: Any,
                 containingClass: Optional[Any] = None,
                 summary: Optional[str] = None,
                 description: Optional[str] = None,
                 examples: Optional[str] = None,
                 preserveVariadics: bool = True,
                 globalNamespace: Optional[dict] = None):
        self._obj = obj
        self._containingClass = containingClass
        self._summary = summary
        self._description = description
        self._examples = examples
        self._globalNamespace = globalNamespace
        self._preserveVariadics = preserveVariadics

    # --------------------
    # Signature and source
    # --------------------

    def _getSignatureInfo(self) -> Dict[str, Any]:
        # Return a dictionary with the extracted signature information:
        # - 'annotations': Parameter annotations.
        # - 'defaults': Default values for parameters.
        # - 'return': Return type annotation.
        from collections import defaultdict

        result: defaultdict[str, Union[dict, ParsedAnnotation]] = defaultdict(dict)
        result['annotations'] = self._extractParameterAnnotations()
        result['defaults'] = self._extractDefaultValues()
        result['return'] = self._extractReturnAnnotation()

        return dict(result)

    def _extractParameterAnnotations(self) -> Dict[str, ParsedAnnotation]:
        # Extract annotations for the parameters of the object.
        annotations = {}
        hints = self._getTypeHints()
        signature = self._getSignature()
        for name, param in signature.parameters.items():
            if name in {'self', 'cls'}:
                continue

            annotation = hints.get(name, param.annotation)
            annotations[name] = self._parseTypeAnnotation(annotation)

        return annotations

    def _extractReturnAnnotation(self) -> Optional[ParsedAnnotation]:
        # Extract the return type annotation of the object.
        hints = self._getTypeHints()
        signature = self._getSignature()

        if signature:
            returnAnnotation = hints.get('return', signature.return_annotation)
            return self._parseTypeAnnotation(returnAnnotation)
        return None

    def _extractDefaultValues(self) -> Dict[str, Any]:
        # Extract default values for the parameters of the object.
        defaults = {}
        signature = self._getSignature()
        for name, param in signature.parameters.items():
            if name in {'self', 'cls'}:
                continue
            if param.default is not inspect.Signature.empty:
                defaults[name] = param.default

        return defaults

    def _getRaisedExceptions(self) -> Set[str]:
        # Get the exceptions raised by the object based on the `obj` source.
        source = inspect.getsource(self.obj)
        dedentedSource = textwrap.dedent(source)
        tree = ast.parse(dedentedSource)
        extractor = CodeAnalyzer()
        extractor.visit(tree)
        return extractor.exceptions

    @staticmethod
    def _getNormalizers(source: str) -> Dict[str, str]:
        # Extract normalizer names from the given source.
        dedentedSource = textwrap.dedent(source)
        tree = ast.parse(dedentedSource)
        extractor = CodeAnalyzer()
        extractor.visit(tree)
        return extractor.normalizers

    # ----------
    # Type hints
    # ----------

    def _createTypeString(self, key: Optional[str] = None) -> str:
        # Create a formatted type string for a parameter or return type.
        if key is not None:
            annotation = self._extractParameterAnnotations()[key]
        else:
            annotation = self._extractReturnAnnotation()

        def _typeToString(annotation: Any) -> str:
            if isinstance(annotation, tuple):
                container, elements = annotation[0], annotation[1]
                if container == 'typing.Union':
                    return " or ".join([_typeToString(e) for e in elements])
                return (
                    f"{self._assignRole(container)} of "
                    f"{', '.join([_typeToString(e) for e in elements])} "
                    f"items"
                )
            elif annotation.startswith('Optional[') and annotation.endswith(']'):
                elements = [annotation[9:-1], 'None']
                return " or ".join([_typeToString(e) for e in elements])
            return self._assignRole(annotation)

        return _typeToString(annotation)

    def _parseTypeAnnotation(self,
                             annotation: Any
                             ) -> ParsedAnnotation:
        # Parses the type annotation of a parameter or return type.
        # builtins
        try:
            if hasattr(annotation, '__name__'):
                return annotation.__name__

            origin = get_origin(annotation)

            if origin is not None:
                if hasattr(origin, '__name__'):
                    containerName = origin.__name__
                else:
                    containerName = str(origin)
                elements = get_args(annotation)
                return containerName, [
                    self._parseTypeAnnotation(elem) for elem in elements
                ]
            return str(annotation)

        except AttributeError as exc:
            logging.error("Error parsing annotation: %s", exc)
            return "Unknown"

    # -------
    # Helpers
    # -------

    def _getSignature(self) -> Optional[inspect.Signature]:
        # Select signature getter based on object type.
        if (not isinstance(self.obj, type)
                and self.objectName == 'dynamicProperty'):
            return self._mergeSignatures()
        return inspect.signature(self.obj)

    def _getTypeHints(self) -> Dict[str, Any]:
        # Select type hint getter based on object type.
        if self.objectName == 'dynamicProperty':
            return self._mergeTypeHints()
        return get_type_hints(self.obj, globalns=self.globalNamespace)

    def _assignRole(self, objectName: str) -> str:
        # Assign a role to an object based on its type.

        if objectName == 'NoneType':
            return ':obj:`None`'

        def removePrefix(string: str, prefix: str) -> str:
            # Remove a specified prefix from a string.
            if string and string.startswith(prefix):
                return string[len(prefix):]
            return string

        def getMemberRole(objectName: str) -> str:
            # Determine the role of a class member (method, function, etc.).
            className, memberName = objectName.split('.', 1)
            obj = self.globalNamespace.get(className)
            member = getattr(obj, memberName, None)
            typeName = type(obj).__name__

            if callable(member):
                if isinstance(member, type(lambda: None)):
                    typeName = 'method'
                else:
                    typeName = 'function'
            elif isinstance(member, property):
                typeName = 'property'
            else:
                typeName = 'attribute'
            return ROLE_PREFIXES.get(typeName, '')

        objectName = removePrefix(objectName, 'typing.')
        if self.isQualified(objectName):
            prefix = getMemberRole(objectName)
        else:
            prefix = ROLE_PREFIXES.get(objectName, '')
        return (f'{prefix}`{objectName}`'
                if prefix else f':class:`{objectName}`')

    def _resolveSource(self) -> str:
        # Resolves the source based on object type.
        if self.dynamicPropertyObject:
            if self.isGetter:
                obj = Docstring(
                    self.dynamicPropertyObject,
                    containingClass=self.containingClass
                ).getterObject
            elif self.isSetter:
                obj = Docstring(
                    self.dynamicPropertyObject,
                    containingClass=self.containingClass
                ).setterObject
        elif self.isPrivate:
            obj = self.publicObject
        else:
            obj = self.obj
        return inspect.getsource(obj)

    @staticmethod
    def isQualified(objectName) -> bool:
        """Check if the given object name is qualified.

        :param objectName: The name of the object.
        :return: :obj:`True` if the object name is qualified,
            :obj:`False` otherwise.

        """
        return objectName and '.' in objectName and objectName[0].isupper()

    # ------------------
    # Docstring Elements
    # ------------------

    @property
    def summary(self) -> str:
        """Retrieve the summary line of the object.

        If the object is private but has a public counterpart, it fetches the
        first line of the public object's docstring and, if appropriate,
        adjusts it based on whether the object is a getter or setter.

        A warning is given if the provided summary exceeds the LINE_LENGTH setting.

        """
        if self.isPrivate and self.publicQualname:
            _, publicName = self.publicQualname.split('.')
            try:
                publicObject = getattr(self.containingClass, publicName)
                summary = publicObject.__doc__.split('\n')[0]
            except AttributeError:
                summary = 'Summary line'
            if self.isGetter:
                summary = summary.replace('Get or set', 'Get')
            elif self.isSetter:
                summary = summary.replace('Get or set', 'Set')
            return summary or 'Summary line'

        if self._summary and len(self._summary) > LINE_LENGTH:
            logging.warning(
                "The provided 'summary' value is longer than %s characters.",
                LINE_LENGTH
            )

        return self._summary or 'Summary line'

    @property
    def deprecationNotice(self) -> str:
        """Provide a formatted deprecation notice if object is deprecated."""
        objectDocstring = inspect.getdoc(self.obj)
        if not objectDocstring:
            return ''

        pattern = re.compile('`(.*)`')

        for line in objectDocstring.splitlines():
            if DEPRECATION_ID not in line:
                continue

            replacementMatch = pattern.search(line)
            if not replacementMatch:
                continue

            replacementName = replacementMatch.group(1)
            assignedReplacement = self._assignRole(replacementName)
            formatString = FORMAT_STRINGS['deprecated'].format(
                replacement=assignedReplacement)
            directive = f"{DIRECTIVES['deprecated']}\n\n{INDENT}{formatString}"
            return directive

        return ''

    @property
    def description(self) -> str:
        """Retrieve the description of the object.

        If the object is private, an implementation note is appended to the
        description.

        """
        description = textwrap.fill(self._description or 'Description', LINE_LENGTH)
        if self.isPrivate:
            return "\n\n".join([description, self.implementationNote]
                               if self.implementationNote else [description])
        return description

    @property
    def paramSection(self) -> str:
        """Get the parameter section of the docstring."""
        if not isinstance(self.obj, type) and self.objectName == 'dynamicProperty':
            return self.setterValueDescription

        lines = []
        signature = inspect.signature(self.obj)
        for name, param in signature.parameters.items():
            if name == 'self':
                continue

            typeString = self._createTypeString(name)

            # Handle variadics.
            if str(param).startswith('*') and self.preserveVariadics:
                name = f"\\{str(param)}"

            formatString = FORMAT_STRINGS['parameter'].format(
                parameterName=name, typeString=typeString
            )

            if self.isPrivate:
                source = self._resolveSource()
                normalizerDict = self._getNormalizers(source)
                if normalizerDict and name in normalizerDict:
                    normalizer = normalizerDict[name]
                    formatString += FORMAT_STRINGS['normalizer'].format(
                        normalizer=normalizer
                    )

            defaults = self._getSignatureInfo().get('defaults')
            if defaults and name in defaults:
                value = self._formatValue(defaults[name])
                formatString += FORMAT_STRINGS['default'].format(value=value)

            wrapped = textwrap.fill(formatString, LINE_LENGTH, subsequent_indent=INDENT)
            lines.append(wrapped)
        return '\n'.join(lines) or ''

    @property
    def returnSection(self) -> str:
        """Get the return section of the docstring."""
        returnValue = self._extractReturnAnnotation()
        if returnValue in ['NoneType', 'None']:
            return ''

        typeString = self._createTypeString()
        formatString = FORMAT_STRINGS['return'].format(typeString=typeString)

        if self.isPrivate:
            source = self._resolveSource()
            normalizerDict = self._getNormalizers(source)
            if normalizerDict and 'return' in normalizerDict:
                normalizer = normalizerDict['return']
                formatString += FORMAT_STRINGS['normalizer'].format(
                    normalizer=normalizer
                )

        return textwrap.fill(formatString, LINE_LENGTH, subsequent_indent=INDENT)

    @property
    def raisesSection(self) -> str:
        """Get the raises section of the docstring."""
        if self.objectName == 'dynamicProperty':
            return ''

        exceptions = self._getRaisedExceptions()
        lines = []
        for exc in exceptions:
            condition = FORMAT_STRINGS['exception']
            if exc == 'NotImplementedError':
                condition = FORMAT_STRINGS['notImplementedError']
            formatString = FORMAT_STRINGS['raises'].format(
                exception=exc, condition=condition
            )
            wrapped = textwrap.fill(formatString, LINE_LENGTH, subsequent_indent=INDENT)
            lines.append(wrapped)

        return '\n'.join(lines) or ''

    @property
    def overrideNotice(self) -> str:
        """Get an override notice based on the override value."""
        if self.overrideValue == 0:
            return ''
        delimiter = '\n\n' + INDENT
        if self.overrideValue == 1:
            return (DIRECTIVES['note']
                    + delimiter
                    + FORMAT_STRINGS['mayOverride'])
        return (DIRECTIVES['important']
                + delimiter
                + FORMAT_STRINGS['mustOverride'])

    @property
    def examples(self) -> str:
        """Get  and reformat code examples from the object's docstring."""
        found = []
        docstring = inspect.getdoc(self.obj)
        if not docstring:
            return ''

        for element in docstring.split('\n\n'):
            if element.strip().startswith('>>>'):
                found.append(element)
        delimiter = '\n\n'
        return f"Example::{delimiter}{delimiter.join(found)}" if found else ''

    # ----------------
    # Other properties
    # ----------------

    @property
    def obj(self) -> Any:
        """Get the object this instance represents."""
        return self._obj

    @property
    def containingClass(self) -> Optional[Any]:
        """Get the class containing the object."""
        return self._containingClass

    @property
    def publicObject(self):
        """Get the public equivalen of the object."""
        try:
            return getattr(self.containingClass, self.publicQualname.split('.')[-1])
        except AttributeError:
            return self.obj

    @property
    def globalNamespace(self) -> Dict[str, Any]:
        """Get the current global namespace."""
        return self._globalNamespace or globals()

    @property
    def preserveVariadics(self) -> bool:
        """Get the setting for preserving variadics."""
        return self._preserveVariadics

    @property
    def objectName(self) -> str:
        """Get the name of the object."""
        try:
            return self.obj.__qualname__
        except AttributeError:
            try:
                return self.obj.__name__
            except AttributeError:
                return self.obj.__class__.__name__

    @property
    def isPrivate(self) -> bool:
        """Check if the object is private (starts with an underscore)."""
        objectName = self.objectName
        if self.isQualified(objectName):
            _, objectName = objectName.split('.')
        return objectName.startswith('_')

    @property
    def isBase(self) -> bool:
        """Check if the object is a base object."""
        return not self.isPrivate or "_base_" in self.objectName

    @property
    def publicQualname(self) -> str:
        """Retrieve the public qualified name of the object, if it exists.

        If the object is a `dynamicProperty`, it returns the
        `dynamicPropertyQualname`.
        If the object is not private, it returns the object's name.
        If the object is private, it formats and checks if the member
        exists in the containing class and returns the formatted name.

        """
        def getNamespace(objectName: str) -> str:
            # Get the name of the object's namespace (i.e., the part of the
            # qualname before the last dot) from `objectName` or `containingClass`.
            if '.' in objectName:
                segments = objectName.split('.')
                return '.'.join(segments[:-1])
            if self.containingClass:
                return self.containingClass.__class__.__qualname__
            return ''

        def objectExists(publicMemberName: str) -> bool:
            # Check if an object exists within a class.
            return self.containingClass and hasattr(
                self.containingClass, publicMemberName
            )

        if self.dynamicPropertyObject.__class__.__name__ == 'dynamicProperty':
            return self.dynamicPropertyQualname

        namespace = getNamespace(self.objectName)
        memberName = (self.objectName.split('.')[-1]
                      if '.' in self.objectName else self.objectName)
        publicMemberName = memberName[1:] if self.isPrivate else memberName
        if not objectExists(publicMemberName):
            magicMemberName = f"__{publicMemberName.lower()}__"
            if not objectExists(magicMemberName):
                raise ValueError(f"Cannot find public member for '{memberName}'.")
            publicMemberName = magicMemberName
        return '.'.join([namespace, publicMemberName])

    @property
    def overrideValue(self) -> int:
        """Check the object's docstring for override instructions.

        Returns 1 if the docstring contains "may override" and 2 if it contains
        "must override".

        """
        docstring = inspect.getdoc(self.obj)
        if docstring:
            if "may override" in docstring:
                return 1
            if "must override" in docstring:
                return 2
        return 0


def insertDocstring(obj: Any,
                    newDocstring: str,
                    preserveVariadics: bool = True) -> str:
    """Insert the generated docstring into the source code of the object.

    :param obj: The object whose docstring will be modified.
    :param newDocstring: The new docstring to be inserted.
    :param preserveVariadics: Whether to preserve variadic
        arguments in the docstring. Defaults to :obj:`True`.
    :return: The updated source code with the new docstring.

    """
    try:
        source = inspect.getsource(obj)
        sourceLines = source.splitlines()
        match = re.match(r"(\s*)", sourceLines[0])
        indent = match.group(1) if match else ''

        # Format the docstring with correct indentation.
        formattedDocstring = textwrap.indent(newDocstring.strip(), indent * 2)

        # Remove the leading triple quotes  and ensure
        # the correct placement of closing triple quotes.
        formattedDocstring = (
            f'"""{formattedDocstring[3:].strip()}\n\n{indent * 2}"""'
        )

        # Handle variadics.
        if '\\*' in formattedDocstring and preserveVariadics:
            formattedDocstring = f'r{formattedDocstring}'

        # Replace existing docstring or insert a new one,
        if obj.__doc__:
            updatedSourceCode = re.sub(
                r'("""[\s\S]*?""")', formattedDocstring, source, count=1
            )
        else:
            signatureEnd = next(
                i for i, line in enumerate(sourceLines)
                if line.strip().endswith(':')
            )
            updatedSourceCode = (
                '\n'.join(sourceLines[:signatureEnd + 1])
                + f'\n{indent}{formattedDocstring}\n'
                + '\n'.join(sourceLines[signatureEnd + 1:])
            )

        return updatedSourceCode
    except TypeError as exc:
        raise TypeError(f"The source of a {obj.__class__.__name__} "
                        "instance can not be inspected.") from exc


def generateDocstring(obj: Any,
                      summary: Optional[str] = None,
                      description: Optional[str] = None,
                      examples: Optional[str] = None,
                      preserveVariadics: bool = True,
                      globalNamespace: Optional[dict] = None,
                      containingClass: Optional[Any] = None) -> str:
    """Generate a docstring for the object.

    Creates a docstring with sections including summary, description,
    parameters, return values, raised exceptions, and examples.

    :param obj: The object for which to generate a docstring.
    :param summary: A brief summary of the object.
    :param description: A detailed description of the object.
    :param examples: Code examples for the object.
    :param preserveVariadics: Whether to preserve variadic arguments
        in the docstring.
    :param globalNamespace: The global namespace.
    :param containingClass: The containing class of the object, if applicable.
    :return: A generated docstring formatted in reST.

    """

    docstring = Docstring(
        obj=obj,
        containingClass=containingClass,
        summary=summary,
        description=description,
        examples=examples,
        preserveVariadics=preserveVariadics,
        globalNamespace=globalNamespace
    )

    preliminarySections = [
        docstring.summary,
        docstring.deprecationNotice,
        docstring.description,
    ]

    middleSections = [
        docstring.paramSection,
        docstring.returnSection,
        docstring.raisesSection,
    ]

    conclusiveSections = [
        docstring.overrideNotice,
        docstring.examples
    ]

    preliminaryContent = '\n\n'.join(filter(None, preliminarySections))
    middleContent = '\n'.join(filter(None, middleSections))
    conclusiveContent = '\n\n'.join(filter(None, conclusiveSections))
    return f"{preliminaryContent}\n\n{middleContent}\n\n{conclusiveContent}"
