from __future__ import absolute_import
from databaker.constants import *

def per_file(tabs):
    return '*'

def per_tab(tab):
    tab.dimension(STATUNIT, PARAMS()[0])
    tab.dimension(MEASURETYPE, PARAMS()[1])
    tab.dimension(UNITMULTIPLIER, PARAMS()[2])
    tab.dimension(UNITOFMEASURE, PARAMS()[3])
    tab.dimension(STATPOP, PARAMS()[4])
    return tab.excel_ref("A1")
