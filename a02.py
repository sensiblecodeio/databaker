import re
from timeit import default_timer as timer
import atexit
import xypath

# NOTE shim
def col(sheet, column):
    if isinstance(column, basestring):
        raise NotImplementedError  # TODO
    else:
        assert isinstance(column, int)
        return sheet._x_index[column]
xypath.Table.col = col

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

obs = sheet.filter("MGSL").assert_one().shift(xypath.DOWN).fill(xypath.RIGHT).fill(xypath.DOWN).filter(is_number)
# note: this is MUCH faster than DOWN/RIGHT
showtime("got obs")

genders = sheet.col(0).filter(lambda x: x.value in ['Male', 'Female', 'All Persons'])
showtime("got genders")

times = sheet.col(0).fill(xypath.DOWN).filter(re.compile("...-... (?:19|20)\d\d"))
showtime("got times")

ages = sheet.filter(re.compile("All aged .*")) # surprised this is fast!
showtime("all_age_labels")

indicators = sheet.filter("Total economically active").fill(xypath.LEFT).fill(xypath.RIGHT)
showtime("indicators")

for i, ob in enumerate(obs):
    if i% 283 == 0:
        out = {}
        out['ob'] = ob.value
        out['gender'] = ob.lookup(genders, xypath.UP)
        out['time'] = ob.lookup(times, xypath.LEFT, strict=True)
        out['age'] = ob.lookup(ages, xypath.UP)
        out['indicator'] = ob.lookup(indicators, xypath.UP, strict=True)
        print out

# TODO filter

