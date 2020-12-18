Feature: Produce a pandas dataframe containing all data values in the format of a 
single observation per row.
    I want to be able to define all dimensions and their relation to the observations.
    Using this I then want to make a pandas dataframe which stores a single observation
    per row with the correct dimension values.

    Scenario: Complete the databaking process - produce a correct dataframe.
    Given we load an xls file named "2018internationaltradeinservicesdatatables.xlsx"

    And get "some_name" from the transform:
    """
    def transform_xlsx():
        tabs = [x for x in tabs if x.name.strip() == "1. NUTS1, industry"]
        return tabs
    """

    And we define the dimensions and observations:
    """
    def dims_and_obs(transform_tab):
        tab = transform_tab

        year = "2018"
        nuts1_area = tab.excel_ref("A4:A42").is_not_blank()
        industry = tab.excel_ref("C3").expand(RIGHT).is_not_blank()
        measure_type = tab.excel_ref("B4").expand(DOWN).is_not_blank()
        unit = "£ millions"

        observations = tab.excel_ref("C4").expand(RIGHT).expand(DOWN).is_not_blank()

        returns = [year, nuts1_area, industry, measure_type, unit, observations]

        return returns
    """

    Then we create a list of dimensions (HDim objects) with their relation to observations.

    And we create a ConversionSegment object.

    And we convert the ConversionSegment object into a pandas dataframe.

    And we do this by defining timeunitmessage which calls the process function.

    And in turn this will define a list (processedrows) by looping through obslist and calling the lookupobs function.

    And this will call the svalue function - for each ob still.

    And also loop for each HDim object in the dimensions list, we define hcell and val by calling the cellvalobs function - still for each ob.

    And we can define val if ob is in cellvalueoverride to return hcell as None and val as cellvalueoverride[ob]

    And (or) if not, we can define hcell if hbagset is not None by calling celllookup(ob) else hcell is None - still for each ob.

    And celllookup returns best_cell using functions of smaller scope: betweencells(), same_row_col() and mult()

    And we finally return hcell and val but val is defined by calling the headcellval function using hcell

    And headcellval can return val as cellvalueoverride[hcell] if hcell is not None and hcell is in cellvalueoverride

    And (or) if hcell is just not None val is assigned as using the svalue function still for each ob.

    And if hcell is None then val is assigned as None too.

    And val can be found and returned if its in cellvalueoverride, it gets assigned as cellvalueoverride[val]

    And (or) val can be found and returned if its type is in cellvalueoverride. val gets assigned as cellvalueoverride[type(val)](val)

    And back in the lookupobs function, a dict can be filled with HDim labels and vals.

    And more processing is done to this dict before returning it to processedrows list - end of looping for each ob.

    And penultimately some stuff is done regarding timeunitmessage including calls to the functions: guesstimeunit() and fixfromtimeunit()

    And lastly the dataframe is declared and defined from the dictionaries in the processedrows list.







