from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Union

from fontParts.world import _EnvironmentDispatcher
from fontParts.base.annotations import CollectionType

if TYPE_CHECKING:
    from fontParts.base.font import BaseFont


def AskString(
    message: str,
    value: Optional[str] = None,
    title: Optional[str] = "FontParts"
) -> str:
    """Dispaly a dialog to ask for a string input.

    :param message: The message to display in the dialog as a :class:`str`.
    :param value: The optional default value to display in the input field as 
        a :class:`str`. Defaults to :obj:`None`.
    :param title: The optional title of the dialog window as a :class:`str`.
        Defaults to ``"FontParts"``.
    :return: A :class:`str` representing the input provided by the user.

    Example::

        >>> AskString("who are you?")

    """
    return dispatcher["AskString"](message=message, value=value, title=title)


def AskYesNoCancel(
        message: str,
        title: Optional[str] = "FontParts",
        default: Optional[int] = 0,
        informativeText: Optional[str] = None
) -> str:
    """Display a dialog to ask a yes, no, or cancel question.

    :param message: The message to display in the dialog as a :class:`str`.
    :param title: The optional title of the dialog window as a :class:`str`.
        Defaults to ``"FontParts"``.
    :param default: The optional default button as an :class:`int`.
        Defaults to ``0``.
    :param informativeText: The optional additional informative text to display in the
        dialog as  a :class:`str`. Defaults to :obj:`None`.
    :return: A :class:`str` representing the user's response: ``"Yes"``, ``"No"``, or 
        ``"Cancel"``.

    Example::

        >>> AskYesNoCancel("Do you want to continue?")

    """
    return dispatcher["AskYesNoCancel"](
        message=message, title=title, default=default, informativeText=informativeText
    )


def FindGlyph(
        aFont: BaseFont,
        message: str = "Search for a glyph:",
        title: str = "FontParts"
) -> str:
    """Display a dialog to search for a glyph within a provided font.

    :param aFont: The font to search for a glyph in as a :class:`BaseFont`.
    :param message: The optional message to display in the dialog as a :class:`str`.
        Defaults to ``"Search for a glyph:"``.
    :param title: The optional title of the dialog window as a :class:`str`.
        Defaults to ``"FontParts"``.
    :return: A :class:`str` representing the name of the matched glyph.

    Example::

        >>> FindGlyph(myFont)

    """
    return dispatcher["FindGlyph"](aFont=aFont, message=message, title=title)


def GetFile(
    message: Optional[str] = None,
    title: Optional[str] = None,
    directory: Optional[str] = None,
    fileName: Optional[str] = None,
    allowsMultipleSelection: bool = False,
    fileTypes: Optional[str] = None,
) -> str:
    """Display a dialog to get a file path.

    :param message: The optional message to display in the dialog as a :class:`str`.
        Defaults to :obj:`None`.
    :param title: The optional title of the dialog window as a :class:`str`.
        Defaults to :obj:`None`.
    :param directory: The optional directory to start the dialog in as a :class:`str`.
        Defaults to :obj:`None`.
    :param fileName: The optional file name to start the dialog with as a :class:`str`.
        Defaults to :obj:`None`.
    :param allowsMultipleSelection: A flag to allow multiple file selection as 
        a :class:`bool`. Defaults to :obj:`False`.
    :param fileTypes: The optional file types to filter the dialog with as 
        a :class:`str`. Defaults to :obj:`None`.
    :return: A :class:`str` representing the path of the selected file.

    Example::

        >>> GetFile()

    """
    return dispatcher["GetFile"](
        message=message,
        title=title,
        directory=directory,
        fileName=fileName,
        allowsMultipleSelection=allowsMultipleSelection,
        fileTypes=fileTypes,
    )


def GetFileOrFolder(
    message: Optional[str] = None,
    title: Optional[str] = None,
    directory: Optional[str] = None,
    fileName: Optional[str] = None,
    allowsMultipleSelection: bool = False,
    fileTypes: Optional[str] = None,
) -> Union[str, CollectionType[str]]:
    """Display a dialog to get file or folder paths.

    :param message: The optional message to display in the dialog as a :class:`str`.
        Defaults to :obj:`None`.
    :param title: The optional title of the dialog window as a :class:`str`.
        Defaults to :obj:`None`.
    :param directory: The optional directory to start the dialog in as a :class:`str`.
        Defaults to :obj:`None`.
    :param fileName: The optional file name to start the dialog with as a :class:`str`.
        Defaults to :obj:`None`.
    :param allowsMultipleSelection: A flag to allow multiple file selection as
        a :class:`bool`. Defaults to :obj:`False`.
    :param fileTypes: The optional file types to filter the dialog with as
        a :class:`str`. Defaults to :obj:`None`.
    :return: A :class:`str` representing the path of the selected file or folder, 
        or a :class:`tuple` of paths if ``allowsMultipleSelection=True``.

    Example::

        >>> GetFileOrFolder()

    """
    return dispatcher["GetFileOrFolder"](
        message=message,
        title=title,
        directory=directory,
        fileName=fileName,
        allowsMultipleSelection=allowsMultipleSelection,
        fileTypes=fileTypes,
    )


