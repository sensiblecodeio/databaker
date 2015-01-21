from constants import *

def per_file(tableset):
    tablelist = set(x.name for x in tableset.tables) # TODO
    tablelist.discard('Notes')
    tablelist.discard('CV notes')
    return tablelist

def per_sheet(sheet):
    code = sheet.filter("Code").assert_one()
    obs = code.shift(DOWN).shift(RIGHT).fill(RIGHT).fill(DOWN) # TODO exclude key
    # note: this is MUCH faster than DOWN/RIGHT
    showtime("got obs")

    code.fill(DOWN).is_header("code", LEFT, strict=True, dim=1)
    descriptions = sheet.filter("Description").assert_one().fill(DOWN)
    descriptions.is_header("description", LEFT, strict=True, dim=2) # feels like this'd make more sense with junction
    descriptions.filter(lambda cell: cell.properties['bold']).is_header("category", UP, dim=3)
    bottom_header = code.fill(RIGHT)
    for header in bottom_header:
        if isinstance(header.value, float):  # is a percentile
            continue  # don't modify it.
        header._cell.value = unicode(header.shift(UP).shift(UP).value) + u' ' + \
                             unicode(header.shift(UP).value) + u' ' + \
                             unicode(header.value)
        header._cell.value = header.value.strip()
    code.fill(RIGHT).is_header('indicator', UP, strict=True)  # TODO allow arithmetic on direction tuples

    # TODO complicated parsing of A1 -> dimensions
    # TODO complicated parsing of left hand - e.g. age + profession vs. region + constituency

    return obs
