from databaker.constants import *

def per_file(tableset):
    return "*"

def per_tab(tab):
    obs = tab.filter("MGSL").assert_one().shift(DOWN).fill(RIGHT).fill(DOWN).filter(is_number).is_not_italic

    tab.col('A').one_of(['Male', 'Female', 'All Persons']).is_header('gender', UP)
    tab.col('A').regex("...-... (?:19|20)\d\d").is_header(TIME, LEFT, strict=True)
    tab.regex("All aged .*").is_header('ages', UP)
    tab.filter("Total economically active").fill(LEFT).fill(RIGHT).is_not_blank.is_header('indicator', UP, strict=True)

    tab.set_header('adjusted_yn', tab.name)
    return obs
