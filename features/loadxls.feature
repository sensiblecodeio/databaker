Feature: Load xls files
  I want to load xls files into databaker

  Scenario Outline: Load xls file 1
  Given we load an xls file named "bulletindataset2v2.xls"
  Then we confirm the names of the loaded tabs are equal to:
    """
    ["Cover Sheet", "Contents", "Table 1a", "Table 1b", "Table 2a", "Table 2b",
    "Table 3a", "Table 3b", "Table 3c", "Table 3d", "Table 4", "Table 4a", "Table 5a",
    "Table 5b", "Table 6a", "Table 7", "Table 8", "Table 9", "Table 10", "Table 11"]
    """

