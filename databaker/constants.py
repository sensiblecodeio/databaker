from xypath import DOWN, UP, LEFT, RIGHT
import bake
from template_csv_default import *        # Import tempalte so constants are availible to recipe
from hamcrest import *

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
