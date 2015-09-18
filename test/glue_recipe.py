import re
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
    return tab
