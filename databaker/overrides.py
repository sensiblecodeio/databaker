"""
Patches xypath and messytables.
"""

from __future__ import absolute_import, division
import re
import datetime
import warnings

import xypath
import messytables
import databaker.utils as utils
import six
from six.moves import range

six.text_type = type(u'')

class MatchNotFound(Exception):
    """failed to find match in bag.group"""
    pass

def string_cell_value(cell):
    # TODO hacky, based off value_for_dimension in bake.py
    # might not all be needed
    if cell is None:
        value = ''
    elif isinstance(cell, (str, six.text_type)):
        value = six.text_type(cell)
    elif isinstance(cell, float):
        if int(cell) == cell:
            value = str(int(cell))
        else:
            value = str(cell)
    elif cell.properties['richtext']:
        from . import richxlrd
        value = richxlrd.RichCell(cell.properties.cell.sheet, cell.y, cell.x).fragments.not_script.value
    elif isinstance(cell.value, (str, six.text_type, float)):
        value = string_cell_value(cell.value)
    else:
        raise NotImplementedError("Tried to stringify {!r}, a {}".format(cell.value, type(cell.value)))
    return value.strip()


class Dimension(object):

# string signature: table.Dimension(label, string_literal)
# bag signature:    bag.Dimension(label, direction, strictness)
# multidimension signature: table.Dimension(label, [subdimensions])

    def __init__(self, bag, label, param1, direction=None, primary_dimension=True, join_function=None):
        """self: the dimension object because this is init
           bag: a bag - either a dimension bag or a table (in the case of a string)
           label: dimension label
           param1: either a strictness for a bag or a literal string
           direction: a direction for a bag"""
        if join_function is None:
            self.join_function = ' '.join
        else:
            self.join_function = join_function
        self.bag = bag
        self.direction = direction  # direction
        if isinstance(param1, six.string_types):
            self.strict = None
            self.string = param1
            self.subdim = []
        elif isinstance(param1, bool):
            self.strict = param1
            self.string = None
            self.subdim = []
        else:
            assert isinstance(param1[0], Dimension), type(param1[0])
            self.strict = None
            self.string = None
            self.subdim = param1
        if primary_dimension:
            self.bag.table.append_dimension(label, self)

    def __call__(self, cell):
        if self.string is not None:
            return self.string
        if self.strict is not None:
            return cell.lookup(self.bag, self.direction, self.strict)
        if self.subdim != []:
            builder = [string_cell_value(subdim(cell)) for subdim in self.subdim]
            return self.join_function(builder)

def dimension(self, *args, **kwargs):
    Dimension(self, *args, **kwargs)
    return self

def subdim(self, *args, **kwargs):
    return Dimension(self, "--fakelabel--", *args, primary_dimension=False, **kwargs)

xypath.Bag.dimension = dimension
xypath.Bag.subdim = subdim


# === XLSCell Overrides ===================================

def text_date(cell):
    xls_format = cell.properties['formatting_string'].upper()
    quarter = int((cell.value.month -1 ) // 3) + 1  # TODO testme!
    print("quarter" + str(quarter))
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
            for col in range(left, right + 1):
                bag = bag | table.get_at(col, None)
        elif left is None and right is None:
            for row in range(top, bottom + 1):
                bag = bag | table.get_at(None, row)
        else:
            for row in range(top, bottom + 1):
                for col in range(left, right + 1):
                    bag = bag | table.get_at(col, row)
        return bag
xypath.Table.excel_ref = excel_ref

def append_dimension(table, label, func):
    if getattr(table, 'headers', None) is None:
        table.headers = {}
        table.max_header = 0
        table.headernames = [None]
    if isinstance(label, six.string_types):
        table.max_header += 1
        number = table.max_header
        table.headernames.append(label)
    else:
        assert isinstance(label, int)
        number = label
    table.headers[number] = func
    utils.showtime("got header {}".format(utils.dim_name(label)))
xypath.Table.append_dimension = append_dimension

def debug_dimensions(table):
    table.append_dimension("ref", lambda cell: xypath.contrib.excel.excel_location(cell))
    table.append_dimension("table", lambda cell: cell.table.name)

xypath.Table.debug_dimensions = debug_dimensions

# === Bag Overrides =======================================

xypath.Bag.regex = lambda self, x: self.filter(re.compile(x))

def glue(bag, expand_function, join_function=None, blank=True):
    """Each cell in the bag is replaced with the content of a number of cells:
       the cell in question and the cells specified by cell_bag.expand_function()
       The other cells will be blanked.
       The cells values will be concatenated with the join_function."""
    if join_function is None:
        join_function = ' '.join
    for cell in bag:
        target_cells = expand_function(cell)
        value = join_function(string_cell_value(value_cell) for value_cell in target_cells)
        if blank:
            for tcell in target_cells:
                tcell._cell.value = ""
        cell._cell.value = value
    return bag
xypath.Bag.glue = glue

def is_date(bag):
    return bag.filter(lambda cell: utils.datematch(cell.value, silent=True))
xypath.Bag.is_date = is_date

def is_number(bag):
    return bag.filter(lambda cell: isinstance(cell.value, (int, float, int)))
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
        for row in range(top, bottom + 1):
            for col in range(left, right + 1):
                outputbag = outputbag | bag.table.get_at(col, row)
    return outputbag
xypath.Bag.children = children

def rich_text(bag):
    r = bag.property.rich
    return r
xypath.Bag.rich_text = rich_text

def spaceprefix(bag, count):
    """filter: cells starting with exactly count whitespace: no more, no less"""
    return bag.filter(re.compile("^\s{%s}\S" % count))
xypath.Bag.spaceprefix = spaceprefix

def is_whitespace(bag):
    """filter: cells which do not contain printable characters"""
    return bag.filter(lambda cell: not six.text_type(cell.value).strip())
xypath.Bag.is_whitespace = is_whitespace

def is_not_whitespace(bag):
    """filter: cells which do contain printable characters"""
    return bag.filter(lambda cell: six.text_type(cell.value).strip())
xypath.Bag.is_not_whitespace = is_not_whitespace

def by_index(bag, items):
    """filter: return numbered items from a bag.
       Note that this is 1-indexed!
       Items can be a list or a single number"""
    if isinstance(items, int):
        return bag.by_index([items])
    new = xypath.Bag(table=bag.table)
    for i, cell in enumerate(bag):
        if i+1 in items:
            new.add(cell._cell)
            if i+1 == max(items):
                return new
    raise xypath.XYPathError("get_nth needed {} items, but bag only contained {}.\n{!r}".format(max(items), len(bag), bag))
xypath.Bag.by_index = by_index

