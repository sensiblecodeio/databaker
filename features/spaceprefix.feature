Feature: Define dimension using bag.spaceprefix(count)
    I want to be able to define a dimension by identifying all items in a bag 
    which contain values prefixed by the same number of whitespace characters.

    Scenario: Define income type by number of whitespace characters prefixing each value
        Given we load an xls file named "balanceofpayments2020q1.xls"
        And select the sheet "Table A"
        And we define cell selections as
        | key             | value                                                |  
        | income_type     | tab.excel_ref("B").spaceprefix(5).is_not_blank()     |
        Then we confirm the cell selection contains "20" cells.
        And we confirm the cell selection is equal to:
        """
        {<B36 '     Trade in services'>, <B42 '     Other primary income'>, <B12 '     Trade in services'>, <B20 '     Total primary income'>, <B41 '     Investment income'>, <B40 '     Compensation of employees'>, <B46 '     General government'>, <B18 '     Other primary income'>, <B49 '     Total secondary income'>, <B44 '     Total primary income'>, <B47 '     Other sectors'>, <B14 '     Total trade'>, <B35 '     Trade in goods'>, <B25 '     Total secondary income'>, <B22 '     General government'>, <B11 '     Trade in goods'>, <B17 '     Investment income'>, <B16 '     Compensation of employees'>, <B38 '     Total trade'>, <B23 '     Other sectors'>}
        """    