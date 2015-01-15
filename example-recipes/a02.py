import re
from timeit import default_timer as timer
import atexit
import xypath

# NOTE shim

def is_header(bag, name, *args, **kwargs):
    if getattr(bag.table, 'headers', None) is None:
        bag.table.headers = {}
    print name, "cell.lookup({}, *{}, **{}".format(bag, args, kwargs)
    bag.table.headers[name] = lambda cell: cell.lookup(bag, *args, **kwargs)
xypath.Bag.is_header = is_header

from xypath import DOWN, RIGHT, UP, LEFT
xypath.Bag.regex = lambda self, x: self.filter(re.compile(x))

def one_of(bag, options):
    return bag.filter(lambda cell: cell.value in options)#
xypath.Bag.one_of = one_of

def showtime(msg='unspecified'):
    global last
    t = timer()
    print "{}: {} ms,  {} ms".format(msg, int(1000*(t - last)), int(1000*(t - start)))
    last = t

def onexit():
    return showtime('exit')

def is_number(cell):
    return type(cell.value) in [int, float, long]  # not CSV safe

atexit.register(onexit)
start = timer()
last = start
# =================================
import xypath

sheet = xypath.Table.from_filename('resource/table-a02.xls', table_name='seasonally adjusted')
showtime("file imported")

def per_sheet(sheet):
    obs = sheet.filter("MGSL").assert_one().shift(DOWN).fill(RIGHT).fill(DOWN).filter(is_number)
    # note: this is MUCH faster than DOWN/RIGHT
    showtime("got obs")

    sheet.col('A').one_of(['Male', 'Female', 'All Persons']).is_header('gender', UP)
    sheet.col('A').fill(DOWN).regex("...-... (?:19|20)\d\d").is_header('time', LEFT, strict=True)
    sheet.regex("All aged .*").is_header('ages', UP)
    sheet.filter("Total economically active").fill(LEFT).fill(RIGHT).is_header('indicator', UP, strict=True)
    showtime("got headers")
    return obs
# ================================
def single_iteration(ob, **foo):
    out = {}
    obj = ob._cell
    out['ob'] = obj
    for name, function in ob.table.headers.items():
        #try:
            out[name] = function(obj)
        #except xypath.xypath.NoLookupError:
        #    print "no lookup for", name
            #raise
    return out

obs = per_sheet(sheet)
for ob in obs:
    output_row=single_iteration(ob)
    print output_row
