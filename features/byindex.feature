Feature: Define a dimension by accessing the element at index n in a bag of cells.
    If I have a bag of cells but want to define a dimension as a single cells
    within the bag, I want to be able to access that value by its index in the bag.

    Scenario: Define by index unit from its index in the row 5 bag.
        Given we load an xls file named "bulletindataset2v2.xls"
        And select the sheet "Table 2a"
        And we define cell selections as
        | key             |value                                         |  
        | unit            | tab.excel_ref("A5"+":Z5").by_index(16)       |
        Then we confirm the cell selection is the correct type.
        """
        <class 'xypath.xypath.Bag'>
        """
        And we confirm the cell selection is equal to:
        """
        {<P5 '(£Million)'>}
        """   