from __future__ import absolute_import, print_function, division
from timeit import default_timer as timer
import re
import warnings
import six
import xypath
import databaker.richxlrd.richxlrd as richxlrd
from datetime import datetime
from databaker.utf8csv import UnicodeWriter

# If there's a custom template, use it. Otherwise use the default.
try:
    import structure_csv_user as template
    from structure_csv_user import *
except ImportError:
    from . import structure_csv_default as template
    from .structure_csv_default import *

def rewrite_headers(row,dims):
    for i in range(0,len(row)):
        if i >= len(template.start.split(',')):
            which_cell_in_spread = (i - len(template.start.split(','))) % len(template.value_spread)
            which_dim = (i - len(template.start.split(','))) // len(template.value_spread)
            which_dim = int(which_dim)
            if value_spread[which_cell_in_spread] == 'value':
                row[i] = dims[which_dim]
    return row

def datematch(date, silent=False):
    """match mmm yyyy, mmm-mmm yyyy, yyyy Qn, yyyy"""
    if not isinstance(date, six.string_types):
        if isinstance(date, float) and date>=1000 and date<=9999 and int(date)==date:
            return "Year"
        if not silent:
            warnings.warn("Couldn't identify date {!r}".format(date))
        return ''
    d = date.strip()
    if re.match('\d{4}$', d):
        return 'Year'
    if re.match('\d{4} [Qq]\d$', d):
        return 'Quarter'
    if re.match('[A-Za-z]{3}-[A-Za-z]{3} \d{4}$', d):
        return 'Quarter'
    if re.match('[A-Za-z]{3} \d{4}$', d):
        return 'Month'
    if not silent:
        warnings.warn("Couldn't identify date {!r}".format(date))
    return ''


def dim_name(dimension):
    # should agree with constants.py
    if isinstance(dimension, int) and dimension <= 0:
        # the last dimension is dimension 0; but we index it as -1.
        return template.dimension_names[dimension-1]
    else:
        return dimension


def parse_ob(ob):
    if isinstance(ob.value, datetime):
        return (ob.value, '')
    if isinstance(ob.value, float):
        return (ob.value, '')
    if ob.properties['richtext']:
        # TODO(sm): rename this variable. It's potentially confusing.
        string = richxlrd.RichCell(ob.properties.cell.sheet, ob.y, ob.x).fragments.not_script.value
    else:
        string = ob.value
    value, datamarker = re.match(r"([-+]?[0-9]+\.?[0-9]*)?(.*)", string).groups()
    if value is None:
        value = ''
    return value.strip(), datamarker.strip()

LAST_METADATA = 0 # since they're numbered -9 for obs, ... 0 for last one
class TechnicalCSV(object):
    def __init__(self, filename, no_lookup_error):
        if six.PY2:
            mode = "wb"
        else:
            mode = "w"
        self.no_lookup_error = no_lookup_error
        self.filehandle = open(filename, mode)
        self.csv_writer = UnicodeWriter(self.filehandle)
        self.row_count = 0
        self.table = None
        self.batchrows = []

    def generate_header_row(self, table):
        assert self.table is None or self.table is table
        header_row = template.start.split(',')

        # create new header row
        for i in range(table.max_header):
            header_row.extend(template.repeat.format(num=i+1).split(','))

        # overwrite dimensions/subject/name as column header (if requested)
        if template.topic_headers_as_dims:
            dims = []
            for dimension in range(1, table.max_header+1):
                dims.append(table.headernames[dimension])
            header_row = rewrite_headers(header_row, dims)
        return header_row


    def footer(self):
        # WDA Observation File Interface Specification Section 1.3
        self.csv_writer.writerow(["*"*9, str(self.row_count)])
        self.filehandle.close()

    # try to put in the batching here
    def handle_observation(self, ob):
        assert self.table is ob.table
        values = self.extract_dimension_values_for_ob(ob)
        self.batchrows.append(values)

    def begin_observation_batch(self, table):
        assert self.table is None or self.table is table
        self.table = table
        assert len(self.batchrows) == 0

    def finish_observation_batch(self):
        for values in self.batchrows:
            output_row = self.yield_dimension_values(values)
            self.output(output_row)
        self.batchrows = []
        self.table = None

    def output(self, row):
        def translator(s):
            if not isinstance(s, six.string_types):
                return six.text_type(s)
            return six.text_type(s.replace('\n',' ').replace('\r', ' '))
        self.csv_writer.writerow([translator(item) for item in row])
        self.row_count += 1

    def cell_for_dimension(self, obj, dimension):
        try:
            cell = self.table.headers.get(dimension, lambda _: None)(obj)
        except xypath.xypath.NoLookupError:
            print("no lookup to dimension {} from cell {}".format(dim_name(dimension), repr(obj)))
            if self.no_lookup_error:
                cell = "NoLookupError"            # if user wants - output 'NoLookUpError' to CSV
            else:
                cell = "" # Otherwise output a blank cell.
        return cell

    def value_for_dimension(self, obj, dimension):
        # implicit: obj
        cell = self.cell_for_dimension(obj, dimension)
        if cell is None:
            value = ''
        elif isinstance(cell, (six.string_types, float)):
            value = cell
        elif cell.properties['richtext']:
            value = richxlrd.RichCell(cell.properties.cell.sheet, cell.y, cell.x).fragments.not_script.value
        else:
            value = cell.value
        return value

    def extract_dimension_values_for_ob(self, ob):
        obj = ob._cell

        # Get fixed headers.
        values = {}
        values[OBS] = obj.value

        for dimension in range(OBS+1, LAST_METADATA + 1):
            values[dimension] = self.value_for_dimension(obj, dimension)

        # Mutate values
        # Special handling per dimension.
        # NOTE  - variables beginning SH_ ... are dependent on user choices from the template file

        if template.SH_Split_OBS:
            if not isinstance(values[OBS], float):  # NOTE xls specific!
                ob_value, dm_value = parse_ob(ob)
                values[OBS] = ob_value
                # the observation is not actually a number
                # store it as a datamarker and nuke the observation field
                if values[template.SH_Split_OBS] == '':
                    values[template.SH_Split_OBS] = dm_value
                elif dm_value:
                    warnings.warn("datamarker lost: {} on {!r}".format(dm_value, ob))

        if template.SH_Create_ONS_time:
            if values[TIMEUNIT] == '' and values[TIME] != '':
                # we've not actually been given a timeunit, but we have a time
                # determine the timeunit from the time
                values[TIMEUNIT] = datematch(values[TIME])

        for dimension in range(1, self.table.max_header+1):
            assert dimension not in values
            values[dimension] = self.value_for_dimension(obj, dimension)
        return values

    def yield_dimension_values(self, values):
        for dimension in range(OBS, LAST_METADATA + 1):
            yield values[dimension]
            if dimension in template.SH_Repeat:         # Calls special handling - repeats
                yield values[dimension]
            for i in range(0, template.SKIP_AFTER[dimension]):
                yield ''

        for dimension in range(1, self.table.max_header+1):
            name = self.table.headernames[dimension]
            value = values[dimension]
            topic_headers = template.get_topic_headers(name, value)
            for col in topic_headers:
                yield col

    
        
start = timer()
last = start
showtime_enabled = True

def showtime(msg='unspecified'):
    if not showtime_enabled:
        return
    global last
    t = timer()
    print("{}: {:.3f}s,  {:.3f}s total".format(msg, t - last, t - start))
    last = t

