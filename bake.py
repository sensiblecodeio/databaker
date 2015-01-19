#!/usr/bin/python
"""
Usage:
  bake.py <recipe> <filenames>...
"""
import imp
from docopt import docopt
import re
from timeit import default_timer as timer
import atexit
import xypath
import xypath.loader

def cell_repr(cell):
    column = xypath.contrib.excel.excel_column_label(cell.x+1)
    return "<{}{!r} {}>".format(column, cell.y+1, cell.value)
xypath.xypath._XYCell.__repr__ = cell_repr

def is_header(bag, name, *args, **kwargs):
    if getattr(bag.table, 'headers', None) is None:
        bag.table.headers = {}
    print name, "cell.lookup({}, *{}, **{}".format(bag, args, kwargs)
    bag.table.headers[name] = lambda cell: cell.lookup(bag, *args, **kwargs)
    showtime("got header {}".format(name))
xypath.Bag.is_header = is_header

xypath.Bag.regex = lambda self, x: self.filter(re.compile(x))

def one_of(bag, options):
    return bag.filter(lambda cell: cell.value in options)#
xypath.Bag.one_of = one_of

def showtime(msg='unspecified'):
    global last
    t = timer()
    print "{}: {} ms,  {} ms".format(msg, int(1000*(t - last)), int(1000*(t - start)))
    last = t

def onexit():
    return showtime('exit')

def is_number(cell):
    return type(cell.value) in [int, float, long]  # not CSV safe

atexit.register(onexit)
start = timer()
last = start

def single_iteration(ob, **foo):
    out = {}
    obj = ob._cell
    out['ob'] = obj
    for name, function in ob.table.headers.items():
        #try:
            out[name] = function(obj)
        #except xypath.xypath.NoLookupError:
        #    print "no lookup for", name
            #raise
    return out

if __name__ == '__main__':
    __version__ = "0.0.0"
    options = docopt(__doc__, version='databaker {}'.format(__version__))
    filenames = options['<filenames>']
    recipe_file = options['<recipe>']
    recipe = imp.load_source("recipe", recipe_file)
    #filenames = ['resource/table-a02.xls']  # will have come from command line glob
    for fn in filenames:
        print fn
        tableset = xypath.loader.table_set(fn)
        showtime("file imported")
        for sheet in xypath.loader.get_sheets(tableset, recipe.per_file(tableset)):
            showtime("sheet imported")
            obs = recipe.per_sheet(sheet)
            for ob in obs:
                output_row=single_iteration(ob)
