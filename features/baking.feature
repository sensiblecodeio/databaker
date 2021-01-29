Feature: Produce a pandas dataframe containing all data values in the format of a 
single observation per row.
    I want to be able to define all dimensions and their relation to the observations.
    Using this I then want to make a pandas dataframe which stores a single observation
    per row with the correct dimension values.

    Scenario: Complete the databaking process - produce a correct dataframe.
    Given we load an xls file named "bakingtestdataset.xls"

    And select the sheet "Sheet1"

    And we define cell selections as
      | key             | value                                   |  
      | year            | tab.excel_ref("A13")                    |
      | month           | tab.excel_ref("B6:B25").is_not_blank()  |
      | day             | tab.excel_ref("C6:C25")                 |
      | top_dims        | tab.excel_ref("D5:I5")                  |
      | over_dim        | tab.excel_ref("D4")                     |
      | bottom_dims     | tab.excel_ref("D26:I26")                |
      | under_dim       | tab.excel_ref("D27")                    |
      | county          | tab.excel_ref("J6:J25")                 |
      | country         | tab.excel_ref("K6:K25").is_not_blank()  |
      | unit            | tab.excel_ref("M13")                    |
      | observations    | tab.excel_ref("D6:I25")                 |

    And we define the dimensions as
    """
    HDim(year, "Year", CLOSEST, LEFT)
    HDim(month, "Month", CLOSEST, ABOVE)
    HDim(day, "Day", DIRECTLY, LEFT)
    HDim(top_dims, "Top Dims", DIRECTLY, ABOVE)
    HDim(over_dim, "Over Dim", CLOSEST, ABOVE)
    HDim(bottom_dims, "Bottom Dims", DIRECTLY, BELOW)
    HDim(under_dim, "Under Dim", CLOSEST, BELOW)
    HDim(county, "County", DIRECTLY, RIGHT)
    HDim(country, "Country", CLOSEST, ABOVE)
    HDim(unit, "Unit", CLOSEST, RIGHT)
    """

    And we create a ConversionSegment object.

    And we convert the ConversionSegment object into a pandas dataframe.

    And we have the file "baking_test.csv" transformed back into a pandas dataframe.

    Then the two dataframes should be identical.