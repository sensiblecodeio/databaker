Feature: Define dimension using bag.spaceprefix(count)
    I want to be able to define a dimension by identifying all items in a bag 
    which contain values prefixed by the same number of whitespace characters.

    Scenario: Define income type by number of whitespace characters prefixing each value
    Given we load an xls file named "balanceofpayments2020q1.xls"
    And get "some_name" from the transform:
    """
    def transform_xlsx():
        tabs = [x for x in tabs if x.name.strip() == "Table A"]
        return tabs
    """
    And we define a bag as every value in column "B".
    And we define income type as each cell which begins with "5" whitespace characters.
    Then we confirm income type contains the correct number of values: "20"

Scenario: Define by index unit as correct cell.
    Given we load an xls file named "balanceofpayments2020q1.xls"
    And get "some_name" from the transform:
    """
    def transform_xlsx():
        tabs = [x for x in tabs if x.name.strip() == "Table A"]
        return tabs
    """
    And we define a bag as every value in column "B".
    And we define income type as each cell which begins with "5" whitespace characters.
    Then we confirm that income type is equal to:
    """
    {<B36 '     Trade in services'>, <B42 '     Other primary income'>, <B12 '     Trade in services'>, <B20 '     Total primary income'>, <B41 '     Investment income'>, <B40 '     Compensation of employees'>, <B46 '     General government'>, <B18 '     Other primary income'>, <B49 '     Total secondary income'>, <B44 '     Total primary income'>, <B47 '     Other sectors'>, <B14 '     Total trade'>, <B35 '     Trade in goods'>, <B25 '     Total secondary income'>, <B22 '     General government'>, <B11 '     Trade in goods'>, <B17 '     Investment income'>, <B16 '     Compensation of employees'>, <B38 '     Total trade'>, <B23 '     Other sectors'>}
    """    