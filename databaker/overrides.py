"""
Patches xypath and messytables.
"""

import re

import xypath
import messytables

import bake

class Dimension(object):

# TODO string signature: (dimself, bag, label, label item)
# TODO bag signature:    (dimself, bag, label, direction, striict)

    def __init__(self, bag, label, selector=None, strict=False):
        """bag: a bag - either a dimension bag or a table (in the case of a string)
           label: dimension label
           selector: either a direction+strictness for a bag or a literal string TODO
           strict: vestigal (soon)"""

        self.bag = bag
        self.selector = selector
        self.strict = strict
        self.bag.table.append_dimension(label, self)

    def __call__(self, cell):
        if isinstance(self.selector, basestring):
            return self.selector
        else:
            return cell.lookup(self.bag, self.selector, self.strict)

def is_header(*args, **kwargs):
    Dimension(*args, **kwargs)

xypath.Bag.is_header = is_header # is this ok?
xypath.Table.set_header = is_header

# ======

class DirBag(object):
    def __init__(self, bag, direction, *args, **kwargs):
        self.bag = bag
        self.direction = direction
        self.args = args
        self.kwargs = kwargs

    def dimension(self, label):
        f = lambda cell: cell.lookup(self.bag, self.direction, *self.args, **self.kwargs)
        self.bag.table.append_dimension(label, f)

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
    coord = xypath.contrib.excel.excel_address_coordinate(reference)
    return table.get_at(*coord)
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
    bake.showtime("got header {}".format(label))
xypath.Table.append_dimension = append_dimension

# === Bag Overrides =======================================

xypath.Bag.regex = lambda self, x: self.filter(re.compile(x))

def with_direction(bag, direction, *args, **kwargs):
    return DirBag(bag, direction, *args, **kwargs)
xypath.Bag.with_direction = with_direction

def group(bag, regex):
    """get the text"""
    bag.assert_one()
    match = re.search(regex, bag.value)
    if not match:
        return None
    matchtext = match.groups(0)[0]
    assert matchtext
    return matchtext
xypath.Bag.group = group

def one_of(bag, options):
    return bag.filter(lambda cell: cell.value in options)#
xypath.Bag.one_of = one_of
