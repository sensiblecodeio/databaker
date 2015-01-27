from constants import *

# NOTE  <A654 u'a  Employees on adult rates whose pay for the survey pay-period was not affected by absence.'>,

"""we could write a complicated script to split these words up, but
   it's easier just to have a lookup"""

def per_file(tabs):
    "ignore tables named Notes or CV Notes"
    tablist = tabs.names  # get a list of names
    tablist.discard('Notes')
    tablist.discard('CV notes')
    return tablist

def per_tab(tab):
    # TODO tab.get_at("A1")
    tab.set_header("A1", tab.get_at(0, 0).value, dim=3)
    # TODO do something about geography!

    code = tab.filter("Code").assert_one()
    obs = code.shift(DOWN).shift(RIGHT).fill(RIGHT).fill(DOWN) # TODO exclude key
    # note: this is MUCH faster than DOWN/RIGHT
    showtime("got obs")

    code.fill(DOWN).is_header("code", LEFT, strict=True, dim=1)
    descriptions = tab.filter("Description").assert_one().fill(DOWN)
    descriptions.is_header("description", LEFT, strict=True, dim=2) # feels like this'd make more sense with junction
    descriptions.is_bold.is_header("category", UP, dim=3)
    bottom_header = code.fill(RIGHT)
    for header in bottom_header:  # this is hacky
        if isinstance(header.value, float):  # is a percentile
            continue  # don't modify it.
        # TODO allow arithmetic on UP, DOWN etc.
        header._cell.value = unicode(header.shift(UP).shift(UP).value) + u' ' + \
                             unicode(header.shift(UP).value) + u' ' + \
                             unicode(header.value)
        header._cell.value = header.value.strip()
    code.fill(RIGHT).is_header('indicator', UP, strict=True)

    return obs
