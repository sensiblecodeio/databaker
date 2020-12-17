Feature: Define a dimension as a value from a single cell reference.
  I want to be able to define a dimension as a value from a single cell reference which stays constant for all observations.

  Scenario: Define unit from single cell reference.
    Given we load an xls file named "bulletindataset2v2.xlsx"
    And get "some_name" from the transform:
    """
    def transform_xlsx():
        tabs = [x for x in tabs if x.name.strip() == "Table 2a"]
        return tabs
    """
    And we define unit as the value in cell "P5"
    Then we confirm unit is defined as type cell, equal to:
    """
    <class 'xypath.xypath.Bag'>
    """

Scenario: Define unit as correct cell.
    Given we load an xls file named "bulletindataset2v2.xlsx"
    And get "some_name" from the transform:
    """
    def transform_xlsx():
        tabs = [x for x in tabs if x.name.strip() == "Table 2a"]
        return tabs
    """
    And we define unit as the value in cell "P5" 
    Then we confirm that unit is equal to:
    """
    {<P5 '(£Million)'>}
    """    
