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
from constants import *
import overrides
import header

csv_filehandle = None

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
        csv_writer.writerow([unicode(outcell) for outcell in rooooow(row)])

    def write_header(tab):
        row = header.start.split(',')
        for i in range(tab.max_header):
            row.extend(header.repeat.format(num=i+1).split(','))
        csv_writer.writerow(row)

    def write_footer(row_count):
        csv_writer.writerow(["*"*9, str(row_count)])


    __version__ = "0.0.0"
    options = docopt(__doc__, version='databaker {}'.format(__version__))
    filenames = options['<filenames>']
    recipe_file = options['<recipe>']
    recipe = imp.load_source("recipe", recipe_file)
    #filenames = ['resource/table-a02.xls']  # will have come from command line glob
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
                    write_header(tab)  # NOTE: assumes same number of dimensions total!
                    header_written=True
                for ob_num, ob in enumerate(obs):  # TODO use const
                    output_row = single_iteration(ob)
                    csv_output(output_row)
                    row_count = row_count + 1
                    if ob_num % int(obs_count / 100) == 0:
                        percent = 1 + 100 * ob_num / obs_count
                        progress = percent / 5
                        print "\b"*50, "Tab {} - {:3d}% - [{}{}]".format(tab_num + 1, percent, '='*progress, " "*(20-progress)),
                    sys.stdout.flush()
                print
        write_footer(row_count)

if __name__ == '__main__':
    main()
