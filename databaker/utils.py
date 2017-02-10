from __future__ import absolute_import, print_function, division
from timeit import default_timer as timer
import re
import warnings
import six
import xypath
import io
import databaker.richxlrd.richxlrd as richxlrd
from datetime import datetime
from databaker.utf8csv import UnicodeWriter

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
        if (isinstance(date, float) or isinstance(date, int)) and date>=1000 and date<=9999 and int(date)==date:
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


