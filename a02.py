from constants import *

def per_file(tableset):
    return "*"

def per_sheet(sheet):
    obs = sheet.filter("MGSL").assert_one().shift(DOWN).fill(RIGHT).fill(DOWN).filter(is_number)
    # note: this is MUCH faster than DOWN/RIGHT
    showtime("got obs")

    sheet.col('A').one_of(['Male', 'Female', 'All Persons']).is_header('gender', UP, dim=1)
    sheet.col('A').fill(DOWN).regex("...-... (?:19|20)\d\d").is_header('time', LEFT, strict=True)
    sheet.regex("All aged .*").is_header('ages', UP, dim=2)
    sheet.filter("Total economically active").fill(LEFT).fill(RIGHT).filter(lambda x: x.value).is_header('indicator', UP, strict=True)
    return obs
