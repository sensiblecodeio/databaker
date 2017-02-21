import os, warnings
import xypath
import xypath.loader
import databaker.constants
from databaker.constants import *      # also brings in template
import databaker.overrides as overrides       # warning: injects additional class functions into xypath and messytables

# core classes and functionality
from databaker.jupybakeutils import HDim, HDimConst, ConversionSegment, Ldatetimeunitloose, Ldatetimeunitforce, pdguessforceTIMEUNIT
from databaker.jupybakecsv import writetechnicalCSV, readtechnicalCSV
from databaker.jupybakehtml import savepreviewhtml

# this lot should be deprecated
from databaker.jupybakecsv import headersfromwdasegment, extraheaderscheck, checktheconstantdimensions, checksegmentobsvalues
from databaker.jupybakecsv import wdamsgstrings, CompareConversionSegments

def loadxlstabs(inputfile, sheetids="*", verbose=True):
    if verbose:
        print("Loading %s which has size %d bytes" % (inputfile, os.path.getsize(inputfile)))
    tableset = xypath.loader.table_set(inputfile, extension='xls')
    tabs = list(xypath.loader.get_sheets(tableset, sheetids))
    tabnames = [ tab.name  for tab in tabs ]
    if verbose:
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

DATABAKER_INPUT_FILE = None


def getinputfilename():
    """ Return DATABAKER_INPUT_FILE from os.environ or this module.

    This is so that DATABAKER_INPUT_FILE could be specified in a notebook and
    then overridden by an environment variable if not.

    Use of environment variables is because nbconvert doesn't allow you to
    easily pass arguments to the notebook.

    Use in notebook is along the lines of:

    DATABAKER_INPUT_FILE = 'myfile.xls'
    f = getinputfilename()

    This way, we can set the filename in the notebook, or at the commmand line
    with environment variables.
    """
    try:
        return os.environ['DATABAKER_INPUT_FILE']
    except KeyError as e:
        return DATABAKER_INPUT_FILE
