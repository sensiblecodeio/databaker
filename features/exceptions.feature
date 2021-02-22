Feature: User friendly exceptions
  I want databaker to create user friendly exceptions where a problem is encountered.

Scenario: A DIRECTLY lookup to where a cell does not exist
    Given we load an xls file named "bakingtestdataset.xls"
    And select the sheet "Sheet1"
    And we define cell selections as
        | key             | value                                   |
        | observations    | tab.excel_ref("D6:D7")                  | 
        | county          | tab.excel_ref("J6").is_not_blank()      |
    And we define the dimensions as
        """
        HDim(county, "County", DIRECTLY, RIGHT)
        """
    And we create a ConversionSegment object.
    And we attempt to extract the dimensions, capturing the first exception as
        """
        DIRECT lookup for cell <D7 7.0> failed. The dimension "County" has no cells directly RIGHT of <D7 7.0> on the horizontal axis.
        """

Scenario: A CLOSEST lookup where there are no dimension cells in the stated direction
    Given we load an xls file named "bakingtestdataset.xls"
    And select the sheet "Sheet1"
    And we define cell selections as
        | key             | value                           |
        | observations    | tab.excel_ref("D6:D26")         | 
        | month           | tab.excel_ref("B27")            |
    And we define the dimensions as
        """
        HDim(month, "Month", CLOSEST, ABOVE)
        """
    And we create a ConversionSegment object.
    And we attempt to extract the dimensions, capturing the first exception as
        """
        Lookup for cell "<D6 1.0>" is impossible. No selected values for dimension "Month" exist in the ABOVE direction from this cell
        """

Scenario: Create a CLOSEST lookup with an empty bag of cells
    Given we load an xls file named "bakingtestdataset.xls"
    And select the sheet "Sheet1"
    And we define cell selections as
        | key             | value                                              |
        | observations    | tab.excel_ref("D6:D26")                            |
        | month           | tab.excel_ref("D1").is_not_blank().is_blank()      |
    Then the dimension 'HDim(month, "Month", CLOSEST, ABOVE)' will fail with the exception
        """
        Aborting. The dimension Month is defined as CLOSEST ABOVE but an empty selection of cells has been passed in as the first argument.
        """

Scenario: Create a DIRECTLY lookup with an empty bag of cells
    Given we load an xls file named "bakingtestdataset.xls"
    And select the sheet "Sheet1"
    And we define cell selections as
        | key             | value                                             |
        | observations    | tab.excel_ref("D6:D7")                            | 
        | county          | tab.excel_ref("J6").is_not_blank().is_blank()     |
    Then the dimension 'HDim(county, "County", DIRECTLY, RIGHT)' will fail with the exception
        """
        Aborting. The dimension County is defined as DIRECTLY RIGHT but an empty selection of cells has been passed in as the first argument.
        """

Scenario: Create a CLOSEST lookup with two equally close cells
    Given we load an xls file named "bakingtestdataset.xls"
    And select the sheet "Sheet1"
    And we define cell selections as
        | key             | value                                 |
        | random          | tab.excel_ref("A1").expand(RIGHT)     | 
        | observations    | tab.excel_ref("J6").is_not_blank()    |
    Then the dimension 'HDim(random, "Random Selection", CLOSEST, ABOVE)' will fail with the exception
        """
        Aborting. You have defined two or more equally valid CLOSEST ABOVE relationships. Trying to add 0:{<B1 ''>} but we already have: {"0": "{<A1 'Test Title'>}"}
        """