from xypath import DOWN, UP, LEFT, RIGHT
from hamcrest import *

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


