import xlutils, xypath
import databaker
import os
import databaker.constants
from databaker.constants import *      # also brings in template
import databaker.databakersolo as ds   # causes the xypath.loader to be overwritten
from databaker.jupybakeutils import HDim, HDimConst, savepreviewhtml, writetechnicalCSV, ConversionSegment

def loadxlstabs(inputfile, sheetids="*"):
    print("Loading %s which has size %d bytes" % (inputfile, os.path.getsize(inputfile)))
    tableset = xypath.loader.table_set(inputfile, extension='xls')
    tabs = list(xypath.loader.get_sheets(tableset, sheetids))
    print("Table names: %s" % ", ".join([tab.name  for tab in tabs]))
    return tabs
    
import pandas as pd
def topandas(conversionsegment):
    return pd.DataFrame.from_dict(conversionsegment.lookupall())
