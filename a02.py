from constants import *

def per_file(tableset):
    return "*"

def per_tab(tab):
    obs = tab.filter("MGSL").assert_one().shift(DOWN).fill(RIGHT).fill(DOWN).filter(is_number).is_not_italic
    # note: this is MUCH faster than DOWN/RIGHT
    showtime("got obs")

    tab.col('A').one_of(['Male', 'Female', 'All Persons']).is_header('gender', UP, dim=1)
    tab.col('A').fill(DOWN).regex("...-... (?:19|20)\d\d").is_header('time', LEFT, strict=True)  # why fill(DOWN)?
    tab.regex("All aged .*").is_header('ages', UP, dim=2)
    tab.filter("Total economically active").fill(LEFT).fill(RIGHT).is_not_blank.is_header('indicator_', UP, strict=True, dim=3)
    # nope. This is a third dimension. Don't use column 5 for anything.
    # TODO tabname not trivially available :(
    # tab.set_header('adjusted_yn', tab.name+"foo", dim=4)
    return obs
