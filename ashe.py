from databaker.constants import *

def per_file(tabs):
    "ignore tables named Notes or CV Notes"
    tablist = tabs.names  # get a list of names
    tablist.discard('Notes')
    tablist.discard('CV notes')
    return tablist

def per_tab(tab):
    tab.set_header("A1", tab.excel_ref("A1").value)

    code = tab.filter("Code").assert_one()
    obs = code.shift(DOWN).shift(RIGHT).fill(RIGHT).fill(DOWN) # TODO exclude keys at right and below

    code.fill(DOWN).is_header(GEOG, LEFT, strict=True)
    descriptions = tab.filter("Description").assert_one().fill(DOWN)
    descriptions.is_header("description", LEFT, strict=True) # feels like this'd make more sense with junction
    descriptions.is_bold.is_header("category", UP)

    # Merges three cells vertically together to make the one they really are
    bottom_header = code.fill(RIGHT)
    for i, header in enumerate(bottom_header):
        if isinstance(header.value, float):  # is a percentile
            continue  # don't modify it.
        header._cell.value = unicode(header.shift(UP).shift(UP).value) + u' ' + \
                             unicode(header.shift(UP).value) + u' ' + \
                             unicode(header.value) + str(i)
        header._cell.value = header.value.strip()
    code.fill(RIGHT).is_header('indicator', UP, strict=True)

    return obs
