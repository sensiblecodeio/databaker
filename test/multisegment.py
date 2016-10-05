from __future__ import absolute_import
import databaker.bake
from databaker.constants import *
from nose.tools import assert_equal

def per_file(tabs):
    return tabs.names

def per_tab(tab):
    obs = tab.filter("ANCHOR").fill(DOWN).shift(RIGHT).extrude(3,0).is_not_blank()
    tab.filter("ANCHOR").fill(DOWN).dimension("left", DIRECTLY, LEFT)
    tab.one_of(["A", "B", "C", "D", "E", "F"]).dimension("top1", DIRECTLY, UP)
    yield obs

    obs = tab.filter("ANCHOR2").fill(RIGHT).fill(DOWN).is_not_blank()
    tab.filter("ANCHOR").fill(DOWN).dimension("left", DIRECTLY, LEFT)
    tab.one_of(["U", "V", "W", "X", "Y", "Z"]).dimension("top2", DIRECTLY, UP)
    yield obs
