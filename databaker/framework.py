import xlutils, xypath
import databaker
import os, warnings
import databaker.constants
from databaker.constants import *      # also brings in template

import xypath.loader
import databaker.overrides as overrides       # warning: changes xypath and messytables

from databaker.jupybakeutils import HDim, HDimConst, ConversionSegment
from databaker.jupybakecsv import writetechnicalCSV, readtechnicalCSV
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

# try to mark up the data into a full pandas table (including tabname and cell position)
from databaker.jupybakeutils import Ldatetimeunitloose, Ldatetimeunitforce
import pandas as pd

def topandas(conversionsegment):
    dvals = [ ]
    for ob in conversionsegment.obslist:
        dval = conversionsegment.lookupobs(ob)
        dval["x"] = ob.x
        dval["y"] = ob.y
        dval["tabname"] = ob.table.name
        dval[OBS] = float(dval[OBS])
        if TIME in dval:
            dval[TIMEUNIT] = Ldatetimeunitloose(dval[TIME])
            sdatetime = Ldatetimeunitforce(dval[TIME], dval[TIMEUNIT]).replace(" ", "")
            dval[TIME] = pd.to_datetime(sdatetime)
        dvals.append(dval)
    df = pd.DataFrame.from_dict(dvals)
    #df.TIME = pd.DatetimeIndex(df.TIME)  # this doesn't work since the column is not an index
    return df

