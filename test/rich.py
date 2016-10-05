from __future__ import absolute_import
from __future__ import print_function
import databaker.bake
from databaker.constants import *
from nose.tools import assert_equal

def per_file(tabs):
    return tabs.names

def per_tab(tab):
    obs = tab.is_not_blank()
    for ob in obs:
        print(ob.properties.rich, ob.value)

    return []
