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
dims = {'time': 19, 'indicator': 5, 'ob': 1, 'datamarker': 2}
maxcol = 43
revdims = None

def update_dim(name, col):
    global dims, maxcol
    assert isinstance(col, int)
    dims[name] = 29 + (col*8)
    maxcol = max(maxcol, (35+col*8))

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
    if isinstance(obj.value, basestring) and obj.value and not 'datamarker' in ob.table.headers.items():
        out['datamarker'] = obj.value
    else:
        out['ob'] = obj.value  # TODO make more like other dims
    for name, function in ob.table.headers.items():
        try:
            cell = function(obj)
            if isinstance(cell, basestring) or isinstance(cell, float):
                out[name] = cell
            else:
                out[name] = cell.value
        except xypath.xypath.NoLookupError:
            print "no lookup for", name
            out[name] = "NoLookupError"
    return out


def rooooow(row):
    return [row.get(revdims.get(i, None), '') for i in range(1, bake.maxcol+1)]


def csv_output(row):
    csv_writer.writerow([unicode(outcell) for outcell in rooooow(row)])

def main():
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
                revdims = {pos: name for name, pos in bake.dims.items()}
                for ob in obs:
                    output_row=single_iteration(ob)
                    csv_output(output_row)

if __name__ == '__main__':
    main()
