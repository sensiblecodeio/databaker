from xypath import DOWN, UP, LEFT, RIGHT

OBS = -4
DATAMARKER = -3
GEOG = -2
TIME = -1
TIMEUNIT = 0

ABOVE = UP
BELOW = DOWN

DIRECTLY = True
CLOSEST = False

def is_number(cell):
    return type(cell.value) in [int, float, long]

