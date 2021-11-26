# POJ Modifications

To fully support Pe̍h-ōe-jī, horizontal advance after any letters containing the glyph `uni0358` (dot above right, called`dotabovert` in this script) must be extended. Contextual kerning does not seem to work in the browser, so we have added separate precomposed characters for all possibilities. We have also added `uni030D` (`verticallinecmb`), plus a precomposed `o + 030D + 0358` to ensure correct horizontal advance for this letter. Ibreve and Udieresisbelow are not currently included in Source Serif, and while they can be produced with combining marks we have included separate glyphs for best results. Finally, we added the `N.sups.sc` glyph to support proper small caps in Pe̍h-ōe-jī. The total set of new glyphs is:

```
# Roman & Italic
Ibreve Ibreve
ibreve ibreve
uni1E72 Udieresisbelow
uni1E73 udieresisbelow
uni030D verticallinecmb
uni030D.cap verticallinecmb.cap
uni0358 dotabovertcmb
uni0358.cap dotabovertcmb.cap
uni004F030D Overticalline
uni004F0358 Odotabovert
uni00D20358 Odotabovertgrave
uni00D30358 Odotabovertacute
uni00D40358 Odotabovertcircumflex
uni014C0358 Odotabovertmacron
uni014E0358 Odotabovertbreve
uni01D10358 Odotabovertcaron
uni006F030D overticalline
uni006F0358 odotabovert
uni00F20358 odotabovertgrave
uni00F30358 odotabovertacute
uni00F40358 odotabovertcircumflex
uni014D0358 odotabovertmacron
uni014F0358 odotabovertbreve
uni01D20358 odotabovertcaron
uni006F030D0358 odotabovertverticalline

# Roman only
Ibreve.sc Ibreve.sc
uni1E72.sc Udieresisbelow.sc
uni004F030D.sc Overticalline.sc
uni004F0358.sc Odotabovert.sc
uni00D20358.sc Odotabovertgrave.sc
uni00D30358.sc Odotabovertacute.sc
uni00D40358.sc Odotabovertcircumflex.sc
uni014C0358.sc Odotabovertmacron.sc
uni014E0358.sc Odotabovertbreve.sc
uni01D10358.sc Odotabovertcaron.sc
uni004F030D0358.sc Odotabovertverticalline.sc
N.sups.sc   N.sups.sc
```

We also added `N.sups.sc` glyphs for each Roman font into a folder at the top level, because `fontforge` seems to be broken at the moment (see note in the script).

The main script is `build-poj.py`, which adds the above glyphs to every file (Roman & Italic, Instances & Masters). The only manual labor is deciding the position of the `dotabovert` component for each font, the data are marked in the `ODotOffsets` table of the script.

We added a script to run `checkoutlinesufo` and `psautohint` on each font before building. We also have to rename the fonts from `Source` to `Chuigoan`. So the full build command is now:

```
python build-poj.py
./build-checkoutlines.sh
./build.sh
./buildVFs.sh
python rename.py
./build-woffs.sh
```

# Source Serif

[Source Serif](https://adobe-fonts.github.io/source-serif/) is an open-source typeface to complement the [Source Sans](https://github.com/adobe-fonts/source-sans-pro) family.


## Getting Involved

Please [open an issue](https://github.com/adobe-fonts/source-serif/issues) to start the discussion.

## Releases

* [Latest release](../../releases/latest)
* [All releases](../../releases)


## Building the fonts from source

### Requirements

To build the binary font files from source, you need to have the [Adobe Font Development Kit for OpenType](https://github.com/adobe-type-tools/afdko/) (AFDKO) installed.

### Building one font

The key to building OTF fonts is `makeotf`, which is part of the AFDKO toolkit. Information and usage instructions can be found by executing `makeotf -h`. TTFs are generated with the `otf2ttf` and `ttfcomponentizer` tools.

Commands to build the Regular style OTF font:

```sh
$ cd /Roman/Instances/Text/Regular
$ makeotf -r
```

Commands to generate the Regular style TTF font:

```sh
$ otf2ttf SourceSerifPro-Regular.otf
$ ttfcomponentizer SourceSerifPro-Regular.ttf
```

### Building all static fonts

For convenience, a shell script named **build.sh** is provided in the root directory. It builds all OTFs and TTFs, and can be executed by typing:

```sh
$ ./build.sh
```

### Building variable fonts

To build the variable TTFs you must install **fontmake**:

```sh
$ pip install fontmake
```

A shell script named **buildVFs.sh** is provided in the root directory.
It generates four variable fonts (two CFF2-OTFs and two TTFs), and can be executed by typing:

```sh
$ ./buildVF.sh
```


