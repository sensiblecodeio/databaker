from __future__ import absolute_import, division
from databaker.constants import *
def per_file(tabs):
    return '*'

def per_tab(tab):
    h = tab.filter("h").dimension("h", DIRECTLY, ABOVE)
    s = tab.excel_ref("A").is_not_blank().dimension(TIME, DIRECTLY, LEFT)
    obs = h.waffle(s)
    return obs
