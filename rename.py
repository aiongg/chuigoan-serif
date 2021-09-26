'''
Replace names in Source Serif font binaries using fontTools
from https://github.com/adobe-fonts/source-serif/issues/40#issuecomment-927284209
'''

import pathlib
import sys
from fontTools import ttLib

copyright_text = "© 2021 Aiong Taigi (http://https://github.com/aiongg/chuigoan-serif), modified from Adobe's Source Serif 4"

target_dir = pathlib.Path(__file__).resolve().parent.joinpath('target')

if not target_dir.is_dir():
    print(f'{target_dir} is not a directory.')
    quit(1)

font_files = target_dir.glob('**/*.*tf')
old_name = 'Source'
# Careful with spaces in the replacement name.
# Some name records can contain them, others can’t.
new_name = 'Chuigoan'

for ff_path in font_files:
    ttf = ttLib.TTFont(ff_path)
    name_table = ttf.get('name')
    name_records = name_table.names
    for nr in name_records:

        # Copyright nameID == 0
        if (nr.nameID == 0):
            new_nr = copyright_text
            name_table.setName(
                new_nr,
                nameID=nr.nameID,
                platformID=nr.platformID,
                platEncID=nr.platEncID,
                langID=nr.langID
            )

        if(
            old_name in nr.toUnicode() and
            # Find-replacing in the copyright statement would result in false
            # information. Change completely, perhaps?
            nr.nameID not in (0, 7)
        ):
            new_nr = nr.toUnicode().replace(old_name, new_name)
            name_table.setName(
                new_nr,
                nameID=nr.nameID,
                platformID=nr.platformID,
                platEncID=nr.platEncID,
                langID=nr.langID)

    new_ps_name = next(
        nr.toUnicode() for nr in name_table.names if nr.nameID == 6)

    new_file_name = pathlib.PurePath(new_ps_name + ff_path.suffix)
    ttf.save(ff_path.parent / new_file_name)
    ff_path.unlink()
