import databaker.bake
from databaker.constants import *
from nose.tools import assert_equal
def per_file(tabs):
    return "*"


def per_tab(tab):
    tab.dimension("header_1", "static_value")
    tab.excel_ref("A1").fill(RIGHT).is_not_blank().dimension('header_2', DIRECTLY, ABOVE)
    obs = tab.excel_ref("A1").fill(RIGHT).is_not_blank().fill(DOWN).is_not_blank()
    assert_equal(tab.excel_ref("A6"), tab.get_at(0,5))
    assert_equal(tab.filter('merged'), tab.filter('mergeanchor').shift(UP).parent())
    assert_equal(tab.filter('merged'), tab.excel_ref("F2"))

    tab.excel_ref("A").filter("a3").assert_one()
    tab.excel_ref("3").filter("a3").assert_one()
    tab.excel_ref("A3").filter("a3").assert_one()
    tab.excel_ref("A:A").filter("a3").assert_one()
    tab.excel_ref("A:B").filter("b3").assert_one()
    tab.excel_ref("4:4").filter("c4").assert_one()
    tab.excel_ref("2:4").filter("c3").assert_one()
    tab.excel_ref("A2:C4").filter("b3").assert_one()


    tab.debug_dimensions()
    return obs

