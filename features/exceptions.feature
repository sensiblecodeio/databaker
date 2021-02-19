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