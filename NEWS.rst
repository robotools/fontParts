0.14.0 (released 2026-01-30)
---------------------------
- `glyph.round` now rounds image offset

0.13.4 (released 2026-01-20)
---------------------------
- Update dependencies to fix issue with tests of `booleanOperations`

0.13.3 (released 2025-08-14)
---------------------------
- Fix `.fromMathGlyph` for the issue of a guideline color coming from defcon, thanks @LettError. #851 #850

0.13.2 (released 2025-07-21)
---------------------------
- Fixed python syntax warning errors due to doc strings, thanks @bgermann. #849

0.13.1 (released 2025-06-11)
---------------------------
- `insertGlyph` will return the inserted glyph object. #727 & #841

0.12.8 (released 2025-06-04)
---------------------------
- Fix bug in `copyData`, #839. Thanks @knutergaard

0.12.7 (released 2025-05-30)
---------------------------
- Fix getting `color` and `name` in _fromMathGlyph`

0.12.6 (released 2025-05-27)
---------------------------
- Fix guideline normalization when value is `None`. See #834. Thanks @typemytype!

0.12.5 (released 2025-04-28)
---------------------------
- Upgrade `BaseDict` normalization. See #831

0.12.4 (released 2025-04-08)
---------------------------
- Mark `base.kerning` docstrings raw to avoid `SyntaxWarning`. See #830

0.12.3 (released 2024-11-08)
---------------------------
- Fixed `copyData` to copy, not link, subdata. See #758

0.12.2 (released 2024-08-07)
---------------------------
- Replace remaining usage of assertEquals with assertEqual. See #720
- Fixes/tweaks to documentation
- Get guidelines from the mathInfo object directly. See #738

0.12.1 (released 2023-10-30)
---------------------------
- Tweak to logic of `setStartSegment`

0.12.0 (released 2023-10-30)
---------------------------
- Fixes to `setStartSegment` so that it keeps the start point on-curve and prevents setting a setting a start segment on an open contour (issues #709 and #412). Thanks @typesupply!
- Fixes to docs and test setup. Boring things.

0.11.0 (released 2022-12-09)
---------------------------
- Expose the `mathGlyph` options. Thanks @typesupply! See #672
- Set defaultLayer to "public.default" when its available. Fixes issue #674. Thanks @typemytype! See #675.
- Add `info.update` to the info object. Thanks @typesupply! See #676

0.10.8 (released 2022-09-03)
---------------------------
- Adds `setStartPoint` to the contour object. Thanks @typemytype! See #668.

0.10.7 (released 2022-07-11)
---------------------------
- Small documentation update and fix for scm tools.

0.10.6 (released 2022-06-21)
---------------------------
- Adds `openFonts` (more than one font). Issue #545. (thanks @typesupply!)

0.10.5 (released 2022-05-10)
---------------------------
- Adds `glyph.autoContourOrder`. Issue #645. (thanks @roberto-arista!)
- Adds `FuzzyNumber` to `base.py`. Needed for the above, copied from defcon. (thanks @typemytype!)

0.10.4 (released 2022-03-17)
---------------------------
- Fixes issue with setting glyph name when copying. Issue #633. (thanks @typemytype!)

0.10.3 (released 2022-02-24)
---------------------------
- Fixes issue with `defaultLayer` and copying a `font`. Issue #630. (thanks @typemytype!)

0.10.2 (released 2022-01-05)
---------------------------
- Add vaidate kwarg to _loadFromGlyph #623. (thanks @ctrlcctrlv)

0.10.1 (released 2021-12-28)
---------------------------
- Update to use Collections.abc.Hashable by @benkiel in #622
- Start testing Python 3.10 by @benkiel in #619

0.10.0 (released 2021-12-28)
---------------------------
- 2021-12-28: Drops support for Python 3.6
- 2021-12-14: Adds tempLib, #615 (thanks @typemytype!)
- Improved docs with #605 and #607. Thanks @driehuis and @arrowtype!

0.9.11 (released 2021-08-06)
---------------------------
- 2021-08-06: Fixes inserting a segment with an open contour, #601 (thanks @typemytype!)

0.9.10 (released 2021-03-09)
---------------------------
- 2021-03-09: Update to Defcon 0.8.0 (thanks @justvanrossum!)

0.9.9 (released 2021-02-13)
---------------------------
- 2021-02-13: Fixed import of version. (#573, thanks @gyscos!)

0.9.8 (released 2021-02-12)
---------------------------
- 2021-02-11: Add support for quadratic curves with no on-curve points in Contour and Segment. (#572, thanks @typemytype!)

0.9.7 (released 2020-12-23)
---------------------------
- 2020-12-23: Change to github actions for CI and release.
- 2020-12-18: fontShell returns `None` when referenced file name doesn't exist for an `Image` (#567, thanks @typemytype)

0.9.6 (released 2020-09-06)
---------------------------
- 2020-09-06: fontShell has `changed()` implemented now

0.9.5 (released 2020-09-04)
---------------------------
- 2020-09-04: Fix for contours not getting updated in fontShell, thanks @justvanrossum!
- 2020-09-03: Fix for error message in normalizeKerningKey, thanks @colinmford!

0.9.4 (released 2020-08-26)
---------------------------
- Fixed release build

0.9.3 (released 2020-08-26)
---------------------------
- 2020-07-14: All rounding uses otRound. #536, fixes #533. Thanks @colinmford!
- 2019-12-23: Allow contour.segment to be empty (#480). Thanks @typemytype!
- 2020-01-08: Image file names now get a png file extension (#482). Thanks @typemytype!
- 2020-02-03: Fixed error in setting contour index (#488). Thanks @typemytype!
- 2020-02-10: Fixed error in PointPositionMixin (#486, fixed by #491)
- 2020-04-01: Added option to turn off normalizer tests
- 2020-04-07: Test fixes and updates. #512. Thanks @schriftgestalt!
- various: Documentation updates and corrections

0.9.2 (released 2019-12-10)
---------------------------
- 2019-12-10: No longer send or recieve images from math glyphs. (thanks @letterror)
- 2019-12-10: Removed unittest2 dependency.
- 2019-10-21: Only use copy in _appendContour only if there is an offset. (thanks @simoncozens)
- 2019-09-29: [fontshell] Accept pathLikeObjects for opening.

0.9.1 (released 2019-09-28)
---------------------------
- 2019-09-28: Change how `glyph.unicode` behaves. Instead of adding to `glyph.unicodes`, on a `set` it sets `glyph.unicodes` to the single value provided (or an empty list if the value was `None`.)
- 2019-09-23: Fix an error in world.py

0.9.0 (released 2019-08-30)
---------------------------
This release only supports Python 3, if you need Python 2 support, use 0.8.9.

- 2019-08-30: Remove Python 2 support.
- 2019-08-30: Change rounding to always round to the higher number, matching what fontTools does for anything visual.


0.8.9 (released 2019-08-25)
---------------------------
- 2019-08-25: Simplify `removeOverlap` in fontShell
- 2019-08-25: Fixup dev-requirements

Note: This will be one of the last releases to support Python2.

0.8.8 (released 2019-08-23)
---------------------------
- 2019-08-23: Fix `removeOverlap` and add `removeOverlap` to fontShell.
- 2019-07-23: Added support for `fileStructure`, for UFOZ.
- 2019-06-07: Allow first point of a contour to be smooth.

0.8.7 (released 2019-06-04)
---------------------------
- 2019-06-04: Change `RemovedWarning` to `RemovedError`
- 2019-03-26: Set the first layer in `layerOrder` as the default layer for `font.interpolate`
- 2019-03-18: A missing glyph in a `get` or `del` now returns `KeyError`

0.8.6 (released 2019-03-15)
---------------------------
- 2019-03-15: Fixed how `bPoint` reports curve types, tangents are now reported as curve.
- 2019-01-30: Fix `OpenFont` in fontShell.
- 2019-01-15: One more fix for RFont (thanks @madig!)

0.8.5 (released 2018-12-17)
---------------------------
- 2018-12-17: Improve glyph insert, only clear if the glyph is already in the font.
- 2018-12-17: Fix for `RFont` and `fs`
- 2018-12-14: Added a `getFlatKerning` method to `Font`. Thanks @typemytype
- 2018-12-14: Fixed glyph order being modified when a glyph is overwritten (thanks @justvanrossum for reporting, @typemytype for fixing)

0.8.4 (released 2018-12-07)
---------------------------
- 2018-12-7: Fixed `setStartSegment` (thanks @typemytype!)

0.8.3 (released 2018-12-05)
---------------------------
- 2018-12-05: `insertSegment` and `insertBPoint` fixed. (thanks @typemytype!)

0.8.2 (released 2018-11-02)
---------------------------
- 2018-11-01: Change to using fonttools.ufoLib
- 2018-10-16: Make compatibility checking for components and anchors more precise (WIP). Thank you @madig

0.8.1 (released 2018-09-20)
---------------------------
- 2018-09-20: Restyled the documentation, thanks @vannavu and @thundernixon
- 2018-09-12: Fixed Travis setup for OSX.
- 2018-09-06: All tests for ``Groups``.
- 2018-09-03: Fixed ``font.round()``.
- 2018-08-30: All tests for ``Image``.

0.8.0 (released 2018-08-21)
---------------------------

- 2018-08-21: Changed behavior of getting margins for empty (no outlines or components) glyphs, now returns `None`. `#346 <https://github.com/robofab-developers/fontParts/pull/346>`_
- 2018-08-20: Add public methods to `mathInfo` in the Info object. `#344 <https://github.com/robofab-developers/fontParts/pull/344>`_

