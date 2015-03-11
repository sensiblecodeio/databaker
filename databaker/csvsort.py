#!/usr/bin/env python
"""
Usage:
    csvsort.py [options] <cols> <files>...

Options:
    --header         Remove first row and replace
    --footer         Remove last row and replace
"""

from docopt import docopt
from utf8csv import UnicodeReader, UnicodeWriter
import re

### options
def parse_columns(colstring):
    if colstring == None:
        return []
    values = re.split("[^0-9]+", colstring)
    return list(int(x) for x in values)

options = docopt(__doc__)
columns = parse_columns(options['<cols>'])
files = options['<files>']
header = int(options['--header'])
footer = int(options['--footer'])

filename = files[0]

def csv_key(row):
    l = len(row)
    foo = list(row[x] for x in columns if x<l)
    return foo

with open(filename, "r") as f:
    all_data = list(UnicodeReader(f))
central_data = all_data[header:-footer]
central_data.sort(key=csv_key)
with open(filename, "w") as f:
    csvout = UnicodeWriter(f)
    if header:
        csvout.writerow(all_data[0])
    for row in central_data:
        csvout.writerow(row)
    if footer:
        csvout.writerow(all_data[-1])
