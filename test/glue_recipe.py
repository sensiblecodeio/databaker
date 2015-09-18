import re
import databaker.bake
from nose.tools import assert_equal

def per_file(tabs):
    return "Table 2b"

def per_tab(tab):
    all_start = re.compile(".*All.*")
    glue_bag = tab.filter(all_start)
    print ("alls:", glue_bag)
    glue_bag.glue(lambda cell: cell.extrude(0,3))
    print ("glued:", glue_bag)
    print ("alls post:", tab.filter(all_start))
    print ("all start post:", tab.filter(all_start))

    tab.dimension("foo", "bar")
    return tab
