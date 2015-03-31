"""
Patches xypath and messytables.
"""

import re
import datetime
import warnings

import xypath
import messytables
import bake

class MatchNotFound(Exception):
    """failed to find match in bag.group"""
    pass

class Dimension(object):

# TODO string signature: (dimself, bag, label, label item)
# TODO bag signature:    (dimself, bag, label, direction, striict)

    def __init__(self, bag, label, param1, direction=None):
        """bag: a bag - either a dimension bag or a table (in the case of a string)
           label: dimension label
           param1: either a strictness for a bag or a literal string
           direction: a direction for a bag"""

        self.bag = bag
        self.strict = None
        self.string = None
        if isinstance(param1, basestring):
            self.string = param1
        else:
            self.strict = param1
        self.direction = direction  # direction
        self.bag.table.append_dimension(label, self)

    def __call__(self, cell):
        if self.string is not None:
            return self.string
        else:
            return cell.lookup(self.bag, self.direction, self.strict)

def dimension(self, *args, **kwargs):
    Dimension(self, *args, **kwargs)
    return self

xypath.Bag.dimension = dimension

# === XLSCell Overrides ===================================

def text_date(cell):
    xls_format = cell.properties['formatting_string'].upper()
    quarter = int((cell.value.month -1 ) / 3) + 1  # TODO testme!
    if 'Q' in xls_format:
        py_format = "%Y Q{quarter}"
    elif 'D' in xls_format:
        warnings.warn("Day-of-month in date!")
        return cell.value
    elif 'M' in xls_format:
        py_format = "%b %Y"
    elif 'Y' in xls_format:
        py_format = "%Y"
    else:
        warnings.warn("Unable to parse dateformat: {} in {!r}".format(xls_format, cell))
        return cell.value
    return cell.value.strftime(py_format).format(quarter=quarter)

xypath.xypath.Table.from_messy_ = staticmethod(xypath.xypath.Table.from_messy)
def new_from_messy(messy_rowset):
    new_table = xypath.xypath.Table.from_messy_(messy_rowset)
    for cell in new_table.unordered_cells:
        if isinstance(cell.value, datetime.datetime):
            # it was originally an excel date
            cell.value = text_date(cell)
    return new_table
xypath.xypath.Table.from_messy = staticmethod(new_from_messy)

# === Cell Overrides ======================================

def cell_repr(cell):
    column = xypath.contrib.excel.excel_column_label(cell.x+1)
    return "<{}{} {!r}>".format(column, cell.y+1, cell.value)
xypath.xypath._XYCell.__repr__ = cell_repr

# === TableSet Overrides ==================================

@property
def tabnames(tableset):
    return set(x.name for x in tableset.tables)
messytables.TableSet.names = tabnames

# === Table Overrides =====================================

def excel_ref(table, reference):
    if ':' not in reference:
        (col, row) = xypath.contrib.excel.excel_address_coordinate(reference, partial=True)
        return table.get_at(col, row)
    else:
        ((left, top), (right, bottom)) = xypath.contrib.excel.excel_range(reference)
        bag = xypath.Bag(table=table)
        if top is None and bottom is None:
            for col in xrange(left, right + 1):
                bag = bag | table.get_at(col, None)
        elif left is None and right is None:
            for row in xrange(top, bottom + 1):
                bag = bag | table.get_at(None, row)
        else:
            for row in xrange(top, bottom + 1):
                for col in xrange(left, right + 1):
                    bag = bag | table.get_at(col, row)
        return bag
xypath.Table.excel_ref = excel_ref

def append_dimension(table, label, func):
    if getattr(table, 'headers', None) is None:
        table.headers = {}
        table.max_header = 0
        table.headernames = [None]
    if isinstance(label, basestring):
        table.max_header += 1
        number = table.max_header
        table.headernames.append(label)
    else:
        assert isinstance(label, int)
        number = label
    table.headers[number] = func
    bake.showtime("got header {}".format(bake.dim_name(label)))
xypath.Table.append_dimension = append_dimension

def debug_dimensions(table):
    table.append_dimension("ref", lambda cell: xypath.contrib.excel.excel_location(cell))
    table.append_dimension("table", lambda cell: cell.table.name)

xypath.Table.debug_dimensions = debug_dimensions

# === Bag Overrides =======================================

xypath.Bag.regex = lambda self, x: self.filter(re.compile(x))

def is_date(bag):
    return bag.filter(lambda cell: bake.datematch(cell.value, silent=True))
xypath.Bag.is_date = is_date

def is_number(bag):
    return bag.filter(lambda cell: isinstance(cell.value, (int, float, long)))
xypath.Bag.is_number = is_number

def group(bag, regex):
    """get the text"""
    bag.assert_one()
    match = re.search(regex, bag.value)
    if not match:
        raise MatchNotFound("Can't find {!r} in {!r}".format(regex, bag.value))
    matchtext = match.groups(0)[0]
    assert matchtext
    return matchtext
xypath.Bag.group = group

def one_of(bag, options):
    output = None
    for option in options:
        if output is None:
            output = bag.filter(option)
        else:
            output = output | bag.filter(option)
    return output
xypath.Bag.one_of = one_of

def parent(bag):
    """for cell, get its top-left cell"""
    output_bag = xypath.Bag(table = bag.table)
    for cell in bag.unordered:
        row, _, col, _ = cell.properties.raw_span(always=True)
        output_bag.add(cell.table.get_at(col, row)._cell)
    return output_bag
xypath.Bag.parent = parent

def children(bag):
    """for top-left cell, get all cells it spans"""
    outputbag = xypath.Bag(table=bag.table)
    for parent in bag:
        top, bottom, left, right = parent.properties.raw_span(always=True)
        for row in xrange(top, bottom + 1):
            for col in xrange(left, right + 1):
                outputbag = outputbag | bag.table.get_at(col, row)
    return outputbag
xypath.Bag.children = children

def rich_text(bag):
    r = bag.property.rich
    return r
xypath.Bag.rich_text = rich_text
