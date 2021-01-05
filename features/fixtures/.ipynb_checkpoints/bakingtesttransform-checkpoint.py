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


year = tab.excel_ref("A13")

month = tab.excel_ref("B6:B25").is_not_blank()

day = tab.excel_ref("C6:C25")

top_dims = tab.excel_ref("D5:I5")

over_dim = tab.excel_ref("D4")

bottom_dims = tab.excel_ref("D26:I26")

under_dim = tab.excel_ref("D27")

county = tab.excel_ref("J6:J25")

country = tab.excel_ref("K6:K25").is_not_blank()

unit = tab.excel_ref("M13")

observations = tab.excel_ref("D6:I25")


dimensions = [
    HDim(year, "Year", CLOSEST, LEFT),
    HDim(month, "Month", CLOSEST, ABOVE),
    HDim(day, "Day", DIRECTLY, LEFT),
    HDim(top_dims, "Top Dims", DIRECTLY, ABOVE),
    HDim(over_dim, "Over Dim", CLOSEST, ABOVE),
    HDim(bottom_dims, "Bottom Dims", DIRECTLY, BELOW),
    HDim(under_dim, "Under Dim", CLOSEST, BELOW),
    HDim(county, "County", DIRECTLY, RIGHT),
    HDim(country, "Country", CLOSEST, ABOVE),
    HDim(unit, "Unit", CLOSEST, RIGHT)
]

tidy_sheet = ConversionSegment(tab, dimensions, observations)
#savepreviewhtml(tidy_sheet)

df = tidy_sheet.topandas()

df.to_csv("baking_test.csv", index = False)


# -




