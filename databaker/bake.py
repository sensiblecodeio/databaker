#!/usr/bin/python
"""
Usage:
  bake.py <recipe> <filenames>...
"""

import codecs
import sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

import imp
from docopt import docopt
from timeit import default_timer as timer
import atexit
import xypath
import xypath.loader
from utf8csv import UnicodeWriter
import bake

csv_filehandle = None

OBS = -4
DATAMARKER = -3
GEOG = -2
TIME = -1
TIMEUNIT = 0
DIMENSION = 1
DIMENSIONLABEL = 2

skip_after = {OBS: 0,  # 1..2
              DATAMARKER: 12,  # 2..15
              GEOG: 2,  # 15..18/19
              TIME: 0,  # 18/19..20
              TIMEUNIT: 15}  # 20..36/37

def showtime(msg='unspecified'):
    global last
    t = timer()
    print "{}: {} ms,  {} ms".format(msg, int(1000*(t - last)), int(1000*(t - start)))
    last = t

def onexit():
    return showtime('exit')

atexit.register(onexit)
start = timer()
last = start

def single_iteration(ob, **foo):
    out = {}
    obj = ob._cell
    keys = ob.table.headers.keys()

    if isinstance(obj.value, float):
        yield obj.value
    else:
        yield ''

    assert len(keys) == max(keys) - min(keys)
    for dimension in range(DATAMARKER, TIMEUNIT + 1):  # do fixed headers
        try:
            cell = obj.table.headers.get(dimension, lambda _: None)(obj)
            if cell is None:  # TODO special handling per dimension, eg datamarker
                if dimension == DATAMARKER and not isinstance(obj.value, float):
                    value = obj.value
                elif dimension == TIMEUNIT:
                    value = 'quarter [TODO]'
                else:
                    value = ''
            elif isinstance(cell, basestring) or isinstance(cell, float):
                value = cell
            else:
                value = cell.value
        except xypath.xypath.NoLookupError:
            print "no lookup for dimension ", dimension
            value = "NoLookupError"
        yield value
        if dimension == TIME:  # lets do the timewarp again
            yield value
        for i in range(0, skip_after[dimension]):
            yield ''

    for dimension in range(1, obj.table.max_header+1):
        name = obj.table.headernames[dimension]
        try:
            cell = obj.table.headers[dimension](obj)
            if isinstance(cell, basestring) or isinstance(cell, float):
                value = cell
            else:
                value = cell.value
        except xypath.xypath.NoLookupError:
            print "no lookup for dimension ", dimension
            value = "NoLookupError"
        yield name
        yield name
        yield ''
        yield value
        yield value
        yield ''
        yield ''
        yield ''  # NOTE eight yields per loop

def main():
    def csv_output(row):
        csv_writer.writerow([unicode(outcell) for outcell in rooooow(row)])
    __version__ = "0.0.0"
    options = docopt(__doc__, version='databaker {}'.format(__version__))
    filenames = options['<filenames>']
    recipe_file = options['<recipe>']
    recipe = imp.load_source("recipe", recipe_file)
    #filenames = ['resource/table-a02.xls']  # will have come from command line glob
    with open("out.csv", "w") as csv_filehandle:
        csv_writer = UnicodeWriter(csv_filehandle)
        for fn in filenames:
            print fn
            tableset = xypath.loader.table_set(fn, extension='xls')
            showtime("file imported")
            # TODO print sheet name
            for tab in xypath.loader.get_sheets(tableset, recipe.per_file(tableset)):
                showtime("tab imported")
                obs = recipe.per_tab(tab)
                for ob in obs:  # TODO use const
                    output_row=single_iteration(ob)
                    csv_output(output_row)

if __name__ == '__main__':
    main()
