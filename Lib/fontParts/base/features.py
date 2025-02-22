from __future__ import annotations
from typing import TYPE_CHECKING, Tuple, List, Optional

from fontParts.base.base import BaseObject, dynamicProperty, reference
from fontParts.base import normalizers
from fontParts.base.deprecated import DeprecatedFeatures, RemovedFeatures

if TYPE_CHECKING:
    from fontParts.base.font import BaseFont


class BaseFeatures(BaseObject, DeprecatedFeatures, RemovedFeatures):
    """Represent the basis for a features object. 
    
    This class contains the font's `Adobe Font Development Kit for OpenType (AFDKO) 
    <https://github.com/adobe-type-tools/afdko/>`_ feature definitions.
    
    """
    copyAttributes: Tuple[str]  = ("text",)

    def _reprContents(self) -> List[str]:
        contents = []
        if self.font is not None:
            contents.append("for font")
            contents += self.font._reprContents()
        return contents

    # -------
    # Parents
    # -------

    # Font

    _font: Optional[BaseFont] = None

    font: dynamicProperty = dynamicProperty(
        "font", 
    """Get the feature's parent font object.

        This property is read-only.

        :return: The :class:`BaseFont` instance containing the features
            or :obj:`None`.
        :raises AssertionError:
            - If attempting to set the font when it has already been set and is
              not the same as the provided font.

        Example::

            >>> font = features.font

        """
    )

    def _get_font(self) -> Optional[BaseFont]:
        if self._font is None:
            return None
        return self._font()

    def _set_font(self, font: Optional[BaseFont]) -> None:
        if self._font is not None and self._font() != font:
            raise AssertionError(
                "font for features already set and is not same as font"
            )
        if font is not None:
            font = reference(font)
        self._font = font

    # ----
    # Text
    # ----

    text: dynamicProperty = dynamicProperty(
        "base_text",
        """Get or set the features text.
        
        The value must be a `AFDKO FEA formatted
        <https://adobe-type-tools.github.io/afdko/OpenTypeFeatureFileSpecification.html>`_
        :class:`str` or :obj:`None`.
        
        :return: A :class:`str` representing the font's features text, or :obj:`None`.

        """,
    )

    def _get_base_text(self) -> Optional[str]:
        value = self._get_text()
        if value is not None:
            value = normalizers.normalizeFeatureText(value)
        return value

    def _set_base_text(self, value: Optional[str]) -> None:
        if value is not None:
            value = normalizers.normalizeFeatureText(value)
        self._set_text(value)

    def _get_text(self) -> Optional[str]:
        """Get the features text.

        This is the environment implementation of the :attr:`BaseFeatures.text` property
        getter.

        :return: :class:`_empty`. The value will be normalized with
            :func:`normalizers.normalizeFeatureText`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()

    def _set_text(self, value: Optional[str]) -> None:
        """Set the features text.

        Description

        This is the environment implementation of the :attr:`BaseFeatures.text` property
        setter.

        :param value: A `AFDKO FEA formatted
        <https://adobe-type-tools.github.io/afdko/OpenTypeFeatureFileSpecification.html>`_
        :class:`str` or :obj:`None`. The value will have been
            normalized with :func:`normalizers.normalizeFeatureText`.
        :raises NotImplementedError: If the method has not been overridden by a
            subclass.

        .. important::

            Subclasses must override this method.

        """
        self.raiseNotImplementedError()
