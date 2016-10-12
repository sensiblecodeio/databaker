from __future__ import absolute_import, division
from xypath import DOWN, UP, LEFT, RIGHT
from hamcrest import *
import csv

# IF theres a custom template use it, Otherwise use the default.
try:
    from structure_csv_user import *
    import structure_csv_user as template
except ImportError:
    from .structure_csv_default import *
    from . import structure_csv_default as template


ABOVE = UP
BELOW = DOWN

DIRECTLY = True
CLOSEST = False

constant_params = [] # Overridden in main().

class NotEnoughParams(Exception):
    pass

def PARAMS(position=None):
    if position is None:
        return constant_params
    else:
        try:
            return constant_params[position]
        except IndexError:
            raise NotEnoughParams("Unable to find PARAM({!r}). Only {!r} parameters were passed on the command line: {!r}".format(position, len(constant_params), constant_params))
