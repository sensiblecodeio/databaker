from __future__ import absolute_import, division
import databaker.utils
from nose.tools import assert_equal
def per_file(tabs):
    return tabs.names

def per_tab(tab):
    tab.dimension("foo", "bar")
    parse = lambda x: databaker.utils.parse_ob(tab.excel_ref(x))
    assert_equal(parse("C3"), ('2015', ''))
    assert_equal(parse("C4"), ('2015', ''))
    assert_equal(parse("C5"), ('2015', ''))
    assert_equal(parse("E3"), ('2015', 'b'))
    assert_equal(parse("G3"), ('2015', 'a'))
    return tab
