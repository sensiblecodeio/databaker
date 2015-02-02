"""
Patches xypath and messytables.
"""

import re

import xypath
import messytables

import bake

class DirBag(object):
    def __init__(self, bag, direction, *args, **kwargs):
        self.bag = bag
        self.direction = direction
        self.args = args
        self.kwargs = kwargs

    def dimension(self, label):
        if getattr(self.bag.table, 'headers', None) is None:
            self.bag.table.headers = {}
            self.bag.table.max_header = 0
            self.bag.table.headernames = [None]
        if isinstance(label, basestring):
            number = self.bag.table.max_header + 1
            self.bag.table.max_header = number
            self.bag.table.headernames.append(label)
        else:
            assert isinstance(label, int)
            number = label
        self.bag.table.headers[number] = lambda cell: cell.lookup(self.bag, self.direction, *self.args, **self.kwargs)
        bake.showtime("got header {}".format(label))

def cell_repr(cell):
    column = xypath.contrib.excel.excel_column_label(cell.x+1)
    return "<{}{} {!r}>".format(column, cell.y+1, cell.value)
xypath.xypath._XYCell.__repr__ = cell_repr

@property
def tabnames(tableset):
    return set(x.name for x in tableset.tables)
messytables.TableSet.names = tabnames

def is_header(bag, name, direction, dim=None, *args, **kwargs):
    bag.with_direction(direction, *args, **kwargs).dimension(name)
xypath.Bag.is_header = is_header

def set_header(bag, name, text, dim=None):
    if getattr(bag.table, 'headers', None) is None:
        bag.table.headers = {}
        bag.table.max_header = 0
        bag.table.headernames = [None]
    if dim:
        bake.update_dim(name, dim)
    if getattr(bag.table, 'headers', None) is None:
        bag.table.headers = {}
    bag.table.headers[name] = lambda foo: text
xypath.Bag.set_header = set_header

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
