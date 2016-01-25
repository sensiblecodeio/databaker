from xypath import DOWN, UP, LEFT, RIGHT
import bake
from hamcrest import *
import csv

# IF theres a custom template use it, Otherwise use the default.
try:
    from structure_csv_user import *
    import structure_csv_user as template
except ImportError:
    from structure_csv_default import *
    import structure_csv_default as template


ABOVE = UP
BELOW = DOWN

DIRECTLY = True
CLOSEST = False

class NotEnoughParams(Exception):
    pass

def PARAMS(position=None):
    if position is None:
        return bake.Opt.params
    else:
        try:
            return bake.Opt.params[position]
        except IndexError:
            raise NotEnoughParams("Unable to find PARAM({!r}). Only {!r} parameters were passed on the command line: {!r}".format(position, len(bake.Opt.params), bake.Opt.params))
