import re
from databaker.constants import *
import databaker.bake
from nose.tools import assert_equal

def per_file(tabs):
    return "Table 2b"

def per_tab(tab):
    quarters = tab.filter(re.compile("Q\d"))
    years = quarters.shift(LEFT).is_not_blank()
    tab.dimension("KITTEN", [tab.subdim('NOPE', "-"),
                             quarters.subdim("NOPE1", DIRECTLY, LEFT),
                             years.subdim("NOPE2", CLOSEST, ABOVE)])
    print quarters, years
    tab.dimension("foo", "bar")
    return tab