def Message(
        message: str,
        title: Optional[str] = "FontParts",
        informativeText: Optional[str] = None) -> None:
    """Display a message dialog.

    :param message: The message to display in the dialog as a :class:`str`.
    :param title: The optional title of the dialog window as a :class:`str`.
        Defaults to ``"FontParts"``.
    :param informativeText: The optional additional informative text to display in the
        dialog as  a :class:`str`. Defaults to :obj`None`.

    Example::

        >>> Message("This is a message")

    """
    return dispatcher["Message"](
        message=message, title=title, informativeText=informativeText
    )


def PutFile(message: Optional[str] = None, fileName: Optional[str] = None) -> str:
    """Display a dialog to put a file.

    :param message: The optional message to display in the dialog as a :class:`str`.
        Defaults to :obj:`None`.
    :param fileName: The optional file name to start the dialog with as a :class:`str`.
        Defaults to :obj:`None`.
    :return: A :class:`str` representing the path of the selected file.

    Example::

        >>> PutFile()

    """
    return dispatcher["PutFile"](message=message, fileName=fileName)


def SearchList(
        items: CollectionType[str],
        message: Optional[str] = "Select an item:",
        title: Optional[str] = "FontParts"
) -> str:
    """Display a dialog to search a given list.

    :param items: The list of items to search as a :class:`list` of :class:`str`.
    :param message: The optional message to display in the dialog as a :class:`str`.
        Defaults to ``"Select an item:"``.
    :param title: The optional title of the dialog window as a :class:`str`.
        Defaults to ``"FontParts"``.
    :return: A :class:`str` representing the selected item.

    Example::

        >>> SearchList(["a", "b", "c"])

    """
    return dispatcher["SearchList"](items=items, message=message, title=title)


def SelectFont(
        message: Optional[str] = "Select a font:",
        title: Optional[str] = "FontParts",
        allFonts: Optional[CollectionType[str]] = None) -> str:
    """Display a dialog to select a font from all open fonts.

    :param message: The optional message to display in the dialog as a :class:`str`.
        Defaults to ``"Select a font:"``.
    :param title: The optional title of the dialog window as a :class:`str`.
        Defaults to ``"FontParts"``.
    :param allFonts: The optional list of all open fonts as a :class:`list` 
        of :class:`str`. Defaults to :obj:`None`.
    :return: A :class:`str` representing the selected font.

    Example::

        >>> SelectFont()

    """
    return dispatcher["SelectFont"](message=message, title=title, allFonts=allFonts)


def SelectGlyph(
    aFont: BaseFont,
    message: Optional[str] = "Select a glyph:",
    title: Optional[str] = "FontParts"
) -> str:
    """Display a dialog to select a glyph from a given font.

    :param aFont: The font to select a glyph from as a :class:`BaseFont`.
    :param message: The optional message to display in the dialog as a :class:`str`.
        Defaults to ``"Select a glyph:"``.
    :param title: The optional title of the dialog window as a :class:`str`.
        Defaults to ``"FontParts"``.
    :return: A :class:`str` representing the selected glyph.

    Example::

        >>> SelectGlyph(myFont)

    """
    return dispatcher["SelectGlyph"](aFont=aFont, message=message, title=title)


def ProgressBar(
        title: Optional[str] = "RoboFab...",
        ticks: Optional[int] = None,
        label: Optional[str] = None) -> None:
    """Display a progress bar dialog.

    :param title: The optional title of the dialog window as a :class:`str`.
        Defaults to ``"RoboFab..."``.
    :param ticks: The optional number of ticks to display in the progress bar as
        an :class:`int`. Defaults to :obj:`None`.
    :param label: The optional label to display in the progress bar as a :class:`str`.
        Defaults to :obj:`None`.

    Example::

        >>> bar = ProgressBar()
        ... # do something
        >>> bar.close()

    """
    return dispatcher["ProgressBar"](title=title, ticks=ticks, label=label)


# ----------
# Dispatcher
# ----------

dispatcher = _EnvironmentDispatcher(
    [
        "AskString",
        "AskYesNoCancel",
        "FindGlyph",
        "GetFile",
        "GetFolder",
        "GetFileOrFolder",
        "Message",
        "OneList",
        "PutFile",
        "SearchList",
        "SelectFont",
        "SelectGlyph",
        "ProgressBar",
    ]
)
