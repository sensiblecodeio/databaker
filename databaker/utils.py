from __future__ import absolute_import, print_function, division
from timeit import default_timer as timer
import re
import warnings
import six

# If there's a custom template, use it. Otherwise use the default.
try:
    import structure_csv_user as template
    from structure_csv_user import *
except ImportError:
    from . import structure_csv_default as template
    from .structure_csv_default import *

def datematch(date, silent=False):
    """match mmm yyyy, mmm-mmm yyyy, yyyy Qn, yyyy"""
    if not isinstance(date, six.string_types):
        if isinstance(date, float) and date>=1000 and date<=9999 and int(date)==date:
            return "Year"
        if not silent:
            warnings.warn("Couldn't identify date {!r}".format(date))
        return ''
    d = date.strip()
    if re.match('\d{4}$', d):
        return 'Year'
    if re.match('\d{4} [Qq]\d$', d):
        return 'Quarter'
    if re.match('[A-Za-z]{3}-[A-Za-z]{3} \d{4}$', d):
        return 'Quarter'
    if re.match('[A-Za-z]{3} \d{4}$', d):
        return 'Month'
    if not silent:
        warnings.warn("Couldn't identify date {!r}".format(date))
    return ''

def dim_name(dimension):
    # should agree with constants.py
    if isinstance(dimension, int) and dimension <= 0:
        # the last dimension is dimension 0; but we index it as -1.
        return template.dimension_names[dimension-1]
    else:
        return dimension

start = timer()
last = start
showtime_enabled = True

def showtime(msg='unspecified'):
    if not showtime_enabled:
        return
    global last
    t = timer()
    print("{}: {:.3f}s,  {:.3f}s total".format(msg, t - last, t - start))
    last = t
