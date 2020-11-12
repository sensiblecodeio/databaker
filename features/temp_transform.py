from databaker.framework import *

def transform():
    tabs = loadxlstabs("/home/mike/GSS-Cogs/databaker/features/fixtures/bulletindataset2v2.xlsx")
    tabs = [x for x in tabs if x.name == "Table 1"]
    return tabs[0].name
