Feature: Define a dimension by accessing the element at index n in a bag of cells.
    If I have a bag of cells but want to define a dimension as a single cells
    within the bag, I want to be able to access that value by its index in the bag.

    Scenario: Define by index unit from its index in the row 5 bag.
    Given we load an xls file named "bulletindataset2v2.xlsx"
    And get "some_name" from the transform:
    """
    def transform_xlsx():
        tabs = [x for x in tabs if x.name.strip() == "Table 2a"]
        return tabs
    """
    And we define a bag as every value in row "5".
    And we define by index unit as the value at index "16" in this bag.
    Then we confirm by index unit is defined as type cell, equal to:
    """
    <class 'xypath.xypath.Bag'>
    """

Scenario: Define by index unit as correct cell.
    Given we load an xls file named "bulletindataset2v2.xlsx"
    And get "some_name" from the transform:
    """
    def transform_xlsx():
        tabs = [x for x in tabs if x.name.strip() == "Table 2a"]
        return tabs
    """
    And we define a bag as every value in row "5".
    And we define by index unit as the value at index "16" in this bag.
    Then we confirm that by index unit is equal to:
    """
    {<P5 '(£Million)'>}
    """    