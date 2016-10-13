from __future__ import absolute_import, print_function, division
from timeit import default_timer as timer
import re
import warnings
import six
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
        self.header_dimensions = None

    def write_header_if_needed(self, dimensions, ob):
        if self.header_dimensions is not None:
            # we've already written headers.
            return
        self.header_dimensions = dimensions
        header_row = template.start.split(',')

        # create new header row
        for i in range(dimensions):
            header_row.extend(template.repeat.format(num=i+1).split(','))

        # overwrite dimensions/subject/name as column header (if requested)
        if template.topic_headers_as_dims:
            dims = []
            for dimension in range(1, ob._cell.table.max_header+1):
                dims.append(ob._cell.table.headernames[dimension])
            header_row = rewrite_headers(header_row, dims)

        # Write to the file
        self.csv_writer.writerow(header_row)


    def footer(self):
        self.csv_writer.writerow(["*"*9, str(self.row_count)])
        self.filehandle.close()

    def handle_observation(self, ob):
        number_of_dimensions = ob.table.max_header
        self.write_header_if_needed(number_of_dimensions, ob)
        output_row = self.get_dimensions_for_ob(ob)
        self.output(output_row)

    def output(self, row):
        def translator(s):
            if not isinstance(s, six.string_types):
                return six.text_type(s)
            # this is slow. We can't just use translate because some of the
            # strings are unicode. This adds 0.2 seconds to a 3.4 second run.
            return six.text_type(s.replace('\n',' ').replace('\r', ' '))
        self.csv_writer.writerow([translator(item) for item in row])
        self.row_count += 1

    def get_dimensions_for_ob(self, ob):
        def cell_for_dimension(dimension):
            # implicit: obj
            try:
                cell = obj.table.headers.get(dimension, lambda _: None)(obj)
            except xypath.xypath.NoLookupError:
                print("no lookup to dimension {} from cell {}".format(dim_name(dimension), repr(ob._cell)))
                if self.no_lookup-error:
                    cell = "NoLookupError"            # if user wants - output 'NoLookUpError' to CSV
                else:
                    cell = "" # Otherwise output a blank cell.
            return cell

        def value_for_dimension(dimension):
            # implicit: obj
            cell = cell_for_dimension(dimension)
            if cell is None:
                value = ''
            elif isinstance(cell, (six.string_types, float)):
                value = cell
            elif cell.properties['richtext']:
                value = richxlrd.RichCell(cell.properties.cell.sheet, cell.y, cell.x).fragments.not_script.value
            else:
                value = cell.value
            return value

        # TODO not really 'self'y
        """For a single observation cell, provide all the
           information for a single CSV row"""
        out = {}
        obj = ob._cell
        keys = list(ob.table.headers.keys())


        # Get fixed headers.
        values = {}
        values[OBS] = obj.value

        LAST_METADATA = 0 # since they're numbered -9 for obs, ... 0 for last one
        for dimension in range(OBS+1, LAST_METADATA + 1):
            values[dimension] = value_for_dimension(dimension)

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

        for dimension in range(OBS, LAST_METADATA + 1):
            yield values[dimension]
            if dimension in template.SH_Repeat:         # Calls special handling - repeats
                yield values[dimension]
            for i in range(0, template.SKIP_AFTER[dimension]):
                yield ''

        for dimension in range(1, obj.table.max_header+1):
            name = obj.table.headernames[dimension]
            value = value_for_dimension(dimension)
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
