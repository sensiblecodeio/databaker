Feature: Produce a pandas dataframe containing all data values in the format of a 
single observation per row.
    I want to be able to define all dimensions and their relation to the observations.
    Using this I then want to make a pandas dataframe which stores a single observation
    per row with the correct dimension values.

    Scenario: Complete the databaking process - produce a correct dataframe.
    Given we load an xls file named "bakingtestdataset.xls"

    And get "some_name" from the transform:
    """
    def transform_xlsx():
        tabs = [x for x in tabs if x.name.strip() == "Sheet1"]
        return tabs
    """

    And we define the dimensions and observations:

    And we create a list of dimensions (HDim objects) with their relation to observations.

    And we create a ConversionSegment object.

    And we convert the ConversionSegment object into a pandas dataframe.

    And we have the file "baking_test.csv" transformed back into a pandas dataframe.

    Then the two dataframes should be identical.