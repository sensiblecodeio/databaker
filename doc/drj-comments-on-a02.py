"""
drj:

Overall, I think the approach of "It's just a Python program" is good one. It
means we don't have to fiddle around making a compiler (we have to make bits
of one, but that's okay).

Python is well known for its clarity and several projects use it because it
is beginning friendly (ccc-gistemp, Software Carpentry).

I like the idea that most of the time most of the interesting code is of the
form:

    thing.operation().other_operation().got_header()

In particular, it's easy to see how we make make more operations, for common
operations (so if we do .fill(RIGHT).fill(DOWN) a lot we can have
.fill(RECTANGLE) or similar).
"""

from __future__ import absolute_import
from constants import *

def per_file(tableset):
    return "*"

def per_sheet(sheet):

    # This seems a bit long winded but I worked it out. Wonder if we need a more direct "rectangle" thing.
    obs = sheet.filter("MGSL").assert_one().shift(DOWN).fill(RIGHT).fill(DOWN).filter(is_number)
    # note: this is MUCH faster than DOWN/RIGHT
    showtime("got obs")

    # Like the fact that we can declare facts about the spreadsheet in any particular order.
    # (Though we should probably recommend an order).

    # As previously, maybe "is_header" should be "declare_header" or "make_header"
    sheet.col('A').one_of(['Male', 'Female', 'All Persons']).file(LEFT).fill(RIGHT).is_header('gender', UP)

    # This seems a bit confusing. mostly because... regex... BIG SCARE!
    # (Although actually when I thought about it, it was fine)
    sheet.col('A').fill(DOWN).regex("...-... (?:19|20)\d\d").is_header('time', LEFT, strict=True)
    sheet.regex("All aged .*").is_header('ages', UP)

    # Not sure about the "strict" switch, flipping it on and off seems a bit magic.
    # We could use alternatives like "ANYWHERE_ABOVE", or "STRICTLY_LEFT".
    sheet.filter("Total economically active").fill(LEFT).fill(RIGHT).is_header('indicator', UP, strict=True)


    return obs

