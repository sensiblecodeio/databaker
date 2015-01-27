from constants import *

def per_file(tableset):
    return "*"

def per_tab(tab):
    obs = tab.filter("MGSL").assert_one().shift(DOWN).fill(RIGHT).fill(DOWN).filter(is_number).is_not_italic
    # note: this is MUCH faster than DOWN/RIGHT
    tab.col('A').one_of(['Male', 'Female', 'All Persons']).with_direction(UP).dimension("gender")
    tab.col('A').regex("...-... (?:19|20)\d\d").with_direction(LEFT, STRICT).dimension(TIME)
    tab.regex("All aged .*").with_direction(UP).dimension("ages")
    tab.filter("Total economically active").fill(LEFT).fill(RIGHT).is_not_blank.with_direction(UP, STRICT).dimension("indicator")
    # TODO tabname not trivially available :(
    # tab.set_header('adjusted_yn', tab.name+"foo", dim=4)
    return obs
