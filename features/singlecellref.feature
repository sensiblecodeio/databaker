Feature: Define a dimension as a value from a single cell reference.
  I want to be able to define a dimension as a value from a single cell reference which stays constant for all observations.

  Scenario: Define unit from single cell reference.
    Given we load an xls file named "bulletindataset2v2.xls"
    And select the sheet "Table 2a"
    And we define cell selections as
      | key             | value                                   |  
      | unit            | tab.excel_ref("P5")                     |
    Then we confirm the cell selection is the correct type.
    """
    <class 'xypath.xypath.Bag'>
    """
    Then we confirm the cell selection is equal to:
    """
    {<P5 '(£Million)'>}
    """