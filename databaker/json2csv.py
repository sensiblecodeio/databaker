#!/usr/bin/env python
"""
Usage:
    json2csv.py --ons <files>...
"""

from __future__ import absolute_import, print_function, division
from docopt import docopt
import json
import re
from utf8csv import UnicodeWriter

### options
options = docopt(__doc__)
files = options['<files>']
if options['--ons']:
    pass

filename = files[0]

with open(filename, "r") as f:
    data = json.load(f)
print(j)

#with open(filename, V"w") as f:
#    csvout = UnicodeWriter(f)

def ons_rename_headers(data):
    for row in data:
        for i, name in []:
            pass
