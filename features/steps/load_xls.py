import json
import os

from behave import *
from pathlib import Path
from databaker.framework import loadxlstabs
from databaker.jupybakeutils import *
from databaker.structure_csv_default import *
from databaker.constants import *
from databaker.overrides import *

def get_fixture(file_name):
    """Helper to get specific files out of the fixtures dir"""
    feature_path = Path(os.path.dirname(os.path.abspath(__file__))).parent
    fixture_file_path = Path(feature_path, "fixtures", file_name)
    return fixture_file_path

def cell_builder(cell_list):
    cell_set = set()
    for char in range(0, len(str(cell_list))):
        cell = ""
        if str(cell_list)[char] == "<":
            cell = cell + str(cell_list)[char]
            current = char
            next_char = str(cell_list)[current + 1]
            while next_char != ">":
                cell = cell + next_char
                current += 1
                next_char = str(cell_list)[current + 1]
            cell = cell + ">"
            cell_set.add(cell)
    return(cell_set)

@given('we load an xls file named "{xls_file}"')
def step_impl(context, xls_file):
    path_to_xls = get_fixture(xls_file)
    context.last_xls_loaded = path_to_xls
    context.tabs = loadxlstabs(path_to_xls)

@given('select the sheet "{sheet_wanted}"')
def step_impl(context, sheet_wanted):
    context.tab_selected = [x for x in context.tabs if x.name == sheet_wanted][0]

@then(u'the output "{thing_wanted}" should be equal to')
def step_impl(context, thing_wanted):

    expected_output = context.text
    #actual_output = context.databaker_outputs[thing_wanted][0].name
    actual_output = context.tabs[2].name
    assert expected_output == actual_output, "{} \n\ndoes not match the expected output \n\n {}\n".format(str(actual_output), str(expected_output))

@then(u'we confirm the names of the loaded tabs are equal to')
def step_impl(context):
    tabs_wanted = json.loads(context.text)
    for tab in tabs_wanted:
        assert tab in [x.name for x in context.tabs]
    assert len(context.tabs) == len(tabs_wanted)

#From the tab, define all dimensions and observations in the usual transform manner.
@given(u'we define cell selections as')
def step_impl(context):
    tab = context.tab_selected
    context.selections = {}

    for row in context.table:
        context.selections[row[0]] = eval(row[1])

@then('the selection for "{variable_name}" should be equal to')
def step_impl(context, variable_name):
    selection_expected = context.text
    selection_got = [x.value for x in context.selections[variable_name]]
    selection_got.sort()
    assert selection_expected.strip() == str(selection_got).strip(), \
        f'Unexpected selection. Expected \n{selection_expected}\n\nGot:\n{selection_got}'


#Now we build the dimensions list.
@given(u'we define the dimensions as')
def step_impl(context):
    dimension_statments = context.text.split("\n")
    context.dimensions = []
    for ds in dimension_statments:

        if "HDimConst" not in ds:
            # Modify the statment to get the selection from context, so
            # HDim(year, "Year", CLOSEST, LEFT)
            # becomes
            # HDim(context.selections["year"], "Year", CLOSEST, LEFT)
            ds_tokens = ds.split(",")
            ds0 = ds_tokens[0]
            ds0 = ds0.split("(")[0]+f'(context.selections[\'{ds0.split("(")[1]}\'],'
            ds = ds0 + ",".join(ds_tokens[1:])
        context.dimensions.append(eval(ds))

#We use the list to instanciate a conversion segment object.
@given(u'we create a ConversionSegment object.')
def step_impl(context):
    context.tidy_sheet = ConversionSegment(context.tab_selected, context.dimensions, context.selections["observations"])


#The conversion segment object is converted into a dataframe using it's function .topandas()
#This is the function which takes ages because it now loops for all dims and obs.
@given(u'we convert the ConversionSegment object into a pandas dataframe.')
def step_impl(context):
    context.df = context.tidy_sheet.topandas()


#Bring the csv fixture in as the expected output and convert that into a dataframe making sure the data type of the 'Day' dimension is set to 'object'.
@given(u'we have the file "{expected_csv}" transformed back into a pandas dataframe.')
def step_impl(context, expected_csv):
    #raise NotImplementedError(u'STEP: Given we have the expected CSV file transformed back into a pandas dataframe.')
    path_to_csv = get_fixture(expected_csv)
    context.expected_df = pandas.read_csv(path_to_csv, dtype = {"Day": object})


#Use the x.equals(y) function to test both dataframes are identical.
@then(u'the two dataframes should be identical.')
def step_impl(context):
    # Note - forcing to str as under the hood precision differences n float types make this unreliable otherwise
    df1 = context.df.astype(str)
    df2 = context.expected_df.astype(str)
    assert df1.equals(df2), "\n{} \n\ntransform dataframe is not identcial to expected CSV dataframe \n\n {}\n".format((df1), (df2))


