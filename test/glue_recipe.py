import re
from databaker.constants import *
import databaker.bake
from nose.tools import assert_equal

def per_file(tabs):
    return "Table 2b"

def per_tab(tab):
    all_start = re.compile(".*All.*")
    glue_bag = tab.filter(all_start)
    glue_bag.glue(lambda cell: cell.extrude(0,3))
    alls = tab.filter(all_start)
    expected = ['All New Work', 'All Repair and Maintenance', 'All Work']
    for a,b in zip(expected, alls):
        assert a in b.value, [a, b]
    tab.dimension("foo", "bar")
    alls.dimension("all", DIRECTLY, ABOVE)
    year = tab.filter(lambda x: x.value == 2014)
    year.dimension("year", DIRECTLY, LEFT)

    # confirm that cells in indexes are still correct
    for cell in alls:
        assert cell == tab.get_at(cell.x, cell.y)

    print alls
    return alls.waffle(year)
