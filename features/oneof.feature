Feature: Define dimension using bag.one_of()
    I want to be able to define a dimension by identifying all items in a bag 
    which match specific set values.

    Scenario: Define last 5 years by whether the value in the year column matches a value in a list containing strings of the last 5 years.
        Given we load an xls file named "bulletindataset2v2.xls"
        And select the sheet "Table 2a"
        And we define cell selections as
        | key                     |value                                                                                |  
        | construction_type       | tab.excel_ref("A").one_of(["2015.0", "2016.0", "2017.0", "2018.0", "2019.0"])       |
        Then we confirm the cell selection contains "15" cells.
        And we confirm the cell selection is equal to:
        """
        {<A226 2018.0>, <A30 2016.0>, <A190 2015.0>, <A31 2017.0>, <A202 2016.0>, <A111 2016.0>, <A115 2017.0>, <A107 2015.0>, <A119 2018.0>, <A123 2019.0>, <A214 2017.0>, <A32 2018.0>, <A33 2019.0>, <A29 2015.0>, <A238 2019.0>}
        """    