@then(u'we confirm the cell selection is the correct type.')
def step_impl(context):
    expected = context.text
    types = [type(k) for k in context.selections.values()]
    actual = str(types[0])

    assert expected == actual, "{} \n\ndoes not match the expected type \n\n {}\n".format(str(actual), str(expected))


@then(u'we confirm the cell selection is equal to')
def step_impl(context):
    expected = set()
    actual = set()

    #Build a set of cells from the expected output.
    expected = cell_builder(context.text)

    #Build a set of actual values found via databaker.
    actual = cell_builder(str([str(v) for v in context.selections.values()][0]))
 
    #If set difference produces an empty set, then both sets contain the same items regardless of order.
    assert len(expected.difference(actual)) == 0, "{} \n\ndoes not match the expected output \n\n {}\n".format(str(actual), str(expected))


@then(u'we confirm the cell selection contains "{num_of_cells}" cells.')
def step_impl(context, num_of_cells):
    assert len(cell_builder(str([str(v) for v in context.selections.values()][0]))) == int(num_of_cells), "{} \n\nbag contains unexpected number of cells \n\n {}\n".format(len(cell_builder(str([str(v) for v in context.selections.values()][0]))), str(num_of_cells))


@then(u'we confirm the cell selection contains no blank cells.')
def step_impl(context):
    assert "''" not in str(cell_builder(str([str(v) for v in context.selections.values()][0]))), "{} \n\ncontains blank cells \n\n".format(str(cell_builder(str([str(v) for v in context.selections.values()][0]))))


@then(u'we confirm the cell selection contains no value storing cells.')
def step_impl(context):
    assert "." not in str(cell_builder(str([str(v) for v in context.selections.values()][0]))), "{} \n\ncontains blank cells \n\n".format(str(cell_builder(str([str(v) for v in context.selections.values()][0]))))

@then('the "{lookup_type}" dimension "{dimension_label}" has stored lookup information equal to')
def step_impl(context, lookup_type, dimension_label):

    # Get the dimension in question
    hdims = [x for x in context.dimensions if x.label == dimension_label]
    assert len(hdims) == 1, f'Aborting. Must have exactly one dimension with the label {dimension_label}. Got {len(hdims)}.'
    hdim = hdims[0]

    # Get the stored information based on the type of lookup
    if lookup_type == "DIRECTLY":
        info_got = hdim.engine.tiered_dict
    elif lookup_type == "CLOSEST":
        info_got = hdim.engine.ranges
    else:
        raise ValueError(f'This test does not recognise a lookup type of type: {lookup_type}')

    # For the classes to comparable strings for both
    info_expected = json.dumps(json.loads(context.text), default=lambda x: str(x))
    info_got = json.dumps(info_got, default=lambda x: str(x))

    msg = f"""Lookup information does not match what was expected.

Got:
{info_got}

Expected:
{info_expected}
    
    """
    assert info_expected == info_got, msg

@then(u'all lookups to dimension "{dimension_label}" should return the value "{expected_value}"')
def step_impl(context, dimension_label, expected_value):

   # Get the dimension in question
    hdims = [x for x in context.dimensions if x.label == dimension_label]
    assert len(hdims) == 1, f'Aborting. Must have exactly one dimension with the label {dimension_label}. Got {len(hdims)}.'
    hdim = hdims[0]

    obs = context.selections["observations"]
    for ob in obs:
        cell, cell_value = hdim.engine.lookup(ob)
        assert cell is None, f'A constant lookup should be returning type:None for the cell looked up, not {type(cell)}'
        assert cell_value == expected_value, f'Expecting {expected_value}, got {cell_value}'


@then(u'the dimension \'{dim_constructor}\' will fail with the exception')
def step_impl(context, dim_constructor):

    if "HDimConst" in dim_constructor:
        raise NotImplementedError(u'The step is not currently designed to accomodate a HDimConst dimension')

    dc_tokens = dim_constructor.split(",")
    dc0 = dc_tokens[0]
    dc0 = dc0.split("(")[0]+f'(context.selections[\'{dc0.split("(")[1]}\'],'
    ds = dc0 + ",".join(dc_tokens[1:])

    try:
        dimension = eval(ds)
    except Exception as dim_err:
        assert str(dim_err) == context.text, f'Expecting: \n"{context.text}\'\nGot:\n{str(dim_err)}'


@then('the unique contents of the "{column_name}" column should be equal to')
def step_impl(context, column_name):
    assert column_name in context.df.columns.values, 'No column named "{column_name}" present in dataframe'

    values_got = str(sorted(context.df[column_name].unique()))
    values_expected = str(context.text)

    msg = f"""Values extracted do not match what was expected.

Got:
{values_got}

Expected: 
{values_expected}
    
    """
    assert values_got == values_expected, msg

@given('we attempt to extract the dimensions, capturing the first exception as')
def step_impl(context):
    try:
        context.tidy_sheet.topandas()
    except Exception as err:
        got_err_str = str(err)
        expected_err_str = str(context.text)
        msg = f"""Unexpected exception

Got:
{got_err_str}

Expected:
{expected_err_str}
        """
        assert got_err_str == expected_err_str, msg