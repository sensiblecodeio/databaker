from __future__ import absolute_import
import databaker.bake
from databaker.constants import *
from nose.tools import assert_equal
def per_file(tabs):
    return tabs.names


def per_tab(tab):
    tab.dimension("header_1", "static_value")
    tab.excel_ref("A1").fill(RIGHT).is_not_blank().dimension(TIME, DIRECTLY, ABOVE)
    obs = tab.excel_ref("A1").fill(RIGHT).is_not_blank().fill(DOWN).is_not_blank()


    assert_equal(tab.filter('merged'), tab.filter('mergeanchor').shift(UP).parent())
    assert_equal(tab.filter('merged'), tab.excel_ref("F2"))

    mergegroup = tab.filter('mergeanchor').shift(UP).children()
    assert_equal(mergegroup, tab.filter('merged').extrude(*RIGHT).extrude(*DOWN))

    assert_equal(tab.excel_ref("A6"), tab.get_at(0,5))
    tab.excel_ref("A").filter("a3").assert_one()
    tab.excel_ref("3").filter("a3").assert_one()
    tab.excel_ref("A3").filter("a3").assert_one()
    tab.excel_ref("A:A").filter("a3").assert_one()
    tab.excel_ref("A:B").filter("b3").assert_one()
    tab.excel_ref("4:4").filter("c4").assert_one()
    tab.excel_ref("2:4").filter("c3").assert_one()
    tab.excel_ref("A2:C4").filter("b3").assert_one()

    counting = tab.filter("rabbit").fill(RIGHT).is_number()
    assert not counting.filter("sir")
    assert counting.filter(lambda x: x.value == 5)
    assert_equal(len(counting), 5)

    assert_equal(tab.filter("rabbit").group("(a.*i)"), "abbi")

    assert_equal(len(tab.one_of(["rabbit", lambda x: x.value == "sir"])), 2)

    #--
    assert_equal(set(cell.value for cell in tab.excel_ref('R3:T4')),
                 set(["Jan 2001"]))
    assert_equal(tab.excel_ref("Q3").value, "2001 Q1")
    assert_equal(tab.excel_ref("Q4").value, "2001")

    tab.debug_dimensions()
    return obs

