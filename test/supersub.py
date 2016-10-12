from __future__ import absolute_import, print_function, division
from databaker.constants import *
print(PARAMS())

def per_file(tableset):
    return "*"

def per_tab(tab):
    obs = tab.filter("ANCHOR").assert_one().shift(DOWN).shift(RIGHT)
    print(obs)
    tab.filter("ANCHOR").shift(DOWN).assert_one().dimension(TIME, DIRECTLY, LEFT)
    yield obs
