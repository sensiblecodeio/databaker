from constants import *

"""we could write a complicated script to split these words up, but
   it's easier just to have a lookup"""
DEMOGRAPHIC_LOOKUP = {
    "all": ["all", "all"],
    "male": ["male", "all"],
    "female": ["female", "all"],
    "part-time": ["all", "part-time"],
    "full-time": ["all", "part-time"],
    "male part-time": ["male", "part-time"],
    "male full-time": ["male", "part-time"],
    "female part-time": ["female", "part-time"],
    "female full-time": ["female", "part-time"]}

def per_file(tabs):
    "ignore tables named Notes or CV Notes"
    tablist = tabs.names  # get a list of names
    tablist.discard('Notes')
    tablist.discard('CV notes')
    return tablist

def per_sheet(sheet):
    a1 = sheet.get_at(0, 0)  # TODO 'A1'
    # TODO ensure that there's no issues with richtext
    # TODO do something about geography!
    sheet.set_header('time', a1.group("United Kingdom, (20\d\d)"))
    sheet.set_header('tablename', a1.group("Table [^ ]*   ([^-]*) -"), dim=3)
    sheet.set_header('descriptor', a1.group(" - ([^-]*) - "), dim=4)  # TODO sometimes returns None
    gender, parttime = DEMOGRAPHIC_LOOKUP[a1.group('For (.*) employee')]
    sheet.set_header('gender', gender, dim=5)
    sheet.set_header('parttime', parttime, dim=6)

    # ---
    code = sheet.filter("Code").assert_one()
    obs = code.shift(DOWN).shift(RIGHT).fill(RIGHT).fill(DOWN) # TODO exclude key
    # note: this is MUCH faster than DOWN/RIGHT
    showtime("got obs")

    code.fill(DOWN).is_header("code", LEFT, strict=True, dim=1)
    descriptions = sheet.filter("Description").assert_one().fill(DOWN)
    descriptions.is_header("description", LEFT, strict=True, dim=2) # feels like this'd make more sense with junction
    descriptions.is_bold.is_header("category", UP, dim=3)
    bottom_header = code.fill(RIGHT)
    for header in bottom_header:  # this is hacky
        if isinstance(header.value, float):  # is a percentile
            continue  # don't modify it.
        # TODO allow arithmetic on UP, DOWN etc.
        # TODO do with richtext to purge superscripts
        header._cell.value = unicode(header.shift(UP).shift(UP).value) + u' ' + \
                             unicode(header.shift(UP).value) + u' ' + \
                             unicode(header.value)
        header._cell.value = header.value.strip()
    code.fill(RIGHT).is_header('indicator', UP, strict=True)

    return obs
