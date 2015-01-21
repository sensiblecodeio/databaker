from constants import *

def per_file(tableset):
    tablelist = [x.name for x in tableset.tables] # TODO
    tablelist.remove('Notes')
    return tablelist

def per_sheet(sheet):
    code = sheet.filter("Code").assert_one()
    obs = code.shift(DOWN).shift(RIGHT).fill(RIGHT).fill(DOWN) # TODO exclude key
    # note: this is MUCH faster than DOWN/RIGHT
    showtime("got obs")

    code.fill(DOWN).is_header("code", LEFT, strict=True, dim=1)
    sheet.filter("Description").assert_one().fill(DOWN).is_header("description", LEFT, strict=True, dim=2) # feels like this'd make more sense with junction
    bottom_header = code.fill(RIGHT)
    for header in bottom_header:
        header.value = header.shift(UP).shift(UP).value + ' ' + \
                       header.shift(UP).value + ' ' + \
                       header.value
        header.value = header.value.strip()
    code.fill(RIGHT).is_header('header1', UP, strict=True, dim=3)  # TODO allow arithmetic on direction tuples

    # TODO complicated parsing of A1 -> dimensions
    # TODO pre-mangling of ':', '..'
    # TODO mangling of vertical cells together

    return obs
