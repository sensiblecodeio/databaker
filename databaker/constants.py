from xypath import DOWN, UP, LEFT, RIGHT
import bake
from hamcrest import *
import csv

# IF theres a custom template use it, Otherwise use the default.
try:
    from structure_csv_user import *
except ImportError:
    from structure_csv_default import *


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

# Funtion to dynamically assign colours to dimensions for preview
def create_colourlist():
    colours = ["lavender", "violet", "gray25", "sea_green",
              "pale_blue", "blue", "gray25", "rose", "tan", "light_yellow", "light_green", "light_turquoise",
              "light_blue", "sky_blue", "plum", "gold", "lime", "coral", "periwinkle", "ice_blue", "aqua"]
    numbers = []
    for i in range(len(SKIP_AFTER)-1, -(len(colours) - len(SKIP_AFTER)), -1):
        numbers.append(-i)
    colourlist = dict(zip(numbers, colours))
    return colourlist

def rewrite_headers(row,dims):
    for i in range(0,len(row)):
        if i >= len(start.split(',')):
            which_cell_in_spread = (i - len(start.split(','))) % len(value_spread)
            which_dim = (i - len(start.split(','))) / len(value_spread)
            which_dim = int(which_dim)
            if value_spread[which_cell_in_spread] == 'value':
                row[i] = dims[which_dim]
    return row
