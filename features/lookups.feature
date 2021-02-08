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