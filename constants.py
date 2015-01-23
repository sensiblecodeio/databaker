from xypath import DOWN, UP, LEFT, RIGHT
from bake import showtime
import overrides

def is_number(cell):
    return type(cell.value) in [int, float, long]
