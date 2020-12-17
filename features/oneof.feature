Feature: Define dimension using bag.one_of()
    I want to be able to define a dimension by identifying all items in a bag 
    which match specific set values.

    Scenario: Define last 5 years by whether the value in the year column matches a value in a list containing strings of the last 5 years.
    Given we load an xls file named "bulletindataset2v2.xlsx"
    And get "some_name" from the transform:
    """
    def transform_xlsx():
        tabs = [x for x in tabs if x.name.strip() == "Table 2a"]
        return tabs
    """
    And we define all years as every value in from column "A" down
    And we define the last 5 years as every value in all years and in the list: "2015.0,2016.0,2017.0,2018.0,2019.0"
    Then we confirm last 5 years contains the correct number of values: "15"

Scenario: Define the last 5 years as correct the cells.
    Given we load an xls file named "bulletindataset2v2.xlsx"
    And get "some_name" from the transform:
    """
    def transform_xlsx():
        tabs = [x for x in tabs if x.name.strip() == "Table 2a"]
        return tabs
    """
    And we define all years as every value in from column "A" down
    And we define the last 5 years as every value in all years and in the list: "2015.0,2016.0,2017.0,2018.0,2019.0"
    Then we confirm that the last 5 years is equal to:
    """
    {<A226 2018.0>, <A30 2016.0>, <A190 2015.0>, <A31 2017.0>, <A202 2016.0>, <A111 2016.0>, <A115 2017.0>, <A107 2015.0>, <A119 2018.0>, <A123 2019.0>, <A214 2017.0>, <A32 2018.0>, <A33 2019.0>, <A29 2015.0>, <A238 2019.0>}
    """    