#!/usr/bin/python

"""
Usage:
  bake.py <recipe> <filenames>...
"""

import atexit
import codecs
import imp
import sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

from timeit import default_timer as timer

from docopt import docopt
import xypath
import xypath.loader
from utf8csv import UnicodeWriter

import bake
from constants import *
import overrides        # warning: changes xypath and messytables
import header

csv_filehandle = None

SKIP_AFTER = {OBS: 0,           # 1..2
              DATAMARKER: 12,   # 2..15
              GEOG: 2,          # 15..18/19
              TIME: 0,          # 18/19..20
              TIMEUNIT: 15}     # 20..36/37

def showtime(msg='unspecified'):
    global last
    t = timer()
    print "{}: {:.3f}s,  {:.3f}s total".format(msg, t - last, t - start)
    last = t

def onexit():
    return showtime('exit')

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

    # Do fixed headers.
    for dimension in range(DATAMARKER, TIMEUNIT + 1):
        try:
            cell = obj.table.headers.get(dimension, lambda _: None)(obj)
            if cell is None:
                # Special handling per dimension.
                if dimension == DATAMARKER and not isinstance(obj.value, float):
                    value = obj.value
                elif dimension == TIMEUNIT:
                    value = 'quarter [TODO]'
                else:
                    value = ''
            elif isinstance(cell, (basestring, float)):
                value = cell
            else:
                value = cell.value
        except xypath.xypath.NoLookupError:
            print "no lookup for dimension ", dimension
            value = "NoLookupError"
        yield value
        if dimension == TIME:  # lets do the timewarp again
            yield value
        for i in range(0, SKIP_AFTER[dimension]):
            yield ''

    for dimension in range(1, obj.table.max_header+1):
        name = obj.table.headernames[dimension]
        try:
            cell = obj.table.headers[dimension](obj)
            if isinstance(cell, (basestring, float)):
                value = cell
            else:
                value = cell.value
        except xypath.xypath.NoLookupError:
            print "no lookup for dimension ", dimension
            value = "NoLookupError"

        # Eight yields per loop - they are the parameters of an ONS dimension:
        yield name  # Dimension Id
        yield name  # Dimension Label English
        yield ''    # Dimension Label Welsh
        yield value # Dimension Item Id
        yield value # Dimension Item Label English
        yield ''    # Dimension Item Label Welsh
        yield ''    # Is Total
        yield ''    # Is Subtotal

def main():
    def csv_output(row):
        csv_writer.writerow([unicode(item) for item in row])

    def write_header(tab):
        row = header.start.split(',')
        for i in range(tab.max_header):
            row.extend(header.repeat.format(num=i+1).split(','))
        csv_writer.writerow(row)

    def write_footer(row_count):
        csv_writer.writerow(["*"*9, str(row_count)])

    atexit.register(onexit)

    __version__ = "0.0.0"
    options = docopt(__doc__, version='databaker {}'.format(__version__))
    filenames = options['<filenames>']
    recipe_file = options['<recipe>']
    recipe = imp.load_source("recipe", recipe_file)

    header_written = False
    row_count = 0
    with open("out.csv", "w") as csv_filehandle:
        csv_writer = UnicodeWriter(csv_filehandle)
        for fn in filenames:
            print fn
            tableset = xypath.loader.table_set(fn, extension='xls')
            showtime("file imported")
            # TODO print sheet name
            tabs = xypath.loader.get_sheets(tableset, recipe.per_file(tableset))
            for tab_num, tab in enumerate(tabs):
                showtime("tab imported")
                obs = recipe.per_tab(tab)
                obs_count = len(obs)
                if not header_written:
                    # NOTE: assumes same number of dimensions total!
                    write_header(tab)
                    header_written = True
                last_percent = None
                for ob_num, ob in enumerate(obs):  # TODO use const
                    output_row = single_iteration(ob)
                    csv_output(output_row)
                    row_count += 1
                    percent = ((ob_num+1) * 100) // obs_count
                    if percent != last_percent:
                        progress = percent / 5
                        print "\b"*50, "Tab {} - {:3d}% - [{}{}]".format(tab_num + 1, percent, '='*progress, " "*(20-progress)),
                        sys.stdout.flush()
                        last_percent = percent
                print
        write_footer(row_count)

if __name__ == '__main__':
    main()
