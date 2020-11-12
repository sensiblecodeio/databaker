Feature: Load xls files
  I want to load xls files into databaker

  Scenario: Load xlsx file 1
    Given we load an xls file named "bulletindataset2v2.xlsx"
    Then we confirm the names of the loaded tabs are equal to:
    """
    ["Cover Sheet", "Contents", "Table 1a", "Table 1b", "Table 2a", "Table 2b",
    "Table 3a", "Table 3b", "Table 3c", "Table 3d", "Table 4", "Table 4a", "Table 5a",
    "Table 5b", "Table 6a", "Table 7", "Table 8", "Table 9", "Table 10", "Table 11"]
    """

  Scenario: Select a tab just by tab name
    Given we load an xls file named "bulletindataset2v2.xlsx"
    And get "some_name" from the transform:
    """
    def transform():
        tabs = [x for x in tabs if x.name.strip() == "Table 1a"]
        return tabs[0].name
    """
    Then the output "some_name" should be equal to:
    """
    Table 1a
    """ 

    # Repeat for evertyihg we can think of, cell selections, conversionSegments, dataframes etc
    # the above pattern should work universally (witha  bit of tweaking)