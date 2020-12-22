# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
from databaker.framework import *

tabs = loadxlstabs("/Users/charlesrendle/databaker-docker/db-test-suite-methods/databaker/features/fixtures/bakingtestdataset.xlsx")
tab = tabs[0]


year = tab.excel_ref("A4")

month = tab.excel_ref("A6:A25").is_not_blank()

day = tab.excel_ref("B6:B25")

top_dims = tab.excel_ref("C5:H5")

under_dim = tab.excel_ref("C4")

bottom_dims = tab.excel_ref("C26:H26")

under_dim = tab.excel_ref("C27")

county = tab.excel_ref("I6:I25")

country = tab.excel_ref("J6:J25").is_not_blank()

unit = tab.excel_ref("J4")

observations = tab.excel_ref("C6:H25")


dimensions = [
    HDim(year, "Year", CLOSEST, ABOVE),
    HDim(month, "Month", CLOSEST, ABOVE),
    HDim(day, "Day", DIRECTLY, LEFT),
    HDim(top_dims, "Top Dims", DIRECTLY, ABOVE),
    HDim(over_dim, "Over Dim", CLOSEST, ABOVE),
    HDim(bottom_dims, "Bottom Dims", DIRECTLY, BELOW),
    HDim(under_dim, "Under Dim", CLOSEST, BELOW),
    HDim(county, "County", DIRECTLY, RIGHT),
    HDim(country, "Country", CLOSEST, ABOVE),
    HDim(unit, "Unit", CLOSEST, BELOW)
]

tidy_sheet = ConversionSegment(tab, dimensions, observations)
savepreviewhtml(tidy_sheet)
# -


