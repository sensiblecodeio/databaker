Feature: Create lookup engines
  I want databaker to store accurate lookup information for a given dimension, given the direction and type of lookup.

    Scenario: Create a DIRECTLY dimensionsional lookup
    Given we load an xls file named "bakingtestdataset.xls"
    And select the sheet "Sheet1"
    And we define cell selections as
        | key             | value                                   |  
        | day             | tab.excel_ref("C9:C12")                 |
        | county          | tab.excel_ref("J15:J17")                |
        | top_dims        | tab.excel_ref("G5:I5")                  |
        | bottom_dims     | tab.excel_ref("D26:E26")                |
    And we define the dimensions as
        """
        HDim(day, "Day", DIRECTLY, LEFT)
        HDim(county, "County", DIRECTLY, RIGHT)
        HDim(top_dims, "Top Dims", DIRECTLY, ABOVE)
        HDim(bottom_dims, "Bottom Dims", DIRECTLY, BELOW)
        """
    Then the "DIRECTLY" dimension "Day" has stored lookup information equal to
        """
        {"8": {"get": ["{<C9 22.0>}"]}, "9": {"get": ["{<C10 29.0>}"]}, "1": {"0": {"get": ["{<C11 1.0>}"]}, "1": {"get": ["{<C12 8.0>}"]}}}
        """
    Then the "DIRECTLY" dimension "County" has stored lookup information equal to
        """
        {"1": {"4": {"get": ["{<J15 'NI County 5'>}"]}, "5": {"get": ["{<J16 'Sco County 1'>}"]}, "6": {"get": ["{<J17 'Sco County 2'>}"]}}}
        """
    Then the "DIRECTLY" dimension "Top Dims" has stored lookup information equal to
        """
        {"6": {"get": ["{<G5 'Dim 4'>}"]}, "7": {"get": ["{<H5 'Dim 5'>}"]}, "8": {"get": ["{<I5 'Dim 6'>}"]}}
        """
    Then the "DIRECTLY" dimension "Bottom Dims" has stored lookup information equal to
        """
        {"3": {"get": ["{<D26 'Dim 7'>}"]}, "4": {"get": ["{<E26 'Dim 8'>}"]}}
        """ 

    Scenario: Create a CLOSEST dimensionsional lookup
    Given we load an xls file named "bakingtestdataset.xls"
    And select the sheet "Sheet1"
    And we define cell selections as
        | key             | value                                   |  
        | year            | tab.excel_ref("A13")                    |
        | unit            | tab.excel_ref("M13")                    |
        | month           | tab.excel_ref("B6:B15").is_not_blank()  |
        | under_dim       | tab.excel_ref("D27")                    |
    And we define the dimensions as
        """
        HDim(year, "Year", CLOSEST, LEFT)
        HDim(unit, "Unit", CLOSEST, RIGHT)
        HDim(month, "Month", CLOSEST, ABOVE)
        HDim(under_dim, "Under Dim", CLOSEST, BELOW)
        """
    Then the "CLOSEST" dimension "Year" has stored lookup information equal to
        """
        {"0": {"lowest_offset": 0, "highest_offset": 99999999999, "dimension_cell": "{<A13 'Year'>}"}}
        """
    Then the "CLOSEST" dimension "Unit" has stored lookup information equal to
        """
        {"0": {"lowest_offset": 0, "highest_offset": 12, "dimension_cell": "{<M13 'Unit'>}"}}
        """
    Then the "CLOSEST" dimension "Month" has stored lookup information equal to
        """
        {"0": {"lowest_offset": 5, "highest_offset": 9, "dimension_cell": "{<B6 'Jan'>}"}, "1": {"lowest_offset": 10, "highest_offset": 99999999999, "dimension_cell": "{<B11 'Apr'>}"}}
        """
    Then the "CLOSEST" dimension "Under Dim" has stored lookup information equal to
        """
        {"0": {"lowest_offset": 0, "highest_offset": 26, "dimension_cell": "{<D27 'Another Dim 2'>}"}}
        """

Scenario: Create a CONSTANT dimension
    Given we load an xls file named "bakingtestdataset.xls"
        And select the sheet "Sheet1"
        And we define cell selections as
        | key             | value                                   | 
        | observations    | tab.excel_ref("D6:I25")                 |
    And we define the dimensions as
        """
        HDimConst("Constant1", "foo")
        HDimConst("Constant2", "bar")
        """
    Then all lookups to dimension "Constant1" should return the value "foo"
    And all lookups to dimension "Constant2" should return the value "bar"
    
Scenario: Apply cellvalueoverrides with a DIRECTLY lookup
    Given we load an xls file named "bakingtestdataset.xls"
    And select the sheet "Sheet1"
    And we define cell selections as
        | key             | value                                   |
        | observations    | tab.excel_ref("D6:I10")                 | 
        | county          | tab.excel_ref("J6:J10").is_not_blank()  |
    And we define the dimensions as
        """
        HDim(county, "County", DIRECTLY, RIGHT, cellvalueoverride={"Eng County 2": "Mongolia County 1"})
        """
    And we create a ConversionSegment object.
    And we convert the ConversionSegment object into a pandas dataframe.
    Then the unique contents of the "County" column should be equal to
        """
        ['Eng County 1', 'Eng County 3', 'Eng County 4', 'Eng County 5', 'Mongolia County 1']
        """

Scenario: Apply cellvalueoverrides with a CLOSEST lookup
    Given we load an xls file named "bakingtestdataset.xls"
    And select the sheet "Sheet1"
    And we define cell selections as
        | key             | value                                   |
        | observations    | tab.excel_ref("D6:D26")                 | 
        | month           | tab.excel_ref("B6:B25").is_not_blank()  |
    And we define the dimensions as
        """
        HDim(month, "Month", CLOSEST, ABOVE, cellvalueoverride={"Oct": "Of Sundays"})
        """
    And we create a ConversionSegment object.
    And we convert the ConversionSegment object into a pandas dataframe.
    Then the unique contents of the "Month" column should be equal to
        """
        ['Apr', 'Jan', 'Jul', 'Of Sundays']
        """