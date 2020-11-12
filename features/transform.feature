Feature: Databaker Tidy Data Transformation
  I want databaker to create tidy data from spreadsheets
  # NOTE - the above (and this whole file) is waaaaaaaay too broad but its a start, break it out later

  Scenario: Select a tab just by tab name
    Given we load an xls file named "bulletindataset2v2.xlsx"
    And get "some_names" from the transform:
    """
    def transform():
        tabs = [x for x in tabs if x.name == "Table 1"]
        return tabs[0].name
    """
    Then the output "some_names" should be equal to:
    """
    "Table 1"
    """ 
