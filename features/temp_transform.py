from databaker.framework import *

def transform_xlsx():
    tabs = loadxlstabs("/Users/charlesrendle/databaker-docker/db-test-suite-methods/databaker/features/fixtures/2018internationaltradeinservicesdatatables.xlsx")
    tabs = [x for x in tabs if x.name.strip() == "1. NUTS1, industry"]
    #return tabs[0].name
    return tabs
