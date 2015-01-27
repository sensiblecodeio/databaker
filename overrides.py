import re
import xypath
import messytables
import bake

def cell_repr(cell):
    column = xypath.contrib.excel.excel_column_label(cell.x+1)
    return "<{}{} {!r}>".format(column, cell.y+1, cell.value)
xypath.xypath._XYCell.__repr__ = cell_repr

@property
def tabnames(tableset):
    return set(x.name for x in tableset.tables)
messytables.TableSet.names = tabnames

def is_header(bag, name, direction, dim=None, *args, **kwargs):
    if dim:
        bake.update_dim(name, dim) # dim given is one-indexed - see ONS CSV spec.
    if getattr(bag.table, 'headers', None) is None:
        bag.table.headers = {}
    print name, "cell.lookup({}, {}, dim={}, *{}, **{}".format(bag, direction, dim, args, kwargs)
    bag.table.headers[name] = lambda cell: cell.lookup(bag, direction, *args, **kwargs)
    bake.showtime("got header {}".format(name))
xypath.Bag.is_header = is_header

def set_header(bag, name, text, dim=None):
    if dim:
        bake.update_dim(name, dim)
    if getattr(bag.table, 'headers', None) is None:
        bag.table.headers = {}
    bag.table.headers[name] = lambda foo: text
xypath.Bag.set_header = set_header

xypath.Bag.regex = lambda self, x: self.filter(re.compile(x))

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
