#!/usr/bin/env python
"""
Usage:
    sortcsv.py --ons <files>...
    sortcsv.py [options] <cols> <files>...

Options:
    --header         Remove first row and replace
    --footer         Remove last row and replace
"""

from __future__ import absolute_import, division
from docopt import docopt
from databaker.utf8csv import UnicodeReader, UnicodeWriter
import re
import sys
from six import PY2

columns = None

### options
def parse_columns(colstring):
    if colstring == None:
        return []
    values = re.split("[^0-9]+", colstring)
    return list(int(x) for x in values)




def csv_key(row):
    l = len(row)
    foo = list(row[x] for x in columns if x<l)
    return foo

def main(argv=None):
    if argv is None:
        argv=sys.argv
    global columns
    options = docopt(__doc__, argv=argv[1:])
    columns = parse_columns(options['<cols>'])
    files = options['<files>']
    filename = files[0]
    header = int(options['--header'])
    footer = int(options['--footer'])
    if options['--ons']:
        header = 1
        footer = 1
        columns = [3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 23, 24, 25, 36, 36+8, 36+16, 36+24, 36+32, 36+40, 36+48, 36+56, 36+64, 36+72]
        columns = [x-1 for x in columns]
    with open(filename, "r") as f:
        all_data = list(UnicodeReader(f))
    central_data = all_data[header:-footer]
    central_data.sort(key=csv_key)
    if PY2:
        mode = "wb"
    else:
        mode = "w"
    with open(filename, mode) as f:
        csvout = UnicodeWriter(f)
        if header:
            csvout.writerow(all_data[0])
        for row in central_data:
            csvout.writerow(row)
        if footer:
            csvout.writerow(all_data[-1])

if __name__ == '__main__':
    main()
