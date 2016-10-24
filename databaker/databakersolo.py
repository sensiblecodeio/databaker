
#!/usr/bin/python

"""
Usage:
  recipe.py [options] <spreadsheet> [<params>...]

Options:
  --notiming            Suppress timing information.
  --preview             Preview selected cells in Excel.
  --nocsv               Don't produce CSV file.
  --debug               Debug Mode
  --nolookuperrors      Dont output 'NoLookuperror' to final CSV.
"""

from __future__ import absolute_import, division, print_function
import atexit

# Instructions: insert the following two lines at the bottom of the recipe and run it directly as a Python3 scripe
# import databaker.databakersolo
# databaker.databakersolo.runall(per_file, per_tab)

# test script calls (for regression)
# python3 ../../quickcode-ons-recipes/abs/ABS01.py --preview ../../quickcode-ons-recipes/abs/Annual\ Business\ Survey\ Standard\ Extracts\ 2014P\ \(2\).xlsx 
# python3 bake.py --preview ../../quickcode-ons-recipes/abs/ABS01.py ../../quickcode-ons-recipes/abs/Annual\ Business\ Survey\ Standard\ Extracts\ 2014P\ \(2\).xlsx 


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

from databaker.utils import showtime, TechnicalCSV, extract_dimension_values_for_ob, yield_dimension_values
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
        self.recipe_file = sys.argv[0]
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
        self.max_count = max(1, max_count)
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

def make_preview(writer, tabindex, headers, segment):
    # call for each segment
    for i, header in headers.items():
        if hasattr(header, 'bag') and not isinstance(header.bag, xypath.Table):
            for bag in header.bag:
                writer.get_sheet(tabindex).write(bag.y, bag.x, bag.value,
                    xlwt.easyxf('pattern: pattern solid, fore-colour {}'.format(colourlist[i])))
    for ob in segment:
        writer.get_sheet(tabindex).write(ob.y, ob.x, ob.value,
            xlwt.easyxf('pattern: pattern solid, fore-colour {}'.format(colourlist[OBS])))
            

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


    # this is the call of RECIPE.per_file() which filters the list of tables
    tableset = xypath.loader.table_set(spreadsheet, extension='xls')
    showtime("file {!r} imported".format(spreadsheet))
    if opt.preview:
        writer = xlutils.copy.copy(tableset.workbook)
        writer.save(filenames()['preview'])
        
    tabs = list(xypath.loader.get_sheets(tableset, recipe.per_file(tableset)))
    if not tabs:
        print("No matching tabs found.")
        exit(1)

    # this calls RECIPE.per_tab() on each table and batches up the yielded segments and headers into conversionsequence tuples
    conversionsequence = [ ]   # [ (tab, tab_num, {int:dimension} headers, [] headernames, [] segment, int seg_id) ]
    for tab_num, tab in enumerate(tabs):
        showtime("tab {!r} imported".format(tab.name))

        # The callback into the recipe.
        try:
            pertab = recipe.per_tab(tab)
        except Exception:
            crash_msg.append("tab: {!r} {!r}".format(tab_num, tab.name))
            raise
        if isinstance(pertab, xypath.xypath.Bag):
            pertab = [pertab]   # normal case when single list returned rather than yielded 

        # issue here is that pertab can be a generator, where the tab.headers are rewritten between each batch/segment
        for seg_id, segment in enumerate(pertab):  # must be yielded so we can copy out tab.headers which are set between the function calls
            assert tab.max_header == max(tab.headers.keys())
            assert tab.max_header + 1 == len(tab.headernames)
            try:
                conversionsequence.append((tab, tab_num, tab.headers.copy(), tab.headernames.copy(), segment, seg_id))
            except Exception:
                crash_msg.append("segment: {!r}".format(seg_id))
                crash_msg.append("tab: {!r} {!r}".format(tab_num, tab.name))
                raise
            # [D's original] hacky observation wiping
            tab.headers = {}
            tab.max_header = 0
            tab.headernames = [None]
            
    # collected all the work.  now the conversion and saving
    print("we have a conversion sequence size", len(conversionsequence)) 
    
    # write the spreadsheets out all as one batch from the conversionsequence
    if opt.preview:
        print("making preview spreadsheet")
        for tab, tab_num, headers, headernames, segment, seg_id in conversionsequence:
            print("%d" % tab_num, end='.')
            sys.stdout.flush()
            tableset = xypath.loader.table_set(filenames()['preview'], extension='xls')   # load and save between each one
            writer = xlutils.copy.copy(tableset.workbook)
            make_preview(writer, tab.index, headers, segment)
            writer.save(filenames()['preview'])
        print()

    # now generate the csv all into one batch from the conversion system
    if opt.csv and conversionsequence:
        print("making conversion csv")
        batchrows = [ ]
        for tab, tab_num, headers, headernames, segment, seg_id in conversionsequence:
            progress = Progress(len(segment), 'Tab {}'.format(tab_num + 1))
            for ob_num, ob in enumerate(segment):
                assert tab is ob.table
                try:
                    values = extract_dimension_values_for_ob(headers, ob, opt.no_lookup_error)
                    batchrows.append((values, headernames))
                except Exception:
                    crash_msg.append("ob: {!r}".format(ob))
                    crash_msg.append("tab: {!r} {!r}".format(tab_num, tab.name))
                    raise
                progress.update(ob_num)
            print()

        # this is the bloat process I'd like to take this loop outside the loop above
        csv_file = filenames()['csv']
        csv = TechnicalCSV(csv_file, opt.no_lookup_error)
        tab, tab_num, headers, headernames, segment, seg_id = conversionsequence[0]
        csv.csv_writer.writerow(csv.generate_header_row(headers, headernames))  # note that only first batch of headernames is used
        for values, headernames in batchrows:
            output_row = yield_dimension_values(values, headernames)
            csv.output(output_row)
        csv.footer()


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


# replacement of the main function
class Recipe:
    def __init__(self, lper_file, lper_tab):
        self.per_file = lper_file
        self.per_tab = lper_tab
recipe = None
def runall(lper_file, lper_tab):
    if sys.argv[0] == "bake.py":
        print("You are running this solo script using bake.py; quitting runall() now so it may work")
        return
    
    global recipe
    recipe = Recipe(lper_file, lper_tab)
    Opt = Options()
    databaker.utils.showtime_enabled = Opt.timing
    databaker.constants.constant_params = Opt.params
    atexit.register(onexit)
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


    
