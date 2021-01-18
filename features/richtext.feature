Feature: Define dimension using bag.is/is_not_richtext()
    I want to be able to define a dimension by identifying all the richtext or 
    non-richtext values from a bag of cells.

    Scenario: Define construction type by non-richtext values in row "6"
    Given we load an xls file named "bulletindataset2v2.xls"
    And get "some_name" from the transform:
    """
    def transform_xlsx():
        tabs = [x for x in tabs if x.name.strip() == "Table 1a"]
        return tabs
    """
    And we define a bag as every value in row "6".
    And we define construction type as each non-richtext and non-blank cell.
    Then we confirm construction type contains the correct number of values: "7"

Scenario: Define construction type as the correct cells.
    Given we load an xls file named "bulletindataset2v2.xls"
    And get "some_name" from the transform:
    """
    def transform_xlsx():
        tabs = [x for x in tabs if x.name.strip() == "Table 2a"]
        return tabs
    """
    And we define a bag as every value in row "6".
    And we define construction type as each non-richtext and non-blank cell.
    Then we confirm that construction type is equal to:
    """
    {<P6 'All Work'>, <C6 'New Housing'>, <K6 'Repair and Maintenance'>, <J6 'All New Work'>, <E6 'Total Housing'>, <O6 'All Repair and Maintenance'>, <F6 'Other New Work'>}
    """

Scenario: Define construction type by richtext values in row "6"
    Given we load an xls file named "bulletindataset2v2.xls"
    And get "some_name" from the transform:
    """
    def transform_xlsx():
        tabs = [x for x in tabs if x.name.strip() == "Table 2a"]
        return tabs
    """
    And we define a bag as every value in row "6".
    And we define construction type as each richtext and non-blank cell.
    Then we confirm construction type contains the correct number of values: "0"
    And we confirm construction type is equal to:
    """
    set()
    """