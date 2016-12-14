import xlutils, xypath
import databaker
import os, warnings
import databaker.constants
from databaker.constants import *      # also brings in template
import databaker.databakersolo as ds   # causes the xypath.loader to be overwritten

from databaker.jupybakeutils import HDim, HDimConst, ConversionSegment
from databaker.jupybakecsv import writetechnicalCSV, OLDwritetechnicalCSV, readtechnicalCSV
from databaker.jupybakecsv import headersfromwdasegment, extraheaderscheck, checktheconstantdimensions, checksegmentobsvalues
from databaker.jupybakecsv import wdamsgstrings, CompareConversionSegments
from databaker.jupybakehtml import savepreviewhtml


def loadxlstabs(inputfile, sheetids="*"):
    print("Loading %s which has size %d bytes" % (inputfile, os.path.getsize(inputfile)))
    tableset = xypath.loader.table_set(inputfile, extension='xls')
    tabs = list(xypath.loader.get_sheets(tableset, sheetids))
    tabnames = [ tab.name  for tab in tabs ]
    print("Table names: %s" % str(tabnames))
    
    if sheetids != "*":
        if type(sheetids) == str:
            sheetids = [sheetids]
        assert type(sheetids) in [list, tuple], ("What type is this?", type(sheetids))
        for sid in sheetids:
            assert sid in tabnames, (sid, "missing from found tables")
        assert len(sheetids) == len(tabnames), ("Number of selected tables disagree", "len(sheetids) == len(tabnames)", len(sheetids), len(tabnames))
    if len(set(tabnames)) != len(tabnames):
        warnings.warn("Duplicates found in table names list")
    return tabs
    
import pandas as pd
def topandas(conversionsegment):
    return pd.DataFrame.from_dict(conversionsegment.lookupall())

