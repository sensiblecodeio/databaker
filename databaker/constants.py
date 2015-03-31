from xypath import DOWN, UP, LEFT, RIGHT
import bake
from hamcrest import *

OBS = -9
DATAMARKER = -8
STATUNIT = -7
MEASURETYPE = -6
UNITMULTIPLIER = -5
UNITOFMEASURE = -4
GEOG = -3
TIME = -2
TIMEUNIT = -1
STATPOP = 0

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
