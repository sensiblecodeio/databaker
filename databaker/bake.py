#!/usr/bin/python

"""
Usage:
  bake.py [options] <recipe> <spreadsheet> [<params>...]

Options:
  --notiming            Suppress timing information.
  --preview             Preview selected cells in Excel.
  --nocsv               Don't produce CSV file.
  --debug               Debug Mode
  --nolookuperrors      Dont output 'NoLookuperror' to final CSV.
"""

from __future__ import absolute_import, division, print_function
import atexit

import imp
import os.path
import sys
import codecs
import six
from six.moves import range
from six.moves import zip
if six.PY2:
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

import xlutils.copy
import xlwt
from docopt import docopt

import xypath
import xypath.loader

from databaker.constants import *
import databaker.overrides as overrides       # warning: changes xypath and messytables

from databaker.utils import showtime, TechnicalCSV
import databaker.utils

# If there's a custom template, use it. Otherwise use the default.
try:
    import structure_csv_user as template
    from structure_csv_user import *
except ImportError:
    from . import structure_csv_default as template
    from .structure_csv_default import *


__version__ = "1.2.1"

crash_msg = []


def onexit():
    return showtime('exit')


class Options(object):
    def __init__(self):
        options = docopt(__doc__, version='databaker {}'.format(__version__))
        self.xls_files = [options['<spreadsheet>']]
        self.recipe_file = options['<recipe>']
        self.timing = not options['--notiming']
        self.preview = options['--preview']
        self.preview_filename = "preview-{spreadsheet}-{recipe}-{params}.xls"
        self.csv_filename = "data-{spreadsheet}-{recipe}-{params}.csv"
        self.csv = not options['--nocsv']
        self.debug = options['--debug']
        self.no_lookup_error = not options['--nolookuperrors']
        self.params = options['<params>']



class Progress(object):
    # creates a progress bar
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
            progress = int(percent // 5)
            print(self.msg.format(self.prefix, percent, '='*progress, " "*(20-progress)), end=' ')
            sys.stdout.flush()
            self.last_percent = percent

def per_file(spreadsheet, recipe, opt):
    def filenames():
        get_base = lambda filename: os.path.splitext(os.path.basename(filename))[0]
        xls_directory = os.path.dirname(spreadsheet)
        xls_base = get_base(spreadsheet)
        recipe_base = get_base(opt.recipe_file)
        parsed_params = ','.join(opt.params)

        csv_filename = opt.csv_filename.format(spreadsheet=xls_base,
                                               recipe=recipe_base,
                                               params=parsed_params)

        csv_path = os.path.join(xls_directory, csv_filename)

        preview_filename = opt.preview_filename.format(spreadsheet=xls_base,
                                                       recipe=recipe_base,
                                                       params=parsed_params)
        preview_path = os.path.join(xls_directory, preview_filename)
        return {'csv': csv_path, 'preview': preview_path}

    def make_preview():
        # call for each segment
        for i, header in tab.headers.items():
            if hasattr(header, 'bag') and not isinstance(header.bag, xypath.Table):
                for bag in header.bag:
                    writer.get_sheet(tab.index).write(bag.y, bag.x, bag.value,
                        xlwt.easyxf('pattern: pattern solid, fore-colour {}'.format(colourlist[i])))
                for ob in segment:
                    writer.get_sheet(tab.index).write(ob.y, ob.x, ob.value,
                        xlwt.easyxf('pattern: pattern solid, fore-colour {}'.format(colourlist[OBS])))


    tableset = xypath.loader.table_set(spreadsheet, extension='xls')
    showtime("file {!r} imported".format(spreadsheet))
    if opt.preview:
        writer = xlutils.copy.copy(tableset.workbook)
    if opt.csv:
        csv_file = filenames()['csv']
        csv = TechnicalCSV(csv_file, opt.no_lookup_error)
    tabs = list(xypath.loader.get_sheets(tableset, recipe.per_file(tableset)))
    if not tabs:
        print("No matching tabs found.")
        exit(1)
    bheaderoutput=False
    for tab_num, tab in enumerate(tabs):
        showtime("tab {!r} imported".format(tab.name))

        ## The callback into the recipe.
        try:
            pertab = recipe.per_tab(tab)
        except Exception:
            crash_msg.append("tab: {!r} {!r}".format(tab_num, tab.name))
            raise

        # Process the per_tab return value.
        if isinstance(pertab, xypath.xypath.Bag):
            pertab = [pertab]

        try:
            for seg_id, segment in enumerate(pertab):
                if opt.debug:
                    print("tab and segment available for interrogation")
                    import pdb; pdb.set_trace()

                if opt.preview:
                    make_preview()

                # TODO(sm): consider removing duplication of len(segment).
                if opt.csv and len(segment) != 0:
                    obs_count = len(segment)
                    progress = Progress(obs_count, 'Tab {}'.format(tab_num + 1))

                    csv.begin_observation_batch(tab)

                    if not bheaderoutput:
                        csv.csv_writer.writerow(csv.generate_header_row(tab))
                        bheaderoutput = True

                    for ob_num, ob in enumerate(segment):
                        assert tab is ob.table
                        try:
                            csv.handle_observation(ob)
                        except Exception:
                            crash_msg.append("ob: {!r}".format(ob))
                            raise
                        progress.update(ob_num)
                    print()
                    csv.finish_observation_batch()

                # hacky observation wiping
                tab.headers = {}
                tab.max_header = 0
                tab.headernames = [None]

        except Exception:
            crash_msg.append("segment: {!r}".format(seg_id))
            crash_msg.append("tab: {!r} {!r}".format(tab_num, tab.name))
            raise


    if opt.csv:
        csv.footer()
    if opt.preview:
        writer.save(filenames()['preview'])

def create_colourlist():
    # Function to dynamically assign colours to dimensions for preview
    "https://github.com/python-excel/xlwt/blob/master/xlwt/Style.py#L309"
    colours = ["lavender", "violet", "gray25", "sea_green",
              "pale_blue", "blue", "gray25", "rose", "tan", "light_yellow", "light_green", "light_turquoise",
              "light_blue", "sky_blue", "plum", "gold", "lime", "coral", "periwinkle", "ice_blue", "aqua"]
    numbers = []
    for i in range(len(template.dimension_names)-1, \
                   -(len(colours) - len(template.dimension_names)), -1):
        numbers.append(-i)
    colourlist = dict(list(zip(numbers, colours)))
    return colourlist
colourlist = create_colourlist()



def main():
    Opt = Options()
    databaker.utils.showtime_enabled = Opt.timing
    databaker.constants.constant_params = Opt.params
    atexit.register(onexit)
    recipe = imp.load_source("recipe", Opt.recipe_file)
    for fn in Opt.xls_files:
        try:
            per_file(fn, recipe, Opt)
        except Exception:
            crash_msg.append("fn: {!r}".format(fn))
            crash_msg.append("recipe: {!r}".format(Opt.recipe_file))
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            print('\n'.join(crash_msg))
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            raise

if __name__ == '__main__':
    main()
