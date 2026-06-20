import unittest
import collections
import tempfile
import os
import shutil
from unittest.mock import PropertyMock, patch
from fontTools.ufoLib import DEFAULT_LAYER_NAME


class TestFont(unittest.TestCase):
    # ------
    # Layers
    # ------

    def getFont_layers(self):
        font, _ = self.objectGenerator("font")
        for name in "ABCD":
            font.newLayer("layer " + name)
        return font

    def test_getLayer_unknown(self):
        font = self.getFont_layers()
        with self.assertRaises(ValueError):
            font.getLayer("There is no layer with this name.")

    def test_removeLayer(self):
        font, _ = self.objectGenerator("font")
        layer = font.newLayer("testLayer")
        self.assertIn(layer, font.layers)
        font.removeLayer("testLayer")
        self.assertNotIn(layer, font.layers)
        with self.assertRaises(ValueError):
            font.removeLayer("testLayer")

    def test_insertLayer(self):
        font, _ = self.objectGenerator("font")
        layer, _ = self.objectGenerator("layer")
        layer.name = "oldName"
        insertedLayer = font.insertLayer(layer, name="newName")
        self.assertEqual(insertedLayer.name, "newName")
        self.assertIn("newName", font.layerOrder)

    def test_insertLayer_name_none(self):
        font, _ = self.objectGenerator("font")
        layer, _ = self.objectGenerator("layer")
        layer.name = "testLayer"
        font.insertLayer(layer, name=None)
        self.assertIn(layer.name, font.layerOrder)

    def test_insertLayer_name_exists(self):
        font, _ = self.objectGenerator("font")
        existingLayer = font.newLayer("existingLayer")
        self.assertIn(existingLayer.name, font.layerOrder)
        newLayer, _ = self.objectGenerator("layer")
        newLayer.name = "newLayer"
        font.insertLayer(newLayer, name=existingLayer.name)
        self.assertIn(existingLayer.name, font.layerOrder)

    def test_dublicateLayer(self):
        font, _ = self.objectGenerator("font")
        existingLayer = font.newLayer("testLayer")
        self.assertIn(existingLayer.name, font.layerOrder)
        duplicatedLayer = font.duplicateLayer(existingLayer.name, "duplicateLayer")
        self.assertIn(duplicatedLayer.name, font.layerOrder)

    def test_duplicateLayer_layerName_missing(self):
        font, _ = self.objectGenerator("font")
        with self.assertRaises(ValueError):
            font.duplicateLayer("missingName", "duplicateLayer")

    def test_duplicateLayer_newLayerName_exists(self):
        font, _ = self.objectGenerator("font")
        existingLayer = font.newLayer("testLayer")
        duplicateLayer = font.newLayer("duplicateLayer")
        with self.assertRaises(ValueError):
            font.duplicateLayer(existingLayer.name, duplicateLayer.name)

    def test_swapLayerNames(self):
        font, _ = self.objectGenerator("font")
        layer1 = font.newLayer("layer1")
        layer2 = font.newLayer("layer2")
        font.swapLayerNames(layer1.name, layer2.name)
        self.assertEqual(layer1.name, "layer2")
        self.assertEqual(layer2.name, "layer1")

    def test_swapLayerNames_names_missing(self):
        font, _ = self.objectGenerator("font")
        layer = font.newLayer("testLayer")
        testCases = [("missingLayer", layer.name), (layer.name, "missingLayer")]
        for name1, name2 in testCases:
            with self.assertRaises(ValueError):
                font.swapLayerNames(name1, name2)

    # ------
    # Glyphs
    # ------

    def getFont_glyphs(self):
        font, _ = self.objectGenerator("font")
        for name in "ABCD":
            font.newGlyph(name)
        return font

    def getFont_guidelines(self):
        font, _ = self.objectGenerator("font")
        font.appendGuideline((1, 2), 0, "Test Guideline 1")
        font.appendGuideline((3, 4), 90, "Test Guideline 2")
        return font

    def test_appendGuideline_valid_object(self):
        font, _ = self.objectGenerator("font")
        src, _ = self.objectGenerator("guideline")
        src.position = (1, 2)
        src.angle = 123
        src.name = "test"
        src.color = (1, 1, 1, 1)
        src.getIdentifier()
        dst = font.appendGuideline(guideline=src)
        self.assertNotEqual(src, dst)
        self.assertEqual(src.position, dst.position)
        self.assertEqual(src.angle, dst.angle)
        self.assertEqual(src.name, dst.name)
        self.assertEqual(src.color, dst.color)
        self.assertEqual(src.identifier, dst.identifier)

    # glyphOrder

    def test_glyphOrder(self):
        font = self.getFont_glyphs()
        expectedGlyphOrder = ["A", "B", "C", "D"]
        self.assertEqual(font.glyphOrder, tuple(expectedGlyphOrder))
        # reverse the excepected glyph order and set it
        expectedGlyphOrder.reverse()
        font.glyphOrder = expectedGlyphOrder
        self.assertEqual(font.glyphOrder, tuple(expectedGlyphOrder))
        # add a glyph
        expectedGlyphOrder.append("newGlyph")
        font.newGlyph("newGlyph")
        self.assertEqual(font.glyphOrder, tuple(expectedGlyphOrder))
        # remove a glyph
        expectedGlyphOrder.remove("newGlyph")
        del font["newGlyph"]
        self.assertEqual(font.glyphOrder, tuple(expectedGlyphOrder))
        # insert a glyph, where the glyph is at the beginning of the glyph order
        glyph, _ = self.objectGenerator("glyph")
        font["D"] = glyph
        self.assertEqual(font.glyphOrder, tuple(expectedGlyphOrder))
        # insert a glyph, where the glyph is at the end of the glyph order
        glyph, _ = self.objectGenerator("glyph")
        font["A"] = glyph
        self.assertEqual(font.glyphOrder, tuple(expectedGlyphOrder))

    # len

    def test_len_initial(self):
        font = self.getFont_glyphs()
        self.assertEqual(len(font), 4)

    def test_len_two_layers(self):
        font = self.getFont_glyphs()
        layer = font.newLayer("test")
        layer.newGlyph("X")
        self.assertEqual(len(font), 4)

    # insert glyphs

    def test_insertGlyph(self):
        font, _ = self.objectGenerator("font")
        glyph, _ = self.objectGenerator("glyph")
        font.insertGlyph(glyph, "inserted1")
        self.assertIn("inserted1", font)
        font["inserted2"] = glyph
        self.assertIn("inserted2", font)
        font.newGlyph("A")
        glyph.unicode = 123
        font["A"] = glyph
        self.assertEqual(font["A"].unicode, 123)

    # add glyphs

    def test_newGlyph_rename(self):
        layer = self.getFont_glyphs()

        layer.newGlyph("A", clear=False, rename=True)
        layer.newGlyph("A", clear=False, rename=True)

        self.assertIn("A", layer)
        self.assertIn("A.1", layer)
        self.assertIn("A.2", layer)

    # ----------
    # Guidelines
    # ----------

    def test_appendGuideline_position(self):
        font = self.getFont_guidelines()
        initialLength = len(font.guidelines)
        font.appendGuideline(position=(0, 0))
        self.assertEqual(len(font.guidelines), initialLength + 1)
        self.assertEqual(font.guidelines[-1].position, (0, 0))

    def test_appendGuideline_overrides(self):
        font = self.getFont_guidelines()
        guideline, _ = self.objectGenerator("guideline")
        guideline.position = (0, 0)
        initialLength = len(font.guidelines)
        font.appendGuideline(
            position=(10, 10),
            angle=1,
            name="test",
            color=(1, 1, 1, 1),
            guideline=guideline,
        )
        self.assertEqual(len(font.guidelines), initialLength + 1)
        self.assertEqual(font.guidelines[-1].position, (10, 10))
        self.assertEqual(font.guidelines[-1].angle, 1)
        self.assertEqual(font.guidelines[-1].name, "test")
        self.assertEqual(font.guidelines[-1].color, (1, 1, 1, 1))

    def test_appendGuideline_raises(self):
        font = self.getFont_guidelines()
        with self.assertRaises(ValueError):
            font.appendGuideline(position=None)

    def test_clearGuideline(self):
        font = self.getFont_guidelines()
        font.clearGuidelines()
        self.assertEqual(font.guidelines, ())

    # ----
    # flatKerning
    # ----

    def test_flatKerning(self):
        font = self.getFont_glyphs()
        # glyph, glyph kerning
        font.kerning["A", "V"] = -100
        font.kerning["V", "A"] = -200
        expected = {("A", "V"): -100, ("V", "A"): -200}
        self.assertEqual(font.getFlatKerning(), expected)
        # add some groups
        font.groups["public.kern1.O"] = ["O", "Ograve"]
        font.groups["public.kern2.O"] = ["O", "Ograve"]
        # group, group kerning
        font.kerning["public.kern1.O", "public.kern2.O"] = -50
        expected = {
            ("O", "O"): -50,
            ("Ograve", "O"): -50,
            ("O", "Ograve"): -50,
            ("Ograve", "Ograve"): -50,
            ("A", "V"): -100,
            ("V", "A"): -200,
        }
        self.assertEqual(font.getFlatKerning(), expected)
        # glyph, group exception
        font.kerning["O", "public.kern2.O"] = -30
        expected = {
            ("O", "O"): -30,
            ("Ograve", "O"): -50,
            ("O", "Ograve"): -30,
            ("Ograve", "Ograve"): -50,
            ("A", "V"): -100,
            ("V", "A"): -200,
        }
        self.assertEqual(font.getFlatKerning(), expected)
        # glyph, glyph exception
        font.kerning["O", "Ograve"] = -70
        expected = {
            ("O", "O"): -30,
            ("Ograve", "O"): -50,
            ("O", "Ograve"): -70,
            ("Ograve", "Ograve"): -50,
            ("A", "V"): -100,
            ("V", "A"): -200,
        }
        self.assertEqual(font.getFlatKerning(), expected)

    # ----
    # Hash
    # ----

    def test_hash_same_object(self):
        font_one = self.getFont_glyphs()
        self.assertEqual(hash(font_one), hash(font_one))

    def test_hash_different_object(self):
        font_one = self.getFont_glyphs()
        font_two = self.getFont_glyphs()
        self.assertNotEqual(hash(font_one), hash(font_two))

    def test_hash_same_object_variable_assignment(self):
        font_one = self.getFont_glyphs()
        a = font_one
        self.assertEqual(hash(font_one), hash(a))

    def test_hash_different_object_variable_assignment(self):
        font_one = self.getFont_glyphs()
        font_two = self.getFont_glyphs()
        a = font_one
        self.assertNotEqual(hash(font_two), hash(a))

    def test_hash_is_hasbable(self):
        font_one = self.getFont_glyphs()
        self.assertEqual(isinstance(font_one, collections.abc.Hashable), True)

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        font_one = self.getFont_glyphs()
        self.assertEqual(font_one, font_one)

    def test_object_not_equal_other(self):
        font_one = self.getFont_glyphs()
        font_two = self.getFont_glyphs()
        self.assertNotEqual(font_one, font_two)

    def test_object_equal_self_variable_assignment(self):
        font_one = self.getFont_glyphs()
        a = font_one
        a.newGlyph("XYZ")
        self.assertEqual(font_one, a)

    def test_object_not_equal_other_variable_assignment(self):
        font_one = self.getFont_glyphs()
        font_two = self.getFont_glyphs()
        a = font_one
        self.assertNotEqual(font_two, a)

    # ---------
    # Selection
    # ---------

    # Font

    def test_selected_true(self):
        font = self.getFont_glyphs()
        try:
            font.selected = False
        except NotImplementedError:
            return
        font.selected = True
        self.assertEqual(font.selected, True)

    def test_selected_false(self):
        font = self.getFont_glyphs()
        try:
            font.selected = False
        except NotImplementedError:
            return
        self.assertEqual(font.selected, False)

    # Layers

    def test_selectedLayer_default(self):
        font = self.getFont_layers()
        try:
            font.defaultLayer.selected = False
        except NotImplementedError:
            return
        self.assertEqual(font.selectedLayers, ())

    def test_selectedLayer_setSubObject(self):
        font = self.getFont_layers()
        try:
            font.defaultLayer.selected = False
        except NotImplementedError:
            return
        layer1 = font.getLayer("layer A")
        layer2 = font.getLayer("layer B")
        layer1.selected = True
        layer2.selected = True
        self.assertEqual(font.selectedLayers, (layer1, layer2))

    def test_selectedLayer_setFilledList(self):
        font = self.getFont_layers()
        try:
            font.defaultLayer.selected = False
        except NotImplementedError:
            return
        layer3 = font.getLayer("layer C")
        layer4 = font.getLayer("layer D")
        font.selectedLayers = [layer3, layer4]
        self.assertEqual(font.selectedLayers, (layer3, layer4))

    def test_selectedLayer_setEmptyList(self):
        font = self.getFont_layers()
        try:
            font.defaultLayer.selected = False
        except NotImplementedError:
            return
        layer1 = font.getLayer("layer A")
        layer1.selected = True
        font.selectedLayers = []
        self.assertEqual(font.selectedLayers, ())

    # Glyphs

    def test_selectedGlyphs_default(self):
        font = self.getFont_glyphs()
        try:
            font.defaultLayer.selected = False
        except NotImplementedError:
            return
        self.assertEqual(font.selectedGlyphs, ())

    def test_selectedGlyphs_setSubObject(self):
        font = self.getFont_glyphs()
        try:
            font.defaultLayer.selected = False
        except NotImplementedError:
            return
        glyph1 = font["A"]
        glyph2 = font["B"]
        glyph1.selected = True
        glyph2.selected = True
        self.assertEqual(
            tuple(sorted(font.selectedGlyphs, key=lambda glyph: glyph.name)),
            (glyph1, glyph2),
        )

    def test_selectedGlyphs_setFilledList(self):
        font = self.getFont_glyphs()
        try:
            font.defaultLayer.selected = False
        except NotImplementedError:
            return
        glyph3 = font["C"]
        glyph4 = font["D"]
        font.selectedGlyphs = [glyph3, glyph4]
        self.assertEqual(
            tuple(sorted(font.selectedGlyphs, key=lambda glyph: glyph.name)),
            (glyph3, glyph4),
        )

    def test_selectedGlyphs_setEmptyList(self):
        font = self.getFont_glyphs()
        try:
            font.defaultLayer.selected = False
        except NotImplementedError:
            return
        glyph1 = font["A"]
        glyph1.selected = True
        font.selectedGlyphs = []
        self.assertEqual(font.selectedGlyphs, ())

    # Glyph names

    def test_selectedGlyphNames_default(self):
        font = self.getFont_glyphs()
        try:
            font.defaultLayer.selected = False
        except NotImplementedError:
            return
        self.assertEqual(font.selectedGlyphs, ())

    def test_selectedGlyphNames_setSubObject(self):
        font = self.getFont_glyphs()
        try:
            font.defaultLayer.selected = False
        except NotImplementedError:
            return
        glyph1 = font["A"]
        glyph2 = font["B"]
        glyph1.selected = True
        glyph2.selected = True
        self.assertEqual(tuple(sorted(font.selectedGlyphNames)), ("A", "B"))

    def test_selectedGlyphNames_setFilledList(self):
        font = self.getFont_glyphs()
        try:
            font.defaultLayer.selected = False
        except NotImplementedError:
            return
        font.selectedGlyphNames = ["C", "D"]
        self.assertEqual(tuple(sorted(font.selectedGlyphNames)), ("C", "D"))

    def test_selectedGlyphNames_setEmptyList(self):
        font = self.getFont_glyphs()
        try:
            font.defaultLayer.selected = False
        except NotImplementedError:
            return
        glyph1 = font["A"]
        glyph1.selected = True
        font.selectedGlyphNames = []
        self.assertEqual(font.selectedGlyphNames, ())

    # Guidelines

    def test_selectedGuidelines_default(self):
        font = self.getFont_guidelines()
        guideline1 = font.guidelines[0]
        try:
            guideline1.selected = False
        except NotImplementedError:
            return
        self.assertEqual(font.selectedGuidelines, ())

    def test_selectedGuidelines_setSubObject(self):
        font = self.getFont_guidelines()
        guideline1 = font.guidelines[0]
        guideline2 = font.guidelines[1]
        try:
            guideline1.selected = False
        except NotImplementedError:
            return
        guideline2.selected = True
        self.assertEqual(font.selectedGuidelines, (guideline2,))

    def test_selectedGuidelines_setFilledList(self):
        font = self.getFont_guidelines()
        guideline1 = font.guidelines[0]
        guideline2 = font.guidelines[1]
        try:
            guideline1.selected = False
        except NotImplementedError:
            return
        font.selectedGuidelines = [guideline1, guideline2]
        self.assertEqual(font.selectedGuidelines, (guideline1, guideline2))

    def test_selectedGuidelines_setEmptyList(self):
        font = self.getFont_guidelines()
        guideline1 = font.guidelines[0]
        try:
            guideline1.selected = True
        except NotImplementedError:
            return
        font.selectedGuidelines = []
        self.assertEqual(font.selectedGuidelines, ())

    # ---------------
    # File Operations
    # ---------------

    # save

    def _saveFontPath(self, ext):
        root = tempfile.mkdtemp()
        return os.path.join(root, f"test{ext}")

    def _tearDownPath(self, path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)

    def _save(self, testCallback, **kwargs):
        path = self._saveFontPath(".ufo")
        font = self.getFont_glyphs()
        font.save(path, **kwargs)
        font.close()
        testCallback(path)
        self._tearDownPath(path)

    def test_save(self):
        def testCases(path):
            self.assertTrue(os.path.exists(path) and os.path.isdir(path))

        self._save(testCases)

    def test_save_formatVersion(self):
        from fontTools.ufoLib import UFOReader

        for version in [
            2,
            3,
        ]:  # fails on formatVersion 1 (but maybe we should not worry about it...)

            def testCases(path):
                reader = UFOReader(path)
                self.assertEqual(reader.formatVersion, version)

            self._save(testCases, formatVersion=version)

    def test_save_fileStructure(self):
        from fontTools.ufoLib import UFOReader, UFOFileStructure

        for fileStructure in [None, "package", "zip"]:

            def testCases(path):
                reader = UFOReader(path)
                expectedFileStructure = fileStructure
                if fileStructure is None:
                    expectedFileStructure = UFOFileStructure.PACKAGE
                else:
                    expectedFileStructure = UFOFileStructure(fileStructure)
                self.assertEqual(reader.fileStructure, expectedFileStructure)

            self._save(testCases, fileStructure=fileStructure)

    def test_save_path_none(self):
        font = self.getFont_glyphs()
        with self.assertRaises(OSError):
            font.save(path=None)

    # copy

    def test_copy(self):
        font = self.getFont_glyphs()
        copy = font.copy()
        self.assertCountEqual(font.keys(), copy.keys())

        font = self.getFont_glyphs()
        font.defaultLayer.name = "hello"
        copy = font.copy()
        self.assertCountEqual(font.keys(), copy.keys())
        self.assertEqual(font.defaultLayerName, copy.defaultLayerName)

        font = self.getFont_guidelines()
        copy = font.copy()
        self.assertEqual(copy.selectedGuidelines, font.selectedGuidelines)

    # generate

    def test_generateFormatToExtension(self):
        font, _ = self.objectGenerator("font")
        cases = [
            ("macttf", ".ttf"),
            ("macttdfont", ".dfont"),
            ("otfcff", ".otf"),
            ("otfttf", ".ttf"),
            ("ufo1", ".ufo"),
            ("ufo2", ".ufo"),
            ("ufo3", ".ufo"),
            ("unixascii", ".pfa"),
        ]
        for fmt, expected_ext in cases:
            with self.subTest(format=fmt):
                result = font.generateFormatToExtension(fmt, fallbackFormat=".fallback")
                self.assertEqual(result, expected_ext)

    def test_generate_format_none(self):
        font = self.getFont_glyphs()
        with self.assertRaises(ValueError):
            font.generate(format=None)

    def test_generate_invalid_format_type(self):
        font = self.getFont_glyphs()
        with self.assertRaises(TypeError):
            font.generate(format=0)

    def test_generate_valid_environmentOption(self):
        import warnings

        font = self.getFont_glyphs()
        with (
            patch.object(
                type(font), "_isValidGenerateEnvironmentOption"
            ) as mockValidate,
            patch.object(type(font), "_generate") as mockGenerate,
        ):
            mockValidate.return_value = True
            with warnings.catch_warnings():
                warnings.simplefilter("error", UserWarning)
                font.generate("otfcff", path="/mock/path.otf", valid_opt="value")

            mockGenerate.assert_called_once_with(
                format="otfcff",
                path="/mock/path.otf",
                environmentOptions={"valid_opt": "value"},
            )

    def test_generate_invalid_environmentOption(self):
        font = self.getFont_glyphs()
        with (
            patch.object(
                type(font), "_isValidGenerateEnvironmentOption"
            ) as mockValidate,
            patch.object(type(font), "_generate") as mockGenerate,
        ):
            mockValidate.return_value = False
            with self.assertWarns(UserWarning):
                font.generate("otfcff", path="/mock/path.otf", invalid_opt="value")

            mockGenerate.assert_called_once_with(
                format="otfcff",
                path="/mock/path.otf",
                environmentOptions={"invalid_opt": "value"},
            )

    def test_generate_path_none_and_self_path_none(self):
        font = self.getFont_glyphs()
        with patch.object(
            type(font), "_isValidGenerateEnvironmentOption"
        ) as mockValidate:
            mockValidate.return_value = True
            with self.assertRaises(OSError):
                font.generate("otfcff", path=None)

    def test_generate_path_none(self):
        font = self.getFont_glyphs()
        with (
            patch.object(type(font), "path", new_callable=PropertyMock) as mockPath,
            patch.object(type(font), "_generate") as mockGenerate,
        ):
            mockPath.return_value = "/src/myfont.otf"
            font.generate("otfcff", path=None)
            expectedPath = os.path.abspath("/src/myfont.otf")
            mockGenerate.assert_called_once()
            actualPath = mockGenerate.call_args[1]["path"]
            self.assertEqual(
                os.path.normpath(actualPath), os.path.normpath(expectedPath)
            )

    def test_generate_path_is_dir_and_self_path_none(self):
        font = self.getFont_glyphs()
        with (
            patch.object(type(font), "path", new_callable=PropertyMock) as mockPath,
            patch.object(os.path, "isdir") as mockIsDir,
        ):
            mockPath.return_value = None
            mockIsDir.return_value = True
            with self.assertRaises(OSError):
                font.generate("otfcff", path="/output/dir")

    def test_generate_path_is_dir(self):
        font = self.getFont_glyphs()
        with (
            patch.object(type(font), "path", new_callable=PropertyMock) as mockPath,
            patch.object(os.path, "isdir") as mockIsDir,
            patch.object(type(font), "_generate") as mockGenerate,
        ):
            mockPath.return_value = "/src/myfont.ufo"
            mockIsDir.return_value = True
            font.generate("otfcff", path="/output/dir")
            expectedPath = os.path.abspath(os.path.join("/output/dir", "myfont.otf"))
            actualPath = mockGenerate.call_args[1]["path"]
            self.assertEqual(
                os.path.normpath(actualPath), os.path.normpath(expectedPath)
            )

    # -----------------
    # Global Operations
    # -----------------

    def test_round(self):
        font, _ = self.objectGenerator("font")
        font.info.xHeight = 450.6
        font.kerning[("A", "V")] = -20.3
        guideline = font.appendGuideline((100.4, 200.7), 0)
        defaultLayer = font.defaultLayer
        glyph = defaultLayer.newGlyph("A")
        glyph.width = 600.8
        font.round()
        self.assertEqual(font.info.xHeight, 451)
        self.assertEqual(font.kerning[("A", "V")], -20)
        self.assertEqual(guideline.position, (100, 201))
        self.assertEqual(glyph.width, 601)

    def test_autoUnicodes(self):
        pass

    # -------------
    # Interpolation
    # -------------

    def test_interpolate(self):
        dstFont, _ = self.objectGenerator("font")
        minFont, _ = self.objectGenerator("font")
        maxFont, _ = self.objectGenerator("font")
        minFont.info.ascender = 100
        minFont.kerning[("A", "V")] = -20
        minLayer = minFont.getLayer(minFont.defaultLayer.name)
        minGlyph = minLayer.newGlyph("A")
        minGlyph.width = 100
        maxFont.info.ascender = 200
        maxFont.kerning[("A", "V")] = -120
        maxLayer = maxFont.getLayer(maxFont.defaultLayer.name)
        maxGlyph = maxLayer.newGlyph("A")
        maxGlyph.width = 200
        dstFont.interpolate(0.5, minFont, maxFont, round=True)
        self.assertEqual(dstFont.info.ascender, 150)
        self.assertEqual(dstFont.kerning[("A", "V")], -70)
        self.assertIn("A", dstFont)
        self.assertEqual(dstFont["A"].width, 150)

    def test_interpolate_invalid_types(self):
        dstFont, _ = self.objectGenerator("font")
        srcFont, _ = self.objectGenerator("font")
        maxFont, _ = self.objectGenerator("font")
        testCases = [
            (0.5, srcFont, "ivalidFontObject"),
            (0.5, "ivalidFontObject", srcFont),
        ]
        for factor, minFont, maxFont in testCases:
            with self.assertRaises(TypeError):
                dstFont.interpolate(factor, minFont, maxFont)

    def test_interpolate_asymmetric_layers(self):
        dstFont, _ = self.objectGenerator("font")
        minFont, _ = self.objectGenerator("font")
        maxFont, _ = self.objectGenerator("font")
        minFont.newLayer("testLayer")
        dstFont.interpolate(0.5, minFont, maxFont)
        self.assertNotIn("testLayer", dstFont.layerOrder)
        self.assertIn(DEFAULT_LAYER_NAME, dstFont.layerOrder)

    @patch("fontParts.base.font.ufoLib.DEFAULT_LAYER_NAME", "invalid.default.layer")
    def test_interpolate_missing_default_layer(self):
        dstFont, _ = self.objectGenerator("font")
        minFont, _ = self.objectGenerator("font")
        maxFont, _ = self.objectGenerator("font")
        dstFont.newLayer("testLayer")
        dstFont.interpolate(0.5, minFont, maxFont)
        self.assertEqual(dstFont.defaultLayer.name, dstFont.layerOrder[0])

    def test_interpolate_global_guidelines(self):
        interpolated_font, _ = self.objectGenerator("font")
        font_min, _ = self.objectGenerator("font")
        font_min.appendGuideline(position=(0, 0), angle=0)
        font_max, _ = self.objectGenerator("font")
        font_max.appendGuideline(position=(200, 200), angle=0)
        interpolated_font.info.interpolate(
            0.5, font_min.info, font_max.info, round=True
        )
        self.assertEqual(len(interpolated_font.guidelines), 1)
        self.assertEqual(interpolated_font.guidelines[0].position, (100, 100))
