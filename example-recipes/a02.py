import re
from timeit import default_timer as timer
import atexit
import xypath

# NOTE shim

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

obs = sheet.filter("MGSL").assert_one().shift(DOWN).fill(RIGHT).fill(DOWN).filter(is_number)
# note: this is MUCH faster than DOWN/RIGHT
showtime("got obs")

genders = sheet.col('A').one_of(['Male', 'Female', 'All Persons'])
showtime("got genders")

times = sheet.col('A').fill(DOWN).regex("...-... (?:19|20)\d\d")
showtime("got times")

ages = sheet.regex("All aged .*") # surprised this is fast!
showtime("all_age_labels")

indicators = sheet.filter("Total economically active").fill(LEFT).fill(RIGHT)
showtime("indicators")

def for_loop():
    for i in obs.unordered_cells:
        out = {}
        out['ob'] = ob

        out['gender'] = ob.lookup(genders, UP)
        try:
            out['time'] = ob.lookup(times, LEFT, strict=True)
        except xypath.xypath.NoLookupError:
            continue
        out['age'] = ob.lookup(ages, UP)
        out['indicator'] = ob.lookup(indicators, UP, strict=True)
        #out['geographic'] = 'UK'
        #out['statistical_unit'] = 'People'
        mystical_output_function(out)

def mystical_output_function(p):
    for item in p:
        print p[item].value,
    print

for_loop()

def magic_loop():
    presto = Magic(obs)
    presto.label("genders", UP)
    presto.evaluate()

def single_iteration(ob):
    out = {}
    out['ob'] = ob.value
    out['gender'] = ob.lookup(genders, UP)
    out['time'] = ob.lookup(times, LEFT, strict=True)
    out['age'] = ob.lookup(ages, UP)
    out['indicator'] = ob.lookup(indicators, UP, strict=True)
    return out
