# -*- coding: utf-8 -*-

import os
import subprocess


PYUIC = 'pyuic5'
UI_DIR = 'ui/'

ui_files = [
    file for file in os.listdir('ui/')
    if os.path.splitext(file)[-1] == '.ui'
]

for file in ui_files:
    outfile = file
    for ch in ' -':
        outfile = outfile.replace(ch, '_')
    subprocess.run([
        PYUIC, os.path.join(UI_DIR, file),
        '-o', os.path.join(UI_DIR, os.path.splitext(outfile)[0] + '.py')
    ])
