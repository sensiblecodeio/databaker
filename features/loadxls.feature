Feature: Load xls files
  I want to load xls files into databaker

  Scenario: Load xlsx file 1
    Given we load an xls file named "2018internationaltradeinservicesdatatables.xls"
    Then we confirm the names of the loaded tabs are equal to:
    """
    ["Notes", "Index", "1. NUTS1, industry", "2. NUTS1, industry, destination",
    "3. NUTS2, industry", "4. NUTS2, industry, destination", "5. NUTS3, destination",
    "6. City Region, industry", "7. City Region, industry, dest.", "8. Travel", "9. Tidy format"]
    """

  Scenario: Select a tab just by tab name
    Given we load an xls file named "2018internationaltradeinservicesdatatables.xls"
    And get "some_name" from the transform:
    """
    def transform_xls():
        tabs = [x for x in tabs if x.name.strip() == "1. NUTS1, industry"]
        #return tabs[0].name
        return tabs
    """
    Then the output "some_name" should be equal to:
    """
    1. NUTS1, industry
    """ 

    # Repeat for evertyihg we can think of, cell selections, conversionSegments, dataframes etc
    # the above pattern should work universally (with a bit of tweaking)