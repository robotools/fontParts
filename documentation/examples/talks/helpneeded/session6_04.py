# robothon06
# ask for a folder
# find (nested) fontlab files in the folder
# open the fonts
# Demonstrates: recursive function,, dialog, os module

import os.path
from fontParts.interface.all.dialogs import GetFolder
from fontParts.world import OpenFont

# this function looks for fontlab files in a folder
def walk(someFolder, extension):
    extension = extension.lower()
    files = []
    # the os module has tools to deal with
    # the operating system. This returns a list of names
    # of stuff in the folder you feed it:
    names = os.listdir(someFolder)
    for n in names:
            p = os.path.join(someFolder, n)
            # if this new thing is a folder itself,
            # call this function again, but now with the
            # new path to check that as well. This is
            # called recursion.
            if os.path.isdir(p):
                # add the results of the other folder
                # to the list
                files += walk(p, extension)
                continue
            # is it a file with the extension we want?
            # add it then!
            if n.lower().find(extension) != -1:
                files.append(p)
    return files

yourFolder = GetFolder("Search a folder:")
if yourFolder is not None:
    fontPaths = walk(yourFolder, ".vfb")
    for path in fontPaths:
        OpenFont(path)
