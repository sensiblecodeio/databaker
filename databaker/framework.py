import xlutils, xypath
import databaker
import os
import databaker.constants
from databaker.constants import *
import databaker.databakersolo as ds   # causes the xypath.loader to be overwritten
from databaker.jupybakeutils import HDim, savepreviewhtml, writetechnicalCSV, ConversionSegment

def loadxlstabs(inputfile):
    print("Loading %s which has size %d bytes" % (inputfile, os.path.getsize(inputfile)))
    tableset = xypath.loader.table_set(inputfile, extension='xls')
    tabs = list(xypath.loader.get_sheets(tableset, "*"))
    print("Table names: %s" % ", ".join([tab.name  for tab in tabs]))
    return tabs
    
