from xypath import DOWN, UP, LEFT, RIGHT

OBS = -4
DATAMARKER = -3
GEOG = -2
TIME = -1
TIMEUNIT = 0

class STRICT(object):
    pass

def is_number(cell):
    return type(cell.value) in [int, float, long]

