#!/usr/bin/py  # TODOthon

"""
Usage:
  bake.py [options] <recipe> <spreadsheets>...

Options:
  --timing    Show detailed timing information.
"""

import atexit
import codecs
import imp
import re
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
import warnings

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

def datematch(date):
    """match mmm yyyy, mmm-mmm yyyy, yyyy Qn, yyyy"""
    d = date.strip()
    if re.match('\d{4}$', d):
        return 'Year'
    if re.match('\d{4} [Qq]\d$', d):
        return 'Quarter'
    if re.match('[A-Za-z]{3}-[A-Za-z]{3} \d{4}$', d):
        return 'Quarter'
    if re.match('[A-Za-z]{3} \d{4}$', d):
        return 'Month'
    warnings.warn("Couldn't identify date {!r}".format(date))
    return ''

class Opt(object):
    __version__ = "0.0.0"
    options = docopt(__doc__, version='databaker {}'.format(__version__))
    xls_files = options['<spreadsheets>']
    recipe_file = options['<recipe>']
    timing = options['--timing']
    csv_file = 'out.csv'

class TechnicalCSV(object):
    def __init__(self, filename):
        self.filehandle = open(filename, "wb")
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

    def footer(self):
        self.csv_writer.writerow(["*"*9, str(self.row_count)])
        self.filehandle.close()

    def handle_observation(self, ob):
        number_of_dimensions = ob.table.max_header
        self.write_header_if_needed(number_of_dimensions)
        output_row = self.get_dimensions_for_ob(ob)
        self.output(output_row)

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


        # Get fixed headers.
        values = {}
        values[OBS] = obj.value

        for dimension in range(DATAMARKER, TIMEUNIT + 1):
            values[dimension] = value_for_dimension(dimension)

        # Mutate values
        # Special handling per dimension.

        if not isinstance(values[OBS], float):  # NOTE xls specific!
            # the observation is not actually a number
            # store it as a datamarker and nuke the observation field
            if values[DATAMARKER] == '':
                values[DATAMARKER] = values[OBS]
            else:
                pass  # TODO warn that we've lost data!
            values[OBS] = ''

        if values[TIMEUNIT] == '' and values[TIME] != '':
            # we've not actually been given a timeunit, but we have a time
            # determine the timeunit from the time
            #
            values[TIMEUNIT] = datematch(values[TIME])

        for dimension in range(OBS, TIMEUNIT + 1):
            yield values[dimension]
            if dimension == TIME:  # lets do the timewarp again
                yield values[dimension]
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


class Progress(object):
    def __init__(self, max_count, prefix=None, msg="\r{}{:3d}% - [{}{}]"):
        self.last_percent = None
        self.max_count = max_count
        self.msg = msg
        if prefix is not None:
            self.prefix = prefix + ' - '
        else:
            self.prefix = ''

    def update(self, count):
        percent = (((count+1) * 100) // self.max_count)
        if percent != self.last_percent:
            progress = percent / 5
            print self.msg.format(self.prefix, percent, '='*progress, " "*(20-progress)),
            sys.stdout.flush()
            self.last_percent = percent

def per_file(fn, recipe, csv):
    tableset = xypath.loader.table_set(fn, extension='xls')
    showtime("file {!r} imported".format(fn))
    tabs = xypath.loader.get_sheets(tableset, recipe.per_file(tableset))
    for tab_num, tab in enumerate(tabs):
        showtime("tab {!r} imported".format(tab.name))
        obs = recipe.per_tab(tab)
        obs_count = len(obs)
        progress = Progress(obs_count, 'Tab {}'.format(tab_num + 1))
        for ob_num, ob in enumerate(obs):  # TODO use const
            csv.handle_observation(ob)
            progress.update(ob_num)
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