0.7.2 (released 2018-08-03)
---------------------------

- 2018-08-03: Allow contours to start and end on an offCurve. `#337 <https://github.com/robofab-developers/fontParts/pull/337>`_

0.7.1 (released 2018-08-02)
---------------------------

- 2018-07-24: Fixed bug in default values in ``BaseDict``. This fixes a bug with default values in ``Kerning`` and ``Groups``.
- 2018-06-28: Improved documentation for ``world.AllFonts``
- 2018-06-20: Fixed a bug in ``world.AllFonts``
- 2018-06-14: Fixed a bug, UFO file format version must be an ``int``.

0.7.0 (released 2018-06-11)
---------------------------

- 2018-06-08: Fixed a bug in ``__bool__`` in ``Image`` that would fail if there was no image data.
- 2018-06-08: Fixed a bug in setting the parents in appending a ``guideline`` to a ``Glyph`` or ``Font``.
- 2018-05-30: Fixed a bug in both the base and fontshell implementations of ``groups.side1KerningGroups``.
- 2018-05-30: Fixed a bug in both the base and fontshell implementations of ``groups.side2KerningGroups``.
- 2018-05-30: Fixed a several bugs in ``BaseDict`` that would return values that hadn't been normalized.
- 2018-05-30: Implemented ``font.__delitem__``
- 2018-05-30: Implemented ``font.__delitem__``.
- 2018-05-30: Implemented ``layer.__delitem__``.
- 2018-05-30: ``font.removeGlyph`` is now an alias for ``font.__delitem__``.
- 2018-05-30: ``layer.removeGlyph`` is now an alias for ``layer.__delitem__``.
- 2018-05-30: ``font.insertGlyph`` is now an alias for ``font.__setitem__``.
- 2018-05-30: ``layer.insertGlyph`` is now an alias for ``layer.__setitem__``.
- 2018-05-30: ``font.appendGuideline`` now accepts a guideline object.
- 2018-05-30: ``glyph.copy`` uses the new append API.
- 2018-05-30: ``glyph.appendGlyph`` uses the new append API.
- 2018-05-30: ``glyph.appendComponent`` now accepts a component object.
- 2018-05-30: ``glyph.appendAnchor`` now accepts and anchor object.
- 2018-05-30: ``glyph.appendGuideline`` now accepts a guideline object.
- 2018-05-30: ``contour.appendSegment`` now accepts a segment object.
- 2018-05-30: ``contour.appendBPoint`` now accepts a bPoint object.
- 2018-05-30: ``contour.appendPoint``  now accepts a point object.
- 2018-05-30: ``contour.insertSegment`` now accepts a segment object.
- 2018-05-30: ``contour.insertBPoint`` now accepts a bPoint object.
- 2018-05-30: ``contour.insertPoint`` now accepts a point object.
