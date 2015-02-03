#!/usr/bin/python

"""
Usage:
  bake.py [options] <recipe> <spreadsheets>...

Options:
  --timing    Show detailed timing information.
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

class DimensionError(Exception):
    pass

SKIP_AFTER = {OBS: 0,           # 1..2
              DATAMARKER: 12,   # 2..15
              GEOG: 2,          # 15..18/19
              TIME: 0,          # 18/19..20
              TIMEUNIT: 15}     # 20..36/37

def showtime(msg='unspecified'):
    if not Opt.timing:
        return
    global last
    t = timer()
    print "{}: {:.3f}s,  {:.3f}s total".format(msg, t - last, t - start)
    last = t

def onexit():
    return showtime('exit')

start = timer()
last = start

class Opt(object):
    __version__ = "0.0.0"
    options = docopt(__doc__, version='databaker {}'.format(__version__))
    xls_files = options['<spreadsheets>']
    recipe_file = options['<recipe>']
    timing = options['--timing']
    csv_file = 'out.csv'

class TechnicalCSV(object):
    def __init__(self, filename):
        self.filehandle = open(filename, "w")
        self.csv_writer = UnicodeWriter(self.filehandle)
        self.row_count = 0
        self.header_dimensions = None

    def write_header_if_needed(self, dimensions):
        if self.header_dimensions is not None:
            if dimensions != self.header_dimensions:
                raise DimensionError("Header had {} dimensions, but this row has {}.".format(self.header_dimensions, dimensions))
            return

        self.header_dimensions = dimensions
        header_row = header.start.split(',')
        for i in range(dimensions):
            header_row.extend(header.repeat.format(num=i+1).split(','))
        self.csv_writer.writerow(header_row)
        self.header_written = True

    def footer(self):
        self.csv_writer.writerow(["*"*9, str(self.row_count)])
        self.filehandle.close()

    def handle_observation(self, ob):
        number_of_dimensions = ob.table.max_header + 1
        self.write_header_if_needed(number_of_dimensions)
        output_row = self.get_dimensions_for_ob(ob)
        csv.output(output_row)

    def output(self, row):
        self.csv_writer.writerow([unicode(item) for item in row])
        self.row_count += 1

    def get_dimensions_for_ob(self, ob):
        def value_for_dimension(dimension):
            # implicit: obj
            try:
                cell = obj.table.headers.get(dimension, lambda _: None)(obj)
                # TODO: move this out so I can change these things depending
                #       on other values easier
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
            return value

        # TODO not really 'self'y
        """For a single observation cell, provide all the
           information for a single CSV row"""
        out = {}
        obj = ob._cell
        keys = ob.table.headers.keys()

        if isinstance(obj.value, float):
            yield obj.value
        else:
            yield ''

        # Do fixed headers.
        for dimension in range(DATAMARKER, TIMEUNIT + 1):
            value = value_for_dimension(dimension)
            yield value
            if dimension == TIME:  # lets do the timewarp again
                yield value
            for i in range(0, SKIP_AFTER[dimension]):
                yield ''

        for dimension in range(1, obj.table.max_header+1):
            name = obj.table.headernames[dimension]
            value = value_for_dimension(dimension)

            # Eight yields per loop - they are the parameters of an ONS dimension:
            yield name  # Dimension Id
            yield name  # Dimension Label English
            yield ''    # Dimension Label Welsh
            yield value # Dimension Item Id
            yield value # Dimension Item Label English
            yield ''    # Dimension Item Label Welsh
            yield ''    # Is Total
            yield ''    # Is Subtotal


def per_file(fn, recipe, csv):
    tableset = xypath.loader.table_set(fn, extension='xls')
    showtime("file {} imported".format(fn))
    # TODO print sheet name
    tabs = xypath.loader.get_sheets(tableset, recipe.per_file(tableset))
    for tab_num, tab in enumerate(tabs):
        showtime("tab imported")
        obs = recipe.per_tab(tab)
        obs_count = len(obs)
        last_percent = None
        for ob_num, ob in enumerate(obs):  # TODO use const
            csv.handle_observation(ob)
            percent = ((ob_num+1) * 100) // obs_count
            if percent != last_percent:
                progress = percent / 5
                print "\r", "Tab {} - {:3d}% - [{}{}]".format(tab_num + 1, percent, '='*progress, " "*(20-progress)),
                sys.stdout.flush()
                last_percent = percent
        print

def main():
    atexit.register(onexit)
    recipe = imp.load_source("recipe", Opt.recipe_file)
    csvout = TechnicalCSV(Opt.csv_file)
    for fn in Opt.xls_files:
        per_file(fn, recipe, csvout)
    csvout.footer()

if __name__ == '__main__':
    main()
