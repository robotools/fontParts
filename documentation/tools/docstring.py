# pylint: disable=R0904, R0913, C0103, C0114, C0415
from typing import (
    get_type_hints,
    get_origin,
    get_args,
    Any,
    Callable,
    Dict,
    Optional,
    List,
    Union,
    Tuple
)
import ast
import inspect
import logging
import re
import textwrap

from fontParts.base.base import dynamicProperty

OptionalCallable = Optional[Callable]
GetterSetterType = Tuple[OptionalCallable, OptionalCallable]

FORMAT_STRINGS: Dict[str, str] = {
    'implementation_note': (
        "This is the environment implementation of {base_object}."
    ),
    'getter_implementation_note': (
        "This is the environment implementation of the {base_object} property getter."
    ),
    'setter_implementation_note': (
        "This is the environment implementation of the {base_object} property setter."
    ),
    'deprecated': (
        "This method is deprecated. Use {replacement} instead."
    ),
    'may_override': (
        "Subclasses may override this method."
    ),
    'must_override': (
        "Subclasses must override this method."
    ),
    'parameter': (
        ":param {parameter_name}: Description of {type_string}."
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
    'not_implemented_error': (
        "the method has not been overridden by a subclass"
    ),
    'return': (
        ":return: {type_string}."
    ),
    'setter_value': (
        "The value must be {type_string}."
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
    'todo': '..todo::'
}


class DynamicPropertyMixin:
    """Provide functionality specific to dynamicProperty objects."""

    def createSetterValueDescription(self) -> Optional[str]:
        """Generate the description string for the setter value."""
        signature = self._mergeSignatures()
        for name in signature.parameters:
            if name == 'self':
                continue

            type_string = self._createTypeString(name)
            format_string = FORMAT_STRINGS['setter_value'].format(
                parameter_name=name, type_string=type_string
            )

            defaults = self._getSignatureInfo().get('defaults')
            if defaults and name in defaults:
                value = self.formatValue(defaults[name])
                format_string += FORMAT_STRINGS['default'].format(value=value)
            return format_string or None

    def createImplementationNote(self) -> Optional[str]:
        """Generate an implementation note for the dynamic property."""
        if not self.publicQualname:
            return None
        role = self._assignRole(self.publicQualname)
        if self.isGetter:
            return FORMAT_STRINGS['getter_implementation_note'].format(
                base_object=role
            )
        if self.isSetter:
            return FORMAT_STRINGS['setter_implementation_note'].format(
                base_object=role
            )
        return FORMAT_STRINGS['implementation_note'].format(base_object=role)

    def _getGetterSetter(self) -> Optional[GetterSetterType]:
        # Retrieve getter and setter functions for the dynamic property.
        try:
            getter = getattr(self.containingClass, self.obj.getterName, None)
            setter = getattr(self.containingClass, self.obj.setterName, None)
        except AttributeError:
            return None
        return getter, setter

    def _mergeSignatures(self) -> inspect.Signature:
        # Merge the signatures of the getter and setter
        getter_signature = inspect.signature(self.getterObject)
        if not self.setterObject:
            return getter_signature

        setter_signature = inspect.signature(self.setterObject)
        params = list(setter_signature.parameters.values())
        return_annotation = getter_signature.return_annotation
        return inspect.Signature(
            parameters=params, return_annotation=return_annotation
        )

    def _mergeTypeHints(self) -> Dict[str, Optional[Any]]:
        """Merge the type hints from the getter and setter."""
        type_hints = {}
        getter_hints = get_type_hints(
            self.getterObject, globalns=self.globalns
        )
        type_hints['value'] = getter_hints.get('return', None)
        if self.setterObject:
            setter_hints = get_type_hints(
                self.setterObject, globalns=self.globalns
            )
            type_hints['return'] = setter_hints.get('value', None)
        return type_hints

    def _formatValue(self, value: Any) -> str:
        """Format a value for inclusion in a docstring."""
        if isinstance(value, str):
            return f"``'{value}'``"
        if isinstance(value, (bool, type(None))):
            return self._assignRole(str(value))
        return f"``{value}``"

    @property
    def dynamicPropertyObject(self) -> Optional[dynamicProperty]:
        """Get the current object's associated dynamicProperty."""
        if self.isGetter or self.isSetter:
            dynamic_property_name = self.dynamicPropertyQualname.split('.')[1]
            return getattr(self.containingClass, dynamic_property_name)
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


class Docstring(DynamicPropertyMixin):
    """Represent a formatted docstring for a given object.

    :param obj: The object to which the docstring belongs.
    :param description: A detailed description to add. Defaults
        to :obj:`None`
    :param examples: Examples to add to the docstring. These will
        override any examples in the objects existing docstring.
    :param preeserve_variadics: If :obj:`True`, variadic parameters
        (`*args` and `**kwargs`) will be preserved and escaped in the
        outputted docstring.
    :param globalns: A global namespace dictionary to be used for type hints.
        Defaults to the current global namespace.
    :param containingClass: The class containing the object, if any.
        Defaults to :obj:`None`

    .. note::

        When ``preserveVariadics=True``, the generated docstring should be
        inserted into your source code as a raw string to correctly preserve
        the asterisk symbols.

    """

    def __init__(self, obj: Any, summary: Optional[str] = None,
                 description: Optional[str] = None,
                 examples: Optional[str] = None,
                 preserveVariadics: bool = True,
                 globalns: Optional[dict] = None,
                 containingClass: Optional[Any] = None):
        self._obj = obj
        self._summary = summary
        self._description = description
        self._examples = examples
        self.preserveVariadics = preserveVariadics
        self.globalns = globalns or globals()
        self.containingClass = containingClass

    def createParamSection(self) -> str:
        """Generate the parameter section of the docstring."""
        if self.objectName == 'dynamicProperty':
            return self.createSetterValueDescription()

        lines = []
        signature = inspect.signature(self.obj)

        for name, param in signature.parameters.items():
            if name == 'self':
                continue

            type_string = self._createTypeString(name)

            # Handle variadics.
            if str(param).startswith('*') and self.preserveVariadics:
                name = f"\\{str(param)}"

            format_string = FORMAT_STRINGS['parameter'].format(
                parameter_name=name, type_string=type_string
            )

            defaults = self._getSignatureInfo().get('defaults')
            if defaults and name in defaults:
                value = self._formatValue(defaults[name])
                format_string += FORMAT_STRINGS['default'].format(value=value)

            lines.append(format_string)
        return '\n'.join(lines)

    def createReturnSection(self) -> Optional[str]:
        """Generate the return section of the docstring."""
        return_value = self._extractReturnAnnotation()
        if return_value == 'NoneType':
            return None

        type_string = self._createTypeString()
        return FORMAT_STRINGS['return'].format(
            type_string=type_string
        )

    def createRaisesSection(self) -> Optional[str]:
        """Generate the raises section of the docstring."""
        if self.objectName == 'dynamicProperty':
            return None
        exceptions = self._getRaisedExceptions()
        lines = []
        for exc in exceptions:
            condition = FORMAT_STRINGS['exception']
            if exc == 'NotImplementedError':
                condition = FORMAT_STRINGS['not_implemented_error']
            lines.append(FORMAT_STRINGS['raises'].format(
                exception=exc, condition=condition)
            )
        return '\n'.join(lines) or None

    def _getSignatureInfo(self) -> Dict[str, Any]:
        # Return a dictionary with the extracted signature information:
        # - 'annotations': Parameter annotations.
        # - 'defaults': Default values for parameters.
        # - 'return': Return type annotation.
        from collections import defaultdict

        result = defaultdict(dict)
        result['annotations'] = self._extractParameterAnnotations()
        result['defaults'] = self._extractDefaultValues()
        result['return'] = self._extractReturnAnnotation()

        return dict(result)

    def _extractParameterAnnotations(self) -> Dict[str, str]:
        # Extract annotations for the parameters of the object.
        hints = self._get_type_hints()
        if self.objectName == 'dynamicProperty':
            signature = self._mergeSignatures()
        else:
            signature = inspect.signature(self.obj)

        annotations = {}
        for name, param in signature.parameters.items():
            if name in {'self', 'cls'}:
                continue
            annotation = hints.get(name, param.annotation)
            annotations[name] = self._parseTypeAnnotation(annotation)

        return annotations

    def _extractDefaultValues(self) -> Dict[str, Any]:
        # Extract default values for the parameters of the object.
        signature = inspect.signature(self.obj)
        defaults = {}
        for name, param in signature.parameters.items():
            if name in {'self', 'cls'}:
                continue
            if param.default is not inspect.Signature.empty:
                defaults[name] = param.default

        return defaults

    def _extractReturnAnnotation(self) -> str:
        # Extract the return type annotation of the object.
        hints = self._get_type_hints()
        if self.objectName == 'dynamicProperty':
            signature = self._mergeSignatures()
        else:
            signature = inspect.signature(self.obj)

        return_annotation = hints.get('return', signature.return_annotation)
        return self._parseTypeAnnotation(return_annotation)

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
                    return " or ".join(
                        [_typeToString(elem) for elem in elements]
                    )
                return (
                    f"{self._assignRole(container)} of "
                    f"{', '.join([_typeToString(elem) for elem in elements])} "
                    f"items"
                )
            return self._assignRole(annotation)

        type_string = _typeToString(annotation)
        return type_string

    def _getRaisedExceptions(self) -> List[str]:
        # Get the exceptions raised by the object based on the source code.
        source = inspect.getsource(self.obj)
        dedented_source = textwrap.dedent(source)
        tree = ast.parse(dedented_source)
        exceptions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Raise):
                if node.exc and isinstance(node.exc, ast.Call):
                    exceptions.append(node.exc.func.id)
                elif node.exc and isinstance(node.exc, ast.Name):
                    exceptions.append(node.exc.id)
            elif isinstance(node, ast.Call):
                if (hasattr(node.func, 'attr')
                        and node.func.attr == 'raiseNotImplementedError'):
                    exceptions.append('NotImplementedError')

        return list(set(exceptions))

    def _parseTypeAnnotation(self,
                             annotation: Any
                             ) -> Union[str, Tuple[str, List[Any]]]:
        # Parses the type annotation of a parameter or return type.
        # builtins
        try:
            if hasattr(annotation, '__name__'):
                return annotation.__name__

            origin = get_origin(annotation)

            if origin is not None:
                if hasattr(origin, '__name__'):
                    container_name = origin.__name__
                else:
                    container_name = str(origin)
                elements = get_args(annotation)
                return container_name, [
                    self._parseTypeAnnotation(elem) for elem in elements
                ]
            return str(annotation)

        except AttributeError as exc:
            logging.error("Error parsing annotation: %s", exc)
            return "Unknown"

    def _get_type_hints(self):
        # Retrieves the type hints for the object.
        if self.objectName == 'dynamicProperty':
            hints = self._mergeTypeHints()
        else:
            hints = get_type_hints(self.obj, globalns=self.globalns)
        return hints

    def _objectExists(self, qualname: str):
        # Check if an object exists within a class.
        containingClass = self.containingClass
        member_name = self.objectName
        if '.' in qualname:
            class_name, member_name = qualname.split('.')
            containingClass = self.globalns.get(class_name)
        if not containingClass:
            return False
        if not hasattr(containingClass, member_name):
            return False
        return True

    @staticmethod
    def _removePrefix(string, prefix):
        # Remove a specified prefix from a string.
        if string.startswith(prefix):
            return string[len(prefix):]
        return string

    def _assignRole(self, objectName: str) -> str:
        # Assign a role to an object based on its type.
        if objectName == 'NoneType':
            return ':obj:`None`'

        objectName = self._removePrefix(objectName, 'typing.')

        if self.isQualified(objectName):
            prefix = self._getMemberRole(objectName)
        else:
            prefix = ROLE_PREFIXES.get(objectName)

        return (f'{prefix}`{objectName}`'
                if prefix else f':class:`{objectName}`')

    def _getMemberRole(self, objectName: str) -> str:
        # Determine the role of a class member (method, function, etc.).
        class_name, member_name = objectName.split('.', 1)
        obj = self.globalns.get(class_name)
        member = getattr(obj, member_name, None)
        type_name = type(obj).__name__

        if callable(member):
            if isinstance(member, type(lambda: None)):
                type_name = 'method'
            else:
                type_name = 'function'
        elif isinstance(member, property):
            type_name = 'property'
        else:
            type_name = 'attribute'

        return ROLE_PREFIXES.get(type_name)

    @staticmethod
    def isQualified(objectName) -> bool:
        """Check if the given object name is qualified.

        :param objectName: The name of the object.
        :return: :obj:`True` if the object name is qualified,
            :obj:`False` otherwise.

        """
        return '.' in objectName and objectName[0].isupper()

    @property
    def source(self) -> str:
        """Get the source code of the object."""
        return inspect.getsource(self.obj)

    @property
    def signature(self) -> inspect.Signature:
        """Get the signature of the object."""
        return inspect.signature(self.obj)

    @property
    def obj(self) -> Any:
        """Get the object this instance represents."""
        return self._obj

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
    def objectDocstring(self) -> Optional[str]:
        """Get the docstring of the object."""
        return inspect.getdoc(self.obj)

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
        """Retrieve the public qualified name of the object.

        If the object is a `dynamicProperty`, it returns the
        `dynamicPropertyQualname`.
        If the object is not private, it returns the object's name.
        If the object is private, it formats and checks if the member exists
        in the containing class and returns the formatted name.

        """
        if self.dynamicPropertyObject.__class__.__name__ == 'dynamicProperty':
            return self.dynamicPropertyQualname
        if not self.isPrivate:
            return self.objectName
        if '.' in self.objectName:
            class_name, member_name = self.objectName.split('.')
            formatted_name = '.'.join([class_name, member_name[1:]])
        if self._objectExists(formatted_name):
            return formatted_name
        return None

    @property
    def overrideValue(self) -> int:
        """Check the object's docstring for override instructions.

        Returns 1 if the docstring contains "may override" and 2 if it contains
        "must override".

        """
        if self.objectDocstring:
            if "may override" in self.objectDocstring:
                return 1
            if "must override" in self.objectDocstring:
                return 2
        return 0

    # ------------------
    # Docstring Elements
    # ------------------

    @property
    def summary(self) -> Optional[str]:
        """Retrieve the summary line of the object.

        If the object is private but has a public counterpart, it fetches the
        first line of the public object's docstring and adjusts it based on
        whether the object is a getter or setter.

        """
        if self.isPrivate and self.publicQualname:
            _, public_name = self.publicQualname.split('.')
            try:
                public_object = getattr(self.containingClass, public_name)
                summary = public_object.__doc__.split('\n')[0]
            except AttributeError:
                summary = 'Summary'
            if self.isGetter:
                summary = summary.replace('Get or set', 'Get')
            if self.isSetter:
                summary = summary.replace('Get or set', 'Set')
            return summary
        return self._summary or 'Summary'

    @property
    def deprecationNotice(self) -> str:
        """Provide a formatted deprecation notice if object is deprecated."""
        identifier = 'This method is deprecated.'
        if not identifier in self.objectDocstring:
            return None
        for line in self.objectDocstring.split('\n'):
            if not identifier in line:
                continue
            replacement_match = re.search('`(.*)`', line)
            if not replacement_match:
                return None
            replacement_name = replacement_match.group(1)
            assigned_replacement = self._assignRole(replacement_name)
            message = FORMAT_STRINGS['deprecated'].format(
                replacement=assigned_replacement)
            return f".. deprecated::\n\n{' '*4}{message}"

    @property
    def description(self) -> str:
        """Retrieve the description of the object.

        If the object is private, an implementation note is appended to the
        description.

        """
        if self.isPrivate:
            implementation_note = self.createImplementationNote()
            return (f"{self._description}\n\n{implementation_note}"
                    if self._description else implementation_note)
        return self._description or 'Description'

    @property
    def paramSection(self) -> str:
        """Get the parameter section of the docstring."""
        return self.createParamSection()

    @property
    def returnSection(self) -> str:
        """Get the return section of the docstring."""
        return self.createReturnSection()

    @property
    def raisesSection(self) -> str:
        """Get the raises section of the docstring."""
        return self.createRaisesSection()

    @property
    def overrideNotice(self) -> str:
        """Get an override notice based on the override value."""
        if self.overrideValue == 0:
            return None
        delimiter = '\n\n' + ' ' * 4
        if self.overrideValue == 1:
            return (DIRECTIVES['note']
                    + delimiter
                    + FORMAT_STRINGS['may_override'])
        return (DIRECTIVES['important']
                + delimiter
                + FORMAT_STRINGS['must_override'])

    @property
    def examples(self) -> Optional[List[str]]:
        """Get  and reformat code examples from the object's docstring."""
        found = []
        for element in self.objectDocstring.split('\n\n'):
            if element.strip().startswith('>>>'):
                found.append(element)
        delimiter = '\n\n'
        return f"Example::{delimiter}{delimiter.join(found)}" if found else None


def insertDocstring(obj: Any,
                    newDocstring: Optional[str] = None,
                    preserveVariadics: bool = True) -> str:
    """Insert the generated docstring into the source code of the object.

    :param obj: The object whose docstring will be modified.
    :param newDocstring: The new docstring to be inserted.
    :param preserveVariadics: Whether to preserve variadic arguments in the
        docstring.
    :return: The updated source code with the new docstring.

    """
    try:
        source = inspect.getsource(obj)
        source_lines = source.splitlines()
        indent = re.match(r"(\s*)", source_lines[0]).group(1)

        # Format the docstring with correct indentation.
        formatted_docstring = textwrap.indent(newDocstring.strip(), indent * 2)

        # Remove the leading triple quotes  and ensure
        # the correct placement of closing triple quotes.
        formatted_docstring = (
            f'"""{formatted_docstring[3:].strip()}\n\n{indent * 2}"""'
        )

        # Handle variadics.
        if '\\*' in formatted_docstring and preserveVariadics:
            formatted_docstring = f'r{formatted_docstring}'

        # Replace existing docstring or insert a new one,
        if obj.__doc__:
            updated_source_code = re.sub(
                r'("""[\s\S]*?""")', formatted_docstring, source, count=1
            )
        else:
            signature_end = next(
                i for i, line in enumerate(source_lines)
                if line.strip().endswith(':')
            )
            updated_source_code = (
                '\n'.join(source_lines[:signature_end + 1])
                + f'\n{indent}{formatted_docstring}\n'
                + '\n'.join(source_lines[signature_end + 1:])
            )

        return updated_source_code
    except TypeError:
        return obj.__doc__


def generateDocstring(obj: Any,
                      summary: Optional[str] = None,
                      description: Optional[str] = None,
                      examples: Optional[str] = None,
                      preserveVariadics: bool = True,
                      globalns: Optional[dict] = None,
                      containingClass: Optional[Any] = None) -> str:
    """Generate a docstring for the object.

    Creates a docstring with sections including summary, description,
    parameters, return values, raised exceptions, and examples.

    :param obj: The object for which to generate a docstring.
    :param summary: A brief summary of the object.
    :param description: A detailed description of the object.
    :param examples: Code examples for the object.
    :param preserveVariadics: Whether to preserve variadic arguments in the docstring.
    :param globalns: The global namespace.
    :param containingClass: The containing class of the object, if applicable.
    :return: A generated docstring formatted in reST.

    """

    docstring = Docstring(
        obj,
        summary,
        description,
        examples,
        preserveVariadics,
        globalns,
        containingClass
    )
    sections = [
        docstring.summary,
        docstring.deprecationNotice,
        docstring.description,
        docstring.paramSection,
        docstring.returnSection,
        docstring.raisesSection,
        docstring.overrideNotice,
        docstring.examples
    ]

    return '\n\n'.join(filter(None, sections))
