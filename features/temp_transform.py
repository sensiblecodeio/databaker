from databaker.framework import *

def transform_xlsx():
    tabs = loadxlstabs("/Users/charlesrendle/databaker-docker/db-test-suite-methods/databaker/features/fixtures/balanceofpayments2020q1.xls")
    tabs = [x for x in tabs if x.name.strip() == "Table A"]
    return tabs